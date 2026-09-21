# IEEE Projection Fidelity Sidecar V1

Status: `IMPLEMENTED / BOUNDED POSITIVE`

This sidecar closes one prospectively identified gap in IEEE Geometry V1: a
declared metric for comparing representations. It consumes the committed
IEEE-9 and IEEE-14 physical frames and does not modify or rerun the frozen
Geometry V1 protocol.

## Question

When the same source-derived eight-component audit state is represented by a
seven-coordinate quotient, what geometry is retained, what is lost, and does
an explicit residual restore the complete record?

## State and operator

The first six coordinates are existing system summaries. Coordinates seven
and eight are the minimum and maximum of the already committed bus-voltage
profile. Both have unit `pu` and form a declared voltage-envelope pair.

After IEEE-9 feature-wise population standardization:

```text
q = (z_min + z_max) / sqrt(2)
r = (z_min - z_max) / sqrt(2)
```

- `Q_ONLY7` stores the first six coordinates and `q`.
- `Q_PLUS_R8` additionally stores `r`.
- `Q_PLUS_R8` is an orthogonal coordinate change, not compression.

## Freeze

- IEEE-9: method development and all fitting;
- IEEE-14: locked evaluation without refit;
- input: committed `ieee_geometry_v1/*_frames.json` artifacts;
- random comparison seed: `8208`;
- primary tolerance: `1e-12`;
- failed frames: retained and never imputed or bridged.

The exact protocol is [`protocol.json`](protocol.json). The canonical result,
summary and reproducible runner live in
[`validation/ieee_projection_fidelity_v1`](../../../validation/ieee_projection_fidelity_v1/README.md).

## Result

All primary gates pass. Quotient plus residual reconstructs both campaigns and
preserves pair distances to numerical tolerance. Quotient-only IEEE-14 distance
NRMSE is `1.23%`; the frozen PCA7 baseline is better at `0.426%`.

The contribution is an explicit and interpretable loss certificate. It is not
a superiority result and does not establish stability prediction, early
warning, risk, causality, control, or physical AXIS08 identity.

## Relationship to IEEE Geometry V1

Geometry V1 remains frozen and continues to report cross-projection agreement
as unknown under its original protocol. This sidecar is a new, separately
declared analysis. A later Orientation protocol may cite the sidecar; it must
not rewrite the V1 report retrospectively.
