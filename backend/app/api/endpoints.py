"""
AgroShield Mesh - REST API Endpoints
"""

import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.db.session import get_db
from backend.app.db.models import (
    UserModel, FarmerModel, FieldModel, CropCycleModel,
    SensorReadingModel, WeatherObservationModel, SatelliteObservationModel,
    RiskAssessmentModel, AdvisoryModel, AdvisoryFeedbackModel, AuditEventModel
)
from backend.app.schemas.domain import (
    FarmerCreate, FarmerResponse,
    FieldCreate, FieldResponse,
    CropCycleCreate, CropCycleResponse,
    SensorReadingCreate, SensorReadingResponse,
    WeatherObservationCreate, WeatherObservationResponse,
    SatelliteObservationCreate, SatelliteObservationResponse,
    RiskAssessmentResponse,
    AdvisoryResponse, AdvisoryReviewRequest,
    AdvisoryFeedbackCreate, AdvisoryFeedbackResponse,
    AuditEventResponse,
    LanguagePreference, ReviewStatus, UserRole
)
from backend.app.core.security import (
    get_password_hash, verify_password, create_access_token,
    get_current_user_payload, compute_sha256_hash, require_roles
)
from backend.app.core.config import settings
from geospatial.geometry import validate_field_boundary, format_map_ready_geojson
from geospatial.raster_analysis import generate_synthetic_raster_grid, compute_zonal_spectral_indices
from agents.risk_engine import AgronomicRiskEngine
from agents.workflow import BoundedAgentWorkflow

router = APIRouter()
workflow_engine = BoundedAgentWorkflow(use_sentence_transformers=False)


def record_audit_event(
    db: Session,
    event_type: str,
    entity_name: str,
    entity_id: str,
    actor_id: str,
    actor_role: str,
    action: str,
    payload_dict: Dict[str, Any],
    ip_address: str = "127.0.0.1",
    request_id: Optional[str] = None
):
    """Appends cryptographically hashed audit record."""
    payload_str = json.dumps(payload_dict, default=str, sort_keys=True)
    payload_hash = compute_sha256_hash(payload_str)

    # Fetch previous event hash for chaining
    last_event = db.query(AuditEventModel).order_by(desc(AuditEventModel.timestamp)).first()
    prev_hash = last_event.payload_hash if last_event else "0" * 64

    audit = AuditEventModel(
        id=str(uuid4()),
        event_type=event_type,
        entity_name=entity_name,
        entity_id=entity_id,
        actor_id=actor_id,
        actor_role=actor_role,
        action=action,
        ip_address=ip_address,
        request_id=request_id or str(uuid4()),
        payload_hash=payload_hash,
        previous_event_hash=prev_hash,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(audit)
    db.commit()


# ==========================================
# HEALTH & VERSION
# ==========================================
@router.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/version", tags=["System"])
def version_info():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "crs": settings.DEFAULT_CRS,
        "rag_sources": ["TNAU Agritech Portal", "ICAR Water Management", "IMD Agromet Advisory"],
        "safety_mode": "read_only_advisory"
    }


