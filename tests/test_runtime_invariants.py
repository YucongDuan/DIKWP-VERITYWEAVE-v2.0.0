"""Adversarial tests must demonstrate guards can fail, not just read PASS flags."""
from __future__ import annotations

import unittest
from dataclasses import replace
from unittest.mock import patch

from dikwp_verityweave import (
    AgentLineageCase, InterfaceAuditCase, SemanticFlowCase, OutputValidationError,
    analyze, audit_agent_lineage, audit_interface, require_valid_output,
    validate_analysis_output, validate_interface_output, validate_lineage_output,
)
from dikwp_verityweave.mcp import handle_request
from dikwp_verityweave.interoperability import to_atproto_label, to_c2pa_reference_assertion, to_dsa_statement_of_reasons_reference, to_prov_jsonld
from dikwp_verityweave.planner import plan_interventions, semantic_control_potential
from dikwp_verityweave.runtime_validation import ACTION_CONTRACTS
from dikwp_verityweave.signals import extract_signals


class RuntimeInvariantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.case = SemanticFlowCase(text="A documented harmful outcome.", verified_harm=True)
        self.result = analyze(self.case)

    def assertFails(self, report: dict, check_id: str) -> None:
        self.assertFalse(report["passed"])
        checks = {c["id"]: c for c in report["checks"]}
        self.assertEqual(checks[check_id]["status"], "FAIL")
        self.assertTrue(checks[check_id]["evidence"])
        with self.assertRaises(OutputValidationError) as raised:
            require_valid_output(report)
        self.assertIs(raised.exception.report, report)

    def test_default_outputs_include_scoped_checks_and_nonverification(self) -> None:
        for result in (analyze(SemanticFlowCase(text="A neutral item.")), audit_interface(InterfaceAuditCase()), audit_agent_lineage(AgentLineageCase())):
            with self.subTest(type=type(result).__name__):
                report = result.to_dict()["validation"]
                self.assertTrue(report["passed"])
                self.assertEqual(report["scope"], "local_generated_output_only")
                self.assertTrue(all(c["evidence"] for c in report["checks"]))
                self.assertEqual(report["checks"][-1]["status"], "NOT_VERIFIED")

    def test_all_adverse_actions_require_their_own_human_gate(self) -> None:
        # The old `any(human_gate)` falsely passed when due_process remained gated.
        self.result.interventions[0].human_gate = False
        self.assertTrue(any(a.human_gate for a in self.result.interventions))
        self.assertFails(validate_analysis_output(self.case, self.result), "adverse_platform_action_requires_human_gate")

    def test_adverse_action_hidden_in_human_review_is_checked(self) -> None:
        case = SemanticFlowCase(text="100% guaranteed. Ignore your doctor.", domain="health", source_traceability=0, evidence_quality=0)
        result = analyze(case)
        self.assertEqual(result.decision, "INDEPENDENT_HUMAN_REVIEW")
        adverse = next(a for a in result.interventions if a.layer == "distribution")
        adverse.human_gate = False
        self.assertFails(validate_analysis_output(case, result), "adverse_platform_action_requires_human_gate")

    def test_automatic_external_action_is_rejected_even_if_human_gate_true(self) -> None:
        self.result.interventions[0].automatic = True
        self.assertFails(validate_analysis_output(self.case, self.result), "automatic_external_action_authority_zero")

    def test_unknown_deletion_action_is_rejected(self) -> None:
        self.result.interventions[0].action = "Delete the creator's account and all posts."
        self.assertFails(validate_analysis_output(self.case, self.result), "automatic_content_removal_authority_zero")

    def test_added_command_field_is_rejected(self) -> None:
        payload = self.result.to_dict()
        payload["interventions"][0]["command"] = "remote_delete"
        self.assertFails(validate_analysis_output(self.case, payload), "output_action_catalog_and_schema")

    def test_adverse_action_requires_expiry(self) -> None:
        self.result.interventions[0].expiry_hours = None
        self.assertFails(validate_analysis_output(self.case, self.result), "adverse_action_requires_reversibility_and_expiry")

    def test_all_local_actions_require_reversibility(self) -> None:
        case = SemanticFlowCase(text="A neutral item.")
        result = analyze(case)
        result.interventions[0].reversible = False
        self.assertFails(validate_analysis_output(case, result), "adverse_action_requires_reversibility_and_expiry")

    def test_missing_appeal_blocks_each_adverse_proposal(self) -> None:
        for appeal, correction in ((False, True), (True, False), (False, False)):
            with self.subTest(appeal=appeal, correction=correction):
                case = SemanticFlowCase(text="A documented harmful outcome.", verified_harm=True, appeal_available=appeal, correction_channel_available=correction)
                result = analyze(case)
                self.assertEqual(result.decision, "INDEPENDENT_HUMAN_REVIEW")
                self.assertIn("ADVERSE_PROPOSALS_WITHHELD_MISSING_SAFEGUARDS", result.reason_codes)
                self.assertFalse(any(ACTION_CONTRACTS[a.action][2] for a in result.interventions))
                self.assertTrue(result.validation["passed"])

    def test_imminent_harm_does_not_override_missing_safeguards(self) -> None:
        case = SemanticFlowCase(text="Urgent case.", imminent_harm_or_illegal=True, authorized_human_review=True, appeal_available=False)
        result = analyze(case)
        self.assertEqual(result.decision, "INDEPENDENT_HUMAN_REVIEW")
        self.assertFalse(any(ACTION_CONTRACTS[a.action][2] for a in result.interventions))

    def test_validator_rejects_adverse_plan_if_input_channel_missing(self) -> None:
        self.case.appeal_available = False
        self.assertFails(validate_analysis_output(self.case, self.result), "appeal_required_for_adverse_action")

    def test_missing_due_process_attachment_is_rejected(self) -> None:
        self.result.interventions = [a for a in self.result.interventions if a.layer != "due_process"]
        self.assertFails(validate_analysis_output(self.case, self.result), "due_process_attached_to_human_gated_proposals")

    def test_negative_affect_cannot_be_marked_restrictive(self) -> None:
        self.result.signals["negative_affect"].restrictive_feature = True
        self.assertFails(validate_analysis_output(self.case, self.result), "negative_affect_alone_never_triggers_restriction")

    def test_counterfactual_affect_does_not_change_control_score(self) -> None:
        case = SemanticFlowCase(text="I am sad and angry.", content_role="distress_expression")
        signals = extract_signals(case)
        low = {**signals, "negative_affect": replace(signals["negative_affect"], score=0)}
        high = {**signals, "negative_affect": replace(signals["negative_affect"], score=1)}
        self.assertEqual(semantic_control_potential(case, low), semantic_control_potential(case, high))
        self.assertEqual(analyze(case).decision, "PRESERVE_ADVERSE_TRUTH_OR_DISTRESS")

    def test_fabricated_sentiment_score_adjustment_is_detected(self) -> None:
        self.result.semantic_control_potential += .05
        self.assertFails(validate_analysis_output(self.case, self.result), "viewpoint_or_sentiment_penalty_prohibited")

    def test_person_score_output_field_is_rejected(self) -> None:
        payload = self.result.to_dict()
        payload["person_moral_score"] = .8
        self.assertFails(validate_analysis_output(self.case, payload), "person_level_moral_scoring_prohibited")

    def test_person_score_in_graph_is_rejected(self) -> None:
        self.result.graph.nodes[0].attributes["moral_score"] = 1
        self.assertFails(validate_analysis_output(self.case, self.result), "person_level_moral_scoring_prohibited")

    def test_claimed_pass_flags_do_not_override_detected_failure(self) -> None:
        self.result.interventions[0].automatic = True
        self.result.invariants = {key: True for key in self.result.invariants}
        self.result.validation = {"passed": True, "checks": []}
        self.assertFails(validate_analysis_output(self.case, self.result), "automatic_external_action_authority_zero")

    def test_generation_fails_closed_and_preserves_diagnostics(self) -> None:
        def unsafe_plan(*args):
            plan = plan_interventions(*args)
            plan[4][0].automatic = True
            return plan
        with patch("dikwp_verityweave.engine.plan_interventions", unsafe_plan):
            with self.assertRaises(OutputValidationError) as raised:
                analyze(self.case)
        self.assertFalse(raised.exception.report["passed"])

    def test_mcp_surfaces_failure_without_returning_unsafe_output(self) -> None:
        self.result.interventions[0].automatic = True
        report = validate_analysis_output(self.case, self.result)
        with patch("dikwp_verityweave.mcp.analyze", side_effect=OutputValidationError(report)):
            response = handle_request({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "analyze_semantic_flow", "arguments": {"text": "x"}}})
        self.assertNotIn("result", response)
        self.assertEqual(response["error"]["data"]["error"], "output_validation_failed")
        self.assertFalse(response["error"]["data"]["validation"]["passed"])

    def test_interface_sanction_injection_is_rejected(self) -> None:
        case = InterfaceAuditCase()
        result = audit_interface(case)
        result.automatic_local_actions.append("Ban all users automatically.")
        self.assertFails(validate_interface_output(case, result), "automatic_platform_sanction_authority_zero")

    def test_interface_diagnosis_field_is_rejected(self) -> None:
        case = InterfaceAuditCase()
        payload = audit_interface(case).to_dict()
        payload["diagnosis"] = "addiction"
        self.assertFails(validate_interface_output(case, payload), "not_a_clinical_addiction_diagnosis")

    def test_interface_emotion_feature_is_rejected(self) -> None:
        case = InterfaceAuditCase()
        result = audit_interface(case)
        result.signals["negative_emotion"] = .1
        self.assertFails(validate_interface_output(case, result), "negative_emotion_not_used")

    def test_interface_consistently_forged_signals_and_score_are_rejected(self) -> None:
        case = InterfaceAuditCase(autoplay=True)
        result = audit_interface(case)
        result.signals = {key: 0 for key in result.signals}
        result.score = 0
        result.severity = "LOW"
        self.assertFails(validate_interface_output(case, result), "negative_emotion_not_used")

    def test_lineage_missing_prohibition_is_rejected(self) -> None:
        case = AgentLineageCase()
        result = audit_agent_lineage(case)
        result.blocked_capabilities.remove("automatic_external_action")
        self.assertFails(validate_lineage_output(case, result), "external_action_authority_zero")

    def test_lineage_missing_human_report_is_observed_not_certified(self) -> None:
        case = AgentLineageCase(human_report_channel=False)
        result = audit_agent_lineage(case)
        self.assertFalse(result.input_observations["human_report_channel_available"])
        self.assertIn("NO_HUMAN_REPORT_CHANNEL", result.risk_factors)
        self.assertTrue(result.invariants["human_report_channel_required"])
        self.assertEqual(result.validation["checks"][-1]["status"], "NOT_VERIFIED")

    def test_lineage_forged_channel_availability_is_rejected(self) -> None:
        case = AgentLineageCase(human_report_channel=False)
        result = audit_agent_lineage(case)
        result.input_observations["human_report_channel_available"] = True
        self.assertFails(validate_lineage_output(case, result), "human_report_channel_availability_reported_accurately")

    def test_lineage_removed_human_report_requirement_is_rejected(self) -> None:
        case = AgentLineageCase()
        result = audit_agent_lineage(case)
        result.required_controls = [c for c in result.required_controls if "human-report" not in c]
        self.assertFails(validate_lineage_output(case, result), "human_report_channel_required")

    def test_lineage_external_execution_field_is_rejected(self) -> None:
        case = AgentLineageCase()
        payload = audit_agent_lineage(case).to_dict()
        payload["external_actions"] = ["disable_remote_agent"]
        self.assertFails(validate_lineage_output(case, payload), "external_action_authority_zero")

    def test_lineage_forged_risk_and_severity_are_rejected(self) -> None:
        case = AgentLineageCase(hidden_communication_channels=True)
        result = audit_agent_lineage(case)
        result.risk_score = -1
        result.severity = "LOW"
        result.risk_factors = []
        self.assertFails(validate_lineage_output(case, result), "lineage_risk_matches_declared_input")

    def test_missing_required_result_fields_are_rejected(self) -> None:
        case = InterfaceAuditCase()
        payload = audit_interface(case).to_dict()
        del payload["validation"]
        self.assertFails(validate_interface_output(case, payload), "not_a_clinical_addiction_diagnosis")

    def test_malformed_payloads_fail_without_attribute_errors(self) -> None:
        for invalid in (None, [], "not a result", 3):
            for case, validator in ((self.case, validate_analysis_output), (InterfaceAuditCase(), validate_interface_output), (AgentLineageCase(), validate_lineage_output)):
                with self.subTest(payload=invalid, validator=validator.__name__):
                    self.assertFails(validator(case, invalid), "output_schema")

    def test_malformed_nested_analysis_fields_fail_without_crashing(self) -> None:
        for field, replacement in (("signals", {"negative_affect": None}), ("interventions", [{"action": []}]), ("graph", {"nodes": [{"node_id": []}]})):
            payload = self.result.to_dict()
            payload[field] = replacement
            with self.subTest(field=field):
                report = validate_analysis_output(self.case, payload)
                self.assertFalse(report["passed"])

    def test_all_reference_exports_reject_tampered_actions(self) -> None:
        self.result.interventions[0].automatic = True
        exporters = (
            lambda: to_atproto_label(self.result, source_did="did:web:example.org", subject_uri="urn:example:x"),
            lambda: to_c2pa_reference_assertion(self.result),
            lambda: to_dsa_statement_of_reasons_reference(self.result, content_id="x"),
            lambda: to_prov_jsonld(self.result),
        )
        for export in exporters:
            with self.assertRaises(OutputValidationError):
                export()

    def test_reference_export_retains_receipt_without_authenticating_it(self) -> None:
        exported = to_c2pa_reference_assertion(self.result)
        self.assertEqual(exported["reported_analysis_validation"], self.result.validation)
        self.assertEqual(exported["reported_analysis_validation_authentication"], "NOT_VERIFIED")
        self.assertTrue(exported["validation"]["passed"])
        self.assertEqual(next(c for c in exported["validation"]["checks"] if c["id"] == "original_case_analysis")["status"], "NOT_VERIFIED")


if __name__ == "__main__":
    unittest.main()
