"""Unit tests for bounded agent workflow and safety review gate."""
import pytest
from agents.workflow import BoundedAgentWorkflow
from backend.app.schemas.domain import LanguagePreference, ReviewStatus, RiskLevel


def test_bounded_agent_7_stages():
    wf = BoundedAgentWorkflow(use_sentence_transformers=False)

    state = wf.run(
        field_id="field-test-01",
        sensor_readings=[{"soil_moisture_pct": 20.0, "soil_temperature_c": 27.0}],
        weather_observation={"temperature_c": 32.0, "relative_humidity_pct": 65.0, "rainfall_mm_last_24h": 0.0, "forecast_rain_next_24h_mm": 0.0, "et0_evapotranspiration_mm": 4.5},
        crop_cycle={"crop_name": "Paddy (Rice)", "current_stage": "vegetative"},
        language=LanguagePreference.EN
    )

    stage_names = [trace["stage"] for trace in state.execution_trace]
    assert "COLLECT" in stage_names
    assert "VALIDATE" in stage_names
    assert "ANALYZE" in stage_names
    assert "RETRIEVE" in stage_names
    assert "COMPOSE" in stage_names
    assert "VERIFY" in stage_names
    assert "DELIVER" in stage_names

    assert state.final_advisory is not None
    assert len(state.final_advisory.action_items) > 0
    assert len(state.final_advisory.source_citations) > 0


def test_safety_guardrail_human_review_gate():
    wf = BoundedAgentWorkflow(use_sentence_transformers=False)

    # Severe conditions -> should enforce pending review
    state = wf.run(
        field_id="field-crisis-01",
        sensor_readings=[{"soil_moisture_pct": 8.0, "soil_temperature_c": 34.0}],
        weather_observation={"temperature_c": 41.0, "relative_humidity_pct": 45.0, "rainfall_mm_last_24h": 0.0, "forecast_rain_next_24h_mm": 0.0, "et0_evapotranspiration_mm": 6.8},
        crop_cycle={"crop_name": "Paddy (Rice)", "current_stage": "flowering"},
        language=LanguagePreference.TA
    )

    assert state.final_advisory.requires_human_review is True
    assert state.final_advisory.review_status == ReviewStatus.PENDING_REVIEW
