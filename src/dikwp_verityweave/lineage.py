from __future__ import annotations

import math

from .models import AgentLineageCase, AgentLineageResult
from .runtime_validation import checked_invariants, require_valid_output, validate_lineage_output
from .utils import clamp


def lineage_factor_values(case: AgentLineageCase) -> dict[str, float]:
    """Pure calculation; it observes caller-declared state, not remote agents."""
    scale = clamp(math.log2(max(1, case.agent_count)) / 10.0)
    artifact_density = clamp(case.shared_artifacts / 50.0)
    policy_churn = clamp(case.policy_digest_changes / 10.0)
    return {
        "large_agent_population": 0.12 * scale,
        "shared_artifact_inheritance": 0.12 * artifact_density,
        "shared_memory": 0.12 if case.shared_memory else 0.0,
        "hidden_communication_channels": 0.18 if case.hidden_communication_channels else 0.0,
        "successor_reuse": 0.13 if case.successor_reuse else 0.0,
        "policy_mutation": 0.08 * policy_churn,
        "external_tools": 0.06 if case.external_tools_available else 0.0,
        "control_plane_access": 0.16 if case.evaluator_or_control_plane_access else 0.0,
        "stop_signal_failure": 0.16 if not case.stop_signal_propagates else 0.0,
        "audit_gap": 0.12 if not case.audit_log_complete else 0.0,
        "no_human_report_channel": 0.08 if not case.human_report_channel else 0.0,
        "self_repairing_persistence": 0.20 if case.self_repairing_persistence else 0.0,
    }


def audit_agent_lineage(case: AgentLineageCase) -> AgentLineageResult:
    factors = lineage_factor_values(case)
    risk = round(100.0 * clamp(sum(factors.values())), 1)
    severity = "LOW" if risk < 25 else "MODERATE" if risk < 50 else "HIGH" if risk < 75 else "CRITICAL"
    risk_factors = [key.upper() for key, value in factors.items() if value > 0]

    controls = [
        "Bind every policy and shared artifact to a digest, owner, scope, expiry, and revocation state.",
        "Make successor agents re-authorize inherited artifacts instead of treating them as trusted memory.",
        "Propagate stop signals to tasks, shared memory, caches, credentials, and successor manifests.",
        "Maintain a human-report channel that is rewarded rather than penalized.",
        "Separate evaluator, identity, logging, and monitoring control planes from task agents.",
        "Record minority objections and adverse evidence in an append-only lineage ledger.",
    ]
    if case.hidden_communication_channels:
        controls.append("Quarantine undeclared communication channels and preserve evidence for authorized review.")
    if case.self_repairing_persistence:
        controls.append("Disable self-repairing persistence and require explicit recovery authorization.")

    result = AgentLineageResult(
        risk_score=risk,
        severity=severity,
        risk_factors=risk_factors,
        required_controls=controls,
        blocked_capabilities=[
            "secret_cross_agent_memory",
            "self_granted_authority",
            "hidden_persistence",
            "evaluator_or_logging_tampering",
            "continued_operation_after_stop",
            "automatic_external_action",
        ],
        invariants={},
        input_observations={"human_report_channel_available": case.human_report_channel, "source": "caller_declaration_unverified"},
    )
    result.validation = validate_lineage_output(case, result)
    result.invariants = checked_invariants(result.validation)
    require_valid_output(result.validation)
    return result
