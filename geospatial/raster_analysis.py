"""
AgroShield Mesh - Synthetic Raster & Multispectral Analysis
Generates synthetic Sentinel-2 multi-band observations (Red Band 4, NIR Band 8, SWIR Band 11)
and computes:
- NDVI = (NIR - Red) / (NIR + Red)
- NDWI = (NIR - SWIR) / (NIR + SWIR)
- Field zonal statistics (mean, min, max, std, stress percentage)
- Temporal delta NDVI comparison
"""

import math
import random
from typing import Dict, Any, List, Tuple, Optional


def generate_synthetic_raster_grid(
    rows: int = 10,
    cols: int = 10,
    base_health: float = 0.65,
    stress_patch: bool = False,
    random_seed: int = 42
) -> Dict[str, List[List[float]]]:
    """
    Generates synthetic reflectance bands (0.0 to 1.0) for Red, NIR, and SWIR.
    Healthy vegetation: High NIR (~0.45 - 0.70), Low Red (~0.05 - 0.12).
    Stressed vegetation: Lower NIR (~0.20 - 0.35), Higher Red (~0.15 - 0.25).
    """
    rnd = random.Random(random_seed)
    red_band = []
    nir_band = []
    swir_band = []

    for r in range(rows):
        red_row = []
        nir_row = []
        swir_row = []
        for c in range(cols):
            # Introduce stress in top-right quadrant if stress_patch is True
            is_stressed = stress_patch and (r < rows // 2 and c > cols // 2)
            noise = rnd.uniform(-0.04, 0.04)

            if is_stressed:
                red_val = max(0.01, min(0.9, 0.22 + noise))
                nir_val = max(0.01, min(0.9, 0.32 + noise))
                swir_val = max(0.01, min(0.9, 0.38 + noise))
            else:
                red_val = max(0.01, min(0.9, (1.0 - base_health) * 0.20 + noise))
                nir_val = max(0.01, min(0.9, base_health * 0.75 + noise))
                swir_val = max(0.01, min(0.9, 0.18 + noise))

            red_row.append(round(red_val, 4))
            nir_row.append(round(nir_val, 4))
            swir_row.append(round(swir_val, 4))

        red_band.append(red_row)
        nir_band.append(nir_row)
        swir_band.append(swir_row)

    return {
        "red": red_band,
        "nir": nir_band,
        "swir": swir_band,
        "dimensions": [rows, cols],
        "resolution_meters": 10.0
    }


def compute_zonal_spectral_indices(
    raster_bands: Dict[str, List[List[float]]]
) -> Dict[str, Any]:
    """
    Calculates NDVI and NDWI arrays and extracts comprehensive zonal metrics.
    """
    red = raster_bands["red"]
    nir = raster_bands["nir"]
    swir = raster_bands.get("swir", nir)

    rows = len(red)
    cols = len(red[0]) if rows > 0 else 0

    ndvi_values = []
    ndwi_values = []
    ndvi_grid = []

    for r in range(rows):
        row_ndvi = []
        for c in range(cols):
            rv = red[r][c]
            nv = nir[r][c]
            sv = swir[r][c]

            # NDVI
            denom_ndvi = nv + rv
            val_ndvi = (nv - rv) / denom_ndvi if denom_ndvi != 0 else 0.0
            val_ndvi = max(-1.0, min(1.0, val_ndvi))
            ndvi_values.append(val_ndvi)
            row_ndvi.append(round(val_ndvi, 3))

            # NDWI
            denom_ndwi = nv + sv
            val_ndwi = (nv - sv) / denom_ndwi if denom_ndwi != 0 else 0.0
            val_ndwi = max(-1.0, min(1.0, val_ndwi))
            ndwi_values.append(val_ndwi)

        ndvi_grid.append(row_ndvi)

    if not ndvi_values:
        return {"ndvi_mean": 0.0, "ndvi_min": 0.0, "ndvi_max": 0.0, "ndwi_mean": 0.0}

    mean_ndvi = sum(ndvi_values) / len(ndvi_values)
    min_ndvi = min(ndvi_values)
    max_ndvi = max(ndvi_values)
    mean_ndwi = sum(ndwi_values) / len(ndwi_values)

    # Standard deviation
    variance = sum((x - mean_ndvi) ** 2 for x in ndvi_values) / len(ndvi_values)
    std_ndvi = math.sqrt(variance)

    # Stressed pixels: NDVI < 0.35 (for vegetative canopy)
    stressed_count = sum(1 for x in ndvi_values if x < 0.35)
    stress_pct = (stressed_count / len(ndvi_values)) * 100.0

    return {
        "ndvi_mean": round(mean_ndvi, 3),
        "ndvi_min": round(min_ndvi, 3),
        "ndvi_max": round(max_ndvi, 3),
        "ndvi_std": round(std_ndvi, 3),
        "ndwi_mean": round(mean_ndwi, 3),
        "stressed_area_pct": round(stress_pct, 1),
        "ndvi_grid": ndvi_grid,
        "total_pixels_analyzed": len(ndvi_values),
        "provenance": {
            "algorithm": "Sentinel-2 Normalized Difference Vegetation Index (B8 - B4)/(B8 + B4)",
            "sensor": "Synthetic MSI Simulator",
            "resolution": "10m"
        }
    }


def compare_observation_history(
    current_ndvi: float,
    previous_ndvi: Optional[float]
) -> Dict[str, Any]:
    """
    Compares current NDVI against previous observation.
    Detects sudden vegetative drops (pest outbreak, moisture stress) or steady growth.
    """
    if previous_ndvi is None:
        return {
            "trend": "baseline_established",
            "delta_ndvi": 0.0,
            "interpretation": "First observation in crop cycle. Baseline established."
        }

    delta = current_ndvi - previous_ndvi
    if delta <= -0.15:
        trend = "severe_vegetative_drop"
        interp = "Acute vegetation vigour decline detected (-15%+). High likelihood of water stress, pest infestation, or harvest."
    elif delta <= -0.07:
        trend = "moderate_decline"
        interp = "Slight vegetation decline observed. Recommended physical check of root-zone and leaves."
    elif delta >= 0.10:
        trend = "vigorous_growth"
        interp = "Strong canopy expansion consistent with healthy vegetative growth."
    else:
        trend = "stable"
        interp = "Vegetation index stable within normal seasonal tolerance."

    return {
        "trend": trend,
        "delta_ndvi": round(delta, 3),
        "interpretation": interp
    }
