# Memory Generalization — Validation Record

Validation ID: `memory-generalization-v1`  
Recorded run time: `2026-07-13T10:00:00+00:00`  
Status: reproducible synthetic retrieval benchmark

## Preregistered design

```text
Families: Lorenz, Rössler, Kuramoto
Reference episodes: one per family
Samples per trajectory: 2500
Shared context domain: synthetic-dynamical-system
v0.7: clusters=6, window=10, random_state=42
Queries: clean, noise 0.01, noise 0.05, parameter shift
Primary metric: Top-1 family accuracy
Separation: expected-family score minus best alternative
Chance baseline: 1/3
```

Family names were not placed in `Context.domain`; every episode and query used
the same domain. Similarity parameters were not changed after reading results.

## Result

| Condition | Correct | Top-1 accuracy | Mean margin | Minimum margin |
|---|---:|---:|---:|---:|
| Clean | 3/3 | 1.000000 | 0.121384 | 0.066389 |
| Noise 0.01 | 3/3 | 1.000000 | 0.110385 | 0.065990 |
| Noise 0.05 | 3/3 | 1.000000 | 0.110903 | 0.065013 |
| Parameter shift | 2/3 | 0.666667 | -0.023721 | -0.187173 |
| **Overall** | **11/12** | **0.916667** | **0.079738** | **-0.187173** |

The clean and noise conditions retrieve the expected family for all systems.
Parameter-shifted Lorenz and Rössler remain correctly ranked. Parameter-shifted
Kuramoto is confused with Lorenz:

```text
Lorenz similarity:   0.910793
Rössler similarity:  0.882724
Kuramoto similarity: 0.723620
```

This is not corrected after the benchmark. It demonstrates that the current
summary signature can lose family identity when Kuramoto coupling changes.

## Reproducibility

Two complete canonical runs produced byte-identical outputs:

| Artifact | SHA-256 |
|---|---|
| `canonical_result.json` | `63112fbc32e58b325c622546a33152632b47a782f4844f5f7a1581e6a382f8c9` |
| `validation_summary.md` | `630544a493640b8a21afdc8f3be4de15c1d199166bfe6a853d7e6d4d6ef2f38a` |

The full canonical query rankings are committed in
**[canonical_result.json](canonical_result.json)**.

## Interpretation

The heuristic demonstrates useful synthetic-family discrimination and
robustness to the two declared noise levels. It does not yet support claims of:

- semantic similarity
- calibrated retrieval confidence
- outcome relevance
- within-family episode selection
- real-world or cross-domain generality

The observed Kuramoto parameter-shift failure makes the next scientific task
clear: add multiple reference episodes per family and compare the current
summary signature against stronger sequence- or transition-aware retrieval
baselines without tuning on the held-out query.

