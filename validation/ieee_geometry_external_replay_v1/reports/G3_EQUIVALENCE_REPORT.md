# G3 Independent Operator Equivalence Report

**Classification:** `G3_equivalence_passed`  
**Date:** 2026-07-26  
**Scope:** internal specification equivalence only

G3 does not establish external or independent scientific reproduction,
prediction, operational validity, or Comparator value.

## Preconditions

- Approved protocol ID:
  `sr1-ieee-geometry-comparator-analysis-v1`
- Approved version: `1.0.0`
- Approved SHA-256:
  `bd9d0fa2094b17333b18ec7621f33fd32271c2e759f2b01c9b27f76702ffe5ba`
- Candidate and approved protocol bytes: identical
- Approval digest verified before G3: yes
- Frozen V1 hashes matched before G3: 15/15
- Tolerance fixed before comparison:
  `1e-12 + 1e-10 * abs(canonical)`

## Independent implementation

The six manifest-declared operators were implemented in
`independent/operators_v1.py` using the Python standard library. The module does
not import the NEXAH package or production geometry implementation. It fits the
IEEE-9 population standardisation once and applies the same model unchanged to
IEEE-14.

Raw generated independent geometries were written only to:

- `/private/tmp/nexah-sr1-g3-ieee9-first/`
- `/private/tmp/nexah-sr1-g3-full/`

No canonical path was used as an output location.

## IEEE-9 — mandatory first case

- Role: `method_development`
- Campaign positions: 19
- Adjacent steps: 18
- Centred turns: 17
- Solver-failure boundaries: 2
- Overall result: `equivalent`
- Total discrepancies: 0
- First divergence: none

The failed positions at load scales 2.3 and 2.4 remain insufficient/null, the
sampled path terminates without gap bridging, and both failure boundaries retain
the original solver failure.

IEEE-14 was not loaded until this result passed.

## IEEE-14 — frozen target inspection after IEEE-9 pass

- Role: `locked_evaluation`
- Campaign positions: 19
- Adjacent steps: 18
- Centred turns: 17
- Solver-failure boundaries: 0
- Standardisation refit: no
- Tolerance change: no
- IEEE-14-specific branch: no
- Overall result: `equivalent`
- Total discrepancies: 0
- First divergence: none

This was comparison against the existing frozen Geometry artifact. No IEEE-14
Comparator output was generated, loaded, or displayed.

## Per-operator discrepancies

| Operator | IEEE-9 records | IEEE-9 discrepancies | IEEE-14 records | IEEE-14 discrepancies |
|---|---:|---:|---:|---:|
| adjacent displacement | 18 | 0 | 18 | 0 |
| normalized local drift | 18 | 0 | 18 | 0 |
| cumulative campaign path length | 18 | 0 | 18 | 0 |
| direction change | 17 | 0 | 17 | 0 |
| discrete curvature | 17 | 0 | 17 | 0 |
| sampled distance to last converged | 2 | 0 | 0 | 0 |

The discrepancy ledger explicitly contains empty arrays for both cases.

## Tests and preservation

- Sidecar tests: 6 passed
- Production-operator import prohibition: passed
- IEEE-9-first conditional gate: passed
- Status, insufficiency, failure, and gap handling: passed
- No canonical writes: passed
- No Comparator output: passed
- Frozen hashes after G3: 15/15 match
- Frozen V1 modified: no
- G4 begun: no
- Commit created: no

The first test invocation encountered a new-sidecar test discovery path error
before collection. It was preserved in `g3_test_record.json`; correcting the
test root did not alter scientific code, contract, tolerance, or results.

## Decision

`G3_equivalence_passed`

G4 may be considered only through separate approval. It has not begun.

