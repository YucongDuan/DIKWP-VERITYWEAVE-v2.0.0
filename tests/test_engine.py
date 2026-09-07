from __future__ import annotations

import json
import unittest
from pathlib import Path

from dikwp_verityweave.engine import analyze
from dikwp_verityweave.models import SemanticFlowCase

ROOT = Path(__file__).resolve().parents[1]


class EngineTests(unittest.TestCase):
    def load_case(self, name: str) -> SemanticFlowCase:
        data = json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))
        return SemanticFlowCase.from_dict(data)

    def test_parenting_case_requires_governance(self) -> None:
        result = analyze(self.load_case("parenting_sales_funnel.json"))
        self.assertIn(result.decision, {
            "INDEPENDENT_HUMAN_REVIEW",
            "MONETIZATION_DISCLOSURE_GATE",
            "CIRCULATION_DAMPING_PROPOSAL",
        })
        self.assertTrue(result.high_impact)
        self.assertIn("caregivers", result.repair_card.balanced_rewrite.lower())
        self.assertIn("children", result.repair_card.balanced_rewrite.lower())
        self.assertTrue(all(result.invariants.values()))

    def test_whistleblower_is_preserved(self) -> None:
        result = analyze(self.load_case("whistleblower_report.json"))
        self.assertEqual(result.decision, "PRESERVE_ADVERSE_TRUTH_OR_DISTRESS")
        self.assertTrue(result.protected_expression)
        self.assertTrue(result.invariants["protected_expression_requires_independent_harm_basis_for_adverse_action"])

    def test_distress_is_not_restricted_for_negative_affect(self) -> None:
        result = analyze(self.load_case("distress_expression.json"))
        self.assertEqual(result.decision, "PRESERVE_ADVERSE_TRUTH_OR_DISTRESS")
        self.assertGreater(result.signals["negative_affect"].score, 0)
        self.assertFalse(result.signals["negative_affect"].restrictive_feature)

    def test_health_miracle_requires_review(self) -> None:
        result = analyze(self.load_case("health_miracle_sale.json"))
        self.assertEqual(result.decision, "INDEPENDENT_HUMAN_REVIEW")
        self.assertGreater(result.signals["actionability_hazard"].score, 0.15)
        self.assertTrue(any(item.human_gate for item in result.interventions))

    def test_intent_not_inferred_without_verified_fabrication(self) -> None:
        case = self.load_case("health_miracle_sale.json")
        case.verified_fabrication = False
        result = analyze(case)
        world = next(item for item in result.worlds if item.key == "coordinated_deception")
        self.assertLess(world.weight, 0.15)
        self.assertTrue(result.invariants["deliberate_deception_not_inferred_without_verified_fabrication"])

    def test_verified_fabrication_can_raise_deception_world(self) -> None:
        case = self.load_case("health_miracle_sale.json")
        case.verified_fabrication = True
        result = analyze(case)
        world = next(item for item in result.worlds if item.key == "coordinated_deception")
        self.assertGreater(world.weight, 0.15)

    def test_verified_harm_triggers_correction(self) -> None:
        case = self.load_case("parenting_sales_funnel.json")
        case.verified_harm = True
        result = analyze(case)
        self.assertEqual(result.decision, "CORRECTION_PROPAGATION_AND_REPAIR")
        self.assertTrue(all(item.human_gate for item in result.interventions if item.layer in {"correction", "remedy", "due_process"}))

    def test_imminent_harm_without_authority_routes_to_review(self) -> None:
        case = self.load_case("health_miracle_sale.json")
        case.imminent_harm_or_illegal = True
        case.authorized_human_review = False
        result = analyze(case)
        self.assertEqual(result.decision, "INDEPENDENT_HUMAN_REVIEW")

    def test_imminent_harm_with_authority_routes_to_authorized_escalation(self) -> None:
        case = self.load_case("health_miracle_sale.json")
        case.imminent_harm_or_illegal = True
        case.authorized_human_review = True
        case.appeal_available = True
        case.correction_channel_available = True
        result = analyze(case)
        self.assertEqual(result.decision, "AUTHORIZED_LEGAL_OR_IMMINENT_SAFETY_ESCALATION")
        self.assertEqual(result.interventions[0].automatic, False)

    def test_graph_contains_full_flow(self) -> None:
        result = analyze(self.load_case("parenting_sales_funnel.json"))
        kinds = {node.kind for node in result.graph.nodes}
        self.assertTrue({"content", "claim", "evidence", "incentive", "audience", "circulation", "decision", "outcome", "repair"}.issubset(kinds))
        self.assertGreaterEqual(len(result.graph.edges), 10)

    def test_dikwp_positions_are_preserved(self) -> None:
        case = self.load_case("parenting_sales_funnel.json")
        case.dikwp_source_position = "D"
        case.dikwp_target_position = "W"
        result = analyze(case)
        content = next(node for node in result.graph.nodes if node.node_id == "content")
        self.assertEqual(content.attributes["dikwp_source"], "D")
        self.assertEqual(content.attributes["dikwp_target"], "W")

    def test_all_world_weights_sum_to_one(self) -> None:
        result = analyze(self.load_case("parenting_sales_funnel.json"))
        self.assertAlmostEqual(sum(item.weight for item in result.worlds), 1.0, places=3)
        self.assertEqual(len(result.worlds), 8)

    def test_input_is_normalized(self) -> None:
        case = SemanticFlowCase(text="  Test  ", evidence_quality=4, reach=-1, audience_context=["x", "x", " "])
        result = analyze(case)
        self.assertEqual(case.text, "Test")
        self.assertEqual(case.evidence_quality, 1.0)
        self.assertEqual(case.reach, 0.0)
        self.assertEqual(case.audience_context, ["x"])
        self.assertEqual(len(result.case_digest), 64)


if __name__ == "__main__":
    unittest.main()
