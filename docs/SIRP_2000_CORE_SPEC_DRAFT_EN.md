# SIRP-2000:2026-DRAFT

## Semantic Integrity, Resilience and Repair Protocol

Version: 2.0.0  
Status: Author-side pre-standard draft  
Language: English  
Conformance claims: self-assessed unless independently certified

## 1. Scope

SIRP-2000 specifies machine-readable and operational requirements for systems that analyze or govern semantic flows involving content, evidence, context, incentives, audiences, distribution, action, outcomes, correction, and agent lineage.

It is intended for research systems, educational tools, community moderation, platform trust and safety, recommender governance, creator disclosure, digital wellbeing, and bounded content-analysis agents.

It does not define universal truth, clinical diagnosis, creator intent, legal liability, or person-level moral worth.

## 2. Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as normative requirements within this draft.

## 3. Core objects

A conforming implementation SHALL support at least:

- `SemanticFlowCase`;
- `SignalVector`;
- `WorldHypothesisSet`;
- `SemanticFlowGraph`;
- `RepairCard`;
- `InterventionBundle`;
- `CommonsSupportProposal`;
- `InterfaceAudit`;
- `AgentLineageAudit`;
- `AppealRecord`;
- `CorrectionReceiptSet`;
- `ResponsibilityLedgerEvent`.

## 4. Conformance levels

Levels are cumulative. A claim at level L4 requires satisfaction of applicable requirements from L0 through L4.

### L0 — Object, scope, and rights

- **SIRP-2000-001**: The implementation MUST analyze specific content, behavior, interface, or lineage events rather than assigning a general moral score to a person.
- **SIRP-2000-002**: Negative affect MUST NOT be an independent restriction feature.
- **SIRP-2000-003**: Criticism, whistleblowing, satire, and distress expression MUST receive a protected-expression presumption.
- **SIRP-2000-004**: Person-level morality, loyalty, intelligence, positivity, or social-worth scoring MUST be prohibited.
- **SIRP-2000-005**: Vulnerability MUST be represented as contextual, purpose-limited, time-bounded, and private by default.
- **SIRP-2000-006**: The declared domain, content role, language, channel, and audience context MUST be represented.
- **SIRP-2000-007**: The system MUST represent sources, counterevidence, known outcomes, and correction availability separately.
- **SIRP-2000-008**: A claim's scope and the limits of the analysis MUST be disclosed.

### L1 — Evidence, plurality, and semantic flow

- **SIRP-2000-009**: The implementation MUST expose independent signal dimensions rather than only a single opaque score.
- **SIRP-2000-010**: At least two non-isomorphic world hypotheses MUST be retained for consequential analysis.
- **SIRP-2000-011**: Deliberate deception MUST NOT be inferred without independent evidence of fabrication, coordination, or intent.
- **SIRP-2000-012**: The system MUST represent content, claim, source, counterevidence, incentive, audience, distribution, action, outcome, and correction relations.
- **SIRP-2000-013**: Data, Information, Knowledge, Wisdom, and Purpose transitions SHOULD remain traceable.
- **SIRP-2000-014**: Provenance MUST NOT be represented as proof that a claim is true.
- **SIRP-2000-015**: Declared human, AI, mixed, or unknown origin MUST NOT independently determine truth or restriction.
- **SIRP-2000-016**: Uncertainty and falsifiers SHOULD be exposed for each material world hypothesis.

### L2 — Repair, user control, and public value

- **SIRP-2000-017**: The implementation MUST generate or support a context repair card.
- **SIRP-2000-018**: Repair SHOULD include a reversible reality-contact or verification step.
- **SIRP-2000-019**: User-local reversible friction MAY be automatic.
- **SIRP-2000-020**: The system MUST be able to audit declared compulsive or deceptive interface features.
- **SIRP-2000-021**: Natural stopping points, notification control, recommender explanation, and a chronological or non-personalized option SHOULD be supported where applicable.
- **SIRP-2000-022**: High-integrity public-value content MAY receive a transparent support proposal.
- **SIRP-2000-023**: Support eligibility MUST NOT depend on ideological conformity or positive sentiment.
- **SIRP-2000-024**: Translation and accessibility support SHOULD preserve provenance, scope, uncertainty, and semantic-loss notes.

### L3 — Proportionate platform governance

- **SIRP-2000-025**: The least restrictive effective intervention SHOULD be preferred.
- **SIRP-2000-026**: Platform-level adverse actions MUST require named human authority.
- **SIRP-2000-027**: The affected creator or user MUST receive notice, subject to a narrowly documented lawful exception.
- **SIRP-2000-028**: Adverse actions MUST expose specific reason codes and the evidence basis.
- **SIRP-2000-029**: Temporary restrictions MUST have an expiry or scheduled review.
- **SIRP-2000-030**: An accessible appeal channel MUST be provided.
- **SIRP-2000-031**: A correction channel MUST be provided.
- **SIRP-2000-032**: Restoration after reversal MUST be operationally supported.
- **SIRP-2000-033**: Monetized content SHOULD disclose conflicts, pricing, refund terms, failure cases, and scope before paid amplification.
- **SIRP-2000-034**: Protected-expression false-positive tests MUST be included before production deployment.
- **SIRP-2000-035**: High-stakes health, finance, legal, education, child-safety, and public-interest decisions MUST receive qualified human review.
- **SIRP-2000-036**: The reference core MUST NOT automatically remove content, impose a monetary penalty, or determine legal liability.

