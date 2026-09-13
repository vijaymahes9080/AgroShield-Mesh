"""
SQLAlchemy ORM models for AgroShield Mesh.
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import (
    Column, String, Float, Boolean, Integer, DateTime, JSON, Text, ForeignKey
)
from sqlalchemy.orm import relationship
from backend.app.db.session import Base


def gen_uuid():
    return str(uuid.uuid4())


def now_utc():
    return datetime.now(timezone.utc)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(30), default="farmer", nullable=False)  # farmer, agronomist_expert, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=now_utc)


class FarmerModel(Base):
    __tablename__ = "farmers"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    village = Column(String(100), nullable=False)
    taluk = Column(String(100), default="Perundurai")
    district = Column(String(100), default="Erode")
    state = Column(String(100), default="Tamil Nadu")
    language_preference = Column(String(10), default="ta")
    consent_data_sharing = Column(Boolean, default=True)
    consent_satellite_indexing = Column(Boolean, default=True)
    created_at = Column(DateTime, default=now_utc)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc)
    provenance = Column(JSON, default=dict)

    fields = relationship("FieldModel", back_populates="farmer", cascade="all, delete-orphan")


class FieldModel(Base):
    __tablename__ = "fields"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    farmer_id = Column(String(36), ForeignKey("farmers.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    boundary_geojson = Column(JSON, nullable=False)
    area_hectares = Column(Float, nullable=False)
    soil_type = Column(String(50), default="Red Loam")
    irrigation_source = Column(String(50), default="Borewell / Drip")
    elevation_meters = Column(Float, default=240.0)
    srid = Column(Integer, default=4326)
    created_at = Column(DateTime, default=now_utc)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc)
    provenance = Column(JSON, default=dict)

    farmer = relationship("FarmerModel", back_populates="fields")
    crop_cycles = relationship("CropCycleModel", back_populates="field", cascade="all, delete-orphan")
    sensor_readings = relationship("SensorReadingModel", back_populates="field", cascade="all, delete-orphan")
    satellite_observations = relationship("SatelliteObservationModel", back_populates="field", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessmentModel", back_populates="field", cascade="all, delete-orphan")
    advisories = relationship("AdvisoryModel", back_populates="field", cascade="all, delete-orphan")


class CropCycleModel(Base):
    __tablename__ = "crop_cycles"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    field_id = Column(String(36), ForeignKey("fields.id"), nullable=False, index=True)
    crop_name = Column(String(100), nullable=False)
    variety = Column(String(100), default="CO 51")
    season = Column(String(50), default="Kharif / Samba")
    sowing_date = Column(DateTime, nullable=False)
    expected_harvest_date = Column(DateTime, nullable=False)
    current_stage = Column(String(50), default="vegetative")
    expected_yield_tonnes_per_ha = Column(Float, default=6.0)
    active_status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=now_utc)
    provenance = Column(JSON, default=dict)

    field = relationship("FieldModel", back_populates="crop_cycles")


class SensorReadingModel(Base):
    __tablename__ = "sensor_readings"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    field_id = Column(String(36), ForeignKey("fields.id"), nullable=False, index=True)
    device_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, default=now_utc, index=True)
    soil_moisture_pct = Column(Float, nullable=False)
    soil_temperature_c = Column(Float, nullable=False)
    ambient_temperature_c = Column(Float, nullable=False)
    ambient_humidity_pct = Column(Float, nullable=False)
    battery_pct = Column(Float, default=95.0)
    solar_flux_lux = Column(Float, default=45000.0)
    is_valid = Column(Boolean, default=True)
    anomaly_flag = Column(Boolean, default=False)
    anomaly_reason = Column(String(200), nullable=True)
    data_source = Column(String(30), default="observed")
    raw_payload = Column(JSON, nullable=True)
    ingested_at = Column(DateTime, default=now_utc)
    provenance = Column(JSON, default=dict)

    field = relationship("FieldModel", back_populates="sensor_readings")


class WeatherObservationModel(Base):
    __tablename__ = "weather_observations"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    field_id = Column(String(36), nullable=True, index=True)
    grid_location = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=now_utc, index=True)
    source = Column(String(100), default="IMD_AWS_ERODE")
    temperature_c = Column(Float, nullable=False)
    relative_humidity_pct = Column(Float, nullable=False)
    rainfall_mm_last_24h = Column(Float, default=0.0)
    wind_speed_kmh = Column(Float, default=12.0)
    wind_direction_deg = Column(Float, default=180.0)
    forecast_rain_next_24h_mm = Column(Float, default=0.0)
    forecast_rain_next_72h_mm = Column(Float, default=0.0)
    et0_evapotranspiration_mm = Column(Float, default=4.5)
    data_source = Column(String(30), default="observed")
    ingested_at = Column(DateTime, default=now_utc)
    provenance = Column(JSON, default=dict)


class SatelliteObservationModel(Base):
    __tablename__ = "satellite_observations"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    field_id = Column(String(36), ForeignKey("fields.id"), nullable=False, index=True)
    observation_date = Column(DateTime, nullable=False, index=True)
    satellite_mission = Column(String(50), default="Sentinel-2B")
    cloud_cover_pct = Column(Float, default=10.0)
    ndvi_mean = Column(Float, nullable=False)
    ndvi_min = Column(Float, nullable=False)
    ndvi_max = Column(Float, nullable=False)
    ndwi_mean = Column(Float, nullable=False)
    resolution_meters = Column(Float, default=10.0)
    raster_reference_uri = Column(String(255), nullable=True)
    data_source = Column(String(30), default="observed")
    ingested_at = Column(DateTime, default=now_utc)
    provenance = Column(JSON, default=dict)

    field = relationship("FieldModel", back_populates="satellite_observations")


class RiskAssessmentModel(Base):
    __tablename__ = "risk_assessments"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    field_id = Column(String(36), ForeignKey("fields.id"), nullable=False, index=True)
    assessment_date = Column(DateTime, default=now_utc, index=True)
    overall_risk_level = Column(String(30), nullable=False)
    overall_score = Column(Float, nullable=False)
    factor_breakdown = Column(JSON, nullable=False)
    missing_data_status = Column(JSON, nullable=False)
    confidence_score = Column(Float, nullable=False)
    recommended_verification_steps = Column(JSON, default=list)
    calculated_by = Column(String(100), default="AgroShield Deterministic Engine v1.0")
    created_at = Column(DateTime, default=now_utc)
    provenance = Column(JSON, default=dict)

    field = relationship("FieldModel", back_populates="risk_assessments")


class AdvisoryModel(Base):
    __tablename__ = "advisories"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    field_id = Column(String(36), ForeignKey("fields.id"), nullable=False, index=True)
    risk_assessment_id = Column(String(36), nullable=True)
    language = Column(String(10), default="ta")
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    action_items = Column(JSON, nullable=False)
    prohibited_actions = Column(JSON, default=list)
    source_citations = Column(JSON, default=list)
    confidence_level = Column(Float, nullable=False)
    requires_human_review = Column(Boolean, default=False)
    review_status = Column(String(30), default="auto_dispatched")
    reviewed_by = Column(String(100), nullable=True)
    review_notes = Column(Text, nullable=True)
    disclaimer = Column(Text, nullable=False)
    data_sources_used = Column(JSON, default=list)
    generated_at = Column(DateTime, default=now_utc)
    reviewed_at = Column(DateTime, nullable=True)
    provenance = Column(JSON, default=dict)

    field = relationship("FieldModel", back_populates="advisories")
    feedback = relationship("AdvisoryFeedbackModel", back_populates="advisory", uselist=False)


class AdvisoryFeedbackModel(Base):
    __tablename__ = "advisory_feedback"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    advisory_id = Column(String(36), ForeignKey("advisories.id"), nullable=False, unique=True)
    farmer_id = Column(String(36), nullable=False)
    rating = Column(Integer, nullable=False)
    helpful_flag = Column(Boolean, nullable=False)
    actual_action_taken = Column(String(255), nullable=False)
    unnecessary_irrigation_prevented_litres = Column(Float, default=0.0)
    comments = Column(Text, nullable=True)
    recorded_at = Column(DateTime, default=now_utc)
    provenance = Column(JSON, default=dict)

    advisory = relationship("AdvisoryModel", back_populates="feedback")


class AuditEventModel(Base):
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    event_type = Column(String(50), nullable=False, index=True)
    entity_name = Column(String(50), nullable=False)
    entity_id = Column(String(36), nullable=False)
    actor_id = Column(String(50), nullable=False)
    actor_role = Column(String(30), nullable=False)
    action = Column(String(100), nullable=False)
    ip_address = Column(String(45), default="127.0.0.1")
    request_id = Column(String(36), nullable=False)
    payload_hash = Column(String(64), nullable=False)
    previous_event_hash = Column(String(64), nullable=True)
    timestamp = Column(DateTime, default=now_utc, index=True)
