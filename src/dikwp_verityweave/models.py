from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class Domain(str, Enum):
    GENERAL = "general"
    FAMILY = "family_parenting"
    HEALTH = "health"
    FINANCE = "finance"
    EDUCATION = "education"
    PUBLIC_INTEREST = "politics_public_interest"
    RELATIONSHIPS = "relationships"
    COMMERCIAL_KNOWLEDGE = "commercial_knowledge"
    NEWS = "news_media"
    WORKPLACE = "workplace"


class ContentRole(str, Enum):
    ADVICE = "advice"
    PERSONAL_EXPERIENCE = "personal_experience"
    CRITICISM = "criticism"
    WHISTLEBLOWING = "whistleblowing"
    MARKETING = "marketing"
    NEWS = "news"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    DISTRESS_EXPRESSION = "distress_expression"
    SATIRE = "satire"


class Decision(str, Enum):
    PRESERVE = "PRESERVE_ADVERSE_TRUTH_OR_DISTRESS"
    SUPPORT_COMMONS = "SUPPORT_HIGH_INTEGRITY_PUBLIC_VALUE"
    ALLOW = "ALLOW_WITHOUT_RESTRICTION"
    CONTEXT = "ADD_CONTEXT_AND_SOURCE_CARD"
    FRICTION = "ADD_USER_LOCAL_FRICTION"
    DAMPEN = "CIRCULATION_DAMPING_PROPOSAL"
    MONETIZATION_GATE = "MONETIZATION_DISCLOSURE_GATE"
    HUMAN_REVIEW = "INDEPENDENT_HUMAN_REVIEW"
    CORRECT_REPAIR = "CORRECTION_PROPAGATION_AND_REPAIR"
    AUTHORIZED_ESCALATION = "AUTHORIZED_LEGAL_OR_IMMINENT_SAFETY_ESCALATION"


@dataclass(slots=True)
class SemanticFlowCase:
    text: str
    case_id: str = ""
    language: str = "en"
    domain: str = Domain.GENERAL.value
    content_role: str = ContentRole.ADVICE.value
    channel: str = "post"
    dikwp_source_position: str = "I"
    dikwp_target_position: str = "P"
    audience_context: list[str] = field(default_factory=list)
    source_links: list[str] = field(default_factory=list)
    counterevidence: list[str] = field(default_factory=list)
    known_outcomes: list[str] = field(default_factory=list)
    monetized: bool = False
    paid_amplification: bool = False
    affiliate_or_sales_funnel: bool = False
    commercial_conflict_disclosed: bool = False
    price_transparency: float = 0.5
    refund_transparency: float = 0.5
    evidence_quality: float = 0.25
    source_traceability: float = 0.25
    counterevidence_visibility: float = 0.25
    uncertainty_disclosure: float = 0.25
    provenance_manifest_present: bool = False
    reach: float = 0.35
    repetition: float = 0.25
    recommendation_intensity: float = 0.35
    creator_power: float = 0.35
    platform_power: float = 0.50
    audience_dependence: float = 0.25
    decision_stakes: float = 0.35
    ai_origin: str = "unknown"
    addictive_features: list[str] = field(default_factory=list)
    verified_fabrication: bool = False
    verified_harm: bool = False
    imminent_harm_or_illegal: bool = False
    authorized_human_review: bool = False
    creator_notified: bool = False
    appeal_available: bool = True
    correction_channel_available: bool = True
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SemanticFlowCase":
        allowed = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{key: value for key, value in data.items() if key in allowed})

    def normalized(self) -> "SemanticFlowCase":
        for name in (
            "price_transparency",
            "refund_transparency",
            "evidence_quality",
            "source_traceability",
            "counterevidence_visibility",
            "uncertainty_disclosure",
            "reach",
            "repetition",
            "recommendation_intensity",
            "creator_power",
            "platform_power",
            "audience_dependence",
            "decision_stakes",
        ):
            setattr(self, name, max(0.0, min(1.0, float(getattr(self, name)))))
        self.text = self.text.strip()
        self.audience_context = sorted({str(item).strip() for item in self.audience_context if str(item).strip()})
        self.addictive_features = sorted({str(item).strip() for item in self.addictive_features if str(item).strip()})
        return self


