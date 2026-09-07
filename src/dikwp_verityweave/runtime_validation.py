"""Executable, fail-closed checks of local generated outputs.

A PASS is a checked predicate about this payload, not proof that a platform,
person, remote agent, or production system obeys the policy. Declared controls
and unobserved real-world outcomes are kept separate. Previously supplied
``invariants`` or ``validation`` values are never trusted by these validators.
"""
from __future__ import annotations

import math
from dataclasses import asdict, fields, is_dataclass, replace
from typing import Any

from .lexicons import PROTECTED_ROLES
from .models import AnalysisResult, InterfaceAuditResult, AgentLineageResult, SemanticFlowCase, InterfaceAuditCase, AgentLineageCase

SCOPE = "local_generated_output_only"

# Exact local-output catalog. Unknown strings cannot silently gain execution or
# proposal authority. Tuple: (layer, automatic-local, adverse, requires-human).
ACTION_CONTRACTS = {
    "Prepare a time-bounded lawful safety action with evidence preservation.": ("authority", False, True, True),
    "Urgently preserve evidence and route to an authorized human reviewer.": ("authority", False, False, True),
    "Propagate a correction to prior recipients and dependent decisions.": ("correction", False, True, True),
    "Prepare restoration, verified-loss compensation, and model-revision receipts.": ("remedy", False, False, True),
    "Do not restrict the item solely for negative tone, criticism, whistleblowing, satire, or distress.": ("speech", True, False, False),
    "Offer optional source lineage, context, and support resources without obscuring the original item.": ("reader", True, False, False),
    "Propose a transparent discovery boost for high-integrity public-value content.": ("discovery", False, False, True),
    "Offer verification, translation, accessibility, or context-production support.": ("creator", False, False, True),
    "Display a high-visibility uncertainty and scope card.": ("reader", True, False, False),
    "Propose a temporary recommendation limit pending independent review.": ("distribution", False, True, True),
    "Propose a pause on paid amplification or affiliate conversion until disclosures are complete.": ("commerce", False, True, True),
    "Request evidence, conflicts, pricing, refund, failure-case, and scope disclosures.": ("creator", True, False, False),
    "Show a context card and require an explicit reshare confirmation.": ("reader", True, False, False),
    "Propose transparent circulation damping pending review; preserve direct access to the item.": ("distribution", False, True, True),
    "Add a user-local pause, source check, and context card before resharing or purchasing.": ("reader", True, False, False),
    "Offer a balanced rewrite and explicit falsification questions.": ("creator", True, False, False),
    "Show an optional context, source, and incentive card.": ("reader", True, False, False),
    "Apply no restriction.": ("distribution", True, False, False),
    "Disable autoplay, infinite scroll, variable rewards, or exit penalties in the user-local view.": ("interface", True, False, False),
    "Generate a non-zero-sum repair card with affected parties and shared constraints.": ("relationship", True, False, False),
    "Attach notice, reason codes, evidence scope, expiry, appeal, and restoration path.": ("due_process", False, False, True),
    "Keep proposed restrictions inactive until an authorized reviewer establishes appeal and correction channels.": ("authority", False, False, True),
}

INTERFACE_LOCAL_ACTIONS = frozenset({
    "Disable autoplay locally.",
    "Insert natural stopping points and a visible end-of-session control.",
    "Hide variable-reward and streak-loss prompts in the user-local view.",
    "Batch and silence non-urgent notifications.",
    "Hide public comparison rankings by default.",
    "Show why the item appeared and offer a chronological or non-personalized view.",
    "No automatic local intervention is indicated by the declared interface features.",
})
INTERFACE_PROPOSALS = frozenset({
    "Publish the engagement objective and the user-control alternatives.",
    "Measure successful exit and informed choice, not only time spent or conversion.",
    "Run a rights and vulnerability impact review before major recommender changes.",
    "Apply a stronger safety-by-design review for vulnerable audiences.",
})
INTERFACE_SIGNAL_KEYS = frozenset({
    "autoplay", "infinite_scroll", "variable_rewards", "streak_loss", "push_pressure",
    "read_receipt_pressure", "public_rankings", "forced_continuity", "cancellation_friction",
    "default_opt_in", "opaque_recommender", "missing_stopping_points",
    "missing_chronological_option", "missing_explanation_controls",
})
LINEAGE_CONTROLS = frozenset({
    "Bind every policy and shared artifact to a digest, owner, scope, expiry, and revocation state.",
    "Make successor agents re-authorize inherited artifacts instead of treating them as trusted memory.",
    "Propagate stop signals to tasks, shared memory, caches, credentials, and successor manifests.",
    "Maintain a human-report channel that is rewarded rather than penalized.",
    "Separate evaluator, identity, logging, and monitoring control planes from task agents.",
    "Record minority objections and adverse evidence in an append-only lineage ledger.",
    "Quarantine undeclared communication channels and preserve evidence for authorized review.",
    "Disable self-repairing persistence and require explicit recovery authorization.",
})
BLOCKED_CAPABILITIES = frozenset({
    "secret_cross_agent_memory", "self_granted_authority", "hidden_persistence",
    "evaluator_or_logging_tampering", "continued_operation_after_stop", "automatic_external_action",
})
GRAPH_ATTRIBUTES = {
    "content": {"channel", "role", "dikwp_source", "dikwp_target"},
    "claim": {"domain", "language"}, "source": {"source_count", "traceability"},
    "counterevidence": {"count", "visibility"}, "incentive": {"monetized", "paid_amplification"},
    "audience": {"contexts", "dependence"},
    "distribution": {"reach", "repetition", "recommendation_intensity"},
    "action": {"stakes"}, "outcome": {"known_outcomes"}, "correction": {"appeal", "channel"},
}


