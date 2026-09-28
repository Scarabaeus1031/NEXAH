# WP3 Deterministic Core

Decision: `PASS / CORE_COMPLETE / WP4_READY_NOT_ACTIVE`

## Implemented flow

```text
CaseRecord + 2–4 AnalysisRecords
  -> duplicate-key and finite-JSON admission
  -> JSON Schema Draft 2020-12 validation
  -> case, evidence and confirmation link validation
  -> exact automatic or explicit declared-key alignment
  -> deterministic I/L/A/U classification
  -> formula, operand, result, unit and time checks
  -> typed residual and abstention evaluation
  -> frozen claim ceiling
  -> canonical ComparisonRecord + external SHA-256
```

The reference analysis makes `LOST` and `ADDED` directional and reproducible.
It is not treated as truth, quality or recommendation authority.

## Alignment boundary

Automatic alignment is exact only: the canonical claim payloads excluding
their IDs must match. An explicit alignment map may declare which claim IDs
are counterparts under one stable key. That declaration aligns records; it
does not establish semantic equivalence.

Consequently:

- non-identical FACT prose without structured comparison fields becomes
  `UNAVAILABLE / CRITERION_UNAVAILABLE`;
- differing assumptions become `UNAVAILABLE / ASSUMPTION_CONFLICT`;
- differing recommendation statements, conditions or admitted evidence remain
  a typed boundary rather than a recommendation ranking;
- every admitted claim must appear exactly once in the alignment.

## Calculation boundary

The formula evaluator permits only declared operand names, decimal constants,
parentheses and `+`, `-`, `*`, `/`. It uses Python `Decimal` with precision 50.
It does not execute functions, attributes, indexing, imports or arbitrary
Python. Result units and time bases must match exactly; no conversion table is
active. Unsupported or incompatible operations remain residuals or fail
closed.

## Schema engine

The runtime is bound to `jsonschema`'s `Draft202012Validator` plus
`referencing.Registry` and a format checker. Missing schema-engine support is a
hard `SCHEMA_ENGINE_UNAVAILABLE` failure, not a fallback to the narrower WP2
checker.

## Stable output

The output is one schema-valid canonical `ComparisonRecord`. Object keys are
sorted, arrays preserve deterministic engine order, UTF-8 is emitted directly
and exactly one terminal LF is written. The CLI returns the SHA-256 of those
exact bytes.

The frozen record schema contains no embedded self-hash field. WP3 therefore
does not mutate the contract. WP4 may bind the external digest into a receipt
and `ReturnRecord.comparison_sha256`. A self-hash field would require a
versioned schema amendment.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | valid deterministic ComparisonRecord written |
| `2` | JSON, schema, link or I/O rejection |
| `3` | alignment or reference rejection |
| `4` | required schema engine or supported calculation operation unavailable |

## Excluded scope

No LLM, semantic embedding, web search, PDF parser, document extraction,
database, network service, ORION call, UI, Markdown report, receipt, Human
Return workflow, benchmark, product-utility claim, publication or deployment
is part of WP3.
