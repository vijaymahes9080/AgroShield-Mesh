"""
AgroShield Mesh - Standalone n8n Workflow Simulator
Simulates the exact execution branches of n8n:
- Ingestion webhook
- Idempotency & validation
- Risk check
- Bounded advisory generation
- Human review gating (High risk -> Expert queue, Normal -> Mock dispatch)
- Failure fallback branch
"""

import os
import sys
import json
import time
from typing import Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.workflow import BoundedAgentWorkflow
from backend.app.schemas.domain import LanguagePreference, RiskLevel


def run_n8n_simulation(
    field_id: str,
    sensor_payload: Dict[str, Any],
    mock_mode: bool = True
) -> Dict[str, Any]:
    """Runs a simulated n8n pipeline with deterministic checkpoints."""
    print("=" * 65)
    print("🌾 AGROSHIELD MESH — n8n WORKFLOW SIMULATION ENGINE")
    print(f"Mode: {'MOCK DISPATCH' if mock_mode else 'LIVE PRODUCTION'}")
    print("=" * 65)

    # 1. Trigger & Validation
    print("\n[Node 1 & 2] Webhook Trigger & Validation Guard...")
    if "field_id" not in sensor_payload or "soil_moisture_pct" not in sensor_payload:
        print("❌ Validation Error: Missing field_id or soil_moisture_pct. Routing to Failure Branch.")
        return {
            "workflow_status": "failed",
            "error_node": "Validate & Generate Idempotency Key",
            "message": "Missing required telemetry fields."
        }

    idempotency_key = f"{sensor_payload['field_id']}_{int(time.time())}"
    print(f"✅ Telemetry validated. Generated idempotency key: {idempotency_key}")

    # 2. Risk Calculation & Bounded Agent
    print("\n[Node 3 & 4] Backend Ingestion & Bounded Advisory Agent...")
    workflow = BoundedAgentWorkflow(use_sentence_transformers=False)
    state = workflow.run(
        field_id=field_id,
        sensor_readings=[sensor_payload],
        weather_observation={
            "temperature_c": sensor_payload.get("ambient_temperature_c", 35.0),
            "relative_humidity_pct": sensor_payload.get("ambient_humidity_pct", 65.0),
            "rainfall_mm_last_24h": 0.0,
            "forecast_rain_next_24h_mm": 0.0,
            "et0_evapotranspiration_mm": 5.2
        },
        crop_cycle={"crop_name": "Paddy (Rice)", "current_stage": "flowering"},
        language=LanguagePreference.TA
    )

    adv = state.final_advisory
    risk = state.risk_assessment

    print(f"✅ Risk Assessed: Score={risk.overall_score}/100, Level={risk.overall_risk_level.value}")
    print(f"✅ Advisory Composed: {adv.title[:50]}...")
    print(f"   Citations Attached: {len(adv.source_citations)} guides")

    # 3. Decision Gate: If High/Critical Risk -> Expert Review Gate
    print("\n[Node 5] Evaluating Human Review Gate Condition...")
    if adv.requires_human_review:
        print("⚠️ HIGH/CRITICAL RISK DETECTED: requires_human_review == TRUE")
        print("➡️ Routing to Node 6: 'Queue for Expert Agronomist Review'")
        outcome = {
            "workflow_status": "routed_to_expert_gate",
            "advisory_id": "adv-sim-001",
            "field_id": field_id,
            "requires_human_review": True,
            "review_status": "pending_review",
            "action": "Hold notification until an accredited agronomist reviews the advisory in dashboard."
        }
    else:
        print("ℹ️ Standard condition: requires_human_review == FALSE")
        print("➡️ Routing to Node 7: 'Dispatch Mock Farmer Notification'")
        outcome = {
            "workflow_status": "dispatched_mock_notification",
            "channel": "SMS_AND_WHATSAPP_MOCK",
            "recipient": "+91 98*** **210",
            "advisory_title": adv.title,
            "delivered_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "mock_mode": True
        }

    print("\n[Workflow Completed Successfully]")
    print(json.dumps(outcome, indent=2, ensure_ascii=False))
    return outcome


if __name__ == "__main__":
    test_payload = {
        "field_id": "field-perundurai-01",
        "device_id": "AGRO-MESH-004",
        "soil_moisture_pct": 17.5,
        "soil_temperature_c": 29.0,
        "ambient_temperature_c": 36.5,
        "ambient_humidity_pct": 68.0
    }
    run_n8n_simulation("field-perundurai-01", test_payload)
