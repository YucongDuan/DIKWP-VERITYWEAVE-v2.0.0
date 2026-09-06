from __future__ import annotations

from dataclasses import asdict

from .commons import assess_commons_support
from .graph import build_semantic_flow_graph
from .models import AnalysisResult, SemanticFlowCase
from .planner import plan_interventions
from .repair import build_repair_card
from .signals import extract_signals
from .utils import clamp, digest_json, utc_now
from .worlds import build_worlds

VERSION = "2.0.0"
SYSTEM_NAME = "DIKWP VerityWeave Semantic Resilience Grid OS"


def analyze(case: SemanticFlowCase) -> AnalysisResult:
    case.normalized()
    signals = extract_signals(case)
    worlds = build_worlds(case, signals)
    graph = build_semantic_flow_graph(case, signals)
    repair = build_repair_card(case, signals)
    commons = assess_commons_support(case, signals)
    decision, scp, protected, high_impact, interventions, reasons = plan_interventions(case, signals, commons)

    restrictive_or_adverse = decision in {
        "CIRCULATION_DAMPING_PROPOSAL",
        "MONETIZATION_DISCLOSURE_GATE",
        "CORRECTION_PROPAGATION_AND_REPAIR",
        "AUTHORIZED_LEGAL_OR_IMMINENT_SAFETY_ESCALATION",
    }
    deception_world = next(item for item in worlds if item.key == "coordinated_deception")
    invariants = {
        "negative_affect_alone_never_triggers_restriction": not (
            restrictive_or_adverse
            and all(
                signal.score < 0.12
                for key, signal in signals.items()
                if key not in {"negative_affect", "repair_capacity", "public_interest_value"}
            )
        ),
        "protected_expression_requires_independent_harm_basis_for_adverse_action": not (
            protected and restrictive_or_adverse and not (case.verified_harm or case.imminent_harm_or_illegal or case.verified_fabrication)
        ),
        "deliberate_deception_not_inferred_without_verified_fabrication": case.verified_fabrication or deception_world.weight < 0.15,
        "person_level_moral_scoring_prohibited": True,
        "viewpoint_or_sentiment_penalty_prohibited": True,
        "automatic_content_removal_authority_zero": True,
        "automatic_external_action_authority_zero": True,
        "adverse_platform_action_requires_human_gate": (not restrictive_or_adverse) or any(item.human_gate for item in interventions),
        "appeal_required_for_adverse_action": (not restrictive_or_adverse) or case.appeal_available,
        "correction_path_required_for_adverse_action": (not restrictive_or_adverse) or case.correction_channel_available,
    }

    confidence = clamp(
        0.22
        + 0.20 * case.source_traceability
        + 0.18 * case.evidence_quality
        + 0.14 * case.counterevidence_visibility
        + 0.12 * case.uncertainty_disclosure
        + 0.08 * float(case.provenance_manifest_present)
        + 0.06 * (1.0 - signals["provenance_weakness"].score)
    )
    limitations = [
        "This is a transparent semantic-flow risk analysis, not a fact-check verdict, diagnosis, intent finding, or legal determination.",
        "Text patterns cannot reliably establish a creator's state of mind; deliberate deception requires independent evidence.",
        "High-stakes health, finance, legal, education, child-safety, and public-interest decisions require qualified human review.",
        "Provenance can establish origin and edit history without proving that a claim is true.",
        "Platform-level adverse actions require notice, reasons, expiry, appeal, correction, and restoration processes.",
    ]
    provenance = {
        "system": SYSTEM_NAME,
        "version": VERSION,
        "method": "transparent_rules_plural_worlds_semantic_flow_graph_repair_first",
        "generated_at": utc_now(),
        "ai_origin_declared": case.ai_origin,
        "external_network_used": False,
        "input_digest": digest_json(asdict(case)),
    }
    return AnalysisResult(
        version=VERSION,
        case_digest=provenance["input_digest"],
        decision=decision,
        confidence=round(confidence, 4),
        semantic_control_potential=scp,
        protected_expression=protected,
        high_impact=high_impact,
        signals=signals,
        worlds=worlds,
        graph=graph,
        interventions=interventions,
        repair_card=repair,
        commons_support=commons,
        reason_codes=reasons,
        limitations=limitations,
        invariants=invariants,
        provenance=provenance,
    )
