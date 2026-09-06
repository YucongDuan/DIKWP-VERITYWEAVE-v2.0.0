# Platform Interoperability — DIKWP VerityWeave v2.0.0

## Design principle

VerityWeave is a semantic-governance layer. It does not replace platform protocols, provenance standards, or legal reporting systems. It produces bounded reference mappings that a production integrator must sign, validate, and adapt.

## AT Protocol

The system can map a result to an AT Protocol-style label containing:

- source DID;
- subject URI and optional CID;
- label value;
- creation and expiry times;
- reason codes;
- a `reference_only` marker.

The label is unsigned in the reference implementation. A production labeler needs identity, signing, service discovery, revocation, and governance.

## C2PA

The C2PA reference assertion records:

- input digest;
- system and version;
- decision and reason codes;
- limitations;
- the explicit statement that provenance is not truth.

The reference core does not create a production C2PA manifest or trust-chain signature.

## W3C PROV

The system emits a minimal JSON-LD graph linking the input entity to the analysis activity and result. A production integration should add agents, organizations, source artifacts, policy versions, review events, and correction events.

## DSA-style statement of reasons

The reference mapping includes:

- content identifier;
- decision ground;
- reason codes;
- facts and circumstances;
- automated detection status;
- automated decision status;
- human-review requirement;
- appeal and expiry requirements.

It is a design aid, not a claim of legal compliance or a submission to a regulator.

## MCP

The package includes a stateless line-delimited JSON-RPC MCP profile with:

- `tools/list`;
- `tools/call`;
- `resources/list`;
- `resources/read`.

Available tools include semantic-flow analysis, interface audit, agent-lineage audit, and conformance reporting. The server has no external-action tool.

## Local API

The loopback-only API exposes:

```text
GET  /health
POST /analyze
POST /audit-interface
POST /audit-lineage
```

It rejects non-loopback binding in the reference implementation.

## Data portability

All primary records are plain JSON. Markdown reports and a self-contained HTML application are also included. A production deployment should preserve raw inputs, policy versions, human decisions, appeal records, and correction events under explicit retention rules.