# ==========================================
# AUTHENTICATION
# ==========================================
@router.post("/auth/register", tags=["Auth"])
def register_user(payload: Dict[str, str], db: Session = Depends(get_db)):
    username = payload.get("username")
    email = payload.get("email")
    password = payload.get("password")
    role = payload.get("role", UserRole.FARMER.value)

    if not username or not email or not password:
        raise HTTPException(status_code=400, detail="Missing required registration fields")

    existing = db.query(UserModel).filter((UserModel.username == username) | (UserModel.email == email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user = UserModel(
        username=username,
        email=email,
        hashed_password=get_password_hash(password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully", "user_id": user.id, "role": user.role}


@router.post("/auth/token", tags=["Auth"])
def login(payload: Dict[str, str], db: Session = Depends(get_db)):
    username = payload.get("username")
    password = payload.get("password")

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token = create_access_token({"sub": user.id, "username": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "role": user.role, "username": user.username}


# ==========================================
# FARMERS
# ==========================================
@router.post("/farmers", response_model=FarmerResponse, tags=["Farmers"])
def create_farmer(farmer_in: FarmerCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user_payload)):
    db_farmer = FarmerModel(
        name=farmer_in.name,
        phone=farmer_in.phone,
        email=farmer_in.email,
        village=farmer_in.village,
        taluk=farmer_in.taluk,
        district=farmer_in.district,
        state=farmer_in.state,
        language_preference=farmer_in.language_preference.value,
        consent_data_sharing=farmer_in.consent_data_sharing,
        consent_satellite_indexing=farmer_in.consent_satellite_indexing
    )
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)

    record_audit_event(
        db=db,
        event_type="FARMER_REGISTERED",
        entity_name="Farmer",
        entity_id=db_farmer.id,
        actor_id=user.get("sub", "system"),
        actor_role=user.get("role", "admin"),
        action="REGISTER_FARMER",
        payload_dict={"farmer_id": db_farmer.id, "name": db_farmer.name, "village": db_farmer.village}
    )
    return db_farmer


@router.get("/farmers", response_model=List[FarmerResponse], tags=["Farmers"])
def list_farmers(db: Session = Depends(get_db)):
    return db.query(FarmerModel).all()


@router.get("/farmers/{farmer_id}", response_model=FarmerResponse, tags=["Farmers"])
def get_farmer(farmer_id: str, db: Session = Depends(get_db)):
    f = db.query(FarmerModel).filter(FarmerModel.id == farmer_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return f


# ==========================================
# FIELDS
# ==========================================
@router.post("/fields", response_model=FieldResponse, tags=["Fields"])
def create_field(field_in: FieldCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user_payload)):
    # 1. Validate GeoJSON Polygon boundary
    is_valid, reason, calc_area = validate_field_boundary(field_in.boundary_geojson)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Invalid field boundary: {reason}")

    # Use calculated geodesic area if user passed zero or default
    final_area = calc_area if (field_in.area_hectares <= 0.0 or abs(field_in.area_hectares - 1.0) < 0.001) else field_in.area_hectares

    db_field = FieldModel(
        farmer_id=field_in.farmer_id,
        name=field_in.name,
        boundary_geojson=field_in.boundary_geojson,
        area_hectares=round(final_area, 3),
        soil_type=field_in.soil_type,
        irrigation_source=field_in.irrigation_source,
        elevation_meters=field_in.elevation_meters,
        srid=field_in.srid
    )
    db.add(db_field)
    db.commit()
    db.refresh(db_field)

    record_audit_event(
        db=db,
        event_type="FIELD_CREATED",
        entity_name="Field",
        entity_id=db_field.id,
        actor_id=user.get("sub", "system"),
        actor_role=user.get("role", "farmer"),
        action="CREATE_FIELD",
        payload_dict={"field_id": db_field.id, "name": db_field.name, "area_ha": db_field.area_hectares}
    )
    return db_field


@router.get("/fields", response_model=List[FieldResponse], tags=["Fields"])
def list_fields(db: Session = Depends(get_db)):
    return db.query(FieldModel).all()


@router.get("/fields/{field_id}", response_model=FieldResponse, tags=["Fields"])
def get_field(field_id: str, db: Session = Depends(get_db)):
    field = db.query(FieldModel).filter(FieldModel.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    return field


@router.get("/fields-geojson", tags=["Geospatial"])
def get_fields_geojson(db: Session = Depends(get_db)):
    """Returns styled GeoJSON FeatureCollection for all fields with latest risk metrics."""
    fields = db.query(FieldModel).all()
    fields_data = []

    for f in fields:
        # Fetch latest risk assessment if any
        latest_risk = db.query(RiskAssessmentModel).filter(
            RiskAssessmentModel.field_id == f.id
        ).order_by(desc(RiskAssessmentModel.assessment_date)).first()

        latest_sat = db.query(SatelliteObservationModel).filter(
            SatelliteObservationModel.field_id == f.id
        ).order_by(desc(SatelliteObservationModel.observation_date)).first()

        latest_sensor = db.query(SensorReadingModel).filter(
            SensorReadingModel.field_id == f.id
        ).order_by(desc(SensorReadingModel.timestamp)).first()

        fields_data.append({
            "id": f.id,
            "name": f.name,
            "farmer_name": f.farmer.name if f.farmer else "Farmer",
            "boundary_geojson": f.boundary_geojson,
            "area_hectares": f.area_hectares,
            "soil_type": f.soil_type,
            "irrigation_source": f.irrigation_source,
            "current_risk_level": latest_risk.overall_risk_level if latest_risk else "low",
            "ndvi_mean": latest_sat.ndvi_mean if latest_sat else 0.68,
            "soil_moisture_pct": latest_sensor.soil_moisture_pct if latest_sensor else 28.0
        })

    return format_map_ready_geojson(fields_data)


@router.get("/fields/{field_id}/synthetic-raster", tags=["Geospatial"])
def get_field_synthetic_raster(field_id: str, stress_patch: bool = False, db: Session = Depends(get_db)):
    """Generates synthetic Sentinel-2 raster spectral indices (NDVI/NDWI) for field visualization."""
    field = db.query(FieldModel).filter(FieldModel.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    grid = generate_synthetic_raster_grid(rows=12, cols=12, base_health=0.68, stress_patch=stress_patch)
    analysis = compute_zonal_spectral_indices(grid)
    return {
        "field_id": field_id,
        "field_name": field.name,
        "raster_analysis": analysis
    }


# ==========================================
# CROP CYCLES
# ==========================================
@router.post("/fields/{field_id}/crop-cycles", response_model=CropCycleResponse, tags=["Crop Cycles"])
def create_crop_cycle(field_id: str, cycle_in: CropCycleCreate, db: Session = Depends(get_db)):
    field = db.query(FieldModel).filter(FieldModel.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    cycle = CropCycleModel(
        field_id=field_id,
        crop_name=cycle_in.crop_name,
        variety=cycle_in.variety,
        season=cycle_in.season,
        sowing_date=cycle_in.sowing_date,
        expected_harvest_date=cycle_in.expected_harvest_date,
        current_stage=cycle_in.current_stage.value,
        expected_yield_tonnes_per_ha=cycle_in.expected_yield_tonnes_per_ha,
        active_status=cycle_in.active_status
    )
    db.add(cycle)
    db.commit()
    db.refresh(cycle)
    return cycle


@router.get("/fields/{field_id}/crop-cycles", response_model=List[CropCycleResponse], tags=["Crop Cycles"])
def list_crop_cycles(field_id: str, db: Session = Depends(get_db)):
    return db.query(CropCycleModel).filter(CropCycleModel.field_id == field_id).all()


# ==========================================
# SENSOR READINGS INGESTION
# ==========================================
@router.post("/sensor-readings", response_model=SensorReadingResponse, tags=["Telemetry"])
def ingest_sensor_reading(reading_in: SensorReadingCreate, db: Session = Depends(get_db)):
    reading = SensorReadingModel(
        field_id=reading_in.field_id,
        device_id=reading_in.device_id,
        timestamp=reading_in.timestamp,
        soil_moisture_pct=reading_in.soil_moisture_pct,
        soil_temperature_c=reading_in.soil_temperature_c,
        ambient_temperature_c=reading_in.ambient_temperature_c,
        ambient_humidity_pct=reading_in.ambient_humidity_pct,
        battery_pct=reading_in.battery_pct,
        solar_flux_lux=reading_in.solar_flux_lux,
        is_valid=reading_in.is_valid,
        anomaly_flag=reading_in.anomaly_flag,
        anomaly_reason=reading_in.anomaly_reason,
        data_source=reading_in.data_source.value,
        raw_payload=reading_in.raw_payload
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


@router.get("/fields/{field_id}/sensor-readings", response_model=List[SensorReadingResponse], tags=["Telemetry"])
def list_field_sensor_readings(field_id: str, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(SensorReadingModel).filter(
        SensorReadingModel.field_id == field_id
    ).order_by(desc(SensorReadingModel.timestamp)).limit(limit).all()


# ==========================================
# WEATHER OBSERVATIONS INGESTION
# ==========================================
@router.post("/weather-observations", response_model=WeatherObservationResponse, tags=["Weather"])
def ingest_weather_observation(obs_in: WeatherObservationCreate, db: Session = Depends(get_db)):
    obs = WeatherObservationModel(
        field_id=obs_in.field_id,
        grid_location=obs_in.grid_location,
        timestamp=obs_in.timestamp,
        source=obs_in.source,
        temperature_c=obs_in.temperature_c,
        relative_humidity_pct=obs_in.relative_humidity_pct,
        rainfall_mm_last_24h=obs_in.rainfall_mm_last_24h,
        wind_speed_kmh=obs_in.wind_speed_kmh,
        wind_direction_deg=obs_in.wind_direction_deg,
        forecast_rain_next_24h_mm=obs_in.forecast_rain_next_24h_mm,
        forecast_rain_next_72h_mm=obs_in.forecast_rain_next_72h_mm,
        et0_evapotranspiration_mm=obs_in.et0_evapotranspiration_mm,
        data_source=obs_in.data_source.value
    )
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs


@router.get("/weather-observations", response_model=List[WeatherObservationResponse], tags=["Weather"])
def list_weather_observations(limit: int = 20, db: Session = Depends(get_db)):
    return db.query(WeatherObservationModel).order_by(desc(WeatherObservationModel.timestamp)).limit(limit).all()


# ==========================================
# SATELLITE OBSERVATIONS
# ==========================================
@router.post("/satellite-observations", response_model=SatelliteObservationResponse, tags=["Satellite"])
def ingest_satellite_observation(sat_in: SatelliteObservationCreate, db: Session = Depends(get_db)):
    sat = SatelliteObservationModel(
        field_id=sat_in.field_id,
        observation_date=sat_in.observation_date,
        satellite_mission=sat_in.satellite_mission,
        cloud_cover_pct=sat_in.cloud_cover_pct,
        ndvi_mean=sat_in.ndvi_mean,
        ndvi_min=sat_in.ndvi_min,
        ndvi_max=sat_in.ndvi_max,
        ndwi_mean=sat_in.ndwi_mean,
        resolution_meters=sat_in.resolution_meters,
        raster_reference_uri=sat_in.raster_reference_uri,
        data_source=sat_in.data_source.value
    )
    db.add(sat)
    db.commit()
    db.refresh(sat)
    return sat


@router.get("/fields/{field_id}/satellite-observations", response_model=List[SatelliteObservationResponse], tags=["Satellite"])
def list_field_satellite_observations(field_id: str, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(SatelliteObservationModel).filter(
        SatelliteObservationModel.field_id == field_id
    ).order_by(desc(SatelliteObservationModel.observation_date)).limit(limit).all()


# ==========================================
# RISK ASSESSMENTS
# ==========================================
@router.post("/risk-assessments", response_model=RiskAssessmentResponse, tags=["Risk"])
def evaluate_risk_for_field(field_id: str = Query(...), db: Session = Depends(get_db)):
    field = db.query(FieldModel).filter(FieldModel.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    # Fetch latest observations
    sensors = db.query(SensorReadingModel).filter(
        SensorReadingModel.field_id == field_id
    ).order_by(SensorReadingModel.timestamp.asc()).all()
    sensors_dict = [s.__dict__ for s in sensors]

    weather = db.query(WeatherObservationModel).order_by(desc(WeatherObservationModel.timestamp)).first()
    weather_dict = weather.__dict__ if weather else None

    sat = db.query(SatelliteObservationModel).filter(
        SatelliteObservationModel.field_id == field_id
    ).order_by(desc(SatelliteObservationModel.observation_date)).first()
    sat_dict = sat.__dict__ if sat else None

    crop = db.query(CropCycleModel).filter(
        CropCycleModel.field_id == field_id,
        CropCycleModel.active_status == True
    ).first()
    crop_dict = crop.__dict__ if crop else None

    risk = AgronomicRiskEngine.evaluate_field_risk(
        field_id=field_id,
        sensor_readings=sensors_dict,
        weather_obs=weather_dict,
        satellite_obs=sat_dict,
        crop_cycle=crop_dict,
        soil_type=field.soil_type
    )

    db_risk = RiskAssessmentModel(
        field_id=field_id,
        assessment_date=risk.assessment_date,
        overall_risk_level=risk.overall_risk_level.value,
        overall_score=risk.overall_score,
        factor_breakdown=risk.factor_breakdown.dict(),
        missing_data_status=risk.missing_data_status.dict(),
        confidence_score=risk.confidence_score,
        recommended_verification_steps=risk.recommended_verification_steps,
        calculated_by=risk.calculated_by
    )
    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)
    return db_risk


@router.get("/fields/{field_id}/risk-assessments", response_model=List[RiskAssessmentResponse], tags=["Risk"])
def list_field_risk_assessments(field_id: str, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(RiskAssessmentModel).filter(
        RiskAssessmentModel.field_id == field_id
    ).order_by(desc(RiskAssessmentModel.assessment_date)).limit(limit).all()


# ==========================================
# ADVISORIES & EXPERT REVIEW GATE
# ==========================================
@router.post("/advisories", response_model=AdvisoryResponse, tags=["Advisories"])
def generate_field_advisory(
    field_id: str = Query(...),
    language: LanguagePreference = LanguagePreference.TA,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_payload)
):
    field = db.query(FieldModel).filter(FieldModel.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    farmer = field.farmer
    farmer_dict = farmer.__dict__ if farmer else None

    crop = db.query(CropCycleModel).filter(
        CropCycleModel.field_id == field_id,
        CropCycleModel.active_status == True
    ).first()
    crop_dict = crop.__dict__ if crop else None

    sensors = db.query(SensorReadingModel).filter(
        SensorReadingModel.field_id == field_id
    ).order_by(SensorReadingModel.timestamp.asc()).all()
    sensors_dict = [s.__dict__ for s in sensors]

    weather = db.query(WeatherObservationModel).order_by(desc(WeatherObservationModel.timestamp)).first()
    weather_dict = weather.__dict__ if weather else None

    sat = db.query(SatelliteObservationModel).filter(
        SatelliteObservationModel.field_id == field_id
    ).order_by(desc(SatelliteObservationModel.observation_date)).first()
    sat_dict = sat.__dict__ if sat else None

    # Execute Bounded Agent Workflow
    state = workflow_engine.run(
        field_id=field_id,
        farmer_data=farmer_dict,
        field_data=field.__dict__,
        crop_cycle=crop_dict,
        sensor_readings=sensors_dict,
        weather_observation=weather_dict,
        satellite_observation=sat_dict,
        language=language
    )

    if not state.final_advisory:
        raise HTTPException(status_code=500, detail="Advisory generation failed safety verification.")

    adv = state.final_advisory
    citations_data = [c.dict() for c in adv.source_citations]

    db_advisory = AdvisoryModel(
        field_id=field_id,
        risk_assessment_id=state.risk_assessment.id if hasattr(state.risk_assessment, "id") else None,
        language=adv.language.value,
        title=adv.title,
        summary=adv.summary,
        action_items=adv.action_items,
        prohibited_actions=adv.prohibited_actions,
        source_citations=citations_data,
        confidence_level=adv.confidence_level,
        requires_human_review=adv.requires_human_review,
        review_status=adv.review_status.value,
        disclaimer=adv.disclaimer,
        data_sources_used=[d.value for d in adv.data_sources_used],
        provenance={"workflow_stages": [t["stage"] for t in state.execution_trace]}
    )
    db.add(db_advisory)
    db.commit()
    db.refresh(db_advisory)

    record_audit_event(
        db=db,
        event_type="ADVISORY_GENERATED",
        entity_name="Advisory",
        entity_id=db_advisory.id,
        actor_id=user.get("sub", "system"),
        actor_role=user.get("role", "system"),
        action="GENERATE_ADVISORY",
        payload_dict={"advisory_id": db_advisory.id, "review_status": db_advisory.review_status, "requires_review": db_advisory.requires_human_review}
    )
    return db_advisory


@router.get("/advisories", response_model=List[AdvisoryResponse], tags=["Advisories"])
def list_advisories(
    status_filter: Optional[ReviewStatus] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    q = db.query(AdvisoryModel)
    if status_filter:
        q = q.filter(AdvisoryModel.review_status == status_filter.value)
    return q.order_by(desc(AdvisoryModel.generated_at)).limit(limit).all()


@router.get("/fields/{field_id}/advisories", response_model=List[AdvisoryResponse], tags=["Advisories"])
def list_field_advisories(field_id: str, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(AdvisoryModel).filter(
        AdvisoryModel.field_id == field_id
    ).order_by(desc(AdvisoryModel.generated_at)).limit(limit).all()


@router.post("/advisories/{advisory_id}/review", response_model=AdvisoryResponse, tags=["Advisories"])
def review_advisory(
    advisory_id: str,
    review_in: AdvisoryReviewRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_payload)
):
    """
    Expert Review Gate: Human Agronomist approves or rejects advisory.
    """
    adv = db.query(AdvisoryModel).filter(AdvisoryModel.id == advisory_id).first()
    if not adv:
        raise HTTPException(status_code=404, detail="Advisory not found")

    adv.review_status = review_in.review_status.value
    adv.reviewed_by = review_in.reviewer_name
    adv.review_notes = review_in.review_notes
    adv.reviewed_at = datetime.now(timezone.utc)
    if review_in.edited_action_items:
        adv.action_items = review_in.edited_action_items

    db.commit()
    db.refresh(adv)

    record_audit_event(
        db=db,
        event_type="EXPERT_REVIEW_DECISION",
        entity_name="Advisory",
        entity_id=adv.id,
        actor_id=user.get("sub", review_in.reviewer_name),
        actor_role=user.get("role", "agronomist_expert"),
        action=f"REVIEW_{review_in.review_status.value.upper()}",
        payload_dict={"advisory_id": adv.id, "status": adv.review_status, "reviewer": review_in.reviewer_name}
    )
    return adv


# ==========================================
# FEEDBACK
# ==========================================
@router.post("/advisories/{advisory_id}/feedback", response_model=AdvisoryFeedbackResponse, tags=["Feedback"])
def submit_advisory_feedback(
    advisory_id: str,
    fb_in: AdvisoryFeedbackCreate,
    db: Session = Depends(get_db)
):
    adv = db.query(AdvisoryModel).filter(AdvisoryModel.id == advisory_id).first()
    if not adv:
        raise HTTPException(status_code=404, detail="Advisory not found")

    fb = AdvisoryFeedbackModel(
        advisory_id=advisory_id,
        farmer_id=fb_in.farmer_id,
        rating=fb_in.rating,
        helpful_flag=fb_in.helpful_flag,
        actual_action_taken=fb_in.actual_action_taken,
        unnecessary_irrigation_prevented_litres=fb_in.unnecessary_irrigation_prevented_litres or 0.0,
        comments=fb_in.comments,
        recorded_at=datetime.now(timezone.utc)
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb


# ==========================================
# AUDITING
# ==========================================
@router.get("/audit", response_model=List[AuditEventResponse], tags=["Audit"])
def list_audit_events(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(AuditEventModel).order_by(desc(AuditEventModel.timestamp)).limit(limit).all()


@router.get("/audit/{audit_id}", response_model=AuditEventResponse, tags=["Audit"])
def get_audit_event(audit_id: str, db: Session = Depends(get_db)):
    event = db.query(AuditEventModel).filter(AuditEventModel.id == audit_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Audit event not found")
    return event
