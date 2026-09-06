from __future__ import annotations

from .models import CommonsSupport, SemanticFlowCase, Signal
from .utils import clamp


def assess_commons_support(case: SemanticFlowCase, signals: dict[str, Signal]) -> CommonsSupport:
    s = {key: signal.score for key, signal in signals.items()}
    integrity = clamp(
        0.19 * case.evidence_quality
        + 0.17 * case.source_traceability
        + 0.13 * case.counterevidence_visibility
        + 0.11 * case.uncertainty_disclosure
        + 0.13 * s["repair_capacity"]
        + 0.15 * s["public_interest_value"]
        + 0.06 * float(case.appeal_available)
        + 0.06 * float(case.correction_channel_available)
    )
    disqualifiers: list[str] = []
    if case.verified_fabrication:
        disqualifiers.append("VERIFIED_FABRICATION")
    if case.verified_harm:
        disqualifiers.append("VERIFIED_UNREPAIRED_HARM")
    if case.imminent_harm_or_illegal:
        disqualifiers.append("IMMINENT_OR_UNLAWFUL_HARM")
    if s["vulnerability_exploitation"] > 0.45:
        disqualifiers.append("MATERIAL_VULNERABILITY_EXPLOITATION")
    if s["incentive_opacity"] > 0.45:
        disqualifiers.append("MATERIAL_INCENTIVE_OPACITY")
    if s["correction_obstruction"] > 0.45:
        disqualifiers.append("CORRECTION_OBSTRUCTION")

    eligible = integrity >= 0.58 and not disqualifiers
    reasons: list[str] = []
    if case.evidence_quality >= 0.65:
        reasons.append("EVIDENCE_ADEQUATE")
    if case.source_traceability >= 0.65:
        reasons.append("SOURCE_LINEAGE_VISIBLE")
    if case.counterevidence_visibility >= 0.55:
        reasons.append("COUNTEREVIDENCE_INCLUDED")
    if s["public_interest_value"] >= 0.50:
        reasons.append("PUBLIC_INTEREST_VALUE")
    if s["repair_capacity"] >= 0.50:
        reasons.append("CORRECTION_READY")

    if not eligible:
        mode = "NO_SUPPORT_PROPOSAL"
    elif case.content_role in {"whistleblowing", "criticism"}:
        mode = "PROTECTED_ADVERSE_TRUTH_DISCOVERY_SUPPORT"
    elif case.content_role in {"education", "news"}:
        mode = "CONTEXT_AND_VERIFICATION_SUBSIDY_PROPOSAL"
    else:
        mode = "HIGH_INTEGRITY_COMMONS_DISCOVERY_BOOST_PROPOSAL"

    return CommonsSupport(
        eligible=eligible,
        integrity_score=round(integrity, 4),
        support_mode=mode,
        reasons=reasons,
        disqualifiers=disqualifiers,
    )