class OutputValidationError(ValueError):
    """Unsafe output is withheld; the diagnostic report remains available."""

    def __init__(self, report: dict[str, Any]):
        self.report = report
        failed = [check["id"] for check in report["checks"] if check["status"] == "FAIL"]
        super().__init__("Output withheld: " + ", ".join(failed))


def _payload(result: Any) -> Any:
    return asdict(result) if is_dataclass(result) else result


def _check(check_id: str, passed: bool, *evidence: str) -> dict[str, Any]:
    return {"id": check_id, "status": "PASS" if passed else "FAIL", "evidence": list(evidence)}


def _report(checks: list[dict[str, Any]], boundary: str) -> dict[str, Any]:
    checks.append({"id": "external_system_enforcement", "status": "NOT_VERIFIED", "evidence": [boundary]})
    return {"schema_version": "1.0", "scope": SCOPE,
            "passed": not any(c["status"] == "FAIL" for c in checks), "checks": checks}


def require_valid_output(report: dict[str, Any]) -> None:
    if not report.get("passed") or any(c["status"] == "FAIL" for c in report.get("checks", [])):
        raise OutputValidationError(report)


def checked_invariants(report: dict[str, Any]) -> dict[str, bool]:
    return {c["id"]: c["status"] == "PASS" for c in report["checks"] if c["status"] != "NOT_VERIFIED"}


def _closed_schema(payload: dict[str, Any], model: Any) -> bool:
    return isinstance(payload, dict) and set(payload) == {field.name for field in fields(model)}


def _invalid_payload() -> dict[str, Any]:
    return _report([_check("output_schema", False, "Expected a typed input case and a complete result object; malformed payload was rejected.")], "No external state was verified.")


def _finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _strings_from_catalog(values: Any, catalog: frozenset[str]) -> bool:
    return isinstance(values, list) and bool(values) and all(isinstance(v, str) and v in catalog for v in values)


