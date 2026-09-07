from __future__ import annotations

from .models import InterfaceAuditCase, InterfaceAuditResult
from .runtime_validation import checked_invariants, require_valid_output, validate_interface_output
from .utils import clamp


def interface_signal_values(case: InterfaceAuditCase) -> dict[str, float]:
    """Pure feature calculation shared with independent payload validation."""
    return {
        "autoplay": 0.16 if case.autoplay else 0.0,
        "infinite_scroll": 0.17 if case.infinite_scroll else 0.0,
        "variable_rewards": 0.20 if case.variable_rewards else 0.0,
        "streak_loss": 0.16 if case.streak_loss else 0.0,
        "push_pressure": 0.14 * clamp(case.push_frequency),
        "read_receipt_pressure": 0.07 if case.read_receipt_pressure else 0.0,
        "public_rankings": 0.11 if case.public_rankings else 0.0,
        "forced_continuity": 0.14 if case.forced_continuity else 0.0,
        "cancellation_friction": 0.14 if case.cancellation_friction else 0.0,
        "default_opt_in": 0.09 if case.default_opt_in else 0.0,
        "opaque_recommender": 0.12 if case.opaque_recommender else 0.0,
        "missing_stopping_points": 0.12 if not case.natural_stopping_points else 0.0,
        "missing_chronological_option": 0.08 if not case.chronological_option else 0.0,
        "missing_explanation_controls": 0.08 if not case.explanation_controls else 0.0,
    }


def audit_interface(case: InterfaceAuditCase) -> InterfaceAuditResult:
    signals = interface_signal_values(case)
    base = sum(signals.values())
    multiplier = 1.0 + (0.18 if case.youth_audience else 0.0) + (0.22 if case.acute_distress_audience else 0.0)
    score = round(100.0 * clamp(base * multiplier), 1)
    severity = "LOW" if score < 25 else "MODERATE" if score < 50 else "HIGH" if score < 75 else "CRITICAL"

    local_actions: list[str] = []
    if case.autoplay:
        local_actions.append("Disable autoplay locally.")
    if case.infinite_scroll:
        local_actions.append("Insert natural stopping points and a visible end-of-session control.")
    if case.variable_rewards or case.streak_loss:
        local_actions.append("Hide variable-reward and streak-loss prompts in the user-local view.")
    if case.push_frequency > 0.35:
        local_actions.append("Batch and silence non-urgent notifications.")
    if case.public_rankings:
        local_actions.append("Hide public comparison rankings by default.")
    if case.opaque_recommender:
        local_actions.append("Show why the item appeared and offer a chronological or non-personalized view.")
    if not local_actions:
        local_actions.append("No automatic local intervention is indicated by the declared interface features.")

    proposals = [
        "Publish the engagement objective and the user-control alternatives.",
        "Measure successful exit and informed choice, not only time spent or conversion.",
        "Run a rights and vulnerability impact review before major recommender changes.",
    ]
    if case.youth_audience or case.acute_distress_audience:
        proposals.append("Apply a stronger safety-by-design review for vulnerable audiences.")

    result = InterfaceAuditResult(
        score=score,
        severity=severity,
        signals={key: round(value, 4) for key, value in signals.items()},
        automatic_local_actions=local_actions,
        platform_proposals=proposals,
        invariants={},
    )
    result.validation = validate_interface_output(case, result)
    result.invariants = checked_invariants(result.validation)
    require_valid_output(result.validation)
    return result
