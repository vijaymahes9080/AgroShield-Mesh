"""Unit tests for Pydantic domain schemas and PII masking."""
import pytest
from datetime import datetime, timezone
from backend.app.schemas.domain import (
    FarmerCreate, FieldCreate, SensorReadingCreate, RiskLevel,
    DataSourceType, LanguagePreference, ReviewStatus
)
from agents.validator import mask_phone_number, mask_email, mask_farmer_pii


def test_pii_masking():
    assert mask_phone_number("+91 9876543210") == "+9198***210"
    m_email = mask_email("vijaypradhap2004@gmail.com")
    assert m_email.startswith("v")
    assert m_email.endswith("@gmail.com")
    assert "***" in m_email

    farmer_raw = {
        "name": "Vijay Mahes",
        "phone": "+91 9876543210",
        "email": "vijay@gmail.com",
        "village": "Perundurai"
    }
    masked = mask_farmer_pii(farmer_raw)
    assert "***" in masked["phone"]
    assert "***" in masked["email"]
    assert masked["name"] == "Vijay Mahes"


def test_field_schema_validation():
    field = FieldCreate(
        name="Test Paddy Field",
        farmer_id="farmer-01",
        boundary_geojson={
            "type": "Polygon",
            "coordinates": [[[77.58, 11.27], [77.59, 11.27], [77.59, 11.28], [77.58, 11.28], [77.58, 11.27]]]
        },
        area_hectares=1.5,
        soil_type="Red Loam"
    )
    assert field.area_hectares == 1.5
    assert field.soil_type == "Red Loam"


def test_sensor_reading_validation():
    reading = SensorReadingCreate(
        field_id="field-01",
        device_id="NODE-01",
        soil_moisture_pct=25.5,
        soil_temperature_c=28.0,
        ambient_temperature_c=34.0,
        ambient_humidity_pct=65.0,
        battery_pct=92.0
    )
    assert reading.soil_moisture_pct == 25.5
    assert reading.is_valid is True
