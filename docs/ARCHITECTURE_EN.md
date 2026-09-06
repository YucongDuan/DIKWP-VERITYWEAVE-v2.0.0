# Architecture — DIKWP VerityWeave v2.0.0

## Components

```text
Input adapters
  ├─ standalone browser application
  ├─ JSON CLI
  ├─ loopback API
  ├─ browser extension
  └─ stateless MCP tools
        ↓
Case normalization
        ↓
Semantic signal extraction
        ↓
Eight-world interpretation set
        ↓
Semantic-flow graph
        ↓
Repair + positive-commons analysis
        ↓
Proportional intervention planner
        ↓
Human decision boundary
        ↓
Appeal + five-receipt correction
        ↓
Responsibility and agent-lineage ledger
        ↓
Reference protocol exports
```

## Trust boundaries

### Untrusted zone

- user-entered content;
- web selections;
- URLs and metadata;
- imported rule packs;
- model and agent outputs;
- third-party provenance assertions.

### Reference-core zone

- normalized case objects;
- transparent heuristic calculations;
- deterministic intervention proposals;
- local report generation;
- append-only records.

### Human-authority zone

- platform visibility changes;
- paid-amplification pauses;
- identity disclosure;
- legal or safety escalation;
- compensation and restoration decisions;
- policy approval and retirement.

### External systems

The reference core has no direct connector for deletion, ranking, advertising, payments, legal processes, or identity disclosure. Production connectors must be separately authorized and audited.

## Data flow

The default standalone application processes data in browser memory. Local saving occurs only when the user selects it. The Python CLI reads and writes user-specified local files. The local API binds to loopback only.

## Determinism

The rule-based reference core is deterministic for a normalized input except for timestamps and generated appeal identifiers. Input and event digests enable reproduction and comparison.

## Extensibility

Language and domain packs should extend:

- marker dictionaries;
- context-repair templates;
- protected-expression test sets;
- high-stakes review rules;
- calibration documentation.

Extensions must not modify protected invariants such as zero external authority, negative-affect neutrality, or the prohibition on person-level moral scoring.