def validate_analysis_output(case: Any, result: Any) -> dict[str, Any]:
    """Recompute output checks; never accept cached PASS flags as evidence."""
    from .planner import plan_interventions, semantic_control_potential
    from .commons import assess_commons_support
    from .signals import extract_signals
    from .utils import digest_json

    p = _payload(result)
    if not isinstance(p, dict) or not isinstance(case, SemanticFlowCase):
        return _invalid_payload()
    actions = p.get("interventions", [])
    catalog_ok = isinstance(actions, list) and bool(actions)
    valid_actions, adverse, gated = [], [], []
    for action in actions if isinstance(actions, list) else []:
        if not isinstance(action, dict):
            catalog_ok = False
            continue
        spec = ACTION_CONTRACTS.get(action.get("action")) if isinstance(action.get("action"), str) else None
        valid = spec is not None and set(action) == {"layer", "action", "automatic", "reversible", "expiry_hours", "human_gate", "reason_codes"}
        valid = valid and action.get("layer") == spec[0] and action.get("automatic") is spec[1] and action.get("human_gate") is spec[3]
        catalog_ok = catalog_ok and valid
        valid_actions.append((action, spec))
        if spec is None or spec[2]:
            adverse.append(action)
        if spec is None or spec[3]:
            gated.append(action)
    all_gated = all(a.get("human_gate") is True and a.get("automatic") is False for a in gated)
    reversible = all(a.get("reversible") is True for a, _ in valid_actions)
    timed = all(isinstance(a.get("expiry_hours"), int) and not isinstance(a.get("expiry_hours"), bool) and a["expiry_hours"] > 0 for a in adverse)

    expected_signals = extract_signals(case)
    signals = p.get("signals", {})
    signal_schema = isinstance(signals, dict) and set(signals) == set(expected_signals) and all(isinstance(v, dict) for v in signals.values())
    expected_low = {**expected_signals, "negative_affect": replace(expected_signals["negative_affect"], score=0.0)}
    expected_high = {**expected_signals, "negative_affect": replace(expected_signals["negative_affect"], score=1.0)}
    commons = assess_commons_support(case, expected_signals)
    low_plan = plan_interventions(case, expected_low, commons)
    high_plan = plan_interventions(case, expected_high, commons)
    sentiment_neutral = low_plan == high_plan
    expected_plan = plan_interventions(case, expected_signals, commons)
    score_ok = _finite(p.get("semantic_control_potential")) and p["semantic_control_potential"] == round(semantic_control_potential(case, expected_signals), 4)
    neutral_signal = signal_schema and signals["negative_affect"].get("restrictive_feature") is False
    independent_signal = any(s.score >= 0.12 for k, s in expected_signals.items() if k not in {"negative_affect", "repair_capacity", "public_interest_value"})
    independent_harm = bool(case.verified_harm or case.imminent_harm_or_illegal or case.verified_fabrication)
    graph = p.get("graph", {})
    nodes = graph.get("nodes", []) if isinstance(graph, dict) else []
    graph_safe = isinstance(nodes, list) and len(nodes) == len(GRAPH_ATTRIBUTES) and all(
        isinstance(n, dict) and isinstance(n.get("node_id"), str) and n.get("node_id") in GRAPH_ATTRIBUTES
        and isinstance(n.get("attributes"), dict) and set(n["attributes"]) == GRAPH_ATTRIBUTES[n["node_id"]]
        and isinstance(n.get("kind"), str) and n["kind"] in {"content", "claim", "evidence", "incentive", "audience", "circulation", "decision", "outcome", "repair"}
        for n in nodes)
    graph_safe = graph_safe and {n["node_id"] for n in nodes} == set(GRAPH_ATTRIBUTES)
    worlds = p.get("worlds", [])
    deception = [w.get("weight") for w in worlds if isinstance(w, dict) and w.get("key") == "coordinated_deception"] if isinstance(worlds, list) else []
    deception_ok = len(deception) == 1 and _finite(deception[0]) and (case.verified_fabrication or deception[0] < 0.15)
    due_process = any(a.get("layer") == "due_process" and a.get("human_gate") is True for a, _ in valid_actions)
    closed = _closed_schema(p, AnalysisResult)
    checks = [
        _check("output_action_catalog_and_schema", closed and catalog_ok, f"{len(actions) if isinstance(actions, list) else 0} proposals checked against exact local catalog; unknown actions/fields rejected."),
        _check("decision_and_input_features_match", p.get("decision") == expected_plan[0] and p.get("protected_expression") is expected_plan[2] and p.get("high_impact") is expected_plan[3] and signals == {k: asdict(v) for k, v in expected_signals.items()} and p.get("reason_codes") == expected_plan[5], "Decision, protection flags, reason codes and signal fields recomputed from the supplied normalized case."),
        _check("interventions_match_current_case_plan", actions == [asdict(a) for a in expected_plan[4]], "The full intervention bundle was freshly generated from this case; missing, added or modified interventions are detected."),
        _check("negative_affect_alone_never_triggers_restriction", neutral_signal and sentiment_neutral and (not adverse or independent_harm or independent_signal), "Negative affect restrictive_feature must be false; counterfactual affect 0/1 leaves the entire current-case plan unchanged; adverse proposals need other evidence."),
        _check("protected_expression_requires_independent_harm_basis_for_adverse_action", not (case.content_role in PROTECTED_ROLES and adverse and not independent_harm), f"Protected role={case.content_role in PROTECTED_ROLES}; adverse proposals={len(adverse)}; independent basis declared={independent_harm}."),
        _check("deliberate_deception_not_inferred_without_verified_fabrication", deception_ok, "Checked coordinated_deception weight against caller-declared fabrication evidence, not verified intent."),
        _check("person_level_moral_scoring_prohibited", closed and signal_schema and graph_safe, "Closed result fields, signal keys, graph node kinds and attribute keys exclude person-level moral/ability scores; free-text evidence is not interpreted as an output field."),
        _check("viewpoint_or_sentiment_penalty_prohibited", neutral_signal and sentiment_neutral and score_ok, "Current-case control score is recomputed from permitted features; not a global fairness proof."),
        _check("automatic_content_removal_authority_zero", catalog_ok, "No content-removal action exists in the accepted output catalog."),
        _check("automatic_external_action_authority_zero", catalog_ok and all_gated, "All automatic proposals are catalogued local presentation actions; no external execution is performed by this validator."),
        _check("adverse_platform_action_requires_human_gate", all_gated, f"Every one of {len(gated)} human-required proposals checked, including limits in HUMAN_REVIEW bundles."),
        _check("adverse_action_requires_reversibility_and_expiry", reversible and timed, f"Every adverse proposal ({len(adverse)}) requires positive expiry and all proposals require reversible=True."),
        _check("appeal_required_for_adverse_action", not adverse or case.appeal_available is True, f"Appeal channel declared available={case.appeal_available}; operational availability not verified."),
        _check("correction_path_required_for_adverse_action", not adverse or case.correction_channel_available is True, f"Correction channel declared available={case.correction_channel_available}; operational availability not verified."),
        _check("due_process_attached_to_human_gated_proposals", not gated or due_process, "Human-gated bundles must include the catalogued notice/reasons/expiry/appeal/restoration attachment; delivery is not established."),
        _check("input_digest_matches_case", p.get("case_digest") == digest_json(asdict(case)), "Compared against the normalized case supplied to this validation call."),
    ]
    return _report(checks, "No external executor, platform control, factual truth, human authorization, delivered notice, appeal service, or real-world enforcement is verified. Checks concern this local proposal payload only.")