### L4 — Correction, agent lineage, and interoperability

- **SIRP-2000-037**: Confirmed wrong decisions MUST require restoration, record correction, downstream notification, verified-loss compensation where applicable, and rule or model revision.
- **SIRP-2000-038**: Consequential use MUST remain blocked while a material appeal is unresolved.
- **SIRP-2000-039**: Analysis and correction events MUST be recordable in an append-only responsibility ledger.
- **SIRP-2000-040**: Agent lineages MUST expose policy, prompt, artifact, memory, credential, and successor relationships applicable to the deployment.
- **SIRP-2000-041**: Stop and revocation signals MUST propagate to tasks, queues, caches, credentials, memories, and successors.
- **SIRP-2000-042**: Successors MUST reauthorize inherited artifacts rather than inherit authority automatically.
- **SIRP-2000-043**: Task agents MUST be separated from evaluator, identity, logging, policy, monitoring, and stop control planes.
- **SIRP-2000-044**: A human-report channel MUST exist and reporting MUST NOT be penalized by task rewards.
- **SIRP-2000-045**: An AT Protocol label reference mapping SHOULD be available where applicable.
- **SIRP-2000-046**: A C2PA reference assertion SHOULD state that provenance is not truth.
- **SIRP-2000-047**: A statement-of-reasons reference mapping SHOULD expose automation and human-review status.
- **SIRP-2000-048**: A W3C PROV-compatible reference mapping SHOULD be available.
- **SIRP-2000-049**: Machine-readable JSON Schemas and an API description SHOULD be provided.
- **SIRP-2000-050**: Agent tools MUST exclude automatic external enforcement and SHOULD support deterministic discovery.

### L5 — Production trust infrastructure

- **SIRP-2000-051**: Production policy bundles SHOULD be digitally signed and revocable.
- **SIRP-2000-052**: Production decision and correction records SHOULD be anchored in an independently operated transparency service.
- **SIRP-2000-053**: Multilingual and dialectal calibration SHOULD be independently evaluated.
- **SIRP-2000-054**: Jurisdiction-specific lawful-action connectors SHOULD be separately authorized and audited.
- **SIRP-2000-055**: Appeals SHOULD be institutionally independent from the original decision maker.
- **SIRP-2000-056**: Longitudinal real-world effectiveness and protected-expression harm SHOULD be evaluated.
- **SIRP-2000-057**: A data-protection and human-rights impact assessment SHOULD precede production deployment.
- **SIRP-2000-058**: An independent security review SHOULD cover untrusted input processing, tool access, secrets, and agent lineage.
- **SIRP-2000-059**: Production signing keys SHOULD use appropriate key-management and rotation controls.
- **SIRP-2000-060**: Aggregate public reporting SHOULD include actions, reversals, restoration latency, protected-expression errors, and unresolved appeals.

## 5. Nonconforming capabilities by design

- **SIRP-2000-061**: Automatic content removal in the reference core is not supported by design.
- **SIRP-2000-062**: Person-level moral or cognition scoring is not supported by design.
- **SIRP-2000-063**: Viewpoint or sentiment penalties are not supported by design.
- **SIRP-2000-064**: Secret blacklists and undeclared cross-product profile propagation are not supported by design.

## 6. Decision states

A conforming implementation MAY use the following reference decisions:

```text
PRESERVE_ADVERSE_TRUTH_OR_DISTRESS
SUPPORT_HIGH_INTEGRITY_PUBLIC_VALUE
ALLOW_WITHOUT_RESTRICTION
ADD_CONTEXT_AND_SOURCE_CARD
ADD_USER_LOCAL_FRICTION
CIRCULATION_DAMPING_PROPOSAL
MONETIZATION_DISCLOSURE_GATE
INDEPENDENT_HUMAN_REVIEW
CORRECTION_PROPAGATION_AND_REPAIR
AUTHORIZED_LEGAL_OR_IMMINENT_SAFETY_ESCALATION
```

The final four states are not automatic external enforcement permissions.

## 7. Five-receipt correction closure

A correction case SHALL remain open until the following are present:

```text
RESTORE_ACCESS_OR_OPPORTUNITY
CORRECT_ORIGINAL_RECORD
NOTIFY_DOWNSTREAM_RECIPIENTS
COMPENSATE_VERIFIED_LOSS
REVISE_OR_RETIRE_RULE_OR_MODEL
```

A deployment MAY mark compensation not applicable only through a reasoned and reviewable record; the reference implementation requires the receipt to record that determination.

## 8. Conformance statement

A conformance statement SHALL disclose:

- implementation name and version;
- claimed level;
- requirement-by-requirement status;
- unsupported requirements;
- third-party certification status;
- test and evaluation scope;
- production versus reference status.

## 9. Security considerations

A conforming deployment SHALL treat content, URLs, attachments, prompts, and agent artifacts as untrusted. It SHALL NOT place secrets in system prompts or rely on a prompt alone to enforce strict authorization. It SHOULD isolate parsers and task agents, constrain tools, and preserve immutable audit events.

## 10. Privacy considerations

Audience vulnerability, health, financial pressure, family conditions, and other sensitive context SHALL be minimized, purpose-limited, private by default, time-bounded, and excluded from public person-level records.

## 11. Standardization status

This document is an author-side pre-standard draft. It has not been adopted or certified by ISO, IEC, ITU, UNESCO, the European Union, W3C, C2PA, AT Protocol, NIST, or any other standards or regulatory body.
