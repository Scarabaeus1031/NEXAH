# BUILDING_LOG_01 — JANUS Operator Experimental Series

Status:
Exploratory → Structured Dynamical Analysis

System:
JANUS_OPERATOR

Location:
`EXPERIMENTAL/BUILDER_LAB/JANUS_OPERATOR/`

Author:
Thomas Hofmann

---

# 🧭 Purpose

This document tracks the first structured experimental phase
of the JANUS Operator framework.

The goal is not to introduce new mathematics or physics,
but to investigate whether coherent structural signatures
can be extracted from nonlinear dynamical systems.

Focus:

- coherence structure
- transition organization
- curvature coupling
- temporal ordering
- regime geometry
- flow-aligned structure

---

# 🔷 Core Working Idea

The JANUS operator is explored as a:

> directional coherence observable

inside nonlinear dynamical systems.

The central question is:

```text
Can coherent transition structure
be detected before visible geometric reconfiguration occurs?
```

---

# 🔥 Current High-Level Observation

Across multiple experiments, JANUS appears to exhibit:

- non-random temporal structure
- oscillatory coherence regimes
- stable coupling to curvature
- directional lead/lag behavior
- persistent phase organization

Most importantly:

```text
JANUS structure appears BEFORE
strong curvature reorganization.
```

This result is preliminary,
but currently reproducible across runs.

---

# 🧪 Experimental Series Overview

| Experiment | Script | Focus | Result |
|---|---|---|---|
| EXP-1 | `janus_lorenz_field.py` | coherence field geometry | stable dual structure |
| EXP-2 | `janus_ftle_compare.py` | JANUS vs FTLE | partial structural overlap |
| EXP-3 | `janus_switching_prediction.py` | regime transitions | event clustering visible |
| EXP-4 | `janus_curvature_coupling.py` | curvature relationship | stable anti-correlation |
| EXP-5 | `janus_temporal_lead_lag.py` | temporal ordering | JANUS leads curvature |

---

# 🔷 EXP-1 — Lorenz Coherence Field

Script:
`scripts/janus_lorenz_field.py`

Outputs:

- `outputs/janus_lorenz_overlay.png`
- `outputs/janus_lorenz_heatmap.png`
- `outputs/janus_lorenz_vectorfield.png`

---

## Lorenz Overlay

![Lorenz Overlay](outputs/janus_lorenz_overlay.png)

---

## Lorenz Heatmap

![Lorenz Heatmap](outputs/janus_lorenz_heatmap.png)

---

## Lorenz Vectorfield

![Lorenz Vectorfield](outputs/janus_lorenz_vectorfield.png)

---

## Observation

The Lorenz system reveals:

- stable coherence bands
- dual-lobe organization
- structured density layering
- persistent symmetry

The JANUS field does not appear random.

Instead:

- coherent regions cluster spatially
- transitions align with attractor geometry
- low-coherence regions concentrate near switching zones

---

# 🔷 EXP-2 — JANUS vs FTLE

Script:
`scripts/janus_ftle_compare.py`

Outputs:

- `outputs/janus_ftle_overlay.png`
- `outputs/janus_ftle_scatter.png`
- `outputs/janus_ftle_heatmap.png`
- `outputs/janus_ftle_joint_density.png`

---

## FTLE Overlay

![FTLE Overlay](outputs/janus_ftle_overlay.png)

---

## FTLE Scatter

![FTLE Scatter](outputs/janus_ftle_scatter.png)

---

## FTLE Heatmap

![FTLE Heatmap](outputs/janus_ftle_heatmap.png)

---

## FTLE Joint Density

![FTLE Joint Density](outputs/janus_ftle_joint_density.png)

---

## Observation

Results show:

- partial anti-correlation
- structured density bands
- non-uniform overlap regions

Important:

```text
JANUS and FTLE do NOT measure the same structure.
```

Instead:

- FTLE tracks local divergence
- JANUS appears to track coherence organization

---

# 🔷 EXP-3 — Switching Prediction

Script:
`scripts/janus_switching_prediction.py`

Outputs:

- `outputs/janus_switching_distribution.png`
- `outputs/janus_switching_events.png`
- `outputs/janus_switching_phase_overlay.png`
- `outputs/janus_switching_timeseries.png`

---

## Switching Events

![Switching Events](outputs/janus_switching_events.png)

---

## Switching Distribution

![Switching Distribution](outputs/janus_switching_distribution.png)

---

## Switching Phase Overlay

![Switching Phase Overlay](outputs/janus_switching_phase_overlay.png)

---

## Switching Timeseries

![Switching Timeseries](outputs/janus_switching_timeseries.png)

---

## Observation

Switching events cluster near:

- coherence minima
- modulation boundaries
- phase inversion regions

Event distributions are NOT uniform.

Instead:

- events align along structured coherence oscillations
- transition regions repeat periodically

---

# 🔷 EXP-4 — Curvature Coupling

Script:
`scripts/janus_curvature_coupling.py`

Outputs:

- `outputs/janus_curvature_overlay.png`
- `outputs/janus_curvature_profile.png`
- `outputs/janus_curvature_scatter.png`
- `outputs/janus_curvature_density.png`
- `outputs/janus_curvature_heatmap.png`

---

## Curvature Overlay

![Curvature Overlay](outputs/janus_curvature_overlay.png)

---

## Curvature Profile

![Curvature Profile](outputs/janus_curvature_profile.png)

---

## Curvature Scatter

![Curvature Scatter](outputs/janus_curvature_scatter.png)

---

## Curvature Density

![Curvature Density](outputs/janus_curvature_density.png)

---

## Curvature Heatmap

![Curvature Heatmap](outputs/janus_curvature_heatmap.png)

---

## Numerical Results

```text
samples: 8499

correlation Janus vs log curvature:
r = -0.328164

janus mean:
0.770717

curvature mean:
0.099725

low-Janus count:
680

high-curvature count:
680

overlap count:
59
```

---

## Observation

The relationship is:

- stable
- structured
- anti-correlated

Most importantly:

```text
low JANUS coherence regions
align with elevated curvature structure.
```

---

# 🔷 EXP-5 — Temporal Lead/Lag Structure

Script:
`scripts/janus_temporal_lead_lag.py`

Outputs:

- `outputs/cross_correlation_vs_lag.png`
- `outputs/rolling_correlation.png`
- `outputs/event_alignment.png`

---

## Cross Correlation vs Lag

![Cross Correlation](outputs/cross_correlation_vs_lag.png)

---

## Rolling Correlation

![Rolling Correlation](outputs/rolling_correlation.png)

---

## Event Alignment

![Event Alignment](outputs/event_alignment.png)

---

## Numerical Results

```text
peak lag:
71

peak correlation:
-0.811296

rolling corr mean:
0.351823

rolling corr std:
0.032678
```

---

# 🔥 Key Result

```text
JANUS coherence leads curvature.
```

This is currently the strongest result
of the experimental series.

---

## Interpretation

The lead/lag structure indicates:

- coherence organization occurs first
- curvature reconfiguration follows afterward

Observed behavior:

```text
JANUS minima precede curvature peaks.
```

---

## Cross-Correlation Structure

The lag plots show:

- highly structured symmetry
- repeating oscillatory geometry
- stable extrema spacing

The resulting structure resembles:

- periodic phase folding
- mirrored temporal organization
- quasi-axis inversion geometry

---

# 🔷 Structural Properties Observed

Across all experiments:

---

## 1. Oscillatory Coherence Structure

The JANUS signal exhibits:

- persistent oscillation
- modulation envelopes
- stable recurrence

---

## 2. Anti-Correlation with Curvature

Observed repeatedly:

```text
high curvature
↔ low coherence
```

---

## 3. Temporal Ordering

Current evidence suggests:

```text
coherence organization
precedes curvature reorganization
```

---

## 4. Symmetry Structure

Cross-correlation plots reveal:

- mirrored extrema
- periodic inversion
- structured lag geometry

---

## 5. Transition Alignment

Switching events concentrate near:

- coherence minima
- modulation boundaries
- curvature ramps

---

# 🔷 Relation to FIELD_LAYER

Several structures observed in JANUS
visually resemble earlier FIELD_LAYER findings:

- transition corridors
- ridge-aligned geometry
- separatrix-like layers
- regime modulation
- structured switching regions

Important:

```text
This is currently
a structural analogy,
not a formal equivalence.
```

---

# 🔷 Open Questions

Several important questions remain unresolved:

```text
- Does JANUS generalize beyond Lorenz systems?
- Is the lag structure scale invariant?
- Does the symmetry persist under perturbation?
- Is JANUS connected to FTLE ridges?
- Can JANUS predict transition gates?
- Why does the lag stabilize near ~71?
```

---

# 🔷 Current Status

The JANUS Operator now provides:

- coherence field estimation
- temporal phase structure
- curvature coupling analysis
- lead/lag structure extraction
- event alignment analysis
- FTLE comparison
- switching structure detection

---

# 🔥 Current Working Insight

```text
The system does not transition randomly.

It reorganizes through structured coherence geometry.
```

---

# 🔷 Next Experimental Directions

Planned extensions:

- multi-scale lag analysis
- frequency decomposition
- phase synchronization analysis
- stochastic perturbation tests
- attractor transfer systems
- higher-dimensional flow systems
- field-navigation coupling

---

# 🔷 Final Remark

The observed structures emerge from:

- standard dynamical systems
- numerical integration
- geometric field analysis
- coherence extraction

No explicit transition geometry
was manually imposed.

Yet structured temporal organization emerges repeatedly.

Whether JANUS reflects:

- a useful structural observable
- a coherence artifact
- or a deeper transition geometry

remains intentionally open.

The purpose of this log
is to preserve the observations clearly enough
for systematic future investigation.
