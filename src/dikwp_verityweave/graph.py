from __future__ import annotations

from .models import GraphEdge, GraphNode, SemanticFlowCase, SemanticFlowGraph, Signal


def build_semantic_flow_graph(case: SemanticFlowCase, signals: dict[str, Signal]) -> SemanticFlowGraph:
    nodes = [
        GraphNode("content", "content", case.text[:160] or "empty content", {"channel": case.channel, "role": case.content_role, "dikwp_source": case.dikwp_source_position, "dikwp_target": case.dikwp_target_position}),
        GraphNode("claim", "claim", "Primary asserted meaning", {"domain": case.domain, "language": case.language}),
        GraphNode("source", "evidence", "Sources and provenance", {"source_count": len(case.source_links), "traceability": case.source_traceability}),
        GraphNode("counterevidence", "evidence", "Counterevidence and falsifiers", {"count": len(case.counterevidence), "visibility": case.counterevidence_visibility}),
        GraphNode("incentive", "incentive", "Commercial and status incentives", {"monetized": case.monetized, "paid_amplification": case.paid_amplification}),
        GraphNode("audience", "audience", "Audience and temporary vulnerability", {"contexts": case.audience_context, "dependence": case.audience_dependence}),
        GraphNode("distribution", "circulation", "Reach, repetition, and recommendation", {"reach": case.reach, "repetition": case.repetition, "recommendation_intensity": case.recommendation_intensity}),
        GraphNode("action", "decision", "Likely downstream action", {"stakes": case.decision_stakes}),
        GraphNode("outcome", "outcome", "Observed or projected outcomes", {"known_outcomes": case.known_outcomes}),
        GraphNode("correction", "repair", "Appeal and correction path", {"appeal": case.appeal_available, "channel": case.correction_channel_available}),
    ]
    edges = [
        GraphEdge("content", "claim", "expresses"),
        GraphEdge("source", "claim", "supports", 1.0 - signals["evidence_deficit"].score),
        GraphEdge("counterevidence", "claim", "tests", case.counterevidence_visibility),
        GraphEdge("incentive", "content", "shapes", signals["incentive_opacity"].score),
        GraphEdge("distribution", "audience", "exposes", case.recommendation_intensity),
        GraphEdge("claim", "action", "influences", case.decision_stakes),
        GraphEdge("audience", "action", "interprets", signals["vulnerability_exploitation"].score),
        GraphEdge("action", "outcome", "produces"),
        GraphEdge("outcome", "correction", "triggers", 1.0 if case.verified_harm else 0.25),
        GraphEdge("correction", "claim", "revises", signals["repair_capacity"].score),
    ]
    return SemanticFlowGraph(nodes=nodes, edges=edges)
