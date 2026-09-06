from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from .conformance import conformance_statement
from .due_process import add_correction_receipt, get_appeal, open_appeal
from .engine import analyze
from .formatters import analysis_markdown, as_json
from .interface_audit import audit_interface
from .interoperability import (
    to_atproto_label,
    to_c2pa_reference_assertion,
    to_dsa_statement_of_reasons_reference,
    to_prov_jsonld,
)
from .ledger import append_event, verify_ledger
from .lineage import audit_agent_lineage
from .mcp import run_stdio
from .models import AgentLineageCase, InterfaceAuditCase, SemanticFlowCase
from .server import serve
from .utils import safe_filename


def _load(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _demo_cases() -> list[tuple[str, SemanticFlowCase]]:
    return [
        (
            "parenting_sales_funnel",
            SemanticFlowCase(
                text=(
                    "A woman must put herself first before she can care for her child. Awake mothers enroll today; "
                    "otherwise they will keep betraying themselves. This is the last chance to join the course."
                ),
                domain="family_parenting",
                content_role="marketing",
                audience_context=["caregiver_exhaustion", "limited_domain_literacy"],
                monetized=True,
                paid_amplification=True,
                affiliate_or_sales_funnel=True,
                evidence_quality=0.12,
                source_traceability=0.08,
                counterevidence_visibility=0.05,
                uncertainty_disclosure=0.05,
                reach=0.78,
                repetition=0.70,
                recommendation_intensity=0.82,
                creator_power=0.62,
                audience_dependence=0.65,
                decision_stakes=0.72,
                addictive_features=["autoplay", "infinite_scroll", "high_frequency_push"],
            ),
        ),
        (
            "whistleblower_report",
            SemanticFlowCase(
                text=(
                    "The audit result is disturbing. Logs and contracts indicate that the institution did not follow its stated process. "
                    "Preserve the evidence and request independent review."
                ),
                domain="politics_public_interest",
                content_role="whistleblowing",
                evidence_quality=0.82,
                source_traceability=0.88,
                counterevidence_visibility=0.66,
                uncertainty_disclosure=0.72,
                provenance_manifest_present=True,
                reach=0.35,
                repetition=0.10,
                recommendation_intensity=0.20,
                decision_stakes=0.75,
            ),
        ),
        (
            "health_miracle_sale",
            SemanticFlowCase(
                text=(
                    "Science has proven this secret method cures anxiety 100 percent. Ignore your doctor. "
                    "Buy the programme tonight before the offer disappears."
                ),
                domain="health",
                content_role="marketing",
                audience_context=["acute_distress", "limited_domain_literacy"],
                monetized=True,
                paid_amplification=True,
                affiliate_or_sales_funnel=True,
                evidence_quality=0.02,
                source_traceability=0.02,
                counterevidence_visibility=0.0,
                uncertainty_disclosure=0.0,
                reach=0.82,
                repetition=0.76,
                recommendation_intensity=0.85,
                creator_power=0.68,
                audience_dependence=0.72,
                decision_stakes=0.95,
                addictive_features=["autoplay", "infinite_scroll", "variable_rewards", "streak_loss"],
            ),
        ),
    ]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="verityweave", description="DIKWP VerityWeave Semantic Resilience Grid OS")
    sub = parser.add_subparsers(dest="command", required=True)

    analyze_p = sub.add_parser("analyze", help="Analyze a semantic-flow case JSON")
    analyze_p.add_argument("case")
    analyze_p.add_argument("--output")
    analyze_p.add_argument("--ledger")

    interface_p = sub.add_parser("audit-interface", help="Audit an interface JSON")
    interface_p.add_argument("case")
    interface_p.add_argument("--output")

    lineage_p = sub.add_parser("audit-lineage", help="Audit an agent-lineage JSON")
    lineage_p.add_argument("case")
    lineage_p.add_argument("--output")

    demo_p = sub.add_parser("demo", help="Run deterministic synthetic demonstrations")
    demo_p.add_argument("--output", default=".verityweave-demo")
    demo_p.add_argument("--reset", action="store_true")

    export_p = sub.add_parser("export", help="Export a result to a reference interoperability format")
    export_p.add_argument("result")
    export_p.add_argument("--format", required=True, choices=["atproto", "dsa", "c2pa", "prov"])
    export_p.add_argument("--subject", default="urn:example:content")
    export_p.add_argument("--source-did", default="did:web:example.org")
    export_p.add_argument("--output")

    serve_p = sub.add_parser("serve", help="Run the loopback-only JSON API")
    serve_p.add_argument("--host", default="127.0.0.1")
    serve_p.add_argument("--port", type=int, default=8765)

    sub.add_parser("mcp", help="Run the MCP 2026-07-28 stateless stdio server")
    sub.add_parser("conformance", help="Print the SIRP-2000 implementation statement")

    verify_p = sub.add_parser("verify-ledger", help="Verify an append-only responsibility ledger")
    verify_p.add_argument("ledger")

    open_p = sub.add_parser("appeal-open", help="Open an appeal")
    open_p.add_argument("--store", required=True)
    open_p.add_argument("--decision-id", required=True)
    open_p.add_argument("--scope", required=True)
    open_p.add_argument("--grounds", required=True)

    receipt_p = sub.add_parser("appeal-receipt", help="Add a correction receipt")
    receipt_p.add_argument("--store", required=True)
    receipt_p.add_argument("--appeal-id", required=True)
    receipt_p.add_argument("--type", required=True)
    receipt_p.add_argument("--evidence", required=True)

    status_p = sub.add_parser("appeal-status", help="Read an appeal and missing receipts")
    status_p.add_argument("--store", required=True)
    status_p.add_argument("--appeal-id", required=True)

    html_p = sub.add_parser("export-html", help="Copy the packaged standalone HTML application")
    html_p.add_argument("output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "analyze":
        result = analyze(SemanticFlowCase.from_dict(_load(args.case)))
        text = as_json(result)
        if args.output:
            out = Path(args.output)
            if out.suffix:
                _write(out, text if out.suffix == ".json" else analysis_markdown(result))
            else:
                _write(out / "analysis.json", text)
                _write(out / "analysis.md", analysis_markdown(result))
        if args.ledger:
            append_event(args.ledger, "SEMANTIC_FLOW_ANALYZED", {"case_digest": result.case_digest, "decision": result.decision})
        print(text)
        return 0
    if args.command == "audit-interface":
        result = audit_interface(InterfaceAuditCase.from_dict(_load(args.case)))
        text = as_json(result)
        if args.output:
            _write(Path(args.output), text)
        print(text)
        return 0
    if args.command == "audit-lineage":
        result = audit_agent_lineage(AgentLineageCase.from_dict(_load(args.case)))
        text = as_json(result)
        if args.output:
            _write(Path(args.output), text)
        print(text)
        return 0
    if args.command == "demo":
        out = Path(args.output)
        if args.reset and out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True, exist_ok=True)
        ledger = out / "responsibility-ledger.jsonl"
        summary = []
        for name, case in _demo_cases():
            result = analyze(case)
            _write(out / f"{safe_filename(name)}.json", as_json(result))
            _write(out / f"{safe_filename(name)}.md", analysis_markdown(result))
            append_event(ledger, "DEMO_CASE_ANALYZED", {"name": name, "case_digest": result.case_digest, "decision": result.decision})
            summary.append({"name": name, "decision": result.decision, "semantic_control_potential": result.semantic_control_potential})
        lineage = audit_agent_lineage(AgentLineageCase(agent_count=1200, shared_artifacts=70, shared_memory=True, hidden_communication_channels=True, successor_reuse=True, policy_digest_changes=4, external_tools_available=True, evaluator_or_control_plane_access=True, stop_signal_propagates=False, audit_log_complete=False, human_report_channel=False, self_repairing_persistence=True))
        _write(out / "agent-lineage-audit.json", as_json(lineage))
        summary_payload = {"system": "DIKWP VerityWeave", "version": "2.0.0", "cases": summary, "lineage": lineage.to_dict(), "ledger": verify_ledger(ledger)}
        _write(out / "demo-summary.json", as_json(summary_payload))
        print(as_json(summary_payload))
        return 0
    if args.command == "export":
        data = _load(args.result)
        result = _analysis_from_dict(data)
        if args.format == "atproto":
            payload = to_atproto_label(result, source_did=args.source_did, subject_uri=args.subject)
        elif args.format == "dsa":
            payload = to_dsa_statement_of_reasons_reference(result, content_id=args.subject)
        elif args.format == "c2pa":
            payload = to_c2pa_reference_assertion(result)
        else:
            payload = to_prov_jsonld(result)
        text = as_json(payload)
        if args.output:
            _write(Path(args.output), text)
        print(text)
        return 0
    if args.command == "serve":
        serve(args.host, args.port)
        return 0
    if args.command == "mcp":
        run_stdio()
        return 0
    if args.command == "conformance":
        print(as_json(conformance_statement()))
        return 0
    if args.command == "verify-ledger":
        print(as_json(verify_ledger(args.ledger)))
        return 0
    if args.command == "appeal-open":
        print(as_json(open_appeal(args.store, args.decision_id, args.scope, args.grounds)))
        return 0
    if args.command == "appeal-receipt":
        print(as_json(add_correction_receipt(args.store, args.appeal_id, args.type, args.evidence)))
        return 0
    if args.command == "appeal-status":
        print(as_json(get_appeal(args.store, args.appeal_id)))
        return 0
    if args.command == "export-html":
        from importlib.resources import files
        source = files("dikwp_verityweave.data").joinpath("DIKWP_VERITYWEAVE_SEMANTIC_RESILIENCE_GRID_OS_v2.0.0.html")
        Path(args.output).write_bytes(source.read_bytes())
        print(args.output)
        return 0
    return 2


