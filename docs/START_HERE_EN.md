# Start Here — DIKWP VerityWeave Semantic Resilience Grid OS v2.0.0

## What this system does

VerityWeave helps people, communities, platforms, researchers, and bounded software agents reduce manipulation and harmful circulation without treating sadness, criticism, whistleblowing, satire, or bad news as inherently harmful.

It analyzes a **semantic flow**, not a person's character. A semantic flow includes:

- the content;
- its sources and counterevidence;
- omitted context;
- commercial or status incentives;
- the audience and temporary vulnerability;
- interface and recommender amplification;
- the action the content invites;
- observed outcomes;
- appeal, correction, and restoration paths.

## Fastest path

### Standalone application

Open:

```text
DIKWP_VERITYWEAVE_SEMANTIC_RESILIENCE_GRID_OS_v2.0.0.html
```

No installation or network connection is required.

### Python

```bash
python -m pip install -e .
verityweave demo --output .verityweave-demo --reset
```

Analyze the parenting sales-funnel example:

```bash
verityweave analyze examples/parenting_sales_funnel.json \
  --output .verityweave-parenting \
  --ledger .verityweave-parenting/responsibility-ledger.jsonl
```

Audit an interface:

```bash
verityweave audit-interface examples/doomscroll_interface.json
```

Audit an agent lineage:

```bash
verityweave audit-lineage examples/agent_lineage_risk.json
```

Start the local API:

```bash
verityweave serve --host 127.0.0.1 --port 8765
```

Start the stateless MCP server:

```bash
verityweave mcp
```

## Read the output correctly

A VerityWeave decision is a **governance recommendation**, not a factual, clinical, moral, or legal verdict.

The system never claims that text patterns prove intent. It preserves at least eight competing interpretations, including good-faith compression, commercial manipulation, protected adverse truth, satire or expressive speech, and insufficient evidence.

The most important output fields are:

- `decision`: the current proportional governance recommendation;
- `semantic_control_potential`: the modeled potential for the flow to control attention, interpretation, or consequential action;
- `signals`: fifteen independent dimensions;
- `worlds`: competing interpretations and falsifiers;
- `repair_card`: a context-preserving rewrite and reality test;
- `interventions`: automatic user-local actions versus human-gated platform proposals;
- `commons_support`: whether high-integrity public-value content may merit support;
- `invariants`: runtime safety and rights checks;
- `limitations`: what the analysis does not establish.

## Runtime boundaries

The reference core has:

```text
automatic content-removal authority = 0
automatic monetary-penalty authority = 0
automatic legal-determination authority = 0
automatic external-action authority = 0
```

User-local reversible controls may run automatically. Examples include adding a context card, pausing before forwarding, disabling autoplay, or hiding public rankings. Platform-level restrictions remain proposals requiring named human review, reasons, expiry, appeal, correction, and restoration.

## Production deployment checklist

Before connecting VerityWeave to a real platform:

1. define the exact content and behavior scope;
2. conduct a human-rights and data-protection impact assessment;
3. build a multilingual, domain-specific calibration set;
4. include protected criticism, whistleblowing, satire, and distress in false-positive tests;
5. separate detection, adjudication, funding, appeals, and audit authority;
6. publish reason codes and time limits;
7. create an independent correction and restoration process;
8. isolate untrusted content processing;
9. audit shared agent memory, policy artifacts, successors, and stop propagation;
10. run a limited pilot with published failure criteria.

## Status

```text
RESEARCH_ALPHA_REFERENCE_IMPLEMENTATION
```

It is suitable for research, local decision support, controlled pilots, protocol development, and human-reviewed platform integration. It is not a universal truth engine, addiction diagnosis, intent detector, legal decision maker, or certified moderation service.
