from __future__ import annotations

import json
import sys
from typing import Any, Callable

from .conformance import conformance_statement
from .engine import analyze
from .interface_audit import audit_interface
from .lineage import audit_agent_lineage
from .models import AgentLineageCase, InterfaceAuditCase, SemanticFlowCase
from .runtime_validation import OutputValidationError

PROTOCOL_VERSION = "2026-07-28"
SERVER_INFO = {"name": "dikwp-verityweave", "version": "2.0.0"}


def _meta() -> dict[str, Any]:
    return {
        "io.modelcontextprotocol/protocolVersion": PROTOCOL_VERSION,
        "io.modelcontextprotocol/serverInfo": SERVER_INFO,
    }


def _tools() -> list[dict[str, Any]]:
    return sorted(
        [
            {
                "name": "analyze_semantic_flow",
                "title": "Analyze a semantic flow",
                "description": "Analyze content, evidence, incentives, circulation, audience context, repair capacity, and proportionate interventions. No person-level moral score and no external action.",
                "inputSchema": {"type": "object", "required": ["text"], "properties": {"text": {"type": "string"}, "domain": {"type": "string"}, "content_role": {"type": "string"}}, "additionalProperties": True},
                "outputSchema": {"type": "object"},
            },
            {
                "name": "audit_interface",
                "title": "Audit addictive and deceptive interface patterns",
                "description": "Audit autoplay, infinite scroll, variable rewards, exit penalties, opaque recommendations, and related patterns. The result is not a clinical addiction diagnosis.",
                "inputSchema": {"type": "object", "properties": {}, "additionalProperties": True},
                "outputSchema": {"type": "object"},
            },
            {
                "name": "audit_agent_lineage",
                "title": "Audit agent and policy lineage",
                "description": "Assess shared artifacts, hidden channels, successor reuse, policy mutation, stop propagation, and control-plane access.",
                "inputSchema": {"type": "object", "properties": {}, "additionalProperties": True},
                "outputSchema": {"type": "object"},
            },
            {
                "name": "get_conformance_statement",
                "title": "Get SIRP-2000 conformance statement",
                "description": "Return the author-side implementation statement and unsupported-by-design capabilities.",
                "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
                "outputSchema": {"type": "object"},
            },
        ],
        key=lambda item: item["name"],
    )


def _call(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    handlers: dict[str, Callable[[], dict[str, Any]]] = {
        "analyze_semantic_flow": lambda: analyze(SemanticFlowCase.from_dict(arguments)).to_dict(),
        "audit_interface": lambda: audit_interface(InterfaceAuditCase.from_dict(arguments)).to_dict(),
        "audit_agent_lineage": lambda: audit_agent_lineage(AgentLineageCase.from_dict(arguments)).to_dict(),
        "get_conformance_statement": conformance_statement,
    }
    if name not in handlers:
        raise KeyError(f"Unknown tool: {name}")
    return handlers[name]()


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    if "id" not in request:
        return None
    request_id = request.get("id")
    method = request.get("method")
    try:
        if method == "tools/list":
            result = {"resultType": "complete", "tools": _tools(), "ttlMs": 300000, "cacheScope": "public", "_meta": _meta()}
        elif method == "tools/call":
            params = request.get("params") or {}
            name = str(params.get("name", ""))
            arguments = params.get("arguments") or {}
            structured = _call(name, arguments)
            result = {
                "resultType": "complete",
                "content": [{"type": "text", "text": json.dumps(structured, ensure_ascii=False, sort_keys=True)}],
                "structuredContent": structured,
                "isError": False,
                "_meta": _meta(),
            }
        elif method == "resources/list":
            result = {
                "resultType": "complete",
                "resources": [
                    {
                        "uri": "verityweave://constitution",
                        "name": "VerityWeave runtime constitution",
                        "description": "Non-negotiable runtime boundaries and protected-expression rules.",
                        "mimeType": "application/json",
                    }
                ],
                "ttlMs": 300000,
                "cacheScope": "public",
                "_meta": _meta(),
            }
        elif method == "resources/read":
            uri = str((request.get("params") or {}).get("uri", ""))
            if uri != "verityweave://constitution":
                raise KeyError(f"Unknown resource: {uri}")
            constitution = {
                "person_level_moral_scoring": "prohibited",
                "negative_affect_as_restriction_feature": "prohibited",
                "automatic_content_removal_authority": 0,
                "automatic_external_action_authority": 0,
                "protected_adverse_truth_presumption": True,
                "appeal_and_correction_required": True,
            }
            result = {
                "resultType": "complete",
                "contents": [{"uri": uri, "mimeType": "application/json", "text": json.dumps(constitution, sort_keys=True)}],
                "_meta": _meta(),
            }
        else:
            return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": "Method not found"}}
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    except OutputValidationError as exc:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32603, "message": str(exc), "data": {"error": "output_validation_failed", "validation": exc.report}}}
    except (KeyError, ValueError, TypeError) as exc:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32602, "message": str(exc)}}
    except Exception as exc:  # pragma: no cover
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32603, "message": type(exc).__name__}}


def run_stdio() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            if response is not None:
                sys.stdout.write(json.dumps(response, ensure_ascii=False, separators=(",", ":")) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}) + "\n")
            sys.stdout.flush()
