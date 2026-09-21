# IEEE Projection Fidelity V1 — Canonical Summary

Status: **gate passed**

| Metric | Result |
|---|---:|
| Source reproduction maximum error | `0.0` |
| Q+R standardized reconstruction maximum error | `3.55e-15` |
| Q+R raw reconstruction maximum error | `5.68e-14` |
| Q+R pair-distance maximum error | `1.33e-15` |
| Q-only kernel-counterfactual maximum distance | `2.22e-16` |
| Q+R kernel detection | `1.0` |
| Evaluation refit | `false` |

## Comparative result

| Case | Representation | Distance NRMSE | Path error |
|---|---|---:|---:|
| IEEE-9 | Q-only | `4.70%` | `7.07%` |
| IEEE-9 | PCA7 | `1.40e-7` | `1.02e-4%` |
| IEEE-14 | Q-only | `1.23%` | `1.13%` |
| IEEE-14 | PCA7 | `0.426%` | `0.454%` |

Quotient plus residual is an exact and interpretable coordinate decomposition.
It stores eight scalars and is not compression. Quotient-only is not the best
seven-dimensional comparator in this test.
