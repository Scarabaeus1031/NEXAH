# SR-1 G1 Frozen Baseline Identity

**Gate:** G1 — frozen baseline  
**Status:** passed  
**Recorded:** 2026-07-26T03:30:59+02:00

## Repository identity

| Field | Value |
|---|---|
| Repository | NEXAH |
| Git revision | `d3a19138b96aa07dfd623bdebb1003cb02cc60e8` |
| Git description before sidecar creation | `framework-v1.0.0-1-gd3a19138` |
| V1 manifest ID | `phase-v-ieee-geometry-v1` |
| Development case | `ieee9` |
| Evaluation case | `ieee14` |
| Evaluation role | `locked_evaluation` |
| Parameter retuning | `false` |
| Outcome status | `not_observed` |
| Episode update allowed | `false` |

The source worktree was clean before the G1 reference run.

## Frozen operators

1. `adjacent-displacement-v1`
2. `normalized-local-drift-v1`
3. `campaign-path-length-v1`
4. `direction-change-v1`
5. `discrete-curvature-v1`
6. `distance-to-last-converged-v1`

## Canonical G1 result

The unchanged canonical runner reported:

- all ten validation checks passed;
- IEEE-9: 19 declared, 17 converged, 2 failed at load scales 2.3 and 2.4;
- IEEE-14: 19 declared, 19 converged, 0 failed;
- IEEE-14 geometry: 18 available adjacent steps and 17 available centred
  turns;
- IEEE-14 sampled solver boundaries: 0;
- no fabricated failure values;
- no evaluation refit;
- outcome boundary preserved.

The disposable G1 output
`/private/tmp/nexah-sr1-g1-canonical-summary.json` had SHA-256
`bf9ff7f858345c553685ea382440332381d4621aef2c9792a27c3c79b1dd1ff9`,
identical to the committed V1 canonical summary.

## Reference commands

Run from the NEXAH repository root:

```bash
python validation/ieee_geometry_v1/run_validation.py \
  --out /private/tmp/nexah-sr1-g1-canonical-summary.json

python -m pytest tests/validation/test_ieee_geometry_v1.py \
  -q -p no:cacheprovider \
  --basetemp /private/tmp/nexah-sr1-g1-pytest
```

Observed test result: `2 passed in 23.25s`.

## Hash authority

Byte hashes for the frozen inputs, canonical products, runner, summary and test
are recorded in [`fixtures/expected_hashes.json`](fixtures/expected_hashes.json).
The manifest’s typed-payload SHA-256 remains
`ce2de3967ff44d35357b3f6d9d8a3a99d430ef666e6e7e34602d254762273008`;
the file-byte SHA-256 is recorded separately.

