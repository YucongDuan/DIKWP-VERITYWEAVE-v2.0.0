from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from dikwp_verityweave.cli import main

ROOT = Path(__file__).resolve().parents[1]


class CliAndPackagingTests(unittest.TestCase):
    def test_demo_generates_ledger_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(main(["demo", "--output", tmp, "--reset"]), 0)
            summary = json.loads((Path(tmp) / "demo-summary.json").read_text())
            self.assertTrue(summary["ledger"]["valid"])
            self.assertEqual(len(summary["cases"]), 3)

    def test_analyze_writes_json_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(main(["analyze", str(ROOT / "examples/parenting_sales_funnel.json"), "--output", tmp]), 0)
            self.assertTrue((Path(tmp) / "analysis.json").exists())
            self.assertTrue((Path(tmp) / "analysis.md").exists())

    def test_export_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "app.html"
            self.assertEqual(main(["export-html", str(target)]), 0)
            text = target.read_text(encoding="utf-8")
            self.assertIn("VerityWeave Semantic Resilience Grid", text)
            self.assertNotIn("<script src=\"http", text)

    def test_conformance_command(self) -> None:
        self.assertEqual(main(["conformance"]), 0)


if __name__ == "__main__":
    unittest.main()
