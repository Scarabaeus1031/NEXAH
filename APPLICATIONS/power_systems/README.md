# ⚡ Stability Field Dynamics — IEEE Power Systems

## Overview

This module extends classical power system stability analysis into a **dynamic field-based framework**.

Instead of treating stability as a binary outcome (stable vs collapse), we represent system behavior as:

* a continuous field
* a dynamic flow system
* a recurrence-based memory structure
* a resonance-driven organization
* a phase-structured dynamical system

Standard IEEE test systems (starting with 14-bus) are used as benchmarks.

---

## Core Concept

> Stability is not a state — it is a geometry.

This geometry is explored through successive transformations:

* Geometry → field representation
* Field → flow dynamics
* Flow → trajectories
* Trajectories → recurrence (memory)
* Memory → resonance structure
* Resonance → coupling
* Coupling → system-level organization

---

## Fundamental Observation

Across experiments, the system consistently decomposes into:

→ **3 + 1 structure**

* Band A
* Band B
* Gap (interface region)
* Global flow field

However:

| System  | Behavior                                   |
| ------- | ------------------------------------------ |
| IEEE 9  | structure present but dynamically inactive |
| IEEE 14 | structure becomes dynamically coupled      |

> Structure alone is not sufficient —
> interaction determines whether a system forms.

---

## Key Results — IEEE 14

* Dual resonance bands:

  * Band A ≈ 0.008
  * Band B ≈ 0.84

* Gap:

  * ≈ 0.832 (interface region)

* Emergent structures:

  * States: 2
  * Loops: 6

* Coupling metric:

  * C ≈ 0.0036
  * P ≈ 0.47
  * R ≈ 0.27
  * L ≈ 0.028

These results are internally consistent across runs.

---

## Coupling Principle

We define:

C = P × R × L

Where:

* P → flow persistence
* R → recurrence concentration
* L → loop density

Interpretation:

* C ≈ 0 → diffuse regime
* C > 0 → dynamically coupled regime

---

## Local Emergence

Coupling is spatially localized:

C(x,y) = P(x,y) × R(x,y) × L(x,y)

→ Structure appears only in specific regions of the field

### → “Birth zones” of structure

---

## Phase Structure (CCC / GH / KKK)

| Phase | Meaning   | Behavior              |
| ----- | --------- | --------------------- |
| CCC   | expansion | high activity         |
| KKK   | collapse  | absorbing             |
| GH    | interface | transition / coupling |

---

## Phase Insight

> The system is not dominated by expansion or collapse.
>
> Most persistent structure appears in the **interface region (GH)**.

---

## GH Corridor

GH does not appear as isolated points.

→ It forms a **continuous region in phase space**

Properties:

* extended in θ
* bounded in C
* supports trajectories
* associated with non-zero coupling

---

## Corridor Flow Behavior

Particles initialized in GH show:

* constrained radial motion (C)
* less constrained angular motion (θ)
* persistent trajectories

### Interpretation

→ GH behaves like a **band-like dynamical region**,
not a point attractor.

---

## Attractor Interpretation

Classical view:

* attractor = point / set

Observed behavior:

* attractor ≈ **extended region (manifold-like)**

This is a descriptive observation, not yet a formal result.

---

## Structural Dynamics

The system shows anisotropic behavior:

| Dimension   | Behavior         |
| ----------- | ---------------- |
| θ (angular) | less constrained |
| C (radial)  | constrained      |

---

## Noise Sensitivity

| Noise  | Effect                 |
| ------ | ---------------------- |
| low    | no structure           |
| medium | structure appears      |
| high   | structure destabilizes |

→ Noise acts as an **activation parameter**

---

## Time-Dependent Dynamics

Under time-varying parameters:

* noise(t)
* rotation(t)
* damping(t)

the system exhibits:

* cyclic structure formation
* regime switching

This suggests:

→ stability may be **time-dependent**, not static

---

## Development Stages

| Phase | Description          |
| ----- | -------------------- |
| 1     | Classical stability  |
| 2     | Continuous field     |
| 3     | Boundary dynamics    |
| 4     | Flow + particles     |
| 5     | Recurrence / memory  |
| 6     | State detection      |
| 7     | Resonance structure  |
| 8     | Topology             |
| 9     | Coupling metric      |
| 10    | Noise activation     |
| 11    | Phase cycling        |
| 12    | Phase classification |
| 13    | Corridor dynamics    |

---

## System Classification

1. Diffuse regime
2. Activated regime
3. Coupled regime
4. Cyclic regime
5. Phase-structured regime
6. Corridor-dominated regime

---

## Architecture Layers

1. Field layer
2. Dynamic layer
3. Memory layer
4. Resonance layer
5. Topological layer
6. Coupling layer
7. Phase layer
8. Corridor layer

---

## Current Limitation

The current implementation is:

* internally consistent
* structurally reproducible

but:

* not yet coupled to physical IEEE variables
* not responsive to load or voltage collapse
* not predictive

---

## Next Steps

* map physical variables → (C, θ, loops)
* test response under load variation
* evaluate correlation with known stability indicators

---

## Repository Structure

```text
APPLICATIONS/power_systems/stability_field_dynamics/
│
├── ieee_test_cases/
│   ├── core/         # coupling, metrics, fundamental operators
│   ├── pipeline/     # phase data, corridor detection, flow initialization
│   ├── experiments/  # run_scan_* scripts (v1–v36)
│   ├── analysis/     # analysis tools (knick, Fourier, fitting, etc.)
│   ├── outputs/      # plots, CSVs, JSON results
│   ├── logs/         # stability logs and notes
│   └── README.md
```

---

## Working Interpretation

At this stage, the framework should be understood as:

> a structured exploration of dynamical patterns
> in power systems

The key open question remains:

> Do these observed structures correspond to
> physically meaningful stability mechanisms —
> or are they artifacts of the representation?
