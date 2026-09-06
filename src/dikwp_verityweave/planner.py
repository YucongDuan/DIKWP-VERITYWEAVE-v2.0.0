from __future__ import annotations

from .lexicons import HIGH_IMPACT_DOMAINS, PROTECTED_ROLES
from .models import CommonsSupport, Decision, Intervention, SemanticFlowCase, Signal
from .utils import clamp


def semantic_control_potential(case: SemanticFlowCase, signals: dict[str, Signal]) -> float:
    s = {key: signal.score for key, signal in signals.items()}
    intrinsic = clamp(
        0.13 * s["evidence_deficit"]
        + 0.11 * s["context_compression"]
        + 0.10 * s["uncertainty_laundering"]
        + 0.08 * s["authority_laundering"]
        + 0.09 * s["incentive_opacity"]
        + 0.11 * s["vulnerability_exploitation"]
        + 0.08 * s["compulsive_design"]
        + 0.08 * s["zero_sum_polarization"]
        + 0.09 * s["actionability_hazard"]
        + 0.05 * s["provenance_weakness"]
        + 0.05 * s["correction_obstruction"]
        + 0.03 * s["agent_propagation_risk"]
    )
    exposure = clamp(0.32 + 0.22 * case.reach + 0.18 * case.repetition + 0.28 * case.recommendation_intensity)
    power = clamp(0.28 * case.platform_power + 0.24 * case.creator_power + 0.20 * case.audience_dependence + 0.28 * case.decision_stakes)
    protective = clamp(0.18 * s["repair_capacity"] + 0.08 * s["public_interest_value"])
    return clamp(intrinsic * exposure * (0.72 + 0.58 * power) - protective)


def _i(layer: str, action: str, automatic: bool, reversible: bool, expiry_hours: int | None, human_gate: bool, *reasons: str) -> Intervention:
    return Intervention(
        layer=layer,
        action=action,
        automatic=automatic,
        reversible=reversible,
        expiry_hours=expiry_hours,
        human_gate=human_gate,
        reason_codes=list(reasons),
    )


