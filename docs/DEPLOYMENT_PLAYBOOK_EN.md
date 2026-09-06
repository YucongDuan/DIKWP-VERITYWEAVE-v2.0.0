# Deployment Playbook — DIKWP VerityWeave v2.0.0

## Objective

Deploy VerityWeave as a context-repair and semantic-resilience layer, not as an autonomous censorship engine.

## Phase 0 — Institutional constitution

Before processing real users:

- define prohibited uses;
- identify the legal and policy authority for each possible action;
- separate detection, adjudication, appeal, and audit roles;
- define protected-expression categories;
- publish reason codes;
- define retention and deletion rules;
- define what counts as verified fabrication or verified harm;
- establish an independent escalation and correction channel.

**Exit criterion:** signed governance constitution and named role owners.

## Phase 1 — Offline shadow evaluation

Use historical, synthetic, or consented data. Do not affect live ranking, monetization, or visibility.

Required evaluation sets:

- criticism and whistleblowing;
- distress and grief;
- satire and fiction;
- high-integrity warnings;
- commercial overclaims;
- high-stakes health and finance claims;
- parenting and relationship advice;
- multilingual and dialectal samples;
- content from low-power groups;
- adversarial self-sealing and authority-laundering patterns.

**Exit criterion:** published false-positive and false-negative analysis, including protected-expression harms.

## Phase 2 — User-local pilot

Enable only reversible local controls:

- context and source cards;
- read-before-forwarding friction;
- action-risk checklists;
- autoplay and notification controls;
- chronological or non-personalized views;
- local session boundaries.

**Exit criterion:** evidence that users can understand, override, and benefit from the controls without losing access to protected expression.

## Phase 3 — Creator repair pilot

Offer voluntary tools for:

- source and conflict disclosure;
- uncertainty and scope statements;
- counterevidence;
- refund and failure-case disclosure;
- context-preserving rewrites;
- corrections linked to the original item.

**Exit criterion:** measurable correction uptake and no retaliation against creators who acknowledge errors.

## Phase 4 — Human-reviewed circulation proposals

Allow the engine to produce, but not execute, time-bounded circulation or monetization proposals.

Every proposal must contain:

- item identifier;
- evidence basis;
- reason codes;
- protected-expression check;
- less restrictive alternatives;
- proposed expiry;
- human decision;
- appeal path;
- restoration plan.

**Exit criterion:** independent audit of consistency, protected-expression errors, and appeal outcomes.

## Phase 5 — Limited production integration

Connect only actions explicitly authorized by the governing institution. Use signed policy bundles, immutable decision receipts, and downstream correction propagation.

**Exit criterion:** external security review, data-protection review, human-rights review, and real-world evaluation.

## Operational architecture

```text
content event
→ isolated parser
→ signal extraction
→ plural-world analysis
→ repair and commons analysis
→ policy proposal
→ named human decision
→ user/creator notice
→ time-bounded action
→ appeal
→ restoration/correction
→ public aggregate audit
```

## Security controls

- run untrusted parsers in an isolated environment;
- do not pass secrets to content-analysis agents;
- disable outbound network access by default;
- bind policies and prompts to digests;
- log model, prompt, policy, and artifact versions;
- test stop propagation across agents, queues, caches, and successors;
- prevent task agents from modifying evaluator, identity, logging, or policy control planes;
- rotate credentials after lineage incidents;
- maintain a rewarded human-report channel.

## Metrics

Do not optimize only for removed items. Measure:

- reduction in harmful forwarding or high-risk action;
- increase in source checking;
- correction visibility;
- protected-expression false positives;
- appeal reversal rate;
- restoration latency;
- user understanding and control;
- time spent versus successful exit;
- reduction in uncompensated creator or user burden;
- agent-lineage integrity.

## Ninety-day falsification gates

A pilot should be paused or redesigned if:

- protected criticism is disproportionately restricted;
- reason codes cannot explain human decisions;
- appeals are nominal but do not restore downstream records;
- creators receive secret or permanent penalties;
- vulnerable-audience data is repurposed for employment, credit, insurance, or policing;
- automated proposals become de facto decisions;
- the platform's engagement objective remains unchanged while only labels are added;
- shared agent artifacts cannot be traced or revoked.
