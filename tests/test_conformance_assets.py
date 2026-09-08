from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from dikwp_verityweave.conformance import conformance_statement

ROOT = Path(__file__).resolve().parents[1]


class ConformanceAndAssetTests(unittest.TestCase):
    def test_conformance_counts(self) -> None:
        value = conformance_statement()
        self.assertEqual(value["counts"]["implemented"], 46)
        self.assertEqual(value["counts"]["proposal_only"], 4)
        self.assertEqual(value["counts"]["partial"], 10)
        self.assertEqual(value["counts"]["not_supported_by_design"], 4)
        self.assertFalse(value["third_party_certification"])
        self.assertFalse(value["test_execution_performed"])
        self.assertEqual(value["claim_type"], "author_self_declaration")
        self.assertEqual(value["external_enforcement"], "NOT_VERIFIED")
        for requirement in value["requirements"]:
            if requirement["id"] in {f"SIRP-2000-{n:03d}" for n in range(41, 45)}:
                self.assertEqual(requirement["status"], "proposal_only")

    def test_json_assets_parse(self) -> None:
        for path in list((ROOT / "examples").glob("*.json")) + list((ROOT / "resources").glob("*.json")) + list((ROOT / "schemas").glob("*.json")):
            with self.subTest(path=path.name):
                json.loads(path.read_text(encoding="utf-8"))

    def test_openapi_is_loopback_only(self) -> None:
        text = (ROOT / "schemas/openapi.yaml").read_text(encoding="utf-8")
        self.assertIn("127.0.0.1", text)
        self.assertNotIn("0.0.0.0", text)

    def test_standalone_has_no_external_asset_requests(self) -> None:
        text = (ROOT / "web/DIKWP_VERITYWEAVE_SEMANTIC_RESILIENCE_GRID_OS_v2.0.0.html").read_text(encoding="utf-8")
        self.assertNotRegex(text, r"<(script|link|img)[^>]+(?:src|href)=['\"]https?://")

    def test_extension_has_no_host_permissions(self) -> None:
        manifest = json.loads((ROOT / "browser_extension/manifest.json").read_text())
        self.assertEqual(manifest["host_permissions"], [])

    def test_runtime_surfaces_use_english_not_documentation(self) -> None:
        cjk = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
        # Bilingual README/integration guidance and author-supplied dedications
        # are documentation, not accidental UI localization regressions.
        roots = [ROOT / name for name in ("src", "web", "browser_extension", "schemas", "resources", "formal")]
        paths = [p for root in roots for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".py", ".json", ".html", ".js", ".yaml", ".yml", ".toml"}]
        # Keep the language gate while allowing the creator\'s exact Chinese name.
        violations = [str(p.relative_to(ROOT)) for p in paths if cjk.search(p.read_text(encoding="utf-8", errors="ignore").replace("\u6bb5\u7389\u806a", ""))]
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
