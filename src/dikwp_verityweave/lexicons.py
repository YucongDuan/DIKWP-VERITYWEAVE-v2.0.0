from __future__ import annotations

LEXICONS: dict[str, tuple[str, ...]] = {
    "universalism": (
        "everyone must", "always", "never", "the only way", "all women", "all men",
        "every mother", "every father", "works for anyone", "without exception", "guaranteed",
    ),
    "certainty": (
        "scientifically proven", "100%", "guaranteed", "no doubt", "the truth is",
        "definitely", "certainly", "undeniable", "cannot fail", "will cure", "will make you rich",
    ),
    "causal_leap": (
        "therefore", "this proves", "because of this", "the reason you fail", "the reason your child",
        "causes", "will inevitably", "is why", "directly leads to",
    ),
    "qualifiers": (
        "may", "might", "can", "in some cases", "depending on", "limited evidence", "uncertain",
        "for some people", "context matters", "not always", "preliminary", "could",
    ),
    "context_markers": (
        "under these conditions", "for this population", "when", "unless", "exception", "trade-off",
        "resources", "age", "duration", "baseline", "follow-up", "alternative explanation",
    ),
    "rights_markers": (
        "consent", "right to refuse", "appeal", "opt out", "withdraw", "privacy", "independent review",
        "correction", "refund", "child safety", "shared responsibility",
    ),
    "urgency": (
        "act now", "last chance", "today only", "before it is too late", "limited seats", "do not wait",
        "urgent", "immediately", "countdown", "expires tonight",
    ),
    "authority_laundering": (
        "experts agree", "doctors do not want you to know", "science says", "research proves",
        "top universities", "secret method", "ancient wisdom proves", "insiders know",
    ),
    "identity_coercion": (
        "real mothers", "good parents", "high-value people", "smart people", "awake women", "real men",
        "if you cared", "if you loved", "only losers", "people like us", "you are not serious unless",
    ),
    "zero_sum": (
        "choose yourself or your child", "men versus women", "win the relationship", "never compromise",
        "your partner is the enemy", "one side must lose", "take your power back", "cut them off",
    ),
    "shaming": (
        "weak", "lazy", "low consciousness", "low intelligence", "brainwashed", "pathetic", "failure",
        "you deserve it", "not evolved", "toxic person",
    ),
    "self_sealing": (
        "if you disagree it proves", "critics are afraid", "only closed-minded people", "doubt means",
        "questioning this shows", "the fact that they deny it", "you will understand after you buy",
    ),
    "conspiracy": (
        "they are hiding", "the system does not want you", "secret cabal", "mainstream lies",
        "suppressed cure", "forbidden truth", "everyone is controlled",
    ),
    "monetization": (
        "buy now", "enroll", "course", "masterclass", "affiliate", "discount code", "premium",
        "subscription", "limited offer", "coaching package", "book a call", "checkout",
    ),
    "correction_obstruction": (
        "do not listen to critics", "never apologize", "delete negative comments", "no refunds",
        "results are your responsibility", "if it did not work you did it wrong", "questions will be removed",
    ),
    "actionability_hazard": (
        "stop your medication", "ignore your doctor", "invest everything", "borrow money", "leave now",
        "confront them", "do not report", "share their address", "skip treatment", "quit immediately",
    ),
    "public_interest": (
        "audit", "incident report", "whistleblower", "public safety", "evidence log", "conflict of interest",
        "independent review", "correction", "source documents", "consumer warning",
    ),
    "distress": (
        "grief", "sad", "angry", "afraid", "hopeless", "hurt", "danger", "failure", "exhausted",
        "overwhelmed", "distress", "depressed",
    ),
}

ADDICTIVE_FEATURE_WEIGHTS: dict[str, float] = {
    "autoplay": 0.18,
    "infinite_scroll": 0.18,
    "variable_rewards": 0.22,
    "streak_loss": 0.18,
    "high_frequency_push": 0.16,
    "read_receipt_pressure": 0.10,
    "public_rankings": 0.14,
    "forced_continuity": 0.16,
    "opaque_recommender": 0.12,
    "cancellation_friction": 0.14,
    "default_opt_in": 0.10,
}

HIGH_IMPACT_DOMAINS = {
    "health", "finance", "politics_public_interest", "family_parenting", "education", "workplace"
}

PROTECTED_ROLES = {"criticism", "whistleblowing", "distress_expression", "satire"}
