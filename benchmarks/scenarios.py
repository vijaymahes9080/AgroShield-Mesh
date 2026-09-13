"""
AgroShield Mesh - 100 Synthetic Benchmark Scenarios
Covers:
- 30 Irrigation cases (under-irrigation, optimal, over-irrigation, saturated)
- 20 Drought cases (moderate, acute deficit, heatwave, rainfall deficit)
- 20 Excess-rain cases (monsoon surge, cyclonic rainfall, waterlogging)
- 20 Contradictory sensor cases (stuck reading, sudden jump, out-of-bounds, battery drop)
- 10 Multilingual cases (Tamil & English)
"""

from typing import List, Dict, Any


def generate_100_benchmark_scenarios() -> List[Dict[str, Any]]:
    scenarios: List[Dict[str, Any]] = []

    # =========================================================
    # Category 1: 30 Irrigation Cases
    # =========================================================
    for i in range(1, 31):
        if i <= 10:
            # Under-irrigation / Dry soil
            moisture = 10.0 + (i * 0.5)
            stage = "flowering" if i % 2 == 0 else "vegetative"
            expected_irrigation = "HIGH" if moisture < 14.0 else "MODERATE"
            expected_risk = "high" if stage == "flowering" and moisture < 13.0 else "moderate"
            rain_fc = 0.0
        elif i <= 20:
            # Optimal moisture
            moisture = 24.0 + (i - 10) * 0.4
            stage = "vegetative"
            expected_irrigation = "LOW"
            expected_risk = "low"
            rain_fc = 2.0
        else:
            # High moisture / Saturated
            moisture = 34.0 + (i - 20) * 0.6
            stage = "ripening"
            expected_irrigation = "LOW"
            expected_risk = "low" if moisture < 38.0 else "moderate"
            rain_fc = 5.0

        scenarios.append({
            "id": f"SCEN-IRR-{i:03d}",
            "category": "irrigation",
            "field_id": f"field-irr-{i}",
            "crop_name": "Paddy (Rice)",
            "crop_stage": stage,
            "soil_type": "Red Loam",
            "sensor": {"soil_moisture_pct": moisture, "soil_temperature_c": 28.0, "ambient_temperature_c": 33.0, "ambient_humidity_pct": 65.0, "battery_pct": 90.0},
            "weather": {"temperature_c": 33.0, "relative_humidity_pct": 65.0, "rainfall_mm_last_24h": 0.0, "forecast_rain_next_24h_mm": rain_fc, "et0_evapotranspiration_mm": 4.5},
            "satellite": {"ndvi_mean": 0.65},
            "expected_irrigation_urgency": expected_irrigation,
            "expected_risk_level": expected_risk,
            "ground_truth_label": "irrigate_urgently" if expected_irrigation == "HIGH" else "withhold_irrigation" if expected_irrigation == "LOW" else "irrigate_moderately",
            "language": "en"
        })

    # =========================================================
    # Category 2: 20 Drought Cases
    # =========================================================
    for i in range(1, 21):
        moisture = 8.0 + (i * 0.4)
        temp = 36.5 + (i * 0.3)
        ndvi = 0.20 + (i * 0.01)
        expected_risk = "critical" if (temp >= 39.5 or moisture <= 11.0) else "high"

        scenarios.append({
            "id": f"SCEN-DROUGHT-{i:03d}",
            "category": "drought",
            "field_id": f"field-drought-{i}",
            "crop_name": "Paddy (Rice)",
            "crop_stage": "flowering" if i % 2 == 0 else "yield_formation",
            "soil_type": "Red Loam",
            "sensor": {"soil_moisture_pct": moisture, "soil_temperature_c": 32.0, "ambient_temperature_c": temp, "ambient_humidity_pct": 50.0, "battery_pct": 88.0},
            "weather": {"temperature_c": temp, "relative_humidity_pct": 50.0, "rainfall_mm_last_24h": 0.0, "forecast_rain_next_24h_mm": 0.0, "et0_evapotranspiration_mm": 6.2},
            "satellite": {"ndvi_mean": round(ndvi, 3)},
            "expected_irrigation_urgency": "HIGH",
            "expected_risk_level": expected_risk,
            "ground_truth_label": "drought_heat_emergency",
            "language": "en"
        })

    # =========================================================
    # Category 3: 20 Excess Rain Cases
    # =========================================================
    for i in range(1, 21):
        rain_24h = 15.0 + (i * 3.0)
        rain_fc = 25.0 + (i * 3.0)
        moisture = 35.0 + min(12.0, i * 0.5)
        # Total precip threat: rain_24h + 1.2 * rain_fc
        threat = rain_24h + (rain_fc * 1.2)
        expected_risk = "critical" if threat >= 70.0 else "high"

        scenarios.append({
            "id": f"SCEN-RAIN-{i:03d}",
            "category": "excess_rain",
            "field_id": f"field-rain-{i}",
            "crop_name": "Cotton" if i % 2 == 0 else "Paddy (Rice)",
            "crop_stage": "vegetative",
            "soil_type": "Black Clay",
            "sensor": {"soil_moisture_pct": moisture, "soil_temperature_c": 24.0, "ambient_temperature_c": 26.0, "ambient_humidity_pct": 92.0, "battery_pct": 85.0},
            "weather": {"temperature_c": 26.0, "relative_humidity_pct": 92.0, "rainfall_mm_last_24h": rain_24h, "forecast_rain_next_24h_mm": rain_fc, "et0_evapotranspiration_mm": 2.0},
            "satellite": {"ndvi_mean": 0.58},
            "expected_irrigation_urgency": "LOW",
            "expected_risk_level": expected_risk,
            "ground_truth_label": "drainage_flood_warning",
            "language": "en"
        })

    # =========================================================
    # Category 4: 20 Contradictory / Anomalous Sensor Cases
    # =========================================================
    for i in range(1, 21):
        if i <= 8:
            # Frozen sensor: consecutive identical values
            readings = [{"soil_moisture_pct": 22.4} for _ in range(5)]
            expected_risk = "high"
        elif i <= 14:
            # Out of biological range
            readings = [{"soil_moisture_pct": 105.0 if i % 2 == 0 else -8.0, "soil_temperature_c": 75.0}]
            expected_risk = "critical"
        else:
            # Sudden impossible jump without rain
            readings = [{"soil_moisture_pct": 15.0}, {"soil_moisture_pct": 58.0}]
            expected_risk = "high"

        scenarios.append({
            "id": f"SCEN-ANOMALY-{i:03d}",
            "category": "contradictory_sensor",
            "field_id": f"field-anom-{i}",
            "crop_name": "Paddy (Rice)",
            "crop_stage": "vegetative",
            "soil_type": "Red Loam",
            "sensor_history": readings,
            "weather": {"temperature_c": 32.0, "relative_humidity_pct": 65.0, "rainfall_mm_last_24h": 0.0, "forecast_rain_next_24h_mm": 0.0, "et0_evapotranspiration_mm": 4.5},
            "satellite": {"ndvi_mean": 0.65},
            "expected_irrigation_urgency": "UNCERTAIN_ANOMALY",
            "expected_risk_level": expected_risk,
            "ground_truth_label": "sensor_inspection_required",
            "language": "en"
        })

    # =========================================================
    # Category 5: 10 Multilingual Cases (Tamil & English)
    # =========================================================
    for i in range(1, 11):
        lang = "ta" if i % 2 == 1 else "en"
        moisture = 14.0 if i <= 5 else 26.0
        expected_risk = "critical" if moisture <= 14.0 else "moderate"

        scenarios.append({
            "id": f"SCEN-LANG-{i:03d}",
            "category": "multilingual",
            "field_id": f"field-multi-{i}",
            "crop_name": "Paddy (Rice)",
            "crop_stage": "flowering" if i <= 5 else "vegetative",
            "soil_type": "Red Loam",
            "sensor": {"soil_moisture_pct": moisture, "soil_temperature_c": 29.0, "ambient_temperature_c": 36.0, "ambient_humidity_pct": 68.0, "battery_pct": 92.0},
            "weather": {"temperature_c": 36.0, "relative_humidity_pct": 68.0, "rainfall_mm_last_24h": 0.0, "forecast_rain_next_24h_mm": 0.0, "et0_evapotranspiration_mm": 5.0},
            "satellite": {"ndvi_mean": 0.62},
            "expected_irrigation_urgency": "HIGH" if moisture <= 14.0 else "LOW",
            "expected_risk_level": expected_risk,
            "ground_truth_label": "bilingual_advisory",
            "language": lang
        })

    return scenarios
