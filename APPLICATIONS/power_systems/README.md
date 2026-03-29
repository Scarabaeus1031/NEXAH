# ⚡ Stability Field Dynamics — IEEE Power Systems

## Overview

This module extends classical power system stability analysis into a **dynamic, physically grounded and predictive framework**.

Instead of treating stability as a binary outcome (stable vs collapse), system behavior is represented as:

* a continuous field  
* a dynamic flow system  
* a recurrence-based memory structure  
* a resonance-driven organization  
* a phase-structured dynamical system  
* a physically coupled predictive model  
* a **cross-validated early warning system**

Standard IEEE test systems (IEEE 9, 14, 30) are used as benchmarks.

---

## Core Concept

> Stability is not a state — it is a geometry.

This geometry evolves through successive transformations:

* Geometry → field representation  
* Field → flow dynamics  
* Flow → trajectories  
* Trajectories → recurrence (memory)  
* Memory → resonance structure  
* Resonance → coupling  
* Coupling → system-level organization  
* Organization → physical embedding  
* Physical embedding → predictive collapse detection  

---

## 🌐 Field Layer & Flow Dynamics (V64–V69)

A major extension of the framework introduces:

→ the **explicit field representation of dynamics**

Previously:

- structure was inferred from metrics  
- collapse was detected via trajectories  

Now:

→ the system is represented as a **continuous vector field**

---

### Key Transition

From:

→ structure + dynamics  

To:

→ **structure + dynamics + field geometry**

---

### What is new

#### V64–V67 — State Field Expansion

- system states expanded into continuous phase-space  
- curvature structure becomes visible as a field  
- GH corridor appears as embedded region  

---

#### V68 — Off-Manifold Field

- local neighborhoods sampled around trajectory  
- reveals full surrounding field structure  
- identifies:

  - core region  
  - transition band  
  - expansion domain  

→ confirms that trajectory is only a **spine inside a larger field**

---

#### V69 — Flow Field (Critical Step)

- full vector field constructed  
- local flow directions computed  
- streamlines extracted  

This reveals:

→ **how the system moves in state space**

---

### Key Discovery

> The system does not evolve randomly.  
>  
> It follows structured paths inside a field.

Observed:

- consistent directional flow  
- local branching structures  
- smooth global alignment  

---

### Interpretation

The dynamics follow:

→ **geodesics in the field**

Meaning:

- minimal-energy paths  
- natural evolution trajectories  
- fastest approach toward collapse  

---

### Connection to Previous Results

| Previous Concept | Field Interpretation |
|----------------|---------------------|
| Manifold | valley / surface in field |
| Rift | flow-aligned corridor |
| Distance | deviation from flow alignment |
| Branching | local flow divergence |
| Collapse | exit from structured flow |

---

### Visual — Off-Manifold Flow (V69)

![Off-Manifold Flow](outputs/ieee118_v69_off_manifold_flow.png)

→ trajectories follow structured directions  
→ local deviations reveal branching  
→ collapse paths are embedded in the field  

---

### Visual — Stream Field (V69)

![Stream Field](outputs/ieee118_v69_stream_field.png)

→ global flow structure becomes visible  
→ smooth directional alignment across phase space  

---

### Fundamental Insight (Extended)

> The system is not defined by states.  
>  
> It is defined by the field that connects them.  
>  
>  
> Collapse is not a point,  
> not only a process,  
>  
> but a **trajectory inside a geometric flow field**.

---

### Key Discovery

> The system does not evolve randomly.  
>  
> It follows structured paths inside a field.

Observed:

- consistent directional flow  
- local branching structures  
- smooth global alignment  

---

### Interpretation

The dynamics follow:

→ **geodesics in the field**

Meaning:

- minimal-energy paths  
- natural evolution trajectories  
- fastest approach toward collapse  

---

### Connection to Previous Results

| Previous Concept | Field Interpretation |
|----------------|---------------------|
| Manifold | valley / surface in field |
| Rift | flow-aligned corridor |
| Distance | deviation from flow alignment |
| Branching | local flow divergence |
| Collapse | exit from structured flow |

---

### Visual — Off-Manifold Flow (V69)

![Off-Manifold Flow](../outputs/ieee118_v69_off_manifold_flow.png)

→ trajectories follow structured directions  
→ local deviations reveal branching  
→ collapse paths are embedded in the field  

---

### Visual — Stream Field (V69)

![Stream Field](./outputs/ieee118_v69_stream_field.png)

→ global flow structure becomes visible  
→ smooth directional alignment across phase space  

---

### Fundamental Insight (Extended)

> The system is not defined by states.  
>  
> It is defined by the field that connects them.  
>  
>  
> Collapse is not a point,  
> not only a process,  
>  
> but a **trajectory inside a geometric flow field**.

