# From policy declarations to executable evidence

Source remediation: 7 September 2026. This is a revision of the 2.0.0 reference
implementation, not an independently certified new product release.

## What changed

The previous implementation returned several unconditional invariant booleans.
Some tests only checked those booleans. A constant can document an intention; it
cannot demonstrate that a result respects that intention.

The revised Python engine, interface audit, and agent-lineage audit attach a
`validation` receipt. Validators inspect the generated payload and do not trust
its preexisting `invariants` or `validation` flags. Runtime call sites withhold a
payload when a mandatory check fails. The standalone application applies the same
evidence-bound reporting principle and includes its own negative-case tests.

| Status | Meaning | What it does not mean |
| --- | --- | --- |
| `PASS` | A stated predicate was checked on this local result. | All deployments are safe or the input is true. |
| `FAIL` | The generated result violates a checked contract; it is withheld. | The subject of the analysis is a bad person. |
| `NOT_VERIFIED` | A policy, external condition, or outcome is outside observed evidence. | The requirement has been fulfilled. |

`validation.passed` summarizes mandatory local checks only. A report can have
`passed: true` and an external-enforcement `NOT_VERIFIED` entry. The scope is
explicitly `local_generated_output_only`.

## Important checks

- Validate actual intervention content against a bounded action catalog and inspect
  every action's scope, human gate, reversibility, and due-process prerequisites.
- Reject unknown or malformed action/output fields, rather than giving new actions
  implicit permission.
- Keep adverse plans inactive when required appeal/correction channels are absent.
- Test that changing the negative-affect signal alone does not increase restrictive
  scoring; this is a bounded check, not a universal social-bias theorem.
- Distinguish a required human-report channel from the input's claim that such a
  channel is available. Input claims are not independent proof of deployed controls.
- Preserve diagnosis, person-scoring, and external-action boundaries as checked
  output constraints plus explicit unverified real-world conditions.

## Reproduce from source

```bash
make test
make audit
make model-check
make test-browser
# All four, with nonzero exit on any failure:
make verify
```

Without Make, run the Python commands with `src` on `PYTHONPATH` and invoke
`node tests/test_browser_invariants.js`. The surrounding remediation bundle also
provides an operating-system-neutral `reproduce.py` launcher and JSON receipts.

Deliberately invalid fixtures must be rejected. Testing a validator only on the
payload it produced cannot establish that it detects violations. Keep both passing
and failing examples when extending the action catalog.

## Scope and remaining work

The source-pattern audit is not a full security audit. The finite-state checker
proves properties only within its explicitly modeled states and transitions. The
reference core has no enforcement connector: proposed platform actions, legal
reviews, monetary remedies, stop propagation into external agents, and successor
authorization still need real authorized integrations and evidence. No clinical,
legal, or consciousness claim follows from a green test run.

Previously distributed reports under `validation/` describe the earlier snapshot.
Fresh reproduction receipts identify commands, runtime versions, return codes,
and source hashes; do not substitute historical screenshots or badges for a rerun.
