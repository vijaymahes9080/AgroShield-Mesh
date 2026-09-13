"""
AgroShield Mesh - Domain Schemas
Pydantic v2 domain models for Farmers, Fields, Crop Cycles, Sensor Readings,
Weather, Satellite Observations, Risk Assessments, Advisories, Feedback, and Auditing.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4
from pydantic import BaseModel, Field, EmailStr, field_validator


class LanguagePreference(str, Enum):
    EN = "en"
    TA = "ta"


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class DataSourceType(str, Enum):
    OBSERVED = "observed"
    ESTIMATED = "estimated"
    SIMULATED = "simulated"
    MODEL_GENERATED = "model_generated"


class ReviewStatus(str, Enum):
    PENDING_REVIEW = "pending_review"
    EXPERT_APPROVED = "expert_approved"
    REJECTED = "rejected"
    AUTO_DISPATCHED = "auto_dispatched"


class UserRole(str, Enum):
    FARMER = "farmer"
    AGRONOMIST_EXPERT = "agronomist_expert"
    ADMIN = "admin"


# ==========================================
# 1. FARMER
# ==========================================
class FarmerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    email: Optional[EmailStr] = None
    village: str
    taluk: Optional[str] = "Perundurai"
    district: str = "Erode"
    state: str = "Tamil Nadu"
    language_preference: LanguagePreference = LanguagePreference.TA
    consent_data_sharing: bool = Field(default=True, description="Consent for automated advisory & sensor telemetry")
    consent_satellite_indexing: bool = Field(default=True)
    schema_version: str = "1.0.0"


class FarmerCreate(FarmerBase):
    pass


class FarmerResponse(FarmerBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provenance: Dict[str, Any] = Field(default_factory=lambda: {"source": "farmer_registration", "version": "1.0.0"})

    class Config:
        from_attributes = True


# ==========================================
# 2. FIELD
# ==========================================
class FieldBoundary(BaseModel):
    type: str = "Polygon"
    coordinates: List[List[List[float]]]  # GeoJSON Polygon coordinates [lon, lat]


class FieldBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    farmer_id: str
    boundary_geojson: Dict[str, Any] = Field(..., description="GeoJSON polygon in EPSG:4326")
    area_hectares: float = Field(..., gt=0.0)
    soil_type: str = Field(default="Red Loam", description="Red Loam, Black Clay, Sandy Loam, Clay Loam")
    irrigation_source: str = Field(default="Borewell / Drip", description="Canal, Borewell, Well, Rainfed")
    elevation_meters: float = Field(default=240.0)
    srid: int = Field(default=4326, description="Spatial reference ID (WGS84=4326)")
    schema_version: str = "1.0.0"


class FieldCreate(FieldBase):
    pass


class FieldResponse(FieldBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provenance: Dict[str, Any] = Field(default_factory=lambda: {"source": "cadastral_survey", "confidence": 0.98})

    class Config:
        from_attributes = True


# ==========================================
# 3. CROP CYCLE
# ==========================================
class CropStage(str, Enum):
    SOWING = "sowing"
    VEGETATIVE = "vegetative"
    FLOWERING = "flowering"
    YIELD_FORMATION = "yield_formation"
    RIPENING = "ripening"
    HARVESTED = "harvested"


class CropCycleBase(BaseModel):
    field_id: str
    crop_name: str = Field(..., example="Paddy (Rice)")
    variety: str = Field(default="CO 51", example="CO 51 / CR 1009 / BPT 5204")
    season: str = Field(default="Kharif / Samba", example="Navarai / Kuruvai / Samba")
    sowing_date: datetime
    expected_harvest_date: datetime
    current_stage: CropStage = CropStage.VEGETATIVE
    expected_yield_tonnes_per_ha: Optional[float] = 6.2
    active_status: bool = True
    schema_version: str = "1.0.0"


class CropCycleCreate(CropCycleBase):
    pass


class CropCycleResponse(CropCycleBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provenance: Dict[str, Any] = Field(default_factory=lambda: {"source": "farmer_sowing_record", "confidence": 1.0})

    class Config:
        from_attributes = True


# ==========================================
# 4. SENSOR READING
# ==========================================
class SensorReadingBase(BaseModel):
    field_id: str
    device_id: str = Field(..., example="AGRO-NODE-ERD-004")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    soil_moisture_pct: float = Field(..., ge=0.0, le=100.0, description="Volumetric water content percentage")
    soil_temperature_c: float = Field(..., ge=-10.0, le=65.0)
    ambient_temperature_c: float = Field(..., ge=-10.0, le=60.0)
    ambient_humidity_pct: float = Field(..., ge=0.0, le=100.0)
    battery_pct: float = Field(default=95.0, ge=0.0, le=100.0)
    solar_flux_lux: Optional[float] = Field(default=45000.0)
    is_valid: bool = True
    anomaly_flag: bool = False
    anomaly_reason: Optional[str] = None
    data_source: DataSourceType = DataSourceType.OBSERVED
    raw_payload: Optional[Dict[str, Any]] = None
    schema_version: str = "1.0.0"


class SensorReadingCreate(SensorReadingBase):
    pass


class SensorReadingResponse(SensorReadingBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provenance: Dict[str, Any] = Field(default_factory=lambda: {"channel": "mqtt_mesh", "mac_mesh_hop": 2})

    class Config:
        from_attributes = True


# ==========================================
# 5. WEATHER OBSERVATION
# ==========================================
class WeatherObservationBase(BaseModel):
    field_id: Optional[str] = None
    grid_location: Dict[str, float] = Field(default_factory=lambda: {"lat": 11.3410, "lon": 77.7172})
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: str = Field(default="IMD_AWS_ERODE", description="IMD, Open-Meteo, Field Station")
    temperature_c: float
    relative_humidity_pct: float
    rainfall_mm_last_24h: float = Field(default=0.0, ge=0.0)
    wind_speed_kmh: float = Field(default=12.0, ge=0.0)
    wind_direction_deg: Optional[float] = 180.0
    forecast_rain_next_24h_mm: float = Field(default=0.0, ge=0.0)
    forecast_rain_next_72h_mm: float = Field(default=0.0, ge=0.0)
    et0_evapotranspiration_mm: float = Field(default=4.5, description="Reference Evapotranspiration FAO Penman-Monteith")
    data_source: DataSourceType = DataSourceType.OBSERVED
    schema_version: str = "1.0.0"


class WeatherObservationCreate(WeatherObservationBase):
    pass


class WeatherObservationResponse(WeatherObservationBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provenance: Dict[str, Any] = Field(default_factory=lambda: {"source_station": "IMD-District-Agromet-Unit-Erode"})

    class Config:
        from_attributes = True


# ==========================================
# 6. SATELLITE OBSERVATION
# ==========================================
class SatelliteObservationBase(BaseModel):
    field_id: str
    observation_date: datetime
    satellite_mission: str = Field(default="Sentinel-2B", description="Sentinel-2, Landsat-8, or Synthetic-Raster")
    cloud_cover_pct: float = Field(default=12.0, ge=0.0, le=100.0)
    ndvi_mean: float = Field(..., ge=-1.0, le=1.0, description="Normalized Difference Vegetation Index mean")
    ndvi_min: float = Field(..., ge=-1.0, le=1.0)
    ndvi_max: float = Field(..., ge=-1.0, le=1.0)
    ndwi_mean: float = Field(..., ge=-1.0, le=1.0, description="Normalized Difference Water Index")
    resolution_meters: float = Field(default=10.0)
    raster_reference_uri: Optional[str] = None
    data_source: DataSourceType = DataSourceType.OBSERVED
    schema_version: str = "1.0.0"


class SatelliteObservationCreate(SatelliteObservationBase):
    pass


class SatelliteObservationResponse(SatelliteObservationBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provenance: Dict[str, Any] = Field(default_factory=lambda: {"copernicus_granule_id": "S2B_MSIL2A_20260910T045649"})

    class Config:
        from_attributes = True


# ==========================================
# 7. RISK ASSESSMENT
# ==========================================
class RiskFactorBreakdown(BaseModel):
    irrigation_need_score: float = Field(..., ge=0.0, le=100.0)
    heat_stress_score: float = Field(..., ge=0.0, le=100.0)
    drought_risk_score: float = Field(..., ge=0.0, le=100.0)
    excess_rain_risk_score: float = Field(..., ge=0.0, le=100.0)
    sensor_anomaly_score: float = Field(..., ge=0.0, le=100.0)
    weights_applied: Dict[str, float] = Field(default_factory=lambda: {
        "irrigation": 0.35, "heat": 0.20, "drought": 0.20, "excess_rain": 0.15, "sensor_anomaly": 0.10
    })


class MissingDataStatus(BaseModel):
    is_sensor_stale: bool = False
    is_weather_stale: bool = False
    is_satellite_stale: bool = False
    missing_fields: List[str] = Field(default_factory=list)
    confidence_penalty_pct: float = 0.0


class RiskAssessmentBase(BaseModel):
    field_id: str
    assessment_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    overall_risk_level: RiskLevel
    overall_score: float = Field(..., ge=0.0, le=100.0)
    factor_breakdown: RiskFactorBreakdown
    missing_data_status: MissingDataStatus
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    recommended_verification_steps: List[str] = Field(default_factory=list)
    calculated_by: str = "AgroShield Deterministic Agronomic Engine v1.0"
    schema_version: str = "1.0.0"


class RiskAssessmentCreate(RiskAssessmentBase):
    pass


class RiskAssessmentResponse(RiskAssessmentBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provenance: Dict[str, Any] = Field(default_factory=lambda: {"engine": "rule_based_deterministic", "timestamp": datetime.now(timezone.utc).isoformat()})

    class Config:
        from_attributes = True


# ==========================================
# 8. ADVISORY & CITATIONS
# ==========================================
class Citation(BaseModel):
    source_title: str
    author_organization: str = Field(..., example="Tamil Nadu Agricultural University (TNAU)")
    publication_year: int = 2024
    document_section: str
    page_or_bulletin_no: str
    document_hash_sha256: str
    uri_or_reference: Optional[str] = None


class AdvisoryBase(BaseModel):
    field_id: str
    risk_assessment_id: Optional[str] = None
    language: LanguagePreference = LanguagePreference.TA
    title: str = Field(..., min_length=5, max_length=200)
    summary: str
    action_items: List[str] = Field(..., min_length=1)
    prohibited_actions: List[str] = Field(default_factory=list)
    source_citations: List[Citation] = Field(default_factory=list)
    confidence_level: float = Field(..., ge=0.0, le=1.0)
    requires_human_review: bool = Field(default=False)
    review_status: ReviewStatus = ReviewStatus.AUTO_DISPATCHED
    reviewed_by: Optional[str] = None
    review_notes: Optional[str] = None
    disclaimer: str = (
        "AGRONOMIC NOTICE: This guidance is evidence-grounded decision support based on university guidelines. "
        "It does not operate farm equipment autonomously or replace visual on-field agronomic inspection."
    )
    data_sources_used: List[DataSourceType] = Field(default_factory=lambda: [
        DataSourceType.OBSERVED, DataSourceType.MODEL_GENERATED
    ])
    schema_version: str = "1.0.0"


class AdvisoryCreate(AdvisoryBase):
    pass


class AdvisoryResponse(AdvisoryBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reviewed_at: Optional[datetime] = None
    provenance: Dict[str, Any] = Field(default_factory=lambda: {
        "workflow": "bounded_agent_workflow",
        "llm_or_composer": "AgroShield Expert Rule Composer",
        "rag_retrieval_count": 3
    })

    class Config:
        from_attributes = True


class AdvisoryReviewRequest(BaseModel):
    review_status: ReviewStatus = Field(..., description="EXPERT_APPROVED or REJECTED")
    reviewer_name: str
    review_notes: str
    edited_action_items: Optional[List[str]] = None


# ==========================================
# 9. ADVISORY FEEDBACK
# ==========================================
class AdvisoryFeedbackBase(BaseModel):
    advisory_id: str
    farmer_id: str
    rating: int = Field(..., ge=1, le=5, description="1 to 5 star usefulness rating")
    helpful_flag: bool
    actual_action_taken: str = Field(..., example="Irrigated 2.5 hours via drip in morning")
    unnecessary_irrigation_prevented_litres: Optional[float] = Field(default=0.0)
    comments: Optional[str] = None
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: str = "1.0.0"


class AdvisoryFeedbackCreate(AdvisoryFeedbackBase):
    pass


class AdvisoryFeedbackResponse(AdvisoryFeedbackBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    provenance: Dict[str, Any] = Field(default_factory=lambda: {"channel": "farmer_dashboard"})

    class Config:
        from_attributes = True


# ==========================================
# 10. AUDIT EVENT
# ==========================================
class AuditEventBase(BaseModel):
    event_type: str = Field(..., example="FIELD_REGISTERED | RISK_EVALUATED | ADVISORY_APPROVED")
    entity_name: str = Field(..., example="Field | Advisory | RiskAssessment")
    entity_id: str
    actor_id: str
    actor_role: UserRole
    action: str
    ip_address: Optional[str] = "127.0.0.1"
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    payload_hash: str
    previous_event_hash: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: str = "1.0.0"


class AuditEventCreate(AuditEventBase):
    pass


class AuditEventResponse(AuditEventBase):
    id: str = Field(default_factory=lambda: str(uuid4()))

    class Config:
        from_attributes = True
