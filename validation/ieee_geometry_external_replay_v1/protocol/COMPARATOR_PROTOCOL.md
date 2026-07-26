# G2 Comparator Protocol Candidate

Status: **candidate for review; not approved**

Protocol identifier: `sr1-ieee-geometry-comparator-analysis-v1`

This protocol defines only the bounded conventional comparison for frozen IEEE
Geometry V1. It does not compute comparator results. IEEE-9 is the sole
definition and fixture case. No new IEEE-14 comparator output may be read,
generated, or displayed until the candidate protocol is approved and its exact
bytes are bound to the approved SHA-256 record.

The machine-readable authority for G2 is
[`g2_protocol_candidate.json`](g2_protocol_candidate.json). If this Markdown
summary conflicts with that JSON, G2 is not approvable until the conflict is
resolved.

## Tier 0 fields

| ID | Formula | Source scope | Unit |
|---|---|---|---|
| `v_min_pu` | `min(vm_pu)` | every row of the bus entity view | pu |
| `v_dev_rms_pu` | `sqrt(mean((vm_pu - 1.0)^2))` | every row of the bus entity view | pu |
| `l_max_percent` | `max(loading_percent)` | every row of the line entity view; transformers and other branch types excluded | percent |
| `angle_spread_degree` | `max(va_degree) - min(va_degree)` | every row of the bus entity view | degree |

The source fields are the committed physical-frame entity views corresponding
to Pandapower `res_bus.vm_pu`, `res_bus.va_degree`, and
`res_line.loading_percent`. Entity identifiers and their stored order are
preserved. Comparator values are case-local and never compared by entity across
IEEE-9 and IEEE-14.

`v_min_pu`, `l_max_percent`, and `angle_spread_degree` are already inputs to the
seven-feature V1 system-summary projection. They are controls, not independent
validation. `v_dev_rms_pu` is derived from the same bus-voltage profile and is
also not external evidence.

## Scaling and angle rules

- Levels remain in their declared physical units; no z-score, normalisation,
  clipping, sign inversion, or aggregation across fields is permitted.
- Signed adjacent change is `c_i - c_(i-1)`.
- Absolute adjacent change is `abs(c_i - c_(i-1))`.
- Centred absolute second difference is
  `abs(c_(i+1) - 2*c_i + c_(i-1))`.
- Angles use the solver reference stored in `va_degree`.
- No modulo, wrap, or unwrap operation is applied. The comparator is the raw
  finite maximum minus minimum at the same solved frame.

## Availability and missingness

A level is available only when the frame status is `converged`, exactly one bus
view and one line view exist, required fields exist, entity/value row counts
match, the required scope is non-empty, and every required value is a finite
JSON number.

Otherwise all four levels are JSON `null` and the original frame failure is
preserved. A local change requires two adjacent available campaign positions.
A centred value requires three adjacent available positions. A failed or
missing position is never bridged. No interpolation, imputation, carry-forward,
or solver rerun is allowed.

## Numeric comparison and ties

Reference fixture checks use
`abs(actual-expected) <= 1e-12 + 1e-10*abs(expected)`. This tolerance is only an
artifact-comparison rule; it does not alter values.

Ranking is descending by absolute local magnitude. Values belong to one tie
group when the same tolerance rule holds. Spearman calculations use average
ranks for ties. Top-k selection includes the complete boundary tie group and
may therefore contain more than `k` positions. Stable reporting order is
campaign index ascending within a tie group.

## Tier 1 decision

Tier 1 is **omitted at G2**. Pandapower 3.4.0 exposes `runpp` as the stable
high-level solve interface, but it exposes no top-level public Jacobian result.
Producing the candidate smallest singular value would require internal solver
state or low-level modules such as `_ppc`, `pandapower.pf.create_jacobian`,
`pandapower.pypower.makeYbus`, or `pandapower.pypower.dSbus_dV`. Those are
outside the permitted stable-public-interface boundary.

No substitute Tier 1 metric is introduced. Reconsideration would require a
separate protocol revision and approval before any evaluation output.

## Fixtures

The only numerical fixtures are committed IEEE-9 development-frame examples in
[`../fixtures/ieee9_manual_comparator_fixtures.json`](../fixtures/ieee9_manual_comparator_fixtures.json).
They include raw input vectors, expected levels, one adjacent-change check, and
one explicit failed-frame check.

