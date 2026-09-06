from __future__ import annotations

import unittest

from dikwp_verityweave.engine import analyze
from dikwp_verityweave.interoperability import to_atproto_label, to_c2pa_reference_assertion, to_dsa_statement_of_reasons_reference, to_prov_jsonld
from dikwp_verityweave.mcp import PROTOCOL_VERSION, handle_request
from dikwp_verityweave.models import SemanticFlowCase


class InteroperabilityAndMcpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result = analyze(SemanticFlowCase(text="Context matters and evidence should be independently reviewed.", source_traceability=0.8, evidence_quality=0.8, counterevidence_visibility=0.7, uncertainty_disclosure=0.8))

    def test_atproto_reference_label_has_expiry(self) -> None:
        label = to_atproto_label(self.result, source_did="did:web:example.org", subject_uri="at://example/post/1")
        self.assertTrue(label["reference_only"])
        self.assertIn("exp", label)
        self.assertIsNone(label["sig"])

    def test_c2pa_reference_says_provenance_is_not_truth(self) -> None:
        assertion = to_c2pa_reference_assertion(self.result)
        self.assertTrue(assertion["data"]["provenance_is_not_truth"])
        self.assertTrue(assertion["reference_only"])

    def test_dsa_reference_discloses_no_automated_decision(self) -> None:
        reason = to_dsa_statement_of_reasons_reference(self.result, content_id="content-1")
        self.assertTrue(reason["automated_detection_used"])
        self.assertFalse(reason["automated_decision_used"])
        self.assertTrue(reason["appeal_required"])

    def test_prov_reference_links_input_and_activity(self) -> None:
        prov = to_prov_jsonld(self.result)
        self.assertEqual(len(prov["@graph"]), 2)
        self.assertEqual(prov["@graph"][1]["@type"], "prov:Activity")

    def test_mcp_tools_are_deterministically_sorted(self) -> None:
        response = handle_request({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}})
        names = [item["name"] for item in response["result"]["tools"]]
        self.assertEqual(names, sorted(names))
        self.assertEqual(response["result"]["_meta"]["io.modelcontextprotocol/protocolVersion"], PROTOCOL_VERSION)

    def test_mcp_analysis_has_no_external_action(self) -> None:
        response = handle_request({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "analyze_semantic_flow", "arguments": {"text": "I am sad and angry.", "content_role": "distress_expression"}}})
        structured = response["result"]["structuredContent"]
        self.assertTrue(structured["invariants"]["automatic_external_action_authority_zero"])

    def test_mcp_unknown_tool_is_error(self) -> None:
        response = handle_request({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "delete_content", "arguments": {}}})
        self.assertIn("error", response)


if __name__ == "__main__":
    unittest.main()
