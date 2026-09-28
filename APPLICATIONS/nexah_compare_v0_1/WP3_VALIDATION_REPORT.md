# WP3 Runtime Validation Report

Date: `2026-09-28`

Status: `VALID / BOUNDED_MACHINE_EXISTENCE_ONLY`

## Environment

- Python: `/opt/anaconda3/bin/python`
- schema engine: `jsonschema 4.23.0`
- dialect: JSON Schema Draft 2020-12
- test runner: Python standard-library `unittest`

## Commands

```text
/opt/anaconda3/bin/python scripts/validate_runtime.py
/opt/anaconda3/bin/python scripts/nexah_compare.py compare \
  --case fixtures/positive/case.json \
  --analysis fixtures/positive/analysis-a.json \
  --analysis fixtures/positive/analysis-b.json \
  --alignment runtime_fixtures/market-entry-alignment.json \
  --output /tmp/nexah-compare-wp3-output.json
```

Observed runtime suite:

```json
{"profile":"NC01-ADVISORY-0.1","runtime_tests":7,"schema_engine":"jsonschema Draft202012Validator","status":"VALID"}
```

Observed clean CLI result:

```json
{"comparison_id":"CMP-MARKET-ENTRY-ADVISORY-01","comparison_sha256":"0ac593a071b342690ce938bee11143d2b011784d9dd2f76995eeeddaf8d503db","status":"VALID"}
```

## Covered controls

1. Draft-2020-12 validation with local reference registry and date-time format checking.
2. Deterministic output and hash across replay.
3. Input-order-independent exact automatic alignment.
4. Complete exactly-once declared-key alignment.
5. Fail-closed rejection when `EXACT` is declared for non-identical payloads.
6. Decimal formula allowlist and arbitrary-code rejection.
7. Rejection of a non-confirmed analysis.
8. CLI canonical-file and returned-hash parity.
9. WP2 contract regression remains `VALID`.

The synthetic fixture exposes one annual/monthly mismatch as
`TIME_BASIS_MISMATCH`, an outside-reference assumption as `ADDED`, differing
recommendation evidence as `EVIDENCE_ASYMMETRY`, and non-identical FACT prose
without structured equivalence data as `CRITERION_UNAVAILABLE`. No silent unit
conversion or semantic inference occurs.

## Claim boundary

This validates local deterministic machine existence against synthetic WP2
fixtures. It does not validate defect-detection performance, correctness,
Human usefulness, product readiness or the Gate-1 incremental-value route.
Those require later separately authorized packages and the preregistered
benchmark.
