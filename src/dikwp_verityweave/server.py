from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from ipaddress import ip_address
from typing import Any

from .engine import analyze
from .interface_audit import audit_interface
from .lineage import audit_agent_lineage
from .models import AgentLineageCase, InterfaceAuditCase, SemanticFlowCase


class Handler(BaseHTTPRequestHandler):
    server_version = "VerityWeave/2.0"

    def _send(self, status: int, payload: dict[str, Any]) -> None:
        data = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send(200, {"status": "ok", "system": "DIKWP VerityWeave", "version": "2.0.0", "external_action_authority": 0})
        else:
            self._send(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 2_000_000:
                raise ValueError("Request body must be between 1 and 2,000,000 bytes")
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            if self.path == "/analyze":
                result = analyze(SemanticFlowCase.from_dict(body)).to_dict()
            elif self.path == "/audit-interface":
                result = audit_interface(InterfaceAuditCase.from_dict(body)).to_dict()
            elif self.path == "/audit-lineage":
                result = audit_agent_lineage(AgentLineageCase.from_dict(body)).to_dict()
            else:
                self._send(404, {"error": "not_found"})
                return
            self._send(200, result)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self._send(400, {"error": "invalid_request", "detail": str(exc)})
        except Exception as exc:  # pragma: no cover - defensive boundary
            self._send(500, {"error": "internal_error", "detail": type(exc).__name__})

    def log_message(self, fmt: str, *args: Any) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8765) -> None:
    address = ip_address(host)
    if not address.is_loopback:
        raise ValueError("The reference server only binds to a loopback address")
    httpd = ThreadingHTTPServer((host, int(port)), Handler)
    print(f"VerityWeave local API listening on http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
