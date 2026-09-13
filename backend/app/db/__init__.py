"""Database initialization."""
from backend.app.db.session import engine, SessionLocal, Base, get_db
from backend.app.db.models import (
    UserModel, FarmerModel, FieldModel, CropCycleModel,
    SensorReadingModel, WeatherObservationModel, SatelliteObservationModel,
    RiskAssessmentModel, AdvisoryModel, AdvisoryFeedbackModel, AuditEventModel
)


def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


__all__ = [
    "engine", "SessionLocal", "Base", "get_db", "init_db",
    "UserModel", "FarmerModel", "FieldModel", "CropCycleModel",
    "SensorReadingModel", "WeatherObservationModel", "SatelliteObservationModel",
    "RiskAssessmentModel", "AdvisoryModel", "AdvisoryFeedbackModel", "AuditEventModel"
]
