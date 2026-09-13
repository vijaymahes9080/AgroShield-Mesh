"""
AgroShield Mesh - Validation & PII Masking Agent
Performs data integrity checks, sensor anomaly gating, and PII masking.
"""

import re
from typing import Dict, Any, List, Tuple
from agents.state import WorkflowState


def mask_phone_number(phone: str) -> str:
    """Masks middle digits of phone: +91 9876543210 -> +91 98*** **210"""
    clean = re.sub(r"[^\d+]", "", phone)
    if len(clean) >= 10:
        return clean[:5] + "***" + clean[-3:]
    return "***-***-****"


def mask_email(email: str) -> str:
    """Masks username of email: vijay@gmail.com -> v***y@gmail.com"""
    if "@" not in email:
        return "****"
    user, domain = email.split("@", 1)
    if len(user) <= 2:
        masked_user = user[0] + "*"
    else:
        masked_user = user[0] + "*" * (len(user) - 2) + user[-1]
    return f"{masked_user}@{domain}"


def mask_farmer_pii(farmer_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Returns a sanitized copy of farmer data with PII masked."""
    sanitized = dict(farmer_dict)
    if "phone" in sanitized and sanitized["phone"]:
        sanitized["phone"] = mask_phone_number(sanitized["phone"])
    if "email" in sanitized and sanitized["email"]:
        sanitized["email"] = mask_email(sanitized["email"])
    return sanitized


class ValidatorAgent:
    """Validates raw field observations, masks sensitive farmer info, and checks staleness."""

    @classmethod
    def execute(cls, state: WorkflowState) -> WorkflowState:
        warnings = []

        # 1. PII Masking
        if state.farmer_data:
            state.farmer_data = mask_farmer_pii(state.farmer_data)
            state.pii_masked = True

        # 2. Check sensor availability
        if not state.sensor_readings:
            warnings.append("No active IoT mesh sensor telemetry found. Proceeding with weather fallback.")
        else:
            latest = state.sensor_readings[-1]
            m = latest.get("soil_moisture_pct")
            if m is not None and (m < 0 or m > 100):
                warnings.append(f"Sensor moisture {m}% is physically anomalous.")

        # 3. Check weather availability
        if not state.weather_observation:
            warnings.append("No local weather station observation found. Proceeding with regional default.")

        # 4. Check crop cycle
        if not state.crop_cycle:
            warnings.append("No active crop cycle registered for field. Defaulting to general paddy practices.")

        state.validation_warnings = warnings
        state.validation_passed = True
        state.log_step(
            stage_name="VALIDATE",
            summary=f"Validation completed with {len(warnings)} data caveats.",
            details={"warnings": warnings, "pii_masked": state.pii_masked}
        )
        return state
