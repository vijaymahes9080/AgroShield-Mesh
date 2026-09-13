"""Integration tests for FastAPI REST API endpoints."""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_and_version():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

    res_v = client.get("/api/v1/version")
    assert res_v.status_code == 200
    assert "AgroShield" in res_v.json()["name"]


def test_fields_api_flow():
    # 1. List fields
    res_list = client.get("/api/v1/fields")
    assert res_list.status_code == 200
    fields = res_list.json()
    assert len(fields) > 0

    field_id = fields[0]["id"]

    # 2. Get specific field
    res_field = client.get(f"/api/v1/fields/{field_id}")
    assert res_field.status_code == 200
    assert res_field.json()["id"] == field_id

    # 3. GeoJSON feature collection
    res_geo = client.get("/api/v1/fields-geojson")
    assert res_geo.status_code == 200
    assert res_geo.json()["type"] == "FeatureCollection"

    # 4. Synthetic raster
    res_raster = client.get(f"/api/v1/fields/{field_id}/synthetic-raster")
    assert res_raster.status_code == 200
    assert "ndvi_mean" in res_raster.json()["raster_analysis"]


def test_advisory_and_expert_review_flow():
    res_fields = client.get("/api/v1/fields")
    field_id = res_fields.json()[0]["id"]

    # Generate advisory
    res_adv = client.post(f"/api/v1/advisories?field_id={field_id}&language=ta")
    assert res_adv.status_code == 200
    advisory = res_adv.json()
    adv_id = advisory["id"]
    assert len(advisory["action_items"]) > 0

    # Review advisory
    review_payload = {
        "review_status": "expert_approved",
        "reviewer_name": "Dr. Raman (TNAU)",
        "review_notes": "Reviewed and approved for field distribution."
    }
    res_rev = client.post(f"/api/v1/advisories/{adv_id}/review", json=review_payload)
    assert res_rev.status_code == 200
    assert res_rev.json()["review_status"] == "expert_approved"

    # Submit feedback
    fb_payload = {
        "advisory_id": adv_id,
        "farmer_id": "farmer-erode-01",
        "rating": 5,
        "helpful_flag": True,
        "actual_action_taken": "Irrigated 3cm in early morning"
    }
    res_fb = client.post(f"/api/v1/advisories/{adv_id}/feedback", json=fb_payload)
    assert res_fb.status_code == 200
    assert res_fb.json()["rating"] == 5
