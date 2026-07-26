# G3 Independent Operator Equivalence Contract

Status: **frozen before independent result comparison**

Frozen: 2026-07-26

## Purpose

Determine whether the six IEEE Geometry V1 operators can be implemented from
`case_manifest.json` and the committed physical-frame/public-artifact contract
without importing or copying the production geometry implementation.

This is an internal specification-equivalence test. It is not external or
independent scientific reproduction and it does not evaluate Comparator output.

## Inputs and ordering

- manifest:
  `APPLICATIONS/power_systems/ieee_geometry_v1/case_manifest.json`;
- IEEE-9 physical frames:
  `APPLICATIONS/power_systems/ieee_geometry_v1/development_frames.json`;
- IEEE-9 frozen target:
  `APPLICATIONS/power_systems/ieee_geometry_v1/development_geometry.json`;
- IEEE-14 physical frames:
  `APPLICATIONS/power_systems/ieee_geometry_v1/evaluation_frames.json`;
- IEEE-14 frozen target:
  `APPLICATIONS/power_systems/ieee_geometry_v1/evaluation_geometry.json`.

IEEE-9 is generated and compared first. IEEE-14 inputs and target may be loaded
only after IEEE-9 passes this contract. Campaign order, frame IDs, campaign
indices, load scales, case IDs, and case roles are preserved exactly.

## Projection contract

Use only the manifest-declared
`system-summary-standardized-v1` input names and each committed frame's
`system_features`.

Fit arithmetic means and population standard deviations on all and only
converged IEEE-9 feature rows. Apply that same IEEE-9 model unchanged to
IEEE-14. Do not refit, retune, or add a case-specific branch.

A failed frame has projected status `insufficient`, `values: null`, and reason
`failed frame contains no fabricated physical feature vector`. A missing,
misordered, non-finite, or zero-variance projection input is an insufficiency
and must not be repaired.

## Operator and gap contract

1. `adjacent-displacement-v1`: Euclidean norm of adjacent projected-vector
   difference.
2. `normalized-local-drift-v1`: displacement divided by the positive adjacent
   load-scale difference.
3. `campaign-path-length-v1`: cumulative adjacent displacement over the
   contiguous available prefix; terminate at the first unavailable point and
   never restart or bridge.
4. `direction-change-v1`: clipped arccosine of the normalized dot product of
   the two adjacent displacement vectors around the centre point.
5. `discrete-curvature-v1`: direction change divided by half the sum of the two
   adjacent displacement norms.
6. `distance-to-last-converged-v1`: for every sampled failed frame after at
   least one converged frame, failed load scale minus the last converged load
   scale; no temporal interpretation.

Unavailable step/turn values are JSON `null`. Failure text is preserved in
solver-boundary records. A failed position is never bridged.

## Exact fields compared

### Standardisation model

- manifest/projection/fit campaign/fit case identifiers;
- feature names;
- means and population standard deviations;
- status, zero-variance features, and reason.

### Projected frames — all 19 positions

- frame ID, campaign index, load scale;
- status, values, and reason.

### Adjacent steps — all 18 positions

- source/target frame IDs and indices;
- source/target load scales and delta load scale;
- status and reason;
- delta vector;
- displacement;
- normalized local drift;
- cumulative path length;
- parameter semantics.

### Centred turns — all 17 positions

- previous/centre/next frame IDs;
- centre index;
- status and reason;
- direction change radians;
- discrete curvature.

### Solver boundaries and analysis summary

- failed frame/index/load scale;
- last-converged frame/load scale;
- status, distance, preserved solver failure, reason, and boundary type;
- contiguous-converged frame IDs;
- total path length;
- terminal frame ID;
- ordered operator IDs.

Provenance timestamps, generated record IDs, and uncertainty wrappers are not
operator-equivalence fields and are excluded.

## Status and null equivalence

Statuses and strings compare exactly. Integers and booleans compare exactly.
`null` equals only `null`. A null/non-null difference is a discrepancy.
Sequences must have equal length and order. Numeric comparison is permitted
only when both values are finite numbers.

## Frozen numerical tolerance

For every numeric field:

`abs(independent - canonical) <= 1e-12 + 1e-10 * abs(canonical)`

This reuses the G2 artifact tolerance because G3 recomputes deterministic
descriptive formulas from the same committed numeric inputs in the same
declared environment. It is strict enough to admit only ordinary floating-point
operation-order differences, not a changed operator, model, case role, or
policy.

The tolerance may not be changed after any comparison result is inspected. If
it proves inappropriate, G3 stops for review; the result is not rerun under a
weaker rule.

## First divergence and classification

The first divergence is the earliest in:

1. standardisation model;
2. projected campaign position;
3. adjacent step;
4. centred turn;
5. solver boundary;
6. analysis summary.

It records path, independent value, canonical value, relevant physical/projected
inputs, and manifest formula. All later discrepancies remain in the machine
ledger.

An unexplained material IEEE-9 mismatch is
`specification_ambiguity` and stops before IEEE-14. Any mismatch is preserved;
V1 is never patched and tolerance is never weakened.

