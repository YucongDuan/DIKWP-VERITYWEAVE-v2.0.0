from __future__ import annotations

from dataclasses import asdict

from .commons import assess_commons_support
from .graph import build_semantic_flow_graph
from .models import AnalysisResult, SemanticFlowCase
from .planner import plan_interventions
from .repair import build_repair_card
from .runtime_validation import checked_invariants, require_valid_output, validate_analysis_output
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
        "Runtime PASS checks concern this generated local output only; external enforcement and operational safeguards are NOT_VERIFIED.",
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
    result = AnalysisResult(
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
        invariants={},
        provenance=provenance,
    )
    result.validation = validate_analysis_output(case, result)
    result.invariants = checked_invariants(result.validation)
    require_valid_output(result.validation)
    return result