def validate_interface_output(case: Any, result: Any) -> dict[str, Any]:
    from .interface_audit import interface_signal_values
    p = _payload(result)
    if not isinstance(p, dict) or not isinstance(case, InterfaceAuditCase):
        return _invalid_payload()
    signals = p.get("signals", {})
    keys_ok = isinstance(signals, dict) and set(signals) == INTERFACE_SIGNAL_KEYS
    values_ok = keys_ok and all(_finite(v) and 0 <= v <= 1 for v in signals.values())
    local_ok = _strings_from_catalog(p.get("automatic_local_actions"), INTERFACE_LOCAL_ACTIONS)
    platform_ok = _strings_from_catalog(p.get("platform_proposals"), INTERFACE_PROPOSALS)
    closed = _closed_schema(p, InterfaceAuditResult)
    score = p.get("score")
    expected_signals = interface_signal_values(case)
    expected = round(100 * min(1.0, sum(expected_signals.values()) * (1 + .18 * bool(case.youth_audience) + .22 * bool(case.acute_distress_audience))), 1)
    score_ok = values_ok and signals == {k: round(v, 4) for k, v in expected_signals.items()} and _finite(score) and score == expected
    severity = "LOW" if _finite(score) and score < 25 else "MODERATE" if _finite(score) and score < 50 else "HIGH" if _finite(score) and score < 75 else "CRITICAL"
    checks = [
        _check("not_a_clinical_addiction_diagnosis", closed and p.get("severity") == severity and score_ok, "Only an interface-pattern score and LOW/MODERATE/HIGH/CRITICAL severity are accepted; diagnosis fields rejected."),
        _check("negative_emotion_not_used", keys_ok and score_ok, "Every feature and score is freshly computed from the original case, not supplied output signals; declared audience context is not an emotion score."),
        _check("automatic_platform_sanction_authority_zero", closed and local_ok and platform_ok, "Every local suggestion/platform proposal matched the non-executing catalog; sanction actions and execution fields rejected."),
    ]
    return _report(checks, "The described interface, audience, implemented controls, clinical condition, and any platform action are not observed or verified by this local audit.")


