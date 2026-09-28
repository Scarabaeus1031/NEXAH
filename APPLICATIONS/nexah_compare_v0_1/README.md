# NEXAH Compare v0.1 — Contract Package

Status: `WP5_MACHINE_CONDITION_COMPLETE / HOLD_FOR_INDEPENDENT_BASELINE_AND_BLINDED_ADJUDICATION / NO_UI`

This package defines the first machine-readable application contract and the
first bounded deterministic core for the Advisory Report Decision-Assurance
Comparator selected by Mission Control.

It contains:

- four JSON Schemas: Case, Analysis, Comparison and Return;
- a shared definition schema;
- stable-ID and canonicalization rules;
- an exact source-adoption ledger;
- one coherent positive fixture set;
- schema-negative and semantic-boundary fixtures;
- a local dependency-free contract checker.
- a Draft-2020-12 schema-bound comparison CLI;
- exact or explicitly declared-key claim alignment;
- deterministic I/L/A/U, calculation, residual, abstention and claim-ceiling
  generation;
- a canonical ComparisonRecord hash returned beside, not injected into, the
  frozen record.
- a strict local Case-package contract with evidence and output manifest;
- a faithful deterministic Markdown projection;
- a replay-verifiable run receipt;
- a separate hash-bound Human Return workflow.

This is an application layer. It does not modify or extend OLS 1.0, sealed THE
EYE profiles, the NEXAH Kernel or certified ORION. WP4 establishes a local,
replayable working package. WP5 adds one preregistered synthetic Family Office
machine condition in Science Lab: 5/5 seeded defects are surfaced and two runs
are byte-identical. The independent manual baseline and blinded adjudication
remain absent, so no incremental value, Human utility, product readiness or
decision authority is established.

## Record flow

```text
CaseRecord
  + 2–4 Human-confirmed AnalysisRecords
  + exact auto-alignment or explicit declared-key alignment
  -> deterministic comparison
  -> ComparisonRecord
  -> manifest + faithful Markdown + replay receipt
  -> separate Human ReturnRecord
```

## Local validation

```text
python3 scripts/validate_contract.py
```

The checker rejects duplicate keys and non-finite numbers, checks the frozen
schema surface, verifies positive fixture links and asserts the registered
negative controls.

## WP3 runtime

The runtime requires a Python environment containing the pinned ranges in
`requirements-runtime.txt`. The verified local interpreter is
`/opt/anaconda3/bin/python` with `jsonschema 4.23.0`.

```text
/opt/anaconda3/bin/python scripts/nexah_compare.py compare \
  --case fixtures/positive/case.json \
  --analysis fixtures/positive/analysis-a.json \
  --analysis fixtures/positive/analysis-b.json \
  --alignment runtime_fixtures/market-entry-alignment.json \
  --output comparison.json
```

When no alignment map is supplied, only byte-stable exact canonical claim
payload matches are aligned. An explicit declared key maps counterparts but
does not itself prove semantic equivalence. Non-identical prose without a
structured criterion therefore remains `UNAVAILABLE`.

Validation:

```text
/opt/anaconda3/bin/python scripts/validate_runtime.py
```

See `WP3_DETERMINISTIC_CORE.md` and `WP3_VALIDATION_REPORT.md` for the exact
runtime boundary.

## WP4 package workflow

Each package follows `CASE_PACKAGE_CONTRACT.md`. After assembling its declared
inputs and evidence, run and verify it with:

```text
/opt/anaconda3/bin/python scripts/nexah_compare.py run-package --package CASE_DIR
/opt/anaconda3/bin/python scripts/nexah_compare.py verify-package --package CASE_DIR
```

Create a separate Human Return only after reviewing the report:

```text
/opt/anaconda3/bin/python scripts/nexah_compare.py create-return \
  --package CASE_DIR \
  --action ABSTAIN \
  --actor ACTOR-OWNER-01 \
  --statement "Resolve the time-basis mismatch before deciding." \
  --returned-at 2026-09-28T10:00:00Z \
  --residual RES-MARKET-ENTRY-0002
```

`WP4_PACKAGE_REPORT_RETURN.md` and `WP4_VALIDATION_REPORT.md` define the exact
package scope and clean-run evidence. `WP5_TECHNICAL_BENCHMARK.md` records the
machine condition and points to the owning Science Lab package. Overall WP5
remains on HOLD for the independent baseline and blinded adjudication.
