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

## Bound computation evidence bundle

The Core can export the analysis as a closed four-file bundle:

- `analysis.json`: exact canonical sidecar analysis;
- `computation_result.json`: existing `ComputationResultRecord` binding;
- `report.md`: faithful Human-readable projection;
- `manifest.json`: file allowlist, byte counts, SHA-256 checksums, claim
  ceiling and Human-authority boundary.

Export requires an explicit timezone-aware computation timestamp and refuses
to overwrite an existing directory:

```bash
python -m nexah.cli export-ieee-projection-fidelity-evidence \
  validation/ieee_projection_fidelity_v1/canonical_result.json \
  --computed-at 2026-09-21T12:00:00+00:00 \
  --out-dir /tmp/nexah-ieee-projection-evidence
```

Verify every byte and the record-to-analysis cross-reference:

```bash
python -m nexah.cli verify-ieee-projection-fidelity-evidence \
  /tmp/nexah-ieee-projection-evidence
```

The bundle is classified `COMPUTATION_RESULT_ONLY`. It is not an independent
observation, an ORION Orientation Report, a THE EYE A2 comparison result or a
Human decision. A NEXAHEDRON Compare view remains separately governance-gated;
the bundle does not silently activate that deferred product surface.

The exporter preserves the canonical result bytes exactly. It does not rerun
SVD or QR during packaging; this avoids giving platform-level floating-point
variation a new artifact identity. Numerical reproduction remains the job of
the separate canonical validation runner.

The committed reference export is
[`validation/ieee_projection_fidelity_v1/evidence_bundle_v1`](../../../validation/ieee_projection_fidelity_v1/evidence_bundle_v1/manifest.json).
It was sealed with the explicit packaging timestamp
`2026-09-21T21:32:57+00:00`; using that timestamp and the command above
reproduces its `computation_result.json` byte for byte.
