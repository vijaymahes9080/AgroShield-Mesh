"""Unit tests for geospatial geometry and synthetic raster analysis."""
import pytest
from geospatial.coordinates import haversine_distance_km, calculate_polygon_geodesic_area_hectares
from geospatial.geometry import validate_field_boundary, is_point_inside_field
from geospatial.raster_analysis import generate_synthetic_raster_grid, compute_zonal_spectral_indices, compare_observation_history


def test_haversine_distance():
    # Distance between Erode (11.341, 77.717) and Perundurai (11.272, 77.581) is ~16-17 km
    d = haversine_distance_km(11.341, 77.717, 11.272, 77.581)
    assert 14.0 < d < 20.0


def test_field_polygon_validation():
    valid_coords = [
        [77.5810, 11.2720],
        [77.5845, 11.2720],
        [77.5845, 11.2755],
        [77.5810, 11.2755],
        [77.5810, 11.2720]
    ]
    geojson = {"type": "Polygon", "coordinates": [valid_coords]}
    is_valid, msg, area_ha = validate_field_boundary(geojson)
    assert is_valid is True
    assert area_ha > 0.5


def test_point_in_polygon():
    valid_coords = [
        [77.5810, 11.2720],
        [77.5845, 11.2720],
        [77.5845, 11.2755],
        [77.5810, 11.2755],
        [77.5810, 11.2720]
    ]
    geojson = {"type": "Polygon", "coordinates": [valid_coords]}
    assert is_point_inside_field(11.2735, 77.5825, geojson) is True
    assert is_point_inside_field(11.3000, 77.6000, geojson) is False


def test_synthetic_raster_ndvi():
    grid = generate_synthetic_raster_grid(rows=8, cols=8, base_health=0.75, stress_patch=True)
    res = compute_zonal_spectral_indices(grid)
    assert 0.4 < res["ndvi_mean"] < 0.9
    assert res["ndvi_min"] < res["ndvi_max"]
    assert res["stressed_area_pct"] > 0.0

    comp = compare_observation_history(0.55, 0.72)
    assert comp["trend"] == "severe_vegetative_drop"
