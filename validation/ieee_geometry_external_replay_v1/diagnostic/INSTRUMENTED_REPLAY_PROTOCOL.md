# Instrumented evidence-retention replay protocol

Protocol ID: `sr1-g4-instrumented-evidence-retention-v1`  
Version: `1.0.0`  
Status: approved by explicit user authorisation before execution  
Scientific runs authorised: exactly one IEEE-14 diagnostic replay  
Retry authorised: no  
Official G4 classification: `G4_clean_replay_failed`  
Pre-analysis root-cause classification: `E — unresolved`

## Immutable bindings

- Source revision:
  `d3a19138b96aa07dfd623bdebb1003cb02cc60e8`
- Instrumentation:
  `diagnostic/instrumented_replay.py`
- Instrumentation SHA-256:
  `527ee8beaf5475d744b89b27bf1495851c4cfc94372a3745a6a6b51978316d3c`
- Observational verifier:
  `diagnostic/verify_observational_only.py`
- Verifier SHA-256:
  `442443eaa02bad0ec19b5a646e32f6e9dd7056a5a356ef194bc133b17e3b4d72`
- Frozen source hashes:
  `fixtures/expected_hashes.json`
- Preserved first-run evidence:
  `reports/g4_clean_replay/raw/`

Any byte change to this protocol or the instrument invalidates the approval
binding and stops execution.

## Purpose

The single execution exists only to retain the intermediate values omitted by
the original failed G4 run and locate the first divergence. It is not a retry
for a passing result, a new G4 classification, external validation, or
scientific claim.

## Pre-execution requirements

1. Verify every preserved first-run G4 evidence hash.
2. Verify all 15 frozen V1 hashes.
3. Verify the exact source revision and a clean replay checkout.
4. Record OS, architecture, Python executable bytes, full installed-package
   lock, recoverable wheel/build metadata, binary-extension hashes, NumPy
   configuration, BLAS/LAPACK, thread environment, pandapower settings, and
   numba availability.
5. Verify this protocol, its approval binding, the instrument SHA-256, and the
   static observational-only inspection.
6. Stop before the replay if any verification fails.

## Observational-only computation contract

The instrument shall:

- import and call the canonical
  `validation.ieee_geometry_v1.run_validation._fresh_evaluation_campaign`
  entrypoint exactly once;
- use the unchanged frozen manifest, IEEE-9 development frames, development
  standardisation, geometry functions, probes, and brief renderer;
- preserve the canonical scientific call order:
  fresh campaign → analysis → probes → brief → rendered brief;
- perform no direct solver call, parameter assignment, retry, rounding,
  tolerance comparison, sorting of scientific arrays, refit, case-role change,
  or canonical write;
- create evidence payloads and recursive comparisons only after all scientific
  objects have been computed;
- write outputs outside the source checkout.

The only pre-computation write is an execution ledger recording that attempt
one of one has begun. It is outside the source checkout and cannot affect
solver inputs or numerical objects.

## Retained evidence

The diagnostic output shall contain:

- complete fresh evaluation frames;
- all frame statuses, entity views, entity keys and ordered values;
- topology IDs, shapes and null placement;
- complete geometry payload and separately extracted projected frames, steps,
  turns, and solver boundaries;
- complete Orientation context, report, brief JSON and brief Markdown;
- claim-audit inputs and gate checks;
- raw numeric inventory with Python repr, binary64 hexadecimal encoding,
  `float.hex`, and ULP size;
- deterministic recursive diffs against committed frames, geometry,
  Orientation, and brief;
- console stdout/stderr, execution ledger, summary, and artifact hashes.

## Deterministic comparison

Artifact order:

1. frames;
2. geometry;
3. Orientation;
4. brief.

Within mappings, keys are traversed lexicographically. Lists are traversed in
ascending index order. The first difference is the first unequal leaf or
structural record under that traversal. Mapping key order is recorded
separately. Numeric differences include type, repr, raw binary64 bytes,
absolute difference, relative difference, and ULP distance.

No tolerance or rounding is applied.

## Stop conditions

Stop without replay if:

- binding, source revision, frozen hash, preserved evidence hash, clean
  checkout, or observational-only inspection fails;
- the instrument contains other solver or canonical-summary entrypoints;
- the exact environment record cannot be written;
- the output path already exists.

After attempt one begins, no retry is permitted even on failure.

## Prohibitions

No frozen V1, approved G2 protocol, preserved G4 evidence, operator, parameter,
case role, claim, serialization rule, or gate semantic may change. No
Comparator output, tolerance, new metric, combined score, external contact,
G5, G6, commit, publication, or public/scientific claim is authorised.

## Completion

The diagnostic package may update only the root-cause classification. It shall
not alter or supersede `G4_clean_replay_failed`.
