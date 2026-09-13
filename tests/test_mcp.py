"""Unit tests for Model Context Protocol (MCP) tools."""
import pytest
from mcp_server.tools import (
    mcp_get_field_status,
    mcp_get_weather_summary,
    mcp_get_crop_calendar,
    mcp_search_agri_guidance,
    mcp_calculate_irrigation_need,
    mcp_generate_farmer_advisory
)


def test_mcp_get_field_status():
    res = mcp_get_field_status("field-01")
    assert res["status"] == "active"
    assert "provenance" in res
    assert res["provenance"]["safety_mode"] == "read_only"


def test_mcp_get_crop_calendar():
    res = mcp_get_crop_calendar("Cotton", "flowering")
    assert "flowering" in res["stage_data"]
    assert "TNAU" in res["provenance"]["source"]


def test_mcp_calculate_irrigation_need():
    res = mcp_calculate_irrigation_need(soil_moisture_pct=14.0)
    assert res["irrigation_urgency_score"] > 50.0
    assert res["urgency_label"] in ["HIGH", "MODERATE"]


def test_mcp_generate_farmer_advisory():
    res = mcp_generate_farmer_advisory("field-demo", language="ta")
    assert res["advisory"] is not None
    assert "provenance" in res
