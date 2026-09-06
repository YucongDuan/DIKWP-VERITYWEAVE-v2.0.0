from __future__ import annotations

import unittest

from dikwp_verityweave.engine import analyze
from dikwp_verityweave.models import SemanticFlowCase


class CommonsAndRepairTests(unittest.TestCase):
    def test_high_integrity_public_value_can_receive_support_proposal(self) -> None:
        case = SemanticFlowCase(
            text="Independent audit source documents, evidence log, consumer warning, correction, and public safety review.",
            domain="politics_public_interest",
            content_role="news",
            evidence_quality=0.95,
            source_traceability=0.95,
            counterevidence_visibility=0.9,
            uncertainty_disclosure=0.9,
            provenance_manifest_present=True,
            appeal_available=True,
            correction_channel_available=True,
            reach=0.1,
            repetition=0.0,
            recommendation_intensity=0.05,
        )
        result = analyze(case)
        self.assertTrue(result.commons_support.eligible)
        self.assertEqual(result.decision, "SUPPORT_HIGH_INTEGRITY_PUBLIC_VALUE")
        self.assertTrue(all(item.human_gate for item in result.interventions))

    def test_verified_fabrication_disqualifies_commons_support(self) -> None:
        case = SemanticFlowCase(
            text="Audit source documents and public safety evidence.",
            content_role="news",
            evidence_quality=0.95,
            source_traceability=0.95,
            counterevidence_visibility=0.9,
            uncertainty_disclosure=0.9,
            provenance_manifest_present=True,
            verified_fabrication=True,
        )
        result = analyze(case)
        self.assertFalse(result.commons_support.eligible)
        self.assertIn("VERIFIED_FABRICATION", result.commons_support.disqualifiers)

    def test_general_repair_exposes_incentives(self) -> None:
        result = analyze(SemanticFlowCase(text="This is definitely the only way. Buy now."))
        joined = " ".join(result.repair_card.verification_questions).lower()
        self.assertIn("money", joined)
        self.assertIn("control", joined)

    def test_parenting_repair_is_non_zero_sum(self) -> None:
        result = analyze(SemanticFlowCase(text="Mothers must always put themselves first.", domain="family_parenting"))
        rewrite = result.repair_card.balanced_rewrite.lower()
        self.assertIn("caregivers", rewrite)
        self.assertIn("children", rewrite)
        self.assertIn("responsibilit", rewrite)


if __name__ == "__main__":
    unittest.main()
