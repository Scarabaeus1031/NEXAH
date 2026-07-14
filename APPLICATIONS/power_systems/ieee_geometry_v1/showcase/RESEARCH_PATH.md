# IEEE Geometry V1 — Research Path

This path is for readers who want to audit the method rather than only view its
result.

## 1. Protocol before output

Start with the typed [case manifest](../case_manifest.json). It freezes case
roles, variables, units, projections, operators, environment, solver,
insufficiency rules, supported claims, prohibited claims, and the outcome
boundary before interpreting IEEE-14.

## 2. Physical evidence before geometry

Compare [development frames](../development_frames.json) with
[evaluation frames](../evaluation_frames.json). A frame contains raw physical
summaries and entity-aligned bus/line views when the solver converges. Failed
frames contain no fabricated physical values.

## 3. Representation and operators

Read [development geometry](../development_geometry.json) first. Its
standardization statistics are fitted only on IEEE-9. Then inspect
[evaluation geometry](../evaluation_geometry.json), which carries the same
model identity and the six frozen operators:

- adjacent displacement;
- normalized local drift;
- cumulative path length;
- direction change;
- discrete curvature;
- sampled distance from failure to the last converged frame.

These measurements describe the chosen representation and sampling. They are
not automatically physical invariants.

## 4. Multiple perspectives without voting

The [evaluation orientation record](../evaluation_orientation.json) preserves
five separate probes:

1. physical state;
2. sampled geometry;
3. boundary and resolution;
4. provenance and leakage;
5. claim criticism.

Agreement is recorded, but no probe overrides another and no probe executes an
action.

## 5. Validation and negative knowledge

The [validation record](../../../../validation/ieee_geometry_v1/VALIDATION_RECORD.md)
and [machine summary](../../../../validation/ieee_geometry_v1/canonical_summary.json)
show exact replay, checksums, outcome closure, and the complete claim audit.
IEEE-14 supplies positive evidence for unchanged technical application and
negative knowledge about what the frozen grid does not reveal.

## 6. Open research questions

- Which established power-system measures should be compared prospectively
  with the geometric measurements?
- What metric should compare the declared physical projections without being
  selected after viewing the results?
- How stable are local measurements under a predeclared change in sampling
  resolution?
- Which new network should evaluate a revised method after that revision is
  frozen?
- How should calibrated uncertainty be attached claim by claim?
- What licensed, timestamped operational source could support an external
  observed-evidence study?

The last question leads to the
**[Observed-Evidence Bridge](../../../../testkit/observed_evidence/OBSERVED_EVIDENCE_BRIDGE.md)**.
