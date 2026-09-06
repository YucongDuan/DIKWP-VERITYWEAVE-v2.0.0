# Security policy

VerityWeave is a research-alpha reference implementation. Report vulnerabilities privately to the repository owner before public disclosure when a credible exploit could expose sensitive data or enable unauthorized platform action.

The reference core deliberately contains no remote deletion, account sanction, payment, identity, or publication connector. The local HTTP server rejects non-loopback binds. The MCP server exposes analysis-only tools. Generated AT Protocol, C2PA, DSA, and PROV objects are unsigned reference mappings.

Do not run untrusted third-party analyzers, rule packs, or repository code with production credentials. Use process isolation, read-only inputs, strict resource limits, and independent review.