---

## Fundamental Observation

Across all systems:

→ **3 + 1 structure**

* Band A  
* Band B  
* Gap (interface region)  
* Global flow field  

But:

| System  | Behavior |
| ------- | -------- |
| IEEE 9  | weakly structured, fast collapse |
| IEEE 14 | strongly structured, extended transition |
| IEEE 30 | intermediate, smoother degradation |

> Structure alone is insufficient —  
> **interaction and coherence determine stability.**

---

## Physical Coupling

The framework is directly linked to real grid physics:

* voltage magnitude (V)  
* phase angle (θ)  
* power flow (loop proxy)

Mapping:

* C = 1 − V  
* θ = phase angle (rad)  
* loops = flow-weighted phase interaction  

This enables:

* real load scaling experiments  
* detection of non-convergence (true collapse)  
* direct comparison with classical indicators  

---

## Collapse Mechanism (Validated)

The collapse process follows a **universal sequence**:

1. **Coherence (SAFE)**  
2. **Fragmentation (WARNING)**  
3. **Acceleration (CRITICAL)**  
4. **Breakdown (COLLAPSED)**  

---

## Predictive Metrics

The system is defined by four coupled quantities:

1. **Structural intensity**
   → c_struct  

2. **Drift**
   → dc/dload  

3. **Acceleration (curvature)**
   → d²c/dload²  

4. **Fragmentation (coherence loss)**
   → std(θ) × std(loops)  

---

## Key Discovery

> Collapse is not driven by maximum stress.  
>  
> It is driven by **loss of coherence**,  
> followed by **nonlinear acceleration**.

---

## Validation — Multi-System Benchmark (V31–V36)

Tested across:

* IEEE 9  
* IEEE 14  
* IEEE 30  

### Result

Across all systems:

* curvature peak (d²c/dload²) consistently occurs **before collapse**
* lead time is **stable across systems**

Typical values:

| System  | Collapse | Curvature Peak | Lead Time |
|--------|---------|----------------|----------|
| IEEE 9  | ~2.26 | ~2.21 | ~0.04–0.08 |
| IEEE 14 | ~4.00 | ~3.96 | ~0.04–0.15 |
| IEEE 30 | ~3.67 | ~3.61 | ~0.04–0.08 |

---

## Comparison to Classical Indicators (NEW)

Classical signals:

* min(V)  
* dV/dload  
* voltage deviation  

Observed:

* smooth degradation  
* weak early signal  

NEXAH signals:

* curvature spike  
* fragmentation increase  
* divergence emergence  

### Key Result

> NEXAH detects instability **earlier and sharper** than classical indicators.

---

## Divergence Detection (V34–V35)

Defined:

divergence = NEXAH − Classical  

Observed:

* divergence remains small in stable regime  
* increases near transition  
* peaks before collapse  

Extended:

* smoothed divergence  
* augmented divergence (robust signal)

---

## GH Corridor

GH is not a point.

→ It forms a **continuous phase-space corridor**

Properties:

* extended in θ  
* bounded in C  
* dynamically active  
* supports transitions  

---

## Structural Dynamics

| Dimension   | Behavior |
| ----------- | -------- |
| θ (angular) | free / extended |
| C (radial)  | constrained |

---

## Noise Sensitivity

| Noise  | Effect |
| ------ | ------ |
| low    | no structure |
| medium | structure emerges |
| high   | structure destabilizes |

---

## Development Stages

| Phase | Description |
|------|-------------|
| V1–V16 | field → topology |
| V17–V23 | coupling + attractor |
| V24–V32 | phase dynamics |
| V33–V35 | validation + comparison |
| V36     | unified predictor (paper-ready) |

---

## System Classification

1. Diffuse regime  
2. Activated regime  
3. Coupled regime  
4. Cyclic regime  
5. Phase-structured regime  
6. Corridor-dominated regime  
7. **Predictive physical system**

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
9. Physical layer  
10. Predictive layer  

---

## Current State

The framework is now:

* physically grounded  
* multi-system validated  
* predictive  
* comparable to classical methods  
* showing **early-warning capability**

---

## Open Questions

* Generalization to arbitrary networks  
* Node-level localization of collapse  
* Time-domain stability (dynamic simulation)  
* Integration into real-time monitoring  

---

## Repository Structure

```text
APPLICATIONS/power_systems/stability_field_dynamics/
│
├── ieee_test_cases/
│   ├── core/         # physical adapter, metrics
│   ├── pipeline/     # phase + corridor logic
│   ├── experiments/  # run_ieee_* (v1–v36)
│   ├── analysis/     # transforms, fitting
│   ├── outputs/      # CSV + plots
│   ├── logs/         # research logs
│   └── README.md
