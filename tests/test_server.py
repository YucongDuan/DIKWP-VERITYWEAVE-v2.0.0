from __future__ import annotations

import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen

from dikwp_verityweave.server import Handler


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join(timeout=2)

    def get(self, path: str) -> dict:
        with urlopen(f"http://127.0.0.1:{self.port}{path}", timeout=2) as response:
            return json.loads(response.read())

    def post(self, path: str, payload: dict) -> dict:
        request = Request(f"http://127.0.0.1:{self.port}{path}", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
        with urlopen(request, timeout=2) as response:
            return json.loads(response.read())

    def test_health(self) -> None:
        result = self.get("/health")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["external_action_authority"], 0)

    def test_analyze(self) -> None:
        result = self.post("/analyze", {"text": "I am angry and afraid.", "content_role": "distress_expression"})
        self.assertEqual(result["decision"], "PRESERVE_ADVERSE_TRUTH_OR_DISTRESS")

    def test_interface(self) -> None:
        result = self.post("/audit-interface", {"autoplay": True, "infinite_scroll": True})
        self.assertIn(result["severity"], {"LOW", "MODERATE", "HIGH", "CRITICAL"})

    def test_lineage(self) -> None:
        result = self.post("/audit-lineage", {"agent_count": 100, "hidden_communication_channels": True})
        self.assertIn("HIDDEN_COMMUNICATION_CHANNELS", result["risk_factors"])


if __name__ == "__main__":
    unittest.main()
