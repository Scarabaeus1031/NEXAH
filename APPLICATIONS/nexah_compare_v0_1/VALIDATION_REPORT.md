# WP2 Contract Validation Report

Date: `2026-09-27`

Command:

```text
python3 APPLICATIONS/nexah_compare_v0_1/scripts/validate_contract.py
```

Observed result:

```json
{"canonical_profile":"NEXAH_COMPARE_CANONICAL_JSON_0_1","negative_controls":4,"pinned_sources":10,"positive_records":5,"schemas":5,"status":"VALID"}
```

## Checks performed

- all ten pinned source files exist and match their frozen SHA-256;
- exactly five declared schemas exist and use JSON Schema Draft 2020-12;
- every local schema reference resolves;
- every schema and fixture is valid UTF-8 JSON;
- duplicate keys and non-finite values are rejected by the checker;
- positive Case, two Analyses, Comparison and Return link coherently;
- admitted evidence paths are relative and traversal-safe;
- evidence and claim references resolve;
- analysis count is between two and four and the reference is included;
- one claim cannot enter multiple relation groups;
- canonical serialization is byte-identical across two in-memory runs;
- Return binds the exact canonical ComparisonRecord SHA-256;
- all four registered negative controls fail with their expected reason code.

## Negative controls

| Control | Expected result |
|---|---|
| unsupported `TRUTH` claim type | `INVALID_CLAIM_KIND` |
| `../` evidence path traversal | `UNSAFE_EVIDENCE_PATH` |
| model-assisted record not Human-confirmed | `NOT_HUMAN_CONFIRMED` |
| comparison with only one analysis | `ANALYSIS_COUNT_OUT_OF_RANGE` |

## Validation boundary

The dependency-free checker validates this frozen WP2 package and its linked
fixtures. It is not a complete general-purpose JSON Schema implementation and
not the WP3 comparator. WP3 must bind a conforming executable schema engine and
add mutation, self-hash, unit, time, formula and receipt tests before any
technical benchmark.
