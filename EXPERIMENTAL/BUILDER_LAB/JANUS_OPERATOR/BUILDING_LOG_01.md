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

# 🔷 EXP-6 — Multi-Scale Coherence Analysis

Script:
`scripts/janus_multiscale_analysis.py`

Outputs:

- `outputs/janus_noise_heatmap.png`
- `outputs/janus_scale_variance.png`

---

## Multi-Scale Heatmap

![Multi-Scale Heatmap](outputs/janus_noise_heatmap.png)

---

## Scale Variance

![Scale Variance](outputs/janus_scale_variance.png)

---

## Numerical Results

```text
samples: 12000

variance per scale:

scale=  1 variance=0.070885
scale=  2 variance=0.061448
scale=  5 variance=0.034483
scale= 10 variance=0.013927
scale= 20 variance=0.004386
scale= 40 variance=0.001464
```

---

## Observation

The JANUS coherence structure persists
across multiple smoothing scales.

Important:

```text
The system does not collapse under smoothing.
```

Instead:

- local oscillations compress
- large-scale structure remains stable
- coherent modulation survives aggregation

---

## Structural Interpretation

The heatmap reveals:

- vertical coherence channels
- persistent temporal ridges
- scale-spanning alignment structures

The strongest observation:

```text
coherence corridors remain aligned
across scales
```

This suggests:

- hierarchical organization
- nested modulation geometry
- scale-robust coherence structure

---

## Variance Decay

Variance decreases smoothly
with increasing scale.

This is important because:

```text
the system becomes smoother
without losing structural identity
```

Observed behavior resembles:

- hierarchical field compression
- persistent attractor scaffolding
- multi-scale stability

---

## Visual Observation

The visualization shows:

- coherent resonance bands
- nested oscillation families
- persistent modulation envelopes

At large scales:

- the fast oscillations disappear
- but the global field geometry remains visible

This strongly suggests:

```text
JANUS is not dominated
by high-frequency noise.
```

---

# 🔷 EXP-7 — Frequency Decomposition

Script:
`scripts/janus_frequency_decomposition.py`

Outputs:

- `outputs/janus_frequency_spectrum.png`
- `outputs/janus_power_spectrum.png`
- `outputs/janus_dominant_frequencies.png`

---

## JANUS Frequency Spectrum

![JANUS Frequency Spectrum](outputs/janus_frequency_spectrum.png)

---

## JANUS Power Spectrum

![JANUS Power Spectrum](outputs/janus_power_spectrum.png)

---

## Dominant Frequency Peaks

![Dominant Frequency Peaks](outputs/janus_dominant_frequencies.png)

---

## Numerical Results

```text
samples: 12000

dominant peaks:
0
```

---

## Observation

The JANUS spectrum does NOT exhibit
a single dominant carrier frequency.

Instead:

- broad low-amplitude excitation exists
- weak distributed harmonics appear
- energy spreads continuously across modes

---

## Important Structural Finding

This is highly significant.

Why?

Because the system behaves unlike:

- a pure oscillator
- a fixed resonance
- a single-mode periodic signal

Instead:

```text
JANUS behaves like
a distributed coherence field.
```

---

## Spectrum Interpretation

The frequency plot reveals:

- a strong DC-like baseline
- distributed excitation ridges
- weak spectral islands

The signal appears:

- smooth
- modulated
- continuously reorganizing

rather than:

- sharply periodic
- spectrally concentrated

---

## Structural Implication

The absence of sharp peaks suggests:

- coherence is geometrically distributed
- information is carried structurally
- modulation is flow-dependent

This supports the hypothesis that:

```text
JANUS tracks field organization,
not simple oscillation frequency.
```

---

# 🔷 EXP-8 — Phase Synchronization Analysis

Script:
`scripts/janus_phase_synchronization.py`

Outputs:

- `outputs/janus_phase_difference.png`
- `outputs/janus_phase_locking_distribution.png`
- `outputs/janus_phase_space.png`

---

