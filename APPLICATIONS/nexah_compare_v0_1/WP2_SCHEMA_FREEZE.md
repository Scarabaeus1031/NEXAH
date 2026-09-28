# WP2 Schema Freeze

Decision: `PASS / CONTRACT_FROZEN / WP3_READY_NOT_ACTIVE`

## Frozen records

| Record | Responsibility |
|---|---|
| `CaseRecord` | decision question, options, period, constraints, privacy class, admitted evidence and Human confirmation |
| `AnalysisRecord` | source plus explicitly typed facts, assumptions, calculations and recommendations |
| `ComparisonRecord` | reference-relative multirecord I/L/A/U, calculation checks, residuals, abstentions and claim ceiling |
| `ReturnRecord` | Human confirm, amend, abstain or STOP bound to one ComparisonRecord hash |

`common.schema.json` owns only shared leaf definitions: stable IDs, SHA-256,
safe relative paths, decimal strings, periods, confirmation, evidence and
quantities.

## Source decision

The sealed predecessors are pinned, not modified and not imported as a hidden
runtime dependency. WP3 may implement provenance-preserving mechanics under
the new profile while citing `SOURCE_ADOPTION_LEDGER.csv`.

- OLS remains semantic authority.
- THE EYE Gate-1/A1/A2 remains sealed predecessor authority.
- A4 supplies an adapter pattern, not an Advisory mapping.
- Orientation Layer supplies selected field patterns without an automatic OLS
  conformance claim.
- NRRC and CRIC supply bounded record and replay patterns, not wholesale
  shared-contract adoption.
- ORION is not a WP2 dependency.

## Frozen semantic choices

1. Only Human-confirmed structured JSON enters the deterministic core.
2. Claims are exactly `FACT`, `ASSUMPTION`, `CALCULATION` or
   `RECOMMENDATION`.
3. One analysis is a reproducibility reference, not a truth or quality owner.
4. Every compared claim appears in at most one relation group.
5. Multirecord classes are `INVARIANT`, `LOST`, `ADDED` or `UNAVAILABLE`.
6. Decimal quantities are strings and retain unit system and time basis.
7. Unit, time, evidence, formula or criterion incompatibility remains a typed
   residual and may require abstention or STOP.
8. Evidence paths are Case-root relative, hash-bound and traversal-safe.
9. Comparison output carries the frozen no-truth/no-advice claim ceiling.
10. Human Return is separate from the machine comparison result.

## Deferred to WP3

- executable JSON Schema engine integration;
- canonical self-hash population and verification;
- deterministic alignment and comparison algorithms;
- formula evaluation and unit-conversion allowlist;
- CLI, exit codes, receipts and Markdown projection;
- benchmark execution.

No UI, arbitrary document ingestion, model adapter, ORION call, network
service or external action is authorized.
