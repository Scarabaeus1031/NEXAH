# IEEE Scaling Pattern Validation V1

Status: canonical V1 completed and frozen

Artifacts:

- **[VALIDATION_RECORD.md](VALIDATION_RECORD.md)** — audit, result, and interpretation
- **[canonical_result.json](canonical_result.json)** — complete physical scan
- **[canonical_summary.md](canonical_summary.md)** — aggregate metrics
- **[failure_cases.json](failure_cases.json)** — numerical and design failures

This validation reconstructs the historical V32 “fundamental pattern” using
only converged pandapower outputs. Historical plots and claims are context, not
input evidence.

## Hypothesis under test

The historical metric was:

```text
c_struct = std(bus angle in radians)
         × std(1 − bus voltage)
         × mean(normalized per-bus loop signal)
```

with:

```text
dc/dload   = gradient(c_struct, load)
d²c/dload² = gradient(dc/dload, load)
```

The hypothesis is that the maximum positive curvature occurs before the first
non-converged load case, with a similar load-scale lead across systems.

## Frozen design

- dense grid: 200 points from load scale 0.6 to 5.0 inclusive
- historical reference: IEEE-9, IEEE-14, IEEE-30
- extension: IEEE-57, IEEE-118, IEEE-300
- held-out scale: PEGASE-1354, PEGASE-9241
- fresh network and independent Newton–Raphson solution at every load scale
- no random values, noise, drift, controller, fallback physics, or plot input
- collapse boundary: first non-converged load scale
- the scan stops after recording the first non-converged point; post-boundary
  solves cannot affect the precursor curve or boundary
- historical peak: maximum signed second derivative over the converged prefix
- sensitivity peak: same calculation excluding two derivative-edge samples
- resolution sensitivity: repeat peak extraction on every second dense sample
- systems without a failure by 5.0 are right-censored and not scored as a
  precursor success or failure
- systems with fewer than five converged prefix samples are recorded as
  `insufficient_converged_samples`; curvature is not imputed
- non-convergence at the first scan point is recorded as a lower-bound failure,
  not interpreted as an upper collapse boundary
- parameters are not changed after canonical execution

## Reported evidence

- collapse and curvature-peak load scales
- historical, interior, and downsampled lead distances
- whether each detected peak precedes collapse
- coefficient of variation across observed leads
- held-out PEGASE behavior

The validation does not call a peak an early-warning system. A positive lead
alone does not establish robustness, causality, or operational usefulness.
If the interior peak lies exactly at the two-point exclusion boundary, the
apparent lead is treated as derivative-edge sensitivity rather than an
independent interior maximum.

## Canonical conclusion

Boundary acceleration is reproduced for six systems through PEGASE-1354. The
stronger claim of a resolution-independent universal precursor peak is not
confirmed: every interior peak lies at the exclusion boundary and moves under
downsampling. IEEE-300 and held-out PEGASE-9241 are not estimable from the V1
global lower bound and require baseline-anchored continuation in a new version.