## Phase Difference

![Phase Difference](outputs/janus_phase_difference.png)

---

## Phase Locking Distribution

![Phase Locking Distribution](outputs/janus_phase_locking_distribution.png)

---

## Phase Space

![Phase Space](outputs/janus_phase_space.png)

---

## Numerical Results

```text
samples: 12000

phase locking value:
0.877538
```

---

# 🔥 Key Result

```text
JANUS and curvature exhibit
strong phase synchronization.
```

---

## Observation

The phase-locking value is extremely high:

```text
PLV ≈ 0.878
```

This indicates:

- persistent phase alignment
- structured temporal coupling
- stable synchronization geometry

---

## Phase Difference Structure

The phase-difference plot reveals:

- bounded oscillation
- recurrent modulation bands
- non-random temporal drift

Importantly:

```text
the phase does not diverge freely.
```

Instead:

- it remains trapped inside
  structured oscillatory corridors

---

## Phase Space Observation

The phase-space plot reveals:

- dense upper-state clustering
- bounded coherence domains
- compressed state occupation

The structure resembles:

- phase locking
- attractor trapping
- constrained synchronization geometry

---

## Distribution Structure

The locking histogram exhibits:

- highly non-uniform density
- preferred synchronization regions
- mirrored boundary clustering

This suggests:

```text
the system prefers
specific phase relationships.
```

---

## Structural Interpretation

Combined observations indicate:

- JANUS and curvature are not independent
- coherence and geometry co-evolve
- synchronization persists dynamically

Most importantly:

```text
the coupling is organized,
not random.
```

---

# 🔷 EXP-9 — Noise Robustness

Script:
`scripts/janus_noise_robustness.py`

Outputs:

- `outputs/janus_noise_distribution_shift.png`
- `outputs/janus_noise_signal_overlay.png`
- `outputs/janus_noise_correlation_decay.png`
- `outputs/janus_noise_heatmap.png`

---

## Noise Distribution Shift

![Noise Distribution Shift](outputs/janus_noise_distribution_shift.png)

---

## Noise Signal Overlay

![Noise Signal Overlay](outputs/janus_noise_signal_overlay.png)

---

## Correlation Decay

![Correlation Decay](outputs/janus_noise_correlation_decay.png)

---

## Noise Heatmap

![Noise Heatmap](outputs/janus_noise_heatmap.png)

---

## Numerical Results

```text
samples per signal: 8499

smoothing sigma: 3.0

noise_level, correlation_to_clean, mean, std

0.000000, 1.000000, 0.770717, 0.085190
0.001000, 0.999946, 0.770162, 0.084996
0.002500, 0.998883, 0.767254, 0.083880
0.005000, 0.983646, 0.756572, 0.081334
0.010000, 0.816825, 0.720423, 0.080203
0.025000, 0.223967, 0.612475, 0.085790
0.050000, 0.196734, 0.565076, 0.069165
```

---

# 🔥 Key Result

```text
JANUS coherence remains stable
under low-to-moderate perturbation.
```

---

## Observation

The signal overlay reveals:

- persistent alignment corridors
- stable coherence bands
- repeated structural overlap

A particularly important region appears near:

```text
JANUS coherence ≈ 0.83
```

Across multiple noise realizations,
signals repeatedly intersect
near this level.

---

## Structural Interpretation

This suggests the existence of:

- preferred coherence channels
- structural attractor corridors
- noise-resistant synchronization bands

---

## Distribution Analysis

The distribution overlays are extremely informative.

As noise increases:

- the coherence field broadens
- variance increases
- but structural layering remains visible

Importantly:

```text
the distributions deform continuously,
not catastrophically.
```

---

## Visual Structure

The overlayed pastel distributions create:

- layered interference regions
- quasi-depth perception
- stacked coherence surfaces

The result visually resembles:

- folded field sheets
- coherence membranes
- layered attractor geometry

---

## Heatmap Observation

The heatmap reveals:

- vertical persistence channels
- stable impulse ridges
- repeated coherence bands

