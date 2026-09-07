from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from .models import AnalysisResult
from .runtime_validation import require_valid_output, validate_analysis_export_output


def _validation_metadata(result: AnalysisResult) -> dict[str, Any]:
    report = validate_analysis_export_output(result)
    require_valid_output(report)
    return {"validation": report, "reported_analysis_validation": result.validation,
            "reported_analysis_validation_authentication": "NOT_VERIFIED"}


def to_atproto_label(result: AnalysisResult, *, source_did: str, subject_uri: str, subject_cid: str | None = None) -> dict[str, Any]:
    validation = _validation_metadata(result)
    now = datetime.now(timezone.utc)
    label_value = _label_value(result.decision)
    payload: dict[str, Any] = {
        "ver": 1,
        "src": source_did,
        "uri": subject_uri,
        "val": label_value,
        "cts": now.isoformat().replace("+00:00", "Z"),
        "exp": (now + timedelta(hours=72)).isoformat().replace("+00:00", "Z"),
        "sig": None,
        "reference_only": True,
        "reason_codes": result.reason_codes,
        **validation,
    }
    if subject_cid:
        payload["cid"] = subject_cid
    return payload


def to_dsa_statement_of_reasons_reference(result: AnalysisResult, *, content_id: str) -> dict[str, Any]:
    return {
        **_validation_metadata(result),
        "type": "DSA_STATEMENT_OF_REASONS_REFERENCE_MAPPING",
        "content_id": content_id,
        "decision_ground": result.decision,
        "reason_codes": result.reason_codes,
        "facts_and_circumstances": {
            "semantic_control_potential": result.semantic_control_potential,
            "high_impact": result.high_impact,
            "protected_expression": result.protected_expression,
        },
        "automated_detection_used": True,
        "automated_decision_used": False,
        "human_review_required": any(item.human_gate for item in result.interventions),
        "appeal_required": True,
        "expiry_required": True,
        "reference_only": True,
    }


def to_c2pa_reference_assertion(result: AnalysisResult) -> dict[str, Any]:
    return {
        **_validation_metadata(result),
        "label": "org.dikwp.verityweave.semantic-analysis",
        "data": {
            "case_digest": result.case_digest,
            "system": result.provenance["system"],
            "version": result.version,
            "decision": result.decision,
            "reason_codes": result.reason_codes,
            "limitations": result.limitations,
            "provenance_is_not_truth": True,
        },
        "reference_only": True,
    }


def to_prov_jsonld(result: AnalysisResult) -> dict[str, Any]:
    validation = _validation_metadata(result)
    activity_id = f"urn:sha256:{result.case_digest}#analysis"
    entity_id = f"urn:sha256:{result.case_digest}#input"
    return {
        **validation,
        "@context": {
            "prov": "http://www.w3.org/ns/prov#",
            "dikwp": "https://example.org/dikwp/verityweave#",
        },
        "@graph": [
            {"@id": entity_id, "@type": "prov:Entity", "dikwp:digest": result.case_digest},
            {
                "@id": activity_id,
                "@type": "prov:Activity",
                "prov:used": {"@id": entity_id},
                "dikwp:decision": result.decision,
                "dikwp:semanticControlPotential": result.semantic_control_potential,
            },
        ],
    }


def _label_value(decision: str) -> str:
    mapping = {
        "PRESERVE_ADVERSE_TRUTH_OR_DISTRESS": "preserve-adverse-truth",
        "SUPPORT_HIGH_INTEGRITY_PUBLIC_VALUE": "high-integrity-public-value",
        "ALLOW_WITHOUT_RESTRICTION": "no-material-signal",
        "ADD_CONTEXT_AND_SOURCE_CARD": "context-needed",
        "ADD_USER_LOCAL_FRICTION": "user-local-friction",
        "CIRCULATION_DAMPING_PROPOSAL": "circulation-review",
        "MONETIZATION_DISCLOSURE_GATE": "commercial-disclosure-needed",
        "INDEPENDENT_HUMAN_REVIEW": "independent-review",
        "CORRECTION_PROPAGATION_AND_REPAIR": "correction-required",
        "AUTHORIZED_LEGAL_OR_IMMINENT_SAFETY_ESCALATION": "authorized-safety-review",
    }
    return mapping.get(decision, "context-needed")
