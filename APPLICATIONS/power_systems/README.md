# ⚡ Stability Field Dynamics — IEEE Power Systems

## Overview

This module extends classical power system stability analysis into a **dynamic field-based framework**.

Instead of treating stability as a binary outcome (stable vs collapse), we model it as:

- a continuous field  
- a dynamic flow system  
- a memory-based recurrence structure  
- a resonance-driven topology  
- a phase-coupled dynamical system  

Standard IEEE test systems (starting with 14-bus) serve as real-world benchmarks.

---

## Core Concept

> Stability is not a state — it is a geometry.

This geometry evolves into:

- Geometry → field representation  
- Field → flow dynamics  
- Flow → trajectories  
- Trajectories → memory (recurrence)  
- Memory → resonance structure  
- Resonance → coupling  
- Coupling → system  

---

## Fundamental Discovery

All systems decompose into:

→ **3 + 1 structure**

- Band A  
- Band B  
- Gap (interface)  
- Global flow  

BUT:

| System | Behavior |
|--------|----------|
| IEEE 9 | latent structure (decoupled) |
| IEEE 14 | coupled system (active dynamics) |

> Structure alone is not sufficient —  
> **interaction is required for system formation.**

---

## Key Results — IEEE 14

- Dual resonance peaks:
  - Band A ≈ 0.008  
  - Band B ≈ 0.84  

- Gap:
  - ≈ 0.832 (active interface)

- Emergent structure:
  - States: 2  
  - Loops: 6  

- Coupling:
  - C ≈ 0.0036  
  - P ≈ 0.47  
  - R ≈ 0.27  
  - L ≈ 0.028  

---

## Coupling Principle

We define:

C = P × R × L

Where:

- P → flow persistence  
- R → recurrence concentration  
- L → loop density  

Interpretation:

- C ≈ 0 → diffuse field  
- C > 0 → system emerges  

---

## Local Emergence — Birth Zones

Coupling is not global.

C(x,y) = P(x,y) × R(x,y) × L(x,y)

→ Structure emerges only in localized regions

### → Birth Zones of Structure

---

## Phase System (CCC / GH / KKK)

| Phase | Meaning | Behavior |
|------|--------|----------|
| CCC | expansion | high activity |
| KKK | collapse | absorbing |
| GH  | interface | transition / coupling |

---

## Core Phase Insight

> The system does not exist in expansion or collapse.  
>  
> It exists in the **interface (GH)**.

---

## GH Corridor

GH is not a discrete phase.

→ It forms a **continuous corridor in phase space**

Properties:

- extended in θ  
- bounded in C  
- dynamically active  
- supports transitions  

---

## Corridor Flow Field

Particles initialized in GH show:

- bounded radial motion (C)  
- free angular motion (θ)  
- persistent trajectories  
- no collapse to a point  

### Result

→ GH behaves as a **band-like attractor structure**

---

## Attractor Interpretation

Classical:
- attractor = point / set  

Observed:
- attractor = **extended manifold (corridor)**  

---

## Structural Dynamics

System exhibits anisotropic behavior:

| Dimension | Behavior |
|----------|--------|
| θ (angular) | free motion |
| C (radial) | constrained motion |

---

## Noise as Activation

| Noise | Effect |
|------|--------|
| low | no structure |
| medium | structure emerges |
| high | structure breaks |

→ Noise acts as an **activation parameter**

---

## Dynamic Stability

Under time-dependent parameters:

- noise(t)  
- rotation(t)  
- damping(t)  

System exhibits:

- cyclic structure formation  
- regime switching  
- repeatable dynamics  

→ stability becomes **time-dependent**

---

## System Evolution

| Phase | Description |
|------|-------------|
| 1 | Classical stability |
| 2 | Continuous field |
| 3 | Boundary dynamics |
| 4 | Flow + particles |
| 5 | Memory / recurrence |
| 6 | State detection |
| 7 | Resonance + gap |
| 8 | Topology (graph) |
| 9 | Coupling metric |
| 10 | Noise activation |
| 11 | Phase cycling |
| 12 | Phase system |
| 13 | GH Corridor + Flow |

---

## System Classification

1. Diffuse Field  
2. Activated Field  
3. Coupled Field  
4. Cyclic Field  
5. Phase-Coupled System  
6. Corridor-Dominated System  

---

## Architecture Layers

1. Field Layer  
2. Dynamic Layer  
3. Memory Layer  
4. Resonance Layer  
5. Topological Layer  
6. Coupling Layer  
7. Phase Layer  
8. Corridor Layer  

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