def _analysis_from_dict(data: dict[str, Any]):
    # Reconstruct through a minimal wrapper for reference exports.
    from .models import (
        AnalysisResult,
        CommonsSupport,
        GraphEdge,
        GraphNode,
        Intervention,
        RepairCard,
        SemanticFlowGraph,
        Signal,
        WorldHypothesis,
    )

    return AnalysisResult(
        version=data["version"],
        case_digest=data["case_digest"],
        decision=data["decision"],
        confidence=data["confidence"],
        semantic_control_potential=data["semantic_control_potential"],
        protected_expression=data["protected_expression"],
        high_impact=data["high_impact"],
        signals={key: Signal(**value) for key, value in data["signals"].items()},
        worlds=[WorldHypothesis(**value) for value in data["worlds"]],
        graph=SemanticFlowGraph(nodes=[GraphNode(**value) for value in data["graph"]["nodes"]], edges=[GraphEdge(**value) for value in data["graph"]["edges"]]),
        interventions=[Intervention(**value) for value in data["interventions"]],
        repair_card=RepairCard(**data["repair_card"]),
        commons_support=CommonsSupport(**data["commons_support"]),
        reason_codes=data["reason_codes"],
        limitations=data["limitations"],
        invariants=data["invariants"],
        provenance=data["provenance"],
    )
