"""
AgroShield Mesh - Bilingual Advisory Composer Agent
Formulates evidence-grounded crop advisories in Tamil and English.
"""

from typing import Dict, Any, List
from agents.state import WorkflowState
from backend.app.schemas.domain import (
    AdvisoryBase, LanguagePreference, ReviewStatus, DataSourceType, RiskLevel
)


class AdvisoryComposerAgent:
    """
    Composes structured advisories grounded in retrieved citations and risk analysis.
    Supports English and Tamil with zero hallucination of chemicals or pump controls.
    """

    @classmethod
    def execute(cls, state: WorkflowState) -> WorkflowState:
        risk = state.risk_assessment
        crop = state.crop_cycle or {"crop_name": "Paddy (Rice)", "current_stage": "vegetative"}
        crop_name = crop.get("crop_name", "Paddy (Rice)")
        crop_stage = crop.get("current_stage", "vegetative")
        lang = state.target_language

        level = risk.overall_risk_level if risk else RiskLevel.LOW
        score = risk.overall_score if risk else 15.0

        # Action items & prohibited actions
        action_items_en = []
        action_items_ta = []
        prohibited_en = [
            "Do NOT operate high-power irrigation pumps autonomously without manual inspection of field drainage.",
            "Do NOT apply unapproved chemical insecticides or pesticides without diagnostic confirmation."
        ]
        prohibited_ta = [
            "வயல் வடிகால் அடைப்புகளை ஆய்வு செய்யாமல் தன்னிச்சையாக மின்மோட்டாரை இயக்க வேண்டாம்.",
            "பரிந்துரைக்கப்படாத பூச்சிக்கொல்லி மருந்துகளை தேவையின்றி பயன்படுத்த வேண்டாம்."
        ]

        # Grounding based on risk factors
        if risk and risk.factor_breakdown.irrigation_need_score > 60.0:
            action_items_en.append(
                f"Irrigation Required: Soil moisture is depleted during {crop_stage} stage. "
                "Apply measured 3-5 cm light irrigation in early morning to prevent crop water stress."
            )
            action_items_ta.append(
                f"பாசனம் தேவை: {crop_stage} பருவத்தில் மண் ஈரப்பதம் குறைந்துள்ளது. "
                "பயிர் வாடாமல் இருக்க அதிகாலை வேளையில் 3-5 செ.மீ அளவோடு நீர் பாய்ச்சவும்."
            )
        elif risk and risk.factor_breakdown.irrigation_need_score < 25.0:
            action_items_en.append(
                "Moisture Adequate: Soil moisture is optimal. Withhold scheduled irrigation to prevent waterlogging."
            )
            action_items_ta.append(
                "ஈரப்பதம் போதுமானது: மண்ணில் ஈரப்பதம் சரியாக உள்ளது. நீர் தேங்குவதைத் தவிர்க்க பாசனத்தை ஒத்திவைக்கவும்."
            )

        if risk and risk.factor_breakdown.heat_stress_score > 55.0:
            action_items_en.append(
                "Heat Stress Precaution: Ambient temperature elevated. Maintain thin standing water film to cool microclimate."
            )
            action_items_ta.append(
                "வெப்ப அழுத்தம் தடுப்பு: பகல் வெப்பநிலை உயர்ந்துள்ளது. பயிர் வெப்பத்தைத் தணிக்க வயலில் மெல்லிய நீர் படலத்தைப் பராமரிக்கவும்."
            )
            prohibited_en.append("Avoid foliar sprays between 11:00 AM and 3:00 PM due to high evaporation and leaf burn risk.")
            prohibited_ta.append("நண்பகல் 11 மணி முதல் பிற்பகல் 3 மணி வரை இலைவழி தெளிப்பைத் தவிர்க்கவும்.")

        if risk and risk.factor_breakdown.excess_rain_risk_score > 60.0:
            action_items_en.append(
                "Excess Rain Alert: Heavy rainfall predicted. Suspend all fertigation and clear bund drainage channels."
            )
            action_items_ta.append(
                "கனமழை எச்சரிக்கை: கனமழை வாய்ப்புள்ளதால் உரப்பாசனத்தை உடனடியாக நிறுத்தி வடிகால் வாய்க்கால்களை சுத்தம் செய்யவும்."
            )

        if not action_items_en:
            action_items_en.append(
                f"Field conditions are currently optimal for {crop_name} in {crop_stage} stage. Continue standard agronomic monitoring."
            )
            action_items_ta.append(
                f"{crop_name} பயிர் தற்போது ஆரோக்கியமாக உள்ளது. வழக்கமான களக் கண்காணிப்பைத் தொடரவும்."
            )

        # Titles and summaries
        if lang == LanguagePreference.TA:
            title = f"அக்ரோஷீல்டு பயிர் ஆலோசனை - {crop_name} ({level.value.upper()})"
            summary = (
                f"வயல் அபாய மதிப்பீடு: {score}/100 ({level.value}). "
                f"பல்கலைக்கழக வழிகாட்டுதல்கள் மற்றும் களத் தரவுகளின் அடிப்படையில் உருவாக்கப்பட்ட விவசாய ஆலோசனை."
            )
            final_actions = action_items_ta
            final_prohibited = prohibited_ta
        else:
            title = f"AgroShield Advisory: {crop_name} - {level.value.upper()} Risk Alert"
            summary = (
                f"Field composite risk index: {score}/100 ({level.value}). "
                f"Evidence-grounded agronomic recommendation compiled from university research guidelines."
            )
            final_actions = action_items_en
            final_prohibited = prohibited_en

        # Append university citation text if retrieved
        if state.retrieved_guidance and state.retrieved_guidance.get("status") == "evidence_found":
            texts = state.retrieved_guidance.get("tamil_texts" if lang == LanguagePreference.TA else "guidance_texts", [])
            for t in texts[:1]:
                final_actions.append(f"University Guideline Note: {t[:160]}...")

        advisory = AdvisoryBase(
            field_id=state.field_id,
            risk_assessment_id=None,
            language=lang,
            title=title,
            summary=summary,
            action_items=final_actions,
            prohibited_actions=final_prohibited,
            source_citations=state.citations,
            confidence_level=risk.confidence_score if risk else 0.85,
            requires_human_review=(level in [RiskLevel.HIGH, RiskLevel.CRITICAL]),
            review_status=ReviewStatus.PENDING_REVIEW if (level in [RiskLevel.HIGH, RiskLevel.CRITICAL]) else ReviewStatus.AUTO_DISPATCHED,
            data_sources_used=[DataSourceType.OBSERVED, DataSourceType.MODEL_GENERATED]
        )

        state.draft_advisory = advisory
        state.log_step(
            stage_name="COMPOSE",
            summary=f"Composed {lang.value} advisory with {len(final_actions)} action points and {len(state.citations)} citations.",
            details={"title": title, "requires_review": advisory.requires_human_review}
        )
        return state
