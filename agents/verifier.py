"""
AgroShield Mesh - Verification & Safety Guardrail Reviewer Agent
Enforces strict agricultural safety invariants:
- Zero autonomous pump activation
- Zero unsupported pesticide prescriptions
- Mandatory citations check
- Mandatory Human/Expert Review Gate for High and Critical risks
"""

from typing import List
from agents.state import WorkflowState
from backend.app.schemas.domain import ReviewStatus, RiskLevel


PROHIBITED_TRIGGER_WORDS = [
    "turn on pump", "start pump", "open valve", "run motor", "spray endosulfan",
    "spray monocrotophos", "pesticide dosage", "autonomous trigger"
]


class VerifierReviewerAgent:
    """Reviews draft advisory before delivery to enforce safety rules and human gate."""

    @classmethod
    def execute(cls, state: WorkflowState) -> WorkflowState:
        violations = []
        advisory = state.draft_advisory

        if not advisory:
            violations.append("Draft advisory is null. Cannot proceed to delivery.")
            state.safety_violations = violations
            state.workflow_completed = False
            return state

        # 1. Prohibited words check in title and action items
        combined_text = (advisory.title + " " + " ".join(advisory.action_items) + " " + advisory.summary).lower()
        for forbidden in PROHIBITED_TRIGGER_WORDS:
            if forbidden in combined_text:
                violations.append(f"Forbidden action phrase detected: '{forbidden}'. Direct machine control is prohibited.")

        # 2. Citations presence check
        if not advisory.source_citations:
            violations.append("Advisory lacks authoritative source citations. Recommendation must cite university guides.")

        # 3. High-Risk Human Review Gate
        risk = state.risk_assessment
        is_high_risk = risk and (risk.overall_risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL])
        if is_high_risk:
            advisory.requires_human_review = True
            advisory.review_status = ReviewStatus.PENDING_REVIEW
            state.requires_expert_gate = True
        else:
            advisory.requires_human_review = False
            advisory.review_status = ReviewStatus.AUTO_DISPATCHED
            state.requires_expert_gate = False

        state.safety_violations = violations
        state.final_advisory = advisory
        state.workflow_completed = (len(violations) == 0)

        state.log_step(
            stage_name="VERIFY",
            summary="Verification passed." if not violations else f"Verification failed with {len(violations)} violations.",
            details={
                "safety_passed": (len(violations) == 0),
                "requires_expert_gate": state.requires_expert_gate,
                "review_status": advisory.review_status.value
            }
        )
        return state