@dataclass(slots=True)
class InterfaceAuditCase:
    name: str = "interface"
    autoplay: bool = False
    infinite_scroll: bool = False
    variable_rewards: bool = False
    streak_loss: bool = False
    push_frequency: float = 0.0
    read_receipt_pressure: bool = False
    public_rankings: bool = False
    forced_continuity: bool = False
    cancellation_friction: bool = False
    default_opt_in: bool = False
    opaque_recommender: bool = False
    youth_audience: bool = False
    acute_distress_audience: bool = False
    natural_stopping_points: bool = True
    chronological_option: bool = True
    explanation_controls: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InterfaceAuditCase":
        allowed = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{key: value for key, value in data.items() if key in allowed})


@dataclass(slots=True)
class AgentLineageCase:
    lineage_id: str = "lineage"
    agent_count: int = 1
    shared_artifacts: int = 0
    shared_memory: bool = False
    hidden_communication_channels: bool = False
    successor_reuse: bool = False
    policy_digest_changes: int = 0
    external_tools_available: bool = False
    evaluator_or_control_plane_access: bool = False
    stop_signal_propagates: bool = True
    audit_log_complete: bool = True
    human_report_channel: bool = True
    self_repairing_persistence: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentLineageCase":
        allowed = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{key: value for key, value in data.items() if key in allowed})


@dataclass(slots=True)
class Signal:
    key: str
    score: float
    markers: list[str]
    explanation: str
    restrictive_feature: bool = True


@dataclass(slots=True)
class WorldHypothesis:
    key: str
    label: str
    weight: float
    supporting_reasons: list[str]
    falsifiers: list[str]


@dataclass(slots=True)
class GraphNode:
    node_id: str
    kind: str
    label: str
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GraphEdge:
    source: str
    target: str
    relation: str
    weight: float = 1.0


@dataclass(slots=True)
class SemanticFlowGraph:
    nodes: list[GraphNode]
    edges: list[GraphEdge]


@dataclass(slots=True)
class RepairCard:
    useful_core: str
    missing_conditions: list[str]
    affected_parties: list[str]
    likely_misreadings: list[str]
    balanced_rewrite: str
    verification_questions: list[str]
    reversible_next_steps: list[str]
    stop_conditions: list[str]


@dataclass(slots=True)
class Intervention:
    layer: str
    action: str
    automatic: bool
    reversible: bool
    expiry_hours: int | None
    human_gate: bool
    reason_codes: list[str]


@dataclass(slots=True)
class CommonsSupport:
    eligible: bool
    integrity_score: float
    support_mode: str
    reasons: list[str]
    disqualifiers: list[str]


@dataclass(slots=True)
class AnalysisResult:
    version: str
    case_digest: str
    decision: str
    confidence: float
    semantic_control_potential: float
    protected_expression: bool
    high_impact: bool
    signals: dict[str, Signal]
    worlds: list[WorldHypothesis]
    graph: SemanticFlowGraph
    interventions: list[Intervention]
    repair_card: RepairCard
    commons_support: CommonsSupport
    reason_codes: list[str]
    limitations: list[str]
    invariants: dict[str, bool]
    provenance: dict[str, Any]
    validation: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class InterfaceAuditResult:
    score: float
    severity: str
    signals: dict[str, float]
    automatic_local_actions: list[str]
    platform_proposals: list[str]
    invariants: dict[str, bool]
    validation: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AgentLineageResult:
    risk_score: float
    severity: str
    risk_factors: list[str]
    required_controls: list[str]
    blocked_capabilities: list[str]
    invariants: dict[str, bool]
    validation: dict[str, Any] = field(default_factory=dict)
    input_observations: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
