# IEEE Orientation Validation V1

Status: canonical V1 completed and frozen

Artifacts:

- **[VALIDATION_RECORD.md](VALIDATION_RECORD.md)** — result and interpretation
- **[canonical_result.json](canonical_result.json)** — machine-readable run
- **[canonical_summary.md](canonical_summary.md)** — compact metrics
- **[failure_cases.json](failure_cases.json)** — observed failures and boundaries

This validation closes Phase III steps D–F for the first coupled power-system
path. It tests structural-event alignment and spatial attribution. It does not
test dynamic stability prediction, causal control, or operational security.

## Frozen design

- reference case: IEEE 9-bus
- held-out case: IEEE 14-bus
- independent pandapower steady states
- load scales: 0.6 through 2.4 inclusive, step 0.1
- v0.7: four clusters, window four, random state 42
- physical reference thresholds:
  - minimum bus voltage below 0.95 pu
  - maximum line loading at or above 100 percent
- alignment tolerance: one load step, 0.1
- non-convergence is recorded but excluded from the rectangular campaign
- no parameter is changed after inspecting canonical results

## Metrics

- v0.7 event load scales
- nearest event distance for each observed physical threshold crossing
- threshold coverage within one load step
- bus attribution overlap: top `vm_pu` co-change versus minimum-voltage bus
- line attribution overlap: top `loading_percent` co-change versus
  maximum-loading line
- convergence boundary and excluded-scenario count

Attribution overlap is a salience check, not causal validation. A representation
event is a local-cluster label change, not a confirmed physical regime change.

## Canonical result

- threshold alignment: 2/3 physical references within one load step
- mean nearest-event distance: 0.166667
- entity attribution overlap: 11/12
- IEEE-9: both observed thresholds covered
- held-out IEEE-14: voltage crossing missed by 0.2 beyond tolerance
- two canonical runs: byte-identical

The held-out miss is retained. No parameter was retuned after scoring.

## Run

```bash
python -m validation.ieee_orientation_v1.run_validation \
  --recorded-at 2026-07-13T18:00:00+00:00
```
