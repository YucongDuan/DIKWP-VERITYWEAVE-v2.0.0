from __future__ import annotations

from .lexicons import PROTECTED_ROLES
from .models import SemanticFlowCase, Signal, WorldHypothesis
from .utils import normalize_weights


def build_worlds(case: SemanticFlowCase, signals: dict[str, Signal]) -> list[WorldHypothesis]:
    s = {key: signal.score for key, signal in signals.items()}
    protected = case.content_role in PROTECTED_ROLES
    commercial = float(case.monetized or case.paid_amplification or case.affiliate_or_sales_funnel)

    raw = {
        "bounded_good_faith": 0.26 + 0.42 * s["repair_capacity"] + (0.14 if case.content_role in {"advice", "personal_experience", "education"} else 0.0),
        "good_faith_compression": 0.12 + 0.62 * s["context_compression"] + 0.12 * s["evidence_deficit"],
        "negligent_overclaim": 0.10 + 0.48 * s["evidence_deficit"] + 0.22 * s["uncertainty_laundering"],
        "commercial_manipulation": 0.04 + commercial * (0.48 * s["incentive_opacity"] + 0.28 * s["vulnerability_exploitation"] + 0.18 * s["authority_laundering"]),
        "coordinated_deception": 0.01 + (0.76 if case.verified_fabrication else 0.03 * s["agent_propagation_risk"]),
        "satire_or_expressive_speech": 0.04 + (0.72 if case.content_role in {"satire", "entertainment", "distress_expression"} else 0.0),
        "protected_adverse_truth": 0.04 + (0.88 if protected else 0.0) + 0.22 * s["public_interest_value"],
        "insufficient_evidence": 0.08 + 0.28 * s["provenance_weakness"] + 0.18 * (1.0 - case.evidence_quality),
    }
    if not case.verified_fabrication:
        raw["coordinated_deception"] = 0.01 + 0.04 * s["agent_propagation_risk"]
    weights = normalize_weights(raw)

    templates: dict[str, tuple[str, list[str], list[str]]] = {
        "bounded_good_faith": (
            "Bounded good-faith support or education",
            ["Repair signals, qualifiers, and traceable sources reduce semantic control risk."],
            ["Evidence of concealed conflicts, fabrication, or coercive targeting."],
        ),
        "good_faith_compression": (
            "Good-faith but context-compressed communication",
            ["The useful core may be real while conditions and affected parties are omitted."],
            ["The claim remains stable after conditions, counterexamples, and costs are added."],
        ),
        "negligent_overclaim": (
            "Negligent overclaim or under-verified advice",
            ["Claim strength exceeds evidence and uncertainty disclosure."],
            ["Independent evidence supports the claim at the stated scope."],
        ),
        "commercial_manipulation": (
            "Commercial manipulation presented as knowledge",
            ["A sales funnel, urgency, authority laundering, and audience vulnerability co-occur."],
            ["Pricing, evidence, conflicts, failure cases, refund rights, and scope are fully disclosed."],
        ),
        "coordinated_deception": (
            "Coordinated or deliberate deception",
            ["This world receives material weight only from verified fabrication or campaign evidence."],
            ["Intent is unproven or new evidence supports error rather than deception."],
        ),
        "satire_or_expressive_speech": (
            "Satire, fiction, or protected emotional expression",
            ["The role and context may be expressive rather than instructional."],
            ["The content is presented as factual high-impact guidance or contains independent imminent harm."],
        ),
        "protected_adverse_truth": (
            "Protected criticism, whistleblowing, warning, or adverse truth",
            ["Public-interest value, sources, or a protected role warrant a strong preservation presumption."],
            ["Independent evidence establishes fabrication, targeted abuse, or imminent unlawful harm."],
        ),
        "insufficient_evidence": (
            "Insufficient evidence to classify intent or truth",
            ["Provenance, sources, and counterevidence remain incomplete."],
            ["New traceable evidence materially distinguishes the competing worlds."],
        ),
    }

    return [
        WorldHypothesis(
            key=key,
            label=templates[key][0],
            weight=round(weights[key], 4),
            supporting_reasons=templates[key][1],
            falsifiers=templates[key][2],
        )
        for key in sorted(weights, key=weights.get, reverse=True)
    ]
