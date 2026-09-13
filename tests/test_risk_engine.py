"""Unit tests for deterministic baseline risk engine."""
import pytest
from agents.risk_engine import AgronomicRiskEngine
from backend.app.schemas.domain import RiskLevel


def test_irrigation_need_under_drought_vs_rain():
    # Dry soil during flowering -> high irrigation need
    score_dry, details_dry = AgronomicRiskEngine.calculate_irrigation_need(
        soil_moisture_pct=12.0,
        soil_type="Red Loam",
        crop_stage="flowering",
        forecast_rain_24h_mm=0.0
    )
    assert score_dry >= 65.0
    assert details_dry["depletion_ratio"] > 0.8

    # Rain credit: Upcoming heavy rain (30mm) should reduce irrigation need
    score_rain, details_rain = AgronomicRiskEngine.calculate_irrigation_need(
        soil_moisture_pct=12.0,
        soil_type="Red Loam",
        crop_stage="flowering",
        forecast_rain_24h_mm=30.0
    )
    assert score_rain < score_dry


def test_heat_stress_flowering_paddy():
    # Temperature > 35C during flowering triggers heat stress
    score_hot, details = AgronomicRiskEngine.calculate_heat_stress(
        temp_c=38.0,
        humidity_pct=70.0,
        crop_name="Paddy (Rice)",
        crop_stage="flowering"
    )
    assert score_hot >= 75.0
    assert details["flowering_threshold_exceeded"] is True


def test_sensor_anomaly_detection():
    # Frozen consecutive values
    readings = [{"soil_moisture_pct": 21.0} for _ in range(5)]
    score, has_anomaly, reasons = AgronomicRiskEngine.detect_sensor_anomalies(readings)
    assert has_anomaly is True
    assert score >= 40.0
    assert any("Sensor stuck" in r for r in reasons)

    # Physical out-of-bounds check
    bad_readings = [{"soil_moisture_pct": 110.0, "soil_temperature_c": 75.0, "battery_pct": 10.0}]
    b_score, b_anom, b_reasons = AgronomicRiskEngine.detect_sensor_anomalies(bad_readings)
    assert b_anom is True
    assert b_score >= 60.0
