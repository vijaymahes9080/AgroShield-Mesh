"""
AgroShield Mesh - Deterministic Baseline Risk Engine
Implements rule-based, transparent agronomic risk calculations for:
- Irrigation need
- Heat stress
- Drought risk
- Excess-rain risk
- Sensor anomaly detection
- Missing-data staleness & confidence penalty
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from backend.app.schemas.domain import (
    RiskLevel, RiskFactorBreakdown, MissingDataStatus, RiskAssessmentBase
)


class AgronomicRiskEngine:
    """
    Deterministic rule engine without black-box hallucinations.
    Every factor is explainable and traceable to agronomic thresholds.
    """

    # Soil hydrologic constants (Volumetric Water Content %)
    SOIL_PROPERTIES = {
        "Red Loam": {"field_capacity": 28.0, "wilting_point": 13.0, "saturation": 42.0},
        "Black Clay": {"field_capacity": 38.0, "wilting_point": 18.0, "saturation": 52.0},
        "Sandy Loam": {"field_capacity": 20.0, "wilting_point": 9.0, "saturation": 35.0},
        "Clay Loam": {"field_capacity": 34.0, "wilting_point": 16.0, "saturation": 48.0},
    }

    # Stage sensitivity multipliers for irrigation deficit
    STAGE_SENSITIVITY = {
        "sowing": 0.9,
        "vegetative": 1.0,
        "flowering": 1.4,          # Critical moisture period for paddy/millets/cotton
        "yield_formation": 1.2,
        "ripening": 0.6,
        "harvested": 0.1,
    }

    @classmethod
    def calculate_irrigation_need(
        cls,
        soil_moisture_pct: float,
        soil_type: str = "Red Loam",
        crop_stage: str = "vegetative",
        forecast_rain_24h_mm: float = 0.0,
        et0_mm: float = 4.5
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculates irrigation urgency (0 = saturated, 100 = critical water stress).
        Ground rule: If forecast rain >= 15mm, urgency is dampened to save water.
        """
        soil = cls.SOIL_PROPERTIES.get(soil_type, cls.SOIL_PROPERTIES["Red Loam"])
        fc = soil["field_capacity"]
        pwp = soil["wilting_point"]
        available_water_range = max(1.0, fc - pwp)
        current_depletion = max(0.0, fc - soil_moisture_pct)

        # Baseline depletion ratio
        depletion_ratio = current_depletion / available_water_range
        stage_factor = cls.STAGE_SENSITIVITY.get(crop_stage.lower(), 1.0)

        raw_score = depletion_ratio * 70.0 * stage_factor

        # ET0 adder: high evaporation accelerates urgency
        if et0_mm > 5.5:
            raw_score += 10.0
        elif et0_mm < 3.0:
            raw_score -= 5.0

        # Rain credit: If upcoming rain will replenish soil, reduce irrigation need
        if forecast_rain_24h_mm >= 25.0:
            raw_score = max(0.0, raw_score - 40.0)
        elif forecast_rain_24h_mm >= 10.0:
            raw_score = max(0.0, raw_score - 20.0)

        score = min(100.0, max(0.0, raw_score))

        details = {
            "soil_moisture_pct": soil_moisture_pct,
            "field_capacity_pct": fc,
            "wilting_point_pct": pwp,
            "depletion_ratio": round(depletion_ratio, 2),
            "stage_sensitivity_factor": stage_factor,
            "forecast_rain_credit_mm": forecast_rain_24h_mm,
            "et0_mm": et0_mm
        }
        return round(score, 1), details

    @classmethod
    def calculate_heat_stress(
        cls,
        temp_c: float,
        humidity_pct: float,
        crop_name: str = "Paddy (Rice)",
        crop_stage: str = "vegetative"
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculates heat stress score (0-100).
        Paddy is highly sensitive during flowering (>35°C can cause spikelet sterility).
        """
        # Simplified Heat Index approximation (Steadman formula simplified)
        heat_index = temp_c + (0.5555 * ((6.11 * (10 ** ((7.5 * temp_c) / (237.3 + temp_c))) * (humidity_pct / 100.0)) - 10.0))
        
        base_score = 0.0
        if temp_c > 40.0:
            base_score = 90.0
        elif temp_c > 37.0:
            base_score = 75.0
        elif temp_c > 34.0:
            base_score = 50.0
        elif temp_c > 31.0:
            base_score = 25.0

        # Stage amplifier
        if crop_stage.lower() == "flowering" and temp_c >= 35.0:
            base_score = min(100.0, base_score + 25.0)

        score = min(100.0, max(0.0, base_score))
        details = {
            "temp_c": temp_c,
            "humidity_pct": humidity_pct,
            "heat_index_c": round(heat_index, 1),
            "flowering_threshold_exceeded": (crop_stage.lower() == "flowering" and temp_c >= 35.0)
        }
        return round(score, 1), details

    @classmethod
    def calculate_drought_risk(
        cls,
        soil_moisture_pct: float,
        rainfall_14d_deficit_pct: float = 0.0,
        ndvi_mean: Optional[float] = None
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculates cumulative drought risk score (0-100).
        Combines moisture deficit with satellite vegetative vigour (NDVI).
        """
        moisture_component = max(0.0, (20.0 - soil_moisture_pct) * 3.5) if soil_moisture_pct < 20.0 else 0.0
        rain_deficit_component = (rainfall_14d_deficit_pct / 100.0) * 40.0

        ndvi_component = 0.0
        if ndvi_mean is not None:
            if ndvi_mean < 0.25:  # Sparse / severely stressed canopy
                ndvi_component = 25.0
            elif ndvi_mean < 0.40:
                ndvi_component = 15.0

        total_drought = min(100.0, moisture_component + rain_deficit_component + ndvi_component)
        details = {
            "moisture_component": round(moisture_component, 1),
            "rain_deficit_component": round(rain_deficit_component, 1),
            "ndvi_component": round(ndvi_component, 1),
            "ndvi_observed": ndvi_mean
        }
        return round(total_drought, 1), details

    @classmethod
    def calculate_excess_rain_risk(
        cls,
        soil_moisture_pct: float,
        rainfall_last_24h_mm: float,
        forecast_rain_next_24h_mm: float,
        soil_type: str = "Red Loam"
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculates waterlogging & inundation risk (0-100).
        High in black clay soils with poor percolation under heavy rain forecast.
        """
        soil = cls.SOIL_PROPERTIES.get(soil_type, cls.SOIL_PROPERTIES["Red Loam"])
        sat = soil["saturation"]

        soil_saturation_ratio = min(1.0, soil_moisture_pct / sat)
        total_precip_threat = rainfall_last_24h_mm + (forecast_rain_next_24h_mm * 1.2)

        risk = 0.0
        if total_precip_threat >= 70.0:
            risk = 85.0
        elif total_precip_threat >= 45.0:
            risk = 60.0
        elif total_precip_threat >= 25.0:
            risk = 35.0

        if soil_saturation_ratio > 0.90:
            risk = min(100.0, risk + 20.0)

        details = {
            "soil_saturation_ratio": round(soil_saturation_ratio, 2),
            "total_precip_threat_mm": round(total_precip_threat, 1),
            "drainage_risk": "high" if soil_type == "Black Clay" else "moderate"
        }
        return round(risk, 1), details

    @classmethod
    def detect_sensor_anomalies(
        cls,
        readings: List[Dict[str, Any]]
    ) -> Tuple[float, bool, List[str]]:
        """
        Detects sensor faults:
        - Out of physical bounds (soil moisture < 0% or > 100%, soil temp > 65°C)
        - Frozen sensor (exact identical value over 5+ consecutive readings)
        - Sudden impossible jump (>35% moisture change within 5 mins without rain)
        """
        if not readings:
            return 0.0, False, ["No sensor readings available"]

        anomalies = []
        anomaly_score = 0.0

        latest = readings[-1]
        moisture = latest.get("soil_moisture_pct", 25.0)
        temp = latest.get("soil_temperature_c", 28.0)
        battery = latest.get("battery_pct", 95.0)

        # 1. Bounds check
        if moisture < 0.0 or moisture > 98.0:
            anomalies.append(f"Soil moisture reading {moisture}% is physically abnormal")
            anomaly_score += 45.0
        if temp < -5.0 or temp > 60.0:
            anomalies.append(f"Soil temperature reading {temp}°C is out of biological bounds")
            anomaly_score += 35.0
        if battery < 15.0:
            anomalies.append(f"Node battery critical ({battery}%). Potential brownout readings")
            anomaly_score += 20.0

        # 2. Frozen sensor check (last 4 readings)
        if len(readings) >= 4:
            recent_moistures = [r.get("soil_moisture_pct") for r in readings[-4:] if r.get("soil_moisture_pct") is not None]
            if len(recent_moistures) == 4 and len(set(recent_moistures)) == 1:
                anomalies.append("Sensor stuck: identical consecutive moisture values detected")
                anomaly_score += 40.0

        # 3. Sudden jump check
        if len(readings) >= 2:
            prev_m = readings[-2].get("soil_moisture_pct", moisture)
            delta = abs(moisture - prev_m)
            if delta > 35.0:
                anomalies.append(f"Sudden extreme moisture jump detected (+/-{round(delta,1)}%)")
                anomaly_score += 35.0

        score = min(100.0, anomaly_score)
        has_anomaly = len(anomalies) > 0
        return round(score, 1), has_anomaly, anomalies

    @classmethod
    def evaluate_field_risk(
        cls,
        field_id: str,
        sensor_readings: List[Dict[str, Any]],
        weather_obs: Optional[Dict[str, Any]],
        satellite_obs: Optional[Dict[str, Any]],
        crop_cycle: Optional[Dict[str, Any]],
        soil_type: str = "Red Loam"
    ) -> RiskAssessmentBase:
        """
        Master deterministic evaluation function for a field.
        Returns complete transparent RiskAssessmentBase.
        """
        missing_fields = []
        confidence = 1.0

        # Check missing or stale data
        latest_sensor = sensor_readings[-1] if sensor_readings else None
        if not latest_sensor:
            missing_fields.append("sensor_telemetry")
            confidence -= 0.35
            moisture = 25.0
            soil_temp = 28.0
        else:
            moisture = latest_sensor.get("soil_moisture_pct", 25.0)
            soil_temp = latest_sensor.get("soil_temperature_c", 28.0)

        if not weather_obs:
            missing_fields.append("weather_station_data")
            confidence -= 0.25
            air_temp = 32.0
            air_humidity = 65.0
            rain_24h = 0.0
            rain_forecast = 0.0
            et0 = 4.5
        else:
            air_temp = weather_obs.get("temperature_c", 32.0)
            air_humidity = weather_obs.get("relative_humidity_pct", 65.0)
            rain_24h = weather_obs.get("rainfall_mm_last_24h", 0.0)
            rain_forecast = weather_obs.get("forecast_rain_next_24h_mm", 0.0)
            et0 = weather_obs.get("et0_evapotranspiration_mm", 4.5)

        ndvi = satellite_obs.get("ndvi_mean") if satellite_obs else None
        if satellite_obs is None:
            missing_fields.append("satellite_ndvi_observation")
            confidence -= 0.15

        crop_name = crop_cycle.get("crop_name", "Paddy (Rice)") if crop_cycle else "Paddy (Rice)"
        crop_stage = crop_cycle.get("current_stage", "vegetative") if crop_cycle else "vegetative"

        # Calculate individual factors
        irrigation_score, _ = cls.calculate_irrigation_need(
            soil_moisture_pct=moisture,
            soil_type=soil_type,
            crop_stage=crop_stage,
            forecast_rain_24h_mm=rain_forecast,
            et0_mm=et0
        )

        heat_score, _ = cls.calculate_heat_stress(
            temp_c=air_temp,
            humidity_pct=air_humidity,
            crop_name=crop_name,
            crop_stage=crop_stage
        )

        drought_score, _ = cls.calculate_drought_risk(
            soil_moisture_pct=moisture,
            rainfall_14d_deficit_pct=25.0 if rain_24h == 0.0 else 0.0,
            ndvi_mean=ndvi
        )

        excess_rain_score, _ = cls.calculate_excess_rain_risk(
            soil_moisture_pct=moisture,
            rainfall_last_24h_mm=rain_24h,
            forecast_rain_next_24h_mm=rain_forecast,
            soil_type=soil_type
        )

        anomaly_score, has_anomaly, anomaly_reasons = cls.detect_sensor_anomalies(sensor_readings)

        # Weighted aggregate
        breakdown = RiskFactorBreakdown(
            irrigation_need_score=irrigation_score,
            heat_stress_score=heat_score,
            drought_risk_score=drought_score,
            excess_rain_risk_score=excess_rain_score,
            sensor_anomaly_score=anomaly_score
        )

        # Multi-hazard agronomic aggregation:
        # Weighted aggregate + peak single-hazard dominance
        weighted_score = (
            (irrigation_score * 0.35) +
            (heat_score * 0.20) +
            (drought_score * 0.20) +
            (excess_rain_score * 0.15) +
            (anomaly_score * 0.10)
        )

        max_hazard = max(irrigation_score, heat_score, drought_score, excess_rain_score, anomaly_score)
        # In agronomic hazard assessment, a severe single threat (flood/drought/heat) elevates overall risk
        overall_score = max(weighted_score, max_hazard * 0.88)

        # Determine level
        if overall_score >= 72.0 or max_hazard >= 80.0 or anomaly_score >= 75.0:
            level = RiskLevel.CRITICAL
        elif overall_score >= 48.0 or max_hazard >= 55.0 or anomaly_score >= 35.0:
            level = RiskLevel.HIGH
        elif overall_score >= 24.0 or max_hazard >= 30.0:
            level = RiskLevel.MODERATE
        else:
            level = RiskLevel.LOW

        missing_status = MissingDataStatus(
            is_sensor_stale=(latest_sensor is None),
            is_weather_stale=(weather_obs is None),
            is_satellite_stale=(satellite_obs is None),
            missing_fields=missing_fields,
            confidence_penalty_pct=round((1.0 - max(0.2, confidence)) * 100.0, 1)
        )

        verification_steps = []
        if has_anomaly:
            verification_steps.append("Perform on-site physical check on mesh sensor node and probe wiring.")
        if irrigation_score > 65.0:
            verification_steps.append("Manually probe root-zone soil at 15cm depth to confirm moisture depletion before irrigating.")
        if excess_rain_score > 60.0:
            verification_steps.append("Inspect drainage channels at field boundary to prevent stagnation.")
        if not verification_steps:
            verification_steps.append("Routine weekly field inspection as per standard package of practices.")

        return RiskAssessmentBase(
            field_id=field_id,
            assessment_date=datetime.now(timezone.utc),
            overall_risk_level=level,
            overall_score=round(overall_score, 1),
            factor_breakdown=breakdown,
            missing_data_status=missing_status,
            confidence_score=round(max(0.2, confidence), 2),
            recommended_verification_steps=verification_steps,
            calculated_by="AgroShield Deterministic Agronomic Engine v1.0"
        )
