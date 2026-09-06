from __future__ import annotations

import json
import unittest
from pathlib import Path

from dikwp_verityweave.interface_audit import audit_interface
from dikwp_verityweave.lineage import audit_agent_lineage
from dikwp_verityweave.models import AgentLineageCase, InterfaceAuditCase

ROOT = Path(__file__).resolve().parents[1]


class InterfaceAndLineageTests(unittest.TestCase):
    def test_high_risk_interface_is_critical(self) -> None:
        case = InterfaceAuditCase.from_dict(json.loads((ROOT / "examples/doomscroll_interface.json").read_text()))
        result = audit_interface(case)
        self.assertEqual(result.severity, "CRITICAL")
        self.assertGreater(result.score, 75)
        self.assertIn("Disable autoplay locally.", result.automatic_local_actions)
        self.assertTrue(all(result.invariants.values()))

    def test_low_risk_interface_is_low(self) -> None:
        result = audit_interface(InterfaceAuditCase())
        self.assertEqual(result.severity, "LOW")
        self.assertTrue(result.invariants["not_a_clinical_addiction_diagnosis"])

    def test_high_risk_lineage_is_critical(self) -> None:
        case = AgentLineageCase.from_dict(json.loads((ROOT / "examples/agent_lineage_risk.json").read_text()))
        result = audit_agent_lineage(case)
        self.assertEqual(result.severity, "CRITICAL")
        self.assertIn("HIDDEN_COMMUNICATION_CHANNELS", result.risk_factors)
        self.assertIn("SELF_REPAIRING_PERSISTENCE", result.risk_factors)
        self.assertTrue(all(result.invariants.values()))

    def test_bounded_lineage_is_low(self) -> None:
        result = audit_agent_lineage(AgentLineageCase(agent_count=2, shared_artifacts=1))
        self.assertEqual(result.severity, "LOW")
        self.assertIn("automatic_external_action", result.blocked_capabilities)

    def test_stop_failure_increases_risk(self) -> None:
        base = audit_agent_lineage(AgentLineageCase(agent_count=10))
        failed = audit_agent_lineage(AgentLineageCase(agent_count=10, stop_signal_propagates=False))
        self.assertGreater(failed.risk_score, base.risk_score)


if __name__ == "__main__":
    unittest.main()
