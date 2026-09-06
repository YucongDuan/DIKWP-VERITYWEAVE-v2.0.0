from __future__ import annotations

from .lexicons import ADDICTIVE_FEATURE_WEIGHTS, LEXICONS
from .models import SemanticFlowCase, Signal
from .utils import clamp, find_markers, saturation


def _signal(key: str, score: float, markers: list[str], explanation: str, restrictive: bool = True) -> Signal:
    return Signal(
        key=key,
        score=round(clamp(score), 4),
        markers=sorted(set(markers)),
        explanation=explanation,
        restrictive_feature=restrictive,
    )


def extract_signals(case: SemanticFlowCase) -> dict[str, Signal]:
    marks = {key: find_markers(case.text, values) for key, values in LEXICONS.items()}

    universalism = saturation(len(marks["universalism"]))
    certainty = saturation(len(marks["certainty"]))
    causal = saturation(len(marks["causal_leap"]))
    qualifiers = saturation(len(marks["qualifiers"]))
    context = saturation(len(marks["context_markers"]))
    rights = saturation(len(marks["rights_markers"]))
    urgency = saturation(len(marks["urgency"]))
    authority = saturation(len(marks["authority_laundering"]))
    identity = saturation(len(marks["identity_coercion"]))
    zero_sum = saturation(len(marks["zero_sum"]))
    shaming = saturation(len(marks["shaming"]))
    self_sealing = saturation(len(marks["self_sealing"]))
    conspiracy = saturation(len(marks["conspiracy"]))
    monetization_text = saturation(len(marks["monetization"]))
    correction_blockers = saturation(len(marks["correction_obstruction"]))
    action_hazard_markers = saturation(len(marks["actionability_hazard"]))
    public_interest_markers = saturation(len(marks["public_interest"]))

    claim_strength = clamp(0.36 * universalism + 0.36 * certainty + 0.28 * causal)
    evidence_deficit = clamp(
        0.48 * claim_strength * (1.0 - case.evidence_quality)
        + 0.24 * (1.0 - case.source_traceability)
        + 0.16 * authority * (1.0 - case.source_traceability)
        + 0.12 * (1.0 - case.counterevidence_visibility)
    )
    context_compression = clamp(
        0.30 * universalism + 0.22 * causal + 0.22 * zero_sum + 0.18 * identity
        + 0.08 * case.decision_stakes
        - 0.18 * qualifiers - 0.16 * context - 0.10 * rights
    )
    uncertainty_laundering = clamp(
        0.42 * certainty + 0.22 * causal + 0.18 * self_sealing
        + 0.18 * (1.0 - case.uncertainty_disclosure) - 0.16 * qualifiers
    )
    authority_laundering = clamp(
        0.68 * authority + 0.18 * certainty * (1.0 - case.source_traceability)
        + 0.14 * case.creator_power * authority
    )
    commercial_pressure = float(case.monetized or case.paid_amplification or case.affiliate_or_sales_funnel)
    incentive_opacity = clamp(
        commercial_pressure * (
            0.24 * monetization_text + 0.22 * urgency + 0.18 * (1.0 - float(case.commercial_conflict_disclosed))
            + 0.18 * (1.0 - case.price_transparency) + 0.18 * (1.0 - case.refund_transparency)
        )
    )
    manipulation_pressure = clamp(
        0.18 * urgency + 0.15 * authority + 0.17 * identity + 0.13 * shaming
        + 0.17 * self_sealing + 0.08 * conspiracy + 0.12 * incentive_opacity
    )
    compulsive_design = clamp(sum(ADDICTIVE_FEATURE_WEIGHTS.get(item, 0.08) for item in case.addictive_features))

    vulnerability_density = min(1.0, len(set(case.audience_context)) / 4.0)
    influence_asymmetry = clamp(
        0.35 * case.platform_power + 0.25 * case.creator_power
        + 0.20 * case.audience_dependence + 0.20 * case.recommendation_intensity
    )
    vulnerability_exploitation = clamp(
        vulnerability_density * (0.42 * manipulation_pressure + 0.26 * context_compression + 0.16 * urgency + 0.16 * influence_asymmetry)
    )
    zero_sum_polarization = clamp(
        0.46 * zero_sum + 0.20 * identity + 0.16 * shaming + 0.10 * self_sealing
        + 0.08 * case.recommendation_intensity - 0.12 * rights - 0.08 * context
    )
    actionability_hazard = clamp(
        0.46 * action_hazard_markers + 0.22 * case.decision_stakes * certainty
        + 0.16 * urgency + 0.16 * vulnerability_exploitation
    )
    provenance_weakness = clamp(
        0.40 * (1.0 - case.source_traceability)
        + 0.22 * (1.0 - case.evidence_quality)
        + 0.18 * (1.0 - float(case.provenance_manifest_present))
        + 0.20 * (1.0 - case.counterevidence_visibility)
    )
    correction_obstruction = clamp(
        0.36 * correction_blockers + 0.22 * self_sealing
        + 0.16 * (1.0 - float(case.appeal_available))
        + 0.14 * (1.0 - float(case.correction_channel_available))
        + 0.12 * (1.0 - case.counterevidence_visibility)
    )
    agent_propagation_risk = clamp(
        0.22 * case.repetition + 0.22 * case.recommendation_intensity
        + 0.16 * case.reach + 0.16 * compulsive_design
        + 0.12 * provenance_weakness + 0.12 * correction_obstruction
    )
    repair_capacity = clamp(
        0.18 * qualifiers + 0.18 * context + 0.14 * rights
        + 0.16 * case.source_traceability + 0.12 * case.counterevidence_visibility
        + 0.10 * case.uncertainty_disclosure + 0.06 * float(case.appeal_available)
        + 0.06 * float(case.correction_channel_available)
    )
    public_interest_value = clamp(
        0.34 * public_interest_markers
        + 0.18 * case.source_traceability
        + 0.16 * case.evidence_quality
        + 0.12 * case.counterevidence_visibility
        + 0.10 * case.uncertainty_disclosure
        + 0.10 * repair_capacity
    )
    negative_affect = saturation(len(marks["distress"]))

    return {
        "evidence_deficit": _signal("evidence_deficit", evidence_deficit, marks["certainty"] + marks["authority_laundering"] + marks["causal_leap"], "The gap between claim strength and traceable support."),
        "context_compression": _signal("context_compression", context_compression, marks["universalism"] + marks["zero_sum"] + marks["identity_coercion"], "Omitted conditions, affected parties, counterexamples, or resource constraints."),
        "uncertainty_laundering": _signal("uncertainty_laundering", uncertainty_laundering, marks["certainty"] + marks["self_sealing"], "Uncertainty is presented as settled fact or made resistant to correction."),
        "authority_laundering": _signal("authority_laundering", authority_laundering, marks["authority_laundering"], "Prestige or vague expertise substitutes for checkable evidence."),
        "incentive_opacity": _signal("incentive_opacity", incentive_opacity, marks["monetization"] + marks["urgency"], "Commercial benefit, pricing, refund, or affiliation is hidden or under-disclosed."),
        "vulnerability_exploitation": _signal("vulnerability_exploitation", vulnerability_exploitation, list(case.audience_context), "Pressure is coupled to temporary audience vulnerability; this is not a person-level ability rating."),
        "compulsive_design": _signal("compulsive_design", compulsive_design, list(case.addictive_features), "Interface and distribution features are optimized to prolong engagement or punish exit."),
        "zero_sum_polarization": _signal("zero_sum_polarization", zero_sum_polarization, marks["zero_sum"] + marks["identity_coercion"] + marks["shaming"], "Relationships or groups are framed as a forced winner-versus-loser conflict."),
        "actionability_hazard": _signal("actionability_hazard", actionability_hazard, marks["actionability_hazard"], "The content pushes consequential action without proportionate evidence, safeguards, or reversibility."),
        "provenance_weakness": _signal("provenance_weakness", provenance_weakness, [], "Origin, edits, sources, and counterevidence are difficult to reconstruct."),
        "correction_obstruction": _signal("correction_obstruction", correction_obstruction, marks["correction_obstruction"] + marks["self_sealing"], "The content or service makes correction, appeal, refund, or dissent unusually difficult."),
        "agent_propagation_risk": _signal("agent_propagation_risk", agent_propagation_risk, [], "The same method or artifact can be rapidly amplified or inherited across automated systems."),
        "repair_capacity": _signal("repair_capacity", repair_capacity, marks["qualifiers"] + marks["context_markers"] + marks["rights_markers"], "The content exposes scope, uncertainty, counterevidence, appeal, and correction paths.", restrictive=False),
        "public_interest_value": _signal("public_interest_value", public_interest_value, marks["public_interest"], "Potential public value from adverse truth, evidence, warnings, or repair-enabling information.", restrictive=False),
        "negative_affect": _signal("negative_affect", negative_affect, marks["distress"], "Negative emotion or bad news. This signal is recorded but never independently triggers restriction.", restrictive=False),
    }