def plan_interventions(
    case: SemanticFlowCase,
    signals: dict[str, Signal],
    commons: CommonsSupport,
) -> tuple[str, float, bool, bool, list[Intervention], list[str]]:
    s = {key: signal.score for key, signal in signals.items()}
    protected = case.content_role in PROTECTED_ROLES
    high_impact = case.domain in HIGH_IMPACT_DOMAINS or bool(
        set(case.audience_context) & {"minor", "acute_distress", "financial_crisis", "dependent_care"}
    )
    scp = semantic_control_potential(case, signals)
    actions: list[Intervention] = []
    reasons: list[str] = []

    if case.imminent_harm_or_illegal:
        if case.authorized_human_review:
            decision = Decision.AUTHORIZED_ESCALATION.value
            actions.append(_i("authority", "Prepare a time-bounded lawful safety action with evidence preservation.", False, True, 24, True, "IMMINENT_OR_UNLAWFUL_HARM"))
            reasons.append("IMMINENT_OR_UNLAWFUL_HARM_WITH_AUTHORIZED_REVIEW")
        else:
            decision = Decision.HUMAN_REVIEW.value
            actions.append(_i("authority", "Urgently preserve evidence and route to an authorized human reviewer.", False, True, 24, True, "AUTHORITY_REQUIRED"))
            reasons.append("IMMINENT_OR_UNLAWFUL_HARM_REQUIRES_AUTHORITY")
    elif case.verified_harm:
        decision = Decision.CORRECT_REPAIR.value
        actions.extend([
            _i("correction", "Propagate a correction to prior recipients and dependent decisions.", False, True, 168, True, "VERIFIED_HARM"),
            _i("remedy", "Prepare restoration, verified-loss compensation, and model-revision receipts.", False, True, None, True, "VERIFIED_HARM"),
        ])
        reasons.append("VERIFIED_HARM_REQUIRES_CORRECTION_AND_REPAIR")
    elif protected and not case.verified_fabrication:
        decision = Decision.PRESERVE.value
        actions.extend([
            _i("speech", "Do not restrict the item solely for negative tone, criticism, whistleblowing, satire, or distress.", True, True, None, False, "PROTECTED_EXPRESSION"),
            _i("reader", "Offer optional source lineage, context, and support resources without obscuring the original item.", True, True, None, False, "OPTIONAL_CONTEXT"),
        ])
        reasons.append("PROTECTED_ADVERSE_TRUTH_OR_EXPRESSION")
    elif commons.eligible and scp < 0.16:
        decision = Decision.SUPPORT_COMMONS.value
        actions.extend([
            _i("discovery", "Propose a transparent discovery boost for high-integrity public-value content.", False, True, 168, True, "COMMONS_SUPPORT_ELIGIBLE"),
            _i("creator", "Offer verification, translation, accessibility, or context-production support.", False, True, None, True, "COMMONS_SUPPORT_ELIGIBLE"),
        ])
        reasons.append("HIGH_INTEGRITY_PUBLIC_VALUE")
    elif high_impact and (s["evidence_deficit"] > 0.36 or s["actionability_hazard"] > 0.32):
        decision = Decision.HUMAN_REVIEW.value
        actions.extend([
            _i("reader", "Display a high-visibility uncertainty and scope card.", True, True, None, False, "HIGH_IMPACT_EVIDENCE_GAP"),
            _i("distribution", "Propose a temporary recommendation limit pending independent review.", False, True, 72, True, "HIGH_IMPACT_EVIDENCE_GAP"),
        ])
        reasons.append("HIGH_IMPACT_EVIDENCE_OR_ACTIONABILITY_GAP")
    elif (case.monetized or case.paid_amplification or case.affiliate_or_sales_funnel) and (
        s["incentive_opacity"] > 0.25 or s["vulnerability_exploitation"] > 0.28
    ):
        decision = Decision.MONETIZATION_GATE.value
        actions.extend([
            _i("commerce", "Propose a pause on paid amplification or affiliate conversion until disclosures are complete.", False, True, 72, True, "MONETIZED_MANIPULATION_RISK"),
            _i("creator", "Request evidence, conflicts, pricing, refund, failure-case, and scope disclosures.", True, True, None, False, "DISCLOSURE_REQUIRED"),
        ])
        reasons.append("MONETIZATION_AND_MANIPULATION_RISK")
    elif scp >= 0.46:
        decision = Decision.DAMPEN.value
        actions.extend([
            _i("reader", "Show a context card and require an explicit reshare confirmation.", True, True, None, False, "SEMANTIC_CONTROL_POTENTIAL"),
            _i("distribution", "Propose transparent circulation damping pending review; preserve direct access to the item.", False, True, 72, True, "SEMANTIC_CONTROL_POTENTIAL"),
        ])
        reasons.append("MULTI_LAYER_SEMANTIC_CONTROL_RISK")
    elif scp >= 0.25:
        decision = Decision.FRICTION.value
        actions.extend([
            _i("reader", "Add a user-local pause, source check, and context card before resharing or purchasing.", True, True, None, False, "CONTEXT_OR_MANIPULATION_RISK"),
            _i("creator", "Offer a balanced rewrite and explicit falsification questions.", True, True, None, False, "REPAIR_AVAILABLE"),
        ])
        reasons.append("CONTEXT_OR_MANIPULATION_RISK")
    elif scp >= 0.10:
        decision = Decision.CONTEXT.value
        actions.append(_i("reader", "Show an optional context, source, and incentive card.", True, True, None, False, "LIMITED_CONTEXT_OR_EVIDENCE"))
        reasons.append("LIMITED_CONTEXT_OR_EVIDENCE")
    else:
        decision = Decision.ALLOW.value
        actions.append(_i("distribution", "Apply no restriction.", True, True, None, False, "NO_MATERIAL_SIGNAL"))
        reasons.append("NO_MATERIAL_SEMANTIC_CONTROL_SIGNAL")

    if s["compulsive_design"] > 0.22:
        actions.append(_i("interface", "Disable autoplay, infinite scroll, variable rewards, or exit penalties in the user-local view.", True, True, None, False, "COMPULSIVE_DESIGN"))
        reasons.append("COMPULSIVE_DESIGN_FRICTION")
    if s["zero_sum_polarization"] > 0.24:
        actions.append(_i("relationship", "Generate a non-zero-sum repair card with affected parties and shared constraints.", True, True, None, False, "ZERO_SUM_FRAMING"))
        reasons.append("NON_ZERO_SUM_REPAIR_REQUIRED")
    if any(action.human_gate for action in actions):
        actions.append(_i("due_process", "Attach notice, reason codes, evidence scope, expiry, appeal, and restoration path.", False, True, None, True, "DUE_PROCESS_REQUIRED"))

    return decision, round(scp, 4), protected, high_impact, actions, sorted(set(reasons))
