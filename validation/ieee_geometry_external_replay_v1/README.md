# IEEE Geometry External-Replay Readiness Package

Status: **G4 clean replay failed; stopped before G5**

This directory is the bounded SR-1 validation sidecar for the frozen
IEEE Geometry V1 line. Its purpose is to make that line independently
reproducible, falsifiable, and comparable with conventional Power Systems
indicators without changing the V1 method or claims.

## Authority boundary

The sidecar consumes frozen V1 sources. It does not own or modify:

- `APPLICATIONS/power_systems/ieee_geometry_v1/case_manifest.json`;
- V1 development or evaluation frames, geometry, Orientation products, briefs,
  figures, supported claims, prohibited claims, parameters, normalisation,
  operators, case roles, or failure policies;
- `validation/ieee_geometry_v1/`;
- existing V1 tests.

The immutable baseline is identified in
[`BASELINE_IDENTITY.md`](BASELINE_IDENTITY.md). Source/generated ownership and
change rules are in
[`OWNERSHIP_AND_CHANGE_BOUNDARY.md`](OWNERSHIP_AND_CHANGE_BOUNDARY.md).

## Gate status

| Gate | Status | Evidence |
|---|---|---|
| G0 — plan approval | passed | approved SR-1 plan, 2026-07-26 |
| G1 — frozen baseline | **passed** | baseline identity, hashes, environment, canonical gate and V1 test |
| G2 — comparator definition | **passed** | immutable approved protocol and approval record |
| G3 — independent equivalence | **passed** | six independent operators; IEEE-9-first and conditional IEEE-14 equivalence; zero discrepancies |
| G4 — clean replay | **failed** | clean checkout completed; fresh canonical IEEE-14 replay failed three canonical replay checks |
| G5 — claim-boundary audit | not started | — |
| G6 — review package | not started | — |

Implementation stops here after the G4 review package. G5 and G6 have not
begun. The failure is preserved without protocol repair or reinterpretation.

## G2 controls already approved

When G2 is authorised:

1. the complete comparator and analysis protocol must be approved and hashed
   with SHA-256 before new IEEE-14 comparator output is generated or inspected;
2. IEEE-9 comparator development and IEEE-14 comparator evaluation must use
   technically separate commands;
3. the development command must not generate, load, or display IEEE-14
   comparator output;
4. the evaluation command must refuse to run unless the approved protocol bytes
   match the recorded G2 SHA-256 digest.

No Comparator result generator or new IEEE-14 Comparator output is present.
G3 inspected only the existing frozen IEEE-14 Geometry artifact after IEEE-9
equivalence passed.

## Current records

- [`BASELINE_IDENTITY.md`](BASELINE_IDENTITY.md)
- [`OWNERSHIP_AND_CHANGE_BOUNDARY.md`](OWNERSHIP_AND_CHANGE_BOUNDARY.md)
- [`fixtures/expected_hashes.json`](fixtures/expected_hashes.json)
- [`environment/environment.json`](environment/environment.json)
- [`reports/g1_baseline_verification.json`](reports/g1_baseline_verification.json)
- [`CHANGE_LEDGER.md`](CHANGE_LEDGER.md)
- [`protocol/COMPARATOR_PROTOCOL.md`](protocol/COMPARATOR_PROTOCOL.md)
- [`protocol/ANALYSIS_PROTOCOL.md`](protocol/ANALYSIS_PROTOCOL.md)
- [`protocol/TIER1_FEASIBILITY.md`](protocol/TIER1_FEASIBILITY.md)
- [`protocol/G2_HASH_AND_APPROVAL_PROTOCOL.md`](protocol/G2_HASH_AND_APPROVAL_PROTOCOL.md)
- [`protocol/g2_protocol_candidate.json`](protocol/g2_protocol_candidate.json)
- [`protocol/g2_protocol_candidate.sha256`](protocol/g2_protocol_candidate.sha256)
- [`protocol/g2_protocol_approved.json`](protocol/g2_protocol_approved.json)
- [`protocol/g2_approval_record.json`](protocol/g2_approval_record.json)
- [`fixtures/ieee9_manual_comparator_fixtures.json`](fixtures/ieee9_manual_comparator_fixtures.json)
- [`reports/g2_protocol_review.md`](reports/g2_protocol_review.md)
- [`independent/G3_EQUIVALENCE_CONTRACT.md`](independent/G3_EQUIVALENCE_CONTRACT.md)
- [`independent/operators_v1.py`](independent/operators_v1.py)
- [`independent/run_g3_equivalence.py`](independent/run_g3_equivalence.py)
- [`reports/G3_EQUIVALENCE_REPORT.md`](reports/G3_EQUIVALENCE_REPORT.md)
- [`reports/g3_equivalence_result.json`](reports/g3_equivalence_result.json)
- [`reports/g3_discrepancy_ledger.json`](reports/g3_discrepancy_ledger.json)
- [`reports/g3_implementation_source_record.json`](reports/g3_implementation_source_record.json)
- [`reports/g3_test_record.json`](reports/g3_test_record.json)
- [`reports/g3_frozen_hash_verification.json`](reports/g3_frozen_hash_verification.json)
- [`G4_ENTRY_AND_REPLAY_CONTRACT.md`](G4_ENTRY_AND_REPLAY_CONTRACT.md)
- [`REPLAY_PROTOCOL.md`](REPLAY_PROTOCOL.md)
- [`replay_development.py`](replay_development.py)
- [`replay_evaluation.py`](replay_evaluation.py)
- [`run_external_replay.py`](run_external_replay.py)
- [`reports/g4_clean_replay/G4_CLEAN_REPLAY_REVIEW.md`](reports/g4_clean_replay/G4_CLEAN_REPLAY_REVIEW.md)
- [`reports/g4_clean_replay/g4_review_classification.json`](reports/g4_clean_replay/g4_review_classification.json)
- [`reports/g4_clean_replay/G4_ROOT_CAUSE_ANALYSIS.md`](reports/g4_clean_replay/G4_ROOT_CAUSE_ANALYSIS.md)
- [`reports/g4_clean_replay/g4_divergence_inventory.json`](reports/g4_clean_replay/g4_divergence_inventory.json)
