"""
AgroShield Mesh - Geometry validation and spatial queries using Shapely.
"""

from typing import Dict, Any, List, Tuple, Optional
from shapely.geometry import shape, Polygon, Point, mapping
from shapely.validation import explain_validity
from geospatial.coordinates import calculate_polygon_geodesic_area_hectares, haversine_distance_km


def validate_field_boundary(boundary_geojson: Dict[str, Any]) -> Tuple[bool, str, float]:
    """
    Validates GeoJSON Polygon geometry:
    - Checks for valid GeoJSON structure
    - Checks for topological validity (no self-intersections, valid rings)
    - Checks that coordinates fall within valid geographic bounds (lon: -180..180, lat: -90..90)
    - Checks minimum area (at least 0.01 hectares / 100 m^2)
    Returns: (is_valid, message, area_hectares)
    """
    try:
        geom = shape(boundary_geojson)
    except Exception as e:
        return False, f"Invalid GeoJSON geometry format: {str(e)}", 0.0

    if not isinstance(geom, Polygon):
        return False, f"Geometry must be a Polygon, got {geom.geom_type}", 0.0

    if not geom.is_valid:
        reason = explain_validity(geom)
        return False, f"Topologically invalid polygon: {reason}", 0.0

    # Bounds check
    min_lon, min_lat, max_lon, max_lat = geom.bounds
    if not (-180 <= min_lon <= 180 and -180 <= max_lon <= 180 and -90 <= min_lat <= 90 and -90 <= max_lat <= 90):
        return False, "Coordinates outside valid WGS84 range (-180..180 lon, -90..90 lat)", 0.0

    # Extract exterior coordinates
    coords = list(geom.exterior.coords)
    area_ha = calculate_polygon_geodesic_area_hectares(coords)

    if area_ha < 0.005:
        return False, f"Field area too small ({area_ha} ha). Minimum required is 0.01 ha.", area_ha

    return True, "Valid field polygon", area_ha


def is_point_inside_field(lat: float, lon: float, boundary_geojson: Dict[str, Any]) -> bool:
    """Checks if a sensor or GPS coordinate is contained inside the field polygon."""
    geom = shape(boundary_geojson)
    pt = Point(lon, lat)
    return geom.contains(pt) or geom.touches(pt)


def find_nearest_weather_station(
    field_centroid_lat: float,
    field_centroid_lon: float,
    stations: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Finds the nearest weather station to a field centroid using Haversine distance."""
    if not stations:
        return None

    best_station = None
    min_dist_km = float("inf")

    for st in stations:
        s_lat = st.get("lat")
        s_lon = st.get("lon")
        if s_lat is not None and s_lon is not None:
            dist = haversine_distance_km(field_centroid_lat, field_centroid_lon, s_lat, s_lon)
            if dist < min_dist_km:
                min_dist_km = dist
                best_station = {**st, "distance_km": round(dist, 2)}

    return best_station


def format_map_ready_geojson(
    fields_data: List[Dict[str, Any]],
    include_risk_style: bool = True
) -> Dict[str, Any]:
    """
    Transforms fields into a styled GeoJSON FeatureCollection
    ready for Leaflet or MapLibre visualization.
    """
    features = []
    risk_colors = {
        "low": "#10B981",       # Emerald green
        "moderate": "#F59E0B",  # Amber
        "high": "#EF4444",      # Red
        "critical": "#991B1B"   # Dark crimson
    }

    for f in fields_data:
        boundary = f.get("boundary_geojson", {})
        risk_level = f.get("current_risk_level", "low").lower()
        color = risk_colors.get(risk_level, "#3B82F6")

        feature = {
            "type": "Feature",
            "id": f.get("id"),
            "geometry": boundary,
            "properties": {
                "field_id": f.get("id"),
                "name": f.get("name"),
                "farmer_name": f.get("farmer_name", "Farmer"),
                "area_hectares": f.get("area_hectares"),
                "soil_type": f.get("soil_type"),
                "irrigation_source": f.get("irrigation_source"),
                "risk_level": risk_level,
                "ndvi_mean": f.get("ndvi_mean", 0.65),
                "soil_moisture_pct": f.get("soil_moisture_pct", 24.0),
                "fillColor": color,
                "fillOpacity": 0.45,
                "color": color,
                "weight": 2.5
            }
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }
