# IEEE Scaling Pattern V1 — Canonical Record

Status: frozen physical reconstruction of the historical V32 hypothesis

Recorded timestamp: `2026-07-13T19:00:00+00:00`

## Repository audit

The historical repository described a cross-system curvature peak before power
flow collapse and later extended visual scaling work through PEGASE-9241. The
audit found three important limitations in those older lines:

- the IEEE-X solver inserted random voltage arrays after non-convergence
- it added random noise and manual drift to converged voltage arrays
- many later scaling visuals reused hand-designed trigger or inversion formulas

The later Atlas inventory also marks PEGASE-9241 raw trajectory assets as
missing. Historical plots and claims were therefore treated as hypotheses, not
as current validation data.

## Reconstruction

The V32 metric was reconstructed exactly from converged pandapower values:

```text
c_struct = std(theta_rad)
         × std(clip(1 − vm_pu, −1, 1))
         × mean(normalized_bus_loop_signal)
```

No fallback arrays, noise, drift, controller, or historical plot data entered
the calculation. Eight networks were scanned on the same 200-point load grid
from 0.6 to 5.0, stopping after the first non-converged point.

## Canonical result

| System | Boundary | Historical lead | Interior lead | Status |
|---|---:|---:|---:|---|
| IEEE-9 | 2.258291 | 0.044221 | 0.066332 | estimated |
| IEEE-14 | 4.005025 | 0.044221 | 0.066332 | estimated |
| IEEE-30 | 3.673367 | 0.044221 | 0.066332 | estimated |
| IEEE-57 | 1.462312 | 0.044221 | 0.066332 | estimated |
| IEEE-118 | 1.816080 | 0.066332 | 0.066332 | estimated |
| IEEE-300 | 0.600000 | — | — | lower-bound non-convergence |
| PEGASE-1354 | 1.329648 | 0.044221 | 0.066332 | estimated |
| PEGASE-9241 | 0.600000 | — | — | lower-bound non-convergence |

Aggregate observations:

- six systems have a usable converged prefix and upper boundary
- two systems fail at the lower scan bound and are not interpretable as upper
  collapse boundaries
- all six usable historical peaks have positive lead
- historical lead mean: `0.047906`; coefficient of variation: `0.172005`
- all six interior leads equal `0.066332`
- all six interior peaks occur exactly at the two-sample exclusion boundary
- downsampled leads increase to approximately `0.110553–0.132663`

## Interpretation

The reconstruction supports a shared increase in the historical structural
metric's curvature toward the first non-converged load case across IEEE-9,
IEEE-14, IEEE-30, IEEE-57, IEEE-118, and PEGASE-1354.

It does not confirm an independent universal precursor peak. Once two derivative
edge samples are excluded, every selected peak is simply the first remaining
point at that exclusion boundary. Its location also moves under downsampling.
The constant three-grid-step lead is therefore compatible with a numerical
boundary effect applied to a monotonically accelerating curve.

PEGASE-9241 is neither confirmed nor refuted by this V1 scan. Non-convergence at
the lower bound leaves no converged prefix for curvature estimation. IEEE-300
has the same failure. Both require a baseline-anchored continuation design
rather than reinterpretation of this frozen result.

## Reproducibility

Two final canonical executions were byte-identical:

- result SHA-256: `26962152fd794b382e57dbb7cb75cb219a656d1461798e5341fa38e2e238e8c5`
- summary SHA-256: `4e25770b85e30caef65c7d4bdf4ebf4de3dc9432f189a04edcfef9b71c1f06bd`

## Next test

V2 should start from a known converged baseline for each network, trace separate
upward and downward continuation branches, and use derivative estimators whose
peak definition is not fixed by a boundary exclusion rule. PEGASE-9241 must
remain held out from method selection.