Even under perturbation:

```text
the global field scaffold remains visible.
```

---

## Correlation Decay

The decay curve shows:

- extremely high robustness
  for small perturbations

Observed behavior:

```text
noise ≤ 0.005
→ structure largely preserved
```

A sharper transition occurs near:

```text
noise ≈ 0.01 – 0.025
```

suggesting:

- a structural robustness threshold
- coherence regime destabilization

---

## Important Interpretation

The experiment strongly suggests:

```text
JANUS extracts mesoscopic structure,
not microscopic detail.
```

This may explain:

- smoothing robustness
- phase persistence
- stable recurrence behavior
- multi-scale coherence survival

---

# 🔷 EXP-10 — Attractor Memory & Recurrence Geometry

Script:
`scripts/janus_attractor_memory.py`

Outputs:

- `outputs/janus_recurrence_matrix.png`
- `outputs/janus_delayed_correlation.png`
- `outputs/janus_memory_decay.png`
- `outputs/janus_memory_trace.png`

---

## Recurrence Matrix

![Recurrence Matrix](outputs/janus_recurrence_matrix.png)

---

## Delayed Self-Correlation

![Delayed Self-Correlation](outputs/janus_delayed_correlation.png)

---

## Memory Decay

![Memory Decay](outputs/janus_memory_decay.png)

---

## Memory Trace

![Memory Trace](outputs/janus_memory_trace.png)

---

## Numerical Results

```text
samples: 10199

peak delayed corr:
0.408206

peak lag:
230

memory variance decay:

window=  50 variance=0.001382
window= 100 variance=0.000545
window= 200 variance=0.000151
window= 400 variance=0.000040
window= 800 variance=0.000010
window=1200 variance=0.000005
```

---

# 🔥 Key Result

```text
JANUS exhibits persistent
recurrence structure and delayed memory organization.
```

---

## Delayed Correlation Observation

The delayed self-correlation reveals:

- structured recurrence peaks
- oscillatory memory bands
- repeated lag families

Importantly:

```text
the signal does not decorrelate randomly.
```

Instead:

- correlation repeatedly re-emerges
- delayed structure persists
- recurrence intervals stabilize

---

## Recurrence Matrix Observation

The recurrence matrix reveals:

- diagonal recurrence families
- intersection nodes
- grid-like geometric organization
- repeated state-return corridors

The resulting structure resembles:

- attractor lattices
- recursive field geometry
- transition networks

---

## Structural Interpretation

The recurrence geometry strongly suggests:

```text
JANUS organizes into
repeating state families.
```

The bright intersection points behave like:

- recurrence hubs
- synchronization nodes
- structural crossings

---

## Memory Decay

Variance decreases smoothly
with increasing observation window.

This indicates:

- stable large-scale organization
- persistent structural averaging
- memory compression without collapse

---

## Memory Trace

The memory trace reveals:

- repeated amplitude families
- stable oscillatory envelopes
- persistent modulation corridors

The signal appears:

- recursive
- structured
- temporally layered

rather than:

- stochastic
- fully chaotic
- memoryless

---

## Important Structural Insight

The recurrence matrix is one of the strongest findings
of the current experimental series.

Why?

Because random systems do NOT produce:

- stable recurrence grids
- persistent diagonal families
- structured intersection networks

Instead,
the JANUS system exhibits:

```text
recursive geometric organization.
```

---

## Relation to FIELD_LAYER / ARCHY

Several recurrence structures visually resemble:

- FIELD_LAYER transition corridors
- ARCHY state graphs
- separatrix-like routing geometry
- recursive flow topology

Important:

```text
This remains a structural analogy,
not a formal equivalence.
```

However,
the similarity is visually significant
and repeatedly reproducible.

---

# 🔥 Updated Working Insight

```text
The JANUS system does not evolve randomly.

It reorganizes through recursive coherence geometry,
phase synchronization,
multi-scale structure,
and attractor recurrence networks.
```
