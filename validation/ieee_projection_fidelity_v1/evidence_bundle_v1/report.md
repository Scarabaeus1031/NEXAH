# NEXAH Compare — IEEE Projection Fidelity Evidence

- Status: `PASS`
- Decision: `IEEE_PROJECTION_FIDELITY_CONFIRMED`
- Claim ceiling: `BOUNDED_IEEE_REPRESENTATION_FIDELITY_AUDIT`
- Record type: `computation_result`
- Record ID: `computation:ieee-projection-fidelity:sha256:b816d68088cc8aab17475fe2a7dd69acb77bda795104180bc0e885863e3f23e7`
- Protocol: `ieee-projection-fidelity-v1`
- Development: `ieee9`
- Evaluation: `ieee14`
- Evaluation refit: `false`

## Held-out evaluation comparison

| Representation | Stored scalars | Pair-distance NRMSE | Path-length relative error | Turn-angle MAE (degrees) |
|---|---:|---:|---:|---:|
| `FULL8` | 8 | 0 | 0 | 0 |
| `Q_ONLY7` | 7 | 0.0123049609258 | 0.0113004112309 | 0.246817559634 |
| `Q_PLUS_R8` | 8 | 2.37512298525e-16 | 3.19846045407e-16 | 1.48457067044e-13 |
| `PCA7` | 7 | 0.00425637947472 | 0.0045428780152 | 0.259881130059 |

## Quotient–residual checks

- Q+R standardized reconstruction max error: `3.5527136788e-15`
- Q+R raw reconstruction max error: `5.68434188608e-14`
- Q+R pair-distance max error: `1.33226762955e-15`
- Q-only kernel-counterfactual max distance: `2.22044604925e-16`
- Q+R kernel-event detection rate: `1`

## What this establishes

Within the declared campaigns and tolerance, the quotient-only view hides the tested antisymmetric kernel direction, while the explicitly typed residual restores the full standardized coordinate state and the tested geometry.

`Q_PLUS_R8` is an eight-scalar coordinate transformation and exact reconstruction control. It is not a seven-dimensional compression result.

## Nonclaims

- no stability prediction or early warning
- no risk, causal, or control claim
- no physical AXIS08 identity
- no universal compression superiority
- Q_PLUS_R8 stores eight scalars and is not compression

## Numerical and evidence boundary

- Floating-point comparisons are bounded by the declared protocol tolerance.
- This computation result is not an independently observed outcome.

Inspection, interpretation, adoption, rejection, and continuation remain Human-owned.

This document is a faithful projection of `analysis.json` and `computation_result.json`. It is not an ORION Orientation Report, an independent observation, a Human decision, or a THE EYE A2 comparison result.
