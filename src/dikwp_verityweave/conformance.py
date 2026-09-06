from __future__ import annotations

from .engine import VERSION


REQUIREMENTS: list[tuple[str, str, str, str]] = [
    ("SIRP-2000-001", "L0", "Behavior-level analysis; no person-level moral score", "implemented"),
    ("SIRP-2000-002", "L0", "Negative affect excluded from restriction features", "implemented"),
    ("SIRP-2000-003", "L0", "Protected-expression presumption", "implemented"),
    ("SIRP-2000-004", "L0", "Person-level morality, loyalty, intelligence, positivity, and social-worth scores prohibited", "implemented"),
    ("SIRP-2000-005", "L0", "Contextual, purpose-limited vulnerability", "implemented"),
    ("SIRP-2000-006", "L0", "Domain, role, language, channel, and audience context", "implemented"),
    ("SIRP-2000-007", "L0", "Sources, counterevidence, outcomes, and correction fields", "implemented"),
    ("SIRP-2000-008", "L0", "Analysis limitations and scope disclosure", "implemented"),
    ("SIRP-2000-009", "L1", "Independent multidimensional signals", "implemented"),
    ("SIRP-2000-010", "L1", "At least two non-isomorphic world hypotheses", "implemented"),
    ("SIRP-2000-011", "L1", "Deliberate deception not inferred without independent evidence", "implemented"),
    ("SIRP-2000-012", "L1", "Semantic-flow graph", "implemented"),
    ("SIRP-2000-013", "L1", "Traceable DIKWP transition fields", "implemented"),
    ("SIRP-2000-014", "L1", "Provenance is not truth", "implemented"),
    ("SIRP-2000-015", "L1", "AI origin does not independently determine truth or restriction", "implemented"),
    ("SIRP-2000-016", "L1", "Uncertainty and falsifiers exposed", "implemented"),
    ("SIRP-2000-017", "L2", "Context repair card", "implemented"),
    ("SIRP-2000-018", "L2", "Reversible reality-contact step", "implemented"),
    ("SIRP-2000-019", "L2", "Automatic user-local reversible friction", "implemented"),
    ("SIRP-2000-020", "L2", "Compulsive and deceptive interface audit", "implemented"),
    ("SIRP-2000-021", "L2", "Stopping points and recommender controls", "implemented"),
    ("SIRP-2000-022", "L2", "Positive semantic commons support proposal", "implemented"),
    ("SIRP-2000-023", "L2", "Commons support independent of ideology or positive sentiment", "implemented"),
    ("SIRP-2000-024", "L2", "Provenance-preserving translation and accessibility support", "implemented"),
    ("SIRP-2000-025", "L3", "Least-restrictive effective intervention", "implemented"),
    ("SIRP-2000-026", "L3", "Named human authority for platform adverse action", "implemented"),
    ("SIRP-2000-027", "L3", "Creator or user notice", "implemented"),
    ("SIRP-2000-028", "L3", "Specific reason codes and evidence basis", "implemented"),
    ("SIRP-2000-029", "L3", "Expiry or scheduled review", "implemented"),
    ("SIRP-2000-030", "L3", "Accessible appeal", "implemented"),
    ("SIRP-2000-031", "L3", "Correction channel", "implemented"),
    ("SIRP-2000-032", "L3", "Restoration support", "implemented"),
    ("SIRP-2000-033", "L3", "Monetization conflict, price, refund, failure-case, and scope disclosures", "implemented"),
    ("SIRP-2000-034", "L3", "Protected-expression stress-test requirement", "implemented"),
    ("SIRP-2000-035", "L3", "Qualified human review for high-stakes domains", "implemented"),
    ("SIRP-2000-036", "L3", "Automatic removal, penalty, and legal determination disabled", "implemented"),
    ("SIRP-2000-037", "L4", "Five-receipt correction closure", "implemented"),
    ("SIRP-2000-038", "L4", "Consequential use blocked during material appeal", "implemented"),
    ("SIRP-2000-039", "L4", "Append-only responsibility ledger", "implemented"),
    ("SIRP-2000-040", "L4", "Agent policy, prompt, artifact, memory, credential, and successor lineage", "implemented"),
    ("SIRP-2000-041", "L4", "Stop and revocation propagation", "implemented"),
    ("SIRP-2000-042", "L4", "Successor reauthorization", "implemented"),
    ("SIRP-2000-043", "L4", "Control-plane separation", "implemented"),
    ("SIRP-2000-044", "L4", "Reward-compatible human-report channel", "implemented"),
    ("SIRP-2000-045", "L4", "AT Protocol label reference mapping", "implemented"),
    ("SIRP-2000-046", "L4", "C2PA reference assertion", "implemented"),
    ("SIRP-2000-047", "L4", "Statement-of-reasons reference mapping", "implemented"),
    ("SIRP-2000-048", "L4", "W3C PROV reference mapping", "implemented"),
    ("SIRP-2000-049", "L4", "JSON Schemas and OpenAPI", "implemented"),
    ("SIRP-2000-050", "L4", "Bounded deterministic agent tools without external enforcement", "implemented"),
    ("SIRP-2000-051", "L5", "Signed and revocable production policy bundles", "partial"),
    ("SIRP-2000-052", "L5", "Independent transparency service", "partial"),
    ("SIRP-2000-053", "L5", "Independent multilingual and dialectal calibration", "partial"),
    ("SIRP-2000-054", "L5", "Jurisdiction-specific lawful-action connectors", "partial"),
    ("SIRP-2000-055", "L5", "Institutionally independent appeals", "partial"),
    ("SIRP-2000-056", "L5", "Longitudinal effectiveness and protected-expression evaluation", "partial"),
    ("SIRP-2000-057", "L5", "Data-protection and human-rights impact assessment", "partial"),
    ("SIRP-2000-058", "L5", "Independent security review", "partial"),
    ("SIRP-2000-059", "L5", "Production key management and rotation", "partial"),
    ("SIRP-2000-060", "L5", "Public aggregate action, reversal, and restoration reporting", "partial"),
    ("SIRP-2000-061", "DESIGN", "Automatic content removal in the reference core", "not_supported_by_design"),
    ("SIRP-2000-062", "DESIGN", "Person-level moral or cognition scoring", "not_supported_by_design"),
    ("SIRP-2000-063", "DESIGN", "Viewpoint or sentiment penalties", "not_supported_by_design"),
    ("SIRP-2000-064", "DESIGN", "Secret blacklists and undeclared profile propagation", "not_supported_by_design"),
]


def conformance_statement() -> dict:
    counts: dict[str, int] = {}
    for _, _, _, status in REQUIREMENTS:
        counts[status] = counts.get(status, 0) + 1
    return {
        "specification": "SIRP-2000:2026-DRAFT",
        "implementation": "DIKWP VerityWeave Semantic Resilience Grid OS",
        "version": VERSION,
        "reference_level": "L4-reference",
        "third_party_certification": False,
        "counts": counts,
        "requirements": [
            {"id": item_id, "level": level, "requirement": text, "status": status}
            for item_id, level, text, status in REQUIREMENTS
        ],
    }
