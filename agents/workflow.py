"""
AgroShield Mesh - Bounded Agent Workflow Pipeline
Executes the sequential 7-stage pipeline:
COLLECT -> VALIDATE -> ANALYZE -> RETRIEVE -> COMPOSE -> VERIFY -> DELIVER
"""

from typing import Dict, Any, List, Optional
from agents.state import WorkflowState
from agents.validator import ValidatorAgent
from agents.risk_engine import AgronomicRiskEngine
from agents.composer import AdvisoryComposerAgent
from agents.verifier import VerifierReviewerAgent
from rag.retriever import AgriculturalRetriever
from backend.app.schemas.domain import LanguagePreference


class BoundedAgentWorkflow:
    """Orchestrates bounded multi-agent reasoning with deterministic checkpoints."""

    def __init__(self, use_sentence_transformers: bool = False):
        self.retriever = AgriculturalRetriever(use_sentence_transformers=use_sentence_transformers)

    def run(
        self,
        field_id: str,
        farmer_data: Optional[Dict[str, Any]] = None,
        field_data: Optional[Dict[str, Any]] = None,
        crop_cycle: Optional[Dict[str, Any]] = None,
        sensor_readings: Optional[List[Dict[str, Any]]] = None,
        weather_observation: Optional[Dict[str, Any]] = None,
        satellite_observation: Optional[Dict[str, Any]] = None,
        language: LanguagePreference = LanguagePreference.TA
    ) -> WorkflowState:
        """Runs the complete end-to-end bounded workflow."""
        state = WorkflowState(
            field_id=field_id,
            target_language=language,
            farmer_data=farmer_data,
            field_data=field_data,
            crop_cycle=crop_cycle,
            sensor_readings=sensor_readings or [],
            weather_observation=weather_observation,
            satellite_observation=satellite_observation
        )

        # 1. COLLECT
        state.log_step(
            stage_name="COLLECT",
            summary="Collected telemetry: sensor readings, weather report, satellite raster index, and crop cycle.",
            details={
                "sensor_readings_count": len(state.sensor_readings),
                "weather_available": state.weather_observation is not None,
                "satellite_available": state.satellite_observation is not None
            }
        )

        # 2. VALIDATE & MASK PII
        state = ValidatorAgent.execute(state)

        # 3. ANALYZE (Deterministic Risk Engine)
        soil_type = (field_data.get("soil_type") if field_data else "Red Loam") or "Red Loam"
        risk_assessment = AgronomicRiskEngine.evaluate_field_risk(
            field_id=field_id,
            sensor_readings=state.sensor_readings,
            weather_obs=state.weather_observation,
            satellite_obs=state.satellite_observation,
            crop_cycle=state.crop_cycle,
            soil_type=soil_type
        )
        state.risk_assessment = risk_assessment
        state.log_step(
            stage_name="ANALYZE",
            summary=f"Evaluated risk: Score={risk_assessment.overall_score}, Level={risk_assessment.overall_risk_level.value}.",
            details={
                "level": risk_assessment.overall_risk_level.value,
                "score": risk_assessment.overall_score,
                "irrigation_need": risk_assessment.factor_breakdown.irrigation_need_score,
                "heat_stress": risk_assessment.factor_breakdown.heat_stress_score,
                "confidence": risk_assessment.confidence_score
            }
        )

        # 4. RETRIEVE (RAG)
        crop_name = state.crop_cycle.get("crop_name", "Paddy (Rice)") if state.crop_cycle else "Paddy (Rice)"
        crop_stage = state.crop_cycle.get("current_stage", "vegetative") if state.crop_cycle else "vegetative"

        # Determine dominant hazard query
        top_hazard = "irrigation_need"
        if risk_assessment.factor_breakdown.excess_rain_risk_score > 60:
            top_hazard = "excess_rain_risk"
        elif risk_assessment.factor_breakdown.heat_stress_score > 55:
            top_hazard = "heat_stress"
        elif risk_assessment.factor_breakdown.drought_risk_score > 50:
            top_hazard = "drought_risk"

        retrieval_res = self.retriever.retrieve_guidance(
            query=f"{crop_name} {crop_stage} {top_hazard} management water",
            crop_name=crop_name,
            crop_stage=crop_stage,
            hazard_type=top_hazard,
            language=language.value,
            top_k=2
        )
        state.retrieved_guidance = retrieval_res
        state.citations = retrieval_res.get("citations", [])
        state.log_step(
            stage_name="RETRIEVE",
            summary=f"Retrieved {len(state.citations)} university citations for hazard '{top_hazard}'.",
            details={
                "hazard": top_hazard,
                "citations_count": len(state.citations),
                "top_score": retrieval_res.get("top_similarity_score", 0.0)
            }
        )

        # 5. COMPOSE
        state = AdvisoryComposerAgent.execute(state)

        # 6. VERIFY & GUARDRAIL
        state = VerifierReviewerAgent.execute(state)

        # 7. DELIVER
        if state.final_advisory:
            state.log_step(
                stage_name="DELIVER",
                summary=f"Delivered advisory to review queue/dispatch. Review status: {state.final_advisory.review_status.value}.",
                details={
                    "status": state.final_advisory.review_status.value,
                    "requires_review": state.final_advisory.requires_human_review,
                    "action_items_count": len(state.final_advisory.action_items)
                }
            )

        return state
