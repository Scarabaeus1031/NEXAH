# IEEE Projection Fidelity V1 — Validation Record

## Design

- source: committed IEEE Geometry V1 physical frames;
- development: IEEE-9 converged prefix, 17 frames;
- locked evaluation: IEEE-14, 19 frames;
- no solver execution;
- no IEEE-14 fitting or retuning;
- source-derived voltage-envelope pair `min(vm), max(vm)`;
- equal orthogonal quotient/residual transform after IEEE-9 standardization;
- classical PCA, random projection, coordinate-drop and maintained-view controls.

## Result

All primary source, reconstruction, geometry, kernel-blindness and no-refit
gates pass. Detailed values are retained in `canonical_result.json`.

PCA7 preserves held-out pair distances better than quotient-only. The positive
result is therefore the explicit residual certificate and exact reconstruction,
not a compression-superiority claim.

## Relationship to frozen Geometry V1

Geometry V1 remains unchanged. Its original probe correctly continues to state
that its protocol did not declare a cross-projection comparison. This package
is a later, prospective sidecar and must be cited separately.

## Prohibited interpretations

- no elapsed-time dynamics;
- no certified stability boundary;
- no early warning or risk estimate;
- no causal or control recommendation;
- no real-grid generalization;
- no physical AXIS08 identity;
- no new linear-algebra theorem.
