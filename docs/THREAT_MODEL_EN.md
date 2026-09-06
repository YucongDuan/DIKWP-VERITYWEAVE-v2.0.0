# Threat Model — DIKWP VerityWeave v2.0.0

## Protected assets

- freedom to communicate criticism and adverse truth;
- user attention and informed choice;
- source and correction integrity;
- private contextual vulnerability data;
- platform decision accountability;
- agent policy, memory, and artifact lineage;
- appeal and restoration records.

## Threat actors and failure sources

The model does not assume all harm is malicious. Relevant sources include:

- commercial actors using urgency, shame, identity, or hidden conflicts;
- coordinated deception campaigns;
- good-faith creators compressing context;
- platforms optimizing engagement without measuring exit or informed choice;
- automated agents propagating unreviewed policies or artifacts;
- insiders modifying logs, evaluators, or appeal records;
- overconfident institutions suppressing criticism;
- users or reviewers misunderstanding a heuristic score as proof.

## Principal threats

1. sentiment-based censorship;
2. false intent attribution;
3. commercial manipulation disguised as education;
4. high-stakes advice without evidence or reversibility;
5. recommender and interface compulsion;
6. opaque de-amplification and shadow penalties;
7. missing or ineffective appeal;
8. downstream persistence after correction;
9. policy drift across agents and successors;
10. control-plane access by task agents;
11. secret cross-agent communication or memory;
12. false assurance from provenance metadata.

## Security assumptions

The reference implementation assumes the local host and Python runtime are not already compromised. It does not sandbox arbitrary third-party code or validate remote URLs.

## Mitigations

- no network client in the core;
- no shell execution in the core;
- loopback-only server;
- no platform enforcement connector;
- separate protected-expression logic;
- human gates for adverse platform action;
- append-only ledger;
- policy and artifact digest guidance;
- stop and successor controls;
- five-receipt correction closure;
- transparent limitations in every analysis.

## Residual risks

- lexicons and heuristics can be culturally biased;
- context fields can be inaccurate or abused;
- a host application may ignore human gates;
- a human reviewer may be biased or conflicted;
- hash chains do not prove original truth;
- an authorized recipient may misuse sensitive data;
- attackers can adapt wording to avoid markers;
- real-world impact may differ from modeled control potential.
