# Memory Generalization V2

V2 preserves V1 unchanged and introduces a denser, split benchmark.

Canonical artifacts:

- **[VALIDATION_RECORD.md](VALIDATION_RECORD.md)** — frozen result and limits
- **[canonical_result.json](canonical_result.json)** — complete machine-readable run
- **[canonical_summary.md](canonical_summary.md)** — compact metric table

## Design

- 15 reference episodes: five per family
- families: Lorenz, Rössler, Kuramoto
- six validation queries
- six held-out test queries
- shared context domain for every item
- methods declared before scoring:
  - current v0.7 signature
  - instability-sequence profile
  - 50/50 hybrid
- method selection uses validation Top-1, then MRR, then predeclared method order
- held-out test data is not used for method selection

Metrics:

- Top-1 family accuracy
- Recall@3
- Mean Reciprocal Rank
- expected-family margin against the best alternative

## Scientific boundary

The objective remains synthetic system-family retrieval. It does not test
whether a retrieved Outcome is relevant to a decision. The sequence profile is
a validation-only feature derived from the public instability sequence because
v0.7 does not expose raw cluster labels through its current contract.

## Canonical result

The validation split selected `sequence_profile`. It achieved 6/6 Top-1 and
6/6 Recall@3 on the held-out test. The minimum held-out margin was only
`0.003172`, so this is evidence of correct family retrieval in this fixture,
not evidence of robust semantic memory.

## Visual summary

![Memory Generalization V2 validation overview](../../ARCHITECTURE/orientation_layer/visuals/memory-generalization-v2-validation-page-2.png)

The image is explanatory. The canonical JSON and validation record govern the
reported values and scientific interpretation.

## Run

```bash
python -m validation.memory_generalization_v2.run_validation \
  --recorded-at 2026-07-13T12:00:00+00:00
```
