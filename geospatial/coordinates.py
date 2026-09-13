"""
AgroShield Mesh - Geospatial Coordinate Reference Systems (CRS) & Transformations

Supported Coordinate Systems:
- EPSG:4326 (WGS 84): Standard geographic latitude/longitude in decimal degrees.
  Used for all GeoJSON payloads, Leaflet map coordinates, and GPS sensor locations.
- EPSG:3857 (WGS 84 / Pseudo-Mercator): Projected coordinates in meters.
  Used for metric buffer distances and flat map tile rendering.
"""

import math
from typing import Tuple, List, Dict, Any


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes the great-circle distance between two points on the Earth
    in kilometers using the Haversine formula (WGS84 mean radius = 6371.0 km).
    """
    r = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


def calculate_polygon_geodesic_area_hectares(coordinates: List[List[float]]) -> float:
    """
    Calculates the geodesic area of a polygon defined in EPSG:4326 (lon, lat)
    using the trapezoidal spherical approximation formula.
    Returns area in hectares (1 hectare = 10,000 m^2).
    """
    if len(coordinates) < 3:
        return 0.0

    # Ensure closed ring
    ring = coordinates
    if ring[0] != ring[-1]:
        ring = ring + [ring[0]]

    area_sq_m = 0.0
    r = 6378137.0  # WGS84 equatorial radius in meters

    for i in range(len(ring) - 1):
        p1 = ring[i]
        p2 = ring[i + 1]
        lon1, lat1 = math.radians(p1[0]), math.radians(p1[1])
        lon2, lat2 = math.radians(p2[0]), math.radians(p2[1])
        area_sq_m += (lon2 - lon1) * (2.0 + math.sin(lat1) + math.sin(lat2))

    area_sq_m = abs(area_sq_m * (r ** 2) / 4.0)
    return round(area_sq_m / 10000.0, 4)


def epsg4326_to_epsg3857(lon: float, lat: float) -> Tuple[float, float]:
    """Converts WGS84 (lon, lat) to EPSG:3857 Web Mercator (x, y) in meters."""
    r_major = 6378137.0
    x = r_major * math.radians(lon)
    scale = x / lon if lon != 0 else r_major * math.pi / 180.0
    y = 180.0 / math.pi * math.log(math.tan(math.pi / 4.0 + lat * (math.pi / 180.0) / 2.0)) * scale
    return x, y


def epsg3857_to_epsg4326(x: float, y: float) -> Tuple[float, float]:
    """Converts EPSG:3857 Web Mercator (x, y) to WGS84 (lon, lat)."""
    r_major = 6378137.0
    lon = math.degrees(x / r_major)
    lat = math.degrees(2.0 * math.atan(math.exp(y / r_major)) - math.pi / 2.0)
    return lon, lat