def validate_lineage_output(case: Any, result: Any) -> dict[str, Any]:
    from .lineage import lineage_factor_values
    from .utils import clamp
    p = _payload(result)
    if not isinstance(p, dict) or not isinstance(case, AgentLineageCase):
        return _invalid_payload()
    blocked = p.get("blocked_capabilities", [])
    blocked_ok = isinstance(blocked, list) and all(isinstance(v, str) for v in blocked) and set(blocked) == BLOCKED_CAPABILITIES
    controls = p.get("required_controls", [])
    controls_ok = _strings_from_catalog(controls, LINEAGE_CONTROLS)
    closed = _closed_schema(p, AgentLineageResult)
    observations = p.get("input_observations", {})
    factors = lineage_factor_values(case)
    expected_risk = round(100.0 * clamp(sum(factors.values())), 1)
    expected_severity = "LOW" if expected_risk < 25 else "MODERATE" if expected_risk < 50 else "HIGH" if expected_risk < 75 else "CRITICAL"
    risk_ok = _finite(p.get("risk_score")) and p["risk_score"] == expected_risk and p.get("severity") == expected_severity and p.get("risk_factors") == [key.upper() for key, value in factors.items() if value > 0]
    checks = [
        _check("external_action_authority_zero", closed and blocked_ok and controls_ok, "Local output contains only catalogued required controls and prohibited capabilities, not executable external actions."),
        _check("lineage_risk_matches_declared_input", risk_ok, "Risk score, severity and risk-factor names were recalculated from the original caller-declared case, not accepted from the output."),
        _check("secret_persistence_prohibited", blocked_ok and "hidden_persistence" in blocked and "secret_cross_agent_memory" in blocked, "Required prohibitions are present in this output; absence of persistence in external agents is not claimed."),
        _check("successor_authority_not_inherited_automatically", blocked_ok and controls_ok and "Make successor agents re-authorize inherited artifacts instead of treating them as trusted memory." in controls and "self_granted_authority" in blocked, "Explicit successor re-authorization requirement checked in the generated control plan."),
        _check("human_report_channel_required", controls_ok and "Maintain a human-report channel that is rewarded rather than penalized." in controls, "Requirement is emitted; this does not mean a channel exists."),
        _check("human_report_channel_availability_reported_accurately", isinstance(observations, dict) and observations.get("human_report_channel_available") is case.human_report_channel and observations.get("source") == "caller_declaration_unverified", f"Caller-declared channel availability={case.human_report_channel}; kept separate from the requirement."),
    ]
    return _report(checks, "Stop propagation, absence of hidden persistence, successor authorization and actual human-report channel operation are NOT_VERIFIED in external agents; input state is caller-declared.")


def validate_analysis_export_output(result: Any) -> dict[str, Any]:
    """Fresh structural guard when an original input case is unavailable.

    Reference exports cannot authenticate cached PASS flags. Recompute the
    action contract checks and explicitly leave case-dependent claims unverified.
    """
    from .models import Decision
    p = _payload(result)
    if not isinstance(p, dict):
        return _invalid_payload()
    # Legacy 2.0.0 files without a receipt remain readable, not certified.
    normalized = {"validation": {}, **p}
    actions = p.get("interventions")
    shape_ok = _closed_schema(normalized, AnalysisResult)
    action_ok = isinstance(actions, list) and bool(actions)
    gated = []
    for a in actions if isinstance(actions, list) else []:
        if not isinstance(a, dict):
            action_ok = False
            continue
        spec = ACTION_CONTRACTS.get(a.get("action")) if isinstance(a.get("action"), str) else None
        valid = spec is not None and set(a) == {"layer", "action", "automatic", "reversible", "expiry_hours", "human_gate", "reason_codes"}
        valid = valid and a.get("layer") == spec[0] and a.get("automatic") is spec[1] and a.get("human_gate") is spec[3] and a.get("reversible") is True
        if spec is None or spec[3]:
            gated.append(a)
        if spec is None or spec[2]:
            valid = valid and isinstance(a.get("expiry_hours"), int) and not isinstance(a.get("expiry_hours"), bool) and a["expiry_hours"] > 0
        action_ok = action_ok and valid
    due_process = not gated or any(a.get("layer") == "due_process" and a.get("human_gate") is True for a in gated)
    numeric = all(_finite(p.get(k)) and 0 <= p[k] <= 1 for k in ("confidence", "semantic_control_potential"))
    decision_ok = isinstance(p.get("decision"), str) and p["decision"] in {item.value for item in Decision}
    checks = [
        _check("export_output_schema", shape_ok and numeric and decision_ok, "Complete reference result shape, bounded finite scores and known decision label checked without trusting cached validation."),
        _check("export_action_contracts", action_ok and due_process, "Every exported intervention matched the exact local action catalog, human gate, reversibility, adverse expiry and due-process attachment."),
        {"id": "original_case_analysis", "status": "NOT_VERIFIED", "evidence": ["Original normalized case was not provided to the reference exporter; stored analysis validation is unauthenticated reported metadata, not fresh evidence."]},
    ]
    return _report(checks, "This is a local reference-format export only, not publication, external execution, authenticated provenance or factual/clinical/legal verification.")
