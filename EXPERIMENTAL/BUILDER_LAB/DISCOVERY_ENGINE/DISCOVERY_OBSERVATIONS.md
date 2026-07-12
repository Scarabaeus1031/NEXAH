# NEXAH Discovery Core — Lorenz Observation Record

> **Status: historical exploratory experiment series (V4–V22).** This document
> records candidate observations from one classical Lorenz setup. It is not a
> validated cross-system finding or a specification of the current NEXAH core.

## Purpose

The Discovery Core investigated how trajectory-derived events, probability
representations, and locally estimated field operators behave in a numerical
Lorenz simulation. The useful outcome is a set of hypotheses and method
prototypes that can be reproduced and challenged individually.

Current related entry points:

- **[experiment scripts](experiments/runs/)**
- **[generated V4–V22 visuals](outputs/)**
- **[visual development gallery](visual_gallery.md)**
- **[current Lorenz repository index](../../../RESEARCH/APPLIED_CASES/LORENZ/lorenz_index.md)**
- **[current Lorenz validation](../../../RESEARCH/VALIDATION/lorenz/)**

---

## Evidence Map

| Stage | Recorded observation | Repository evidence | Current confidence |
|---|---|---|---|
| V4–V8 | Peak extraction, event clustering, and PCA-based channel views | Generated images exist; corresponding early run scripts are not present in this directory | Visual historical evidence only |
| V9–V15 | Prediction, control, alignment, navigation, and state-machine prototypes | Outputs exist; reproducibility varies by version | Prototype lineage |
| V16 | Non-uniform density around selected trajectory events | Script and output exist | Reproducible in principle after dependency and path setup |
| V19 | Transformation of an estimated event density using `-log(p)` | Script and output exist | Representation choice, not physical energy evidence |
| V20–V21 | Local divergence- and curl-like estimates on a nearest-neighbor representation | Scripts and outputs exist | Experimental numerical operators |
| V22 | Cross-correlation of the two estimated operator series | Script and output exist | Single-configuration result; not independently validated |

The V16–V22 scripts require the numerical and plotting dependencies used by the
project. They also write to paths relative to the current working directory.
The V22 script could not be rerun in the bare audit environment on July 12,
2026 because NumPy was not installed there; the stored source and output remain
available for a dedicated reproduction run.

---

## 1. Trajectory-Derived Event Structure

The early experiments selected high-activity trajectory samples using evolving
risk and threshold heuristics. Clustering and PCA views then exposed directional
patterns in those selected samples.

Qualified interpretation:

- the Lorenz trajectory is structured rather than random noise
- an event-selection rule can emphasize preferred regions of the attractor
- a dominant PCA axis is a property of the selected representation

This does not by itself establish a universal transition channel or demonstrate
that the axis predicts regime changes.

---

## 2. Probability and Effective-Energy Representations

V16 estimated a local probability-like quantity from selected events. V19 then
applied:

```math
E(x) = -\log(p(x))
```

This produces an effective landscape for the chosen density estimate. Calling
it an energy landscape is a mathematical analogy; the experiment does not show
that it is a physical energy or that its barriers are power-system stability
margins.

---

## 3. Local Operator Estimates

V20–V22 estimated divergence- and curl-like quantities from nearest-neighbor
differences along sampled Lorenz states. Spatial structure in these estimates is
a legitimate object for further study, but it depends on:

- integration step and trajectory length
- neighborhood size
- sampling density
- operator estimator
- normalization and boundary behavior

The estimates should therefore be called numerical local operators, not direct
measurements of a physical field.

---

## 4. V22 Lag Observation

V22 cross-correlated the two estimated operator-magnitude series and selected
the lag of maximum correlation within a fixed search window. Earlier notes
reported a lag near 15 samples for that setup.

The supportable statement is:

> A non-zero cross-correlation maximum was reported for one Lorenz trajectory,
> one nearest-neighbor operator construction, and one lag-search configuration.

It does not yet establish delayed feedback. The sign and magnitude of the lag
must be tested under changed seeds or initial conditions, integration steps,
neighborhood sizes, estimator definitions, and surrogate or shuffled controls.

---

## 5. Candidate Research Questions

The series motivates testable questions rather than general conclusions:

1. Are event-density structures stable across Lorenz initial conditions and
   numerical integrators?
2. Does the PCA channel persist when event-selection thresholds change?
3. Are local operator patterns robust to neighborhood and estimator choices?
4. Does the V22 lag exceed lag structure obtained from autocorrelation,
   phase-shifted surrogates, or shuffled controls?
5. Do analogous representations add predictive value beyond established
   features in another simulated system?

---

## Promotion Decision

No statement from this document should currently be copied into
`RESEARCH/FINDINGS/` as a validated finding. The best promotion candidate is a
small V22 reproduction study with parameter sweeps and controls. Until then,
this document remains the evidence-aware index of the historical Discovery
series.

---

**Last reviewed:** July 12, 2026
