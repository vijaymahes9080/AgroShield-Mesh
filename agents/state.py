"""
AgroShield Mesh - Bounded Agent Workflow State
Maintains immutable-first state transitions across the 7-stage pipeline:
COLLECT -> VALIDATE -> ANALYZE -> RETRIEVE -> COMPOSE -> VERIFY -> DELIVER
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from backend.app.schemas.domain import (
    RiskAssessmentBase, AdvisoryBase, Citation, LanguagePreference, ReviewStatus
)


@dataclass
class WorkflowState:
    field_id: str
    target_language: LanguagePreference = LanguagePreference.TA
    current_stage: str = "INITIALIZED"

    # Ingested & collected raw data
    farmer_data: Optional[Dict[str, Any]] = None
    field_data: Optional[Dict[str, Any]] = None
    crop_cycle: Optional[Dict[str, Any]] = None
    sensor_readings: List[Dict[str, Any]] = field(default_factory=list)
    weather_observation: Optional[Dict[str, Any]] = None
    satellite_observation: Optional[Dict[str, Any]] = None

    # Validation outputs
    validation_passed: bool = False
    validation_warnings: List[str] = field(default_factory=list)
    pii_masked: bool = False

    # Risk evaluation
    risk_assessment: Optional[RiskAssessmentBase] = None

    # Evidence retrieval
    retrieved_guidance: Optional[Dict[str, Any]] = None
    citations: List[Citation] = field(default_factory=list)

    # Generated advisory
    draft_advisory: Optional[AdvisoryBase] = None
    final_advisory: Optional[AdvisoryBase] = None

    # Verification & safety
    safety_violations: List[str] = field(default_factory=list)
    requires_expert_gate: bool = False
    workflow_completed: bool = False
    execution_trace: List[Dict[str, Any]] = field(default_factory=list)

    def log_step(self, stage_name: str, summary: str, details: Optional[Dict[str, Any]] = None):
        self.execution_trace.append({
            "stage": stage_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": summary,
            "details": details or {}
        })
        self.current_stage = stage_name
