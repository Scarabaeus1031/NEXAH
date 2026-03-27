# ⚡ Stability Field Dynamics — IEEE Systems

## Overview

This module transforms classical power system stability analysis into a:

- continuous field representation  
- dynamic flow system  
- memory-based recurrence model  
- resonance-driven structure formation  
- topological state graph  

Standard IEEE test systems (starting with 14-bus) are used as real-world benchmarks.

---

## Core Idea

> Stability is not a binary state — it is a geometry.  

Extended into:

- Geometry → field representation  
- Field → flow dynamics  
- Dynamics → memory (recurrence)  
- Memory → resonance structure  
- Resonance → coupled system  

---

## Development Levels

| Level | Description |
|------|-------------|
| V1–V3 | Stability field + boundary detection |
| V4–V7 | Bipolar field, folds, eigenmodes |
| V8–V10 | Current field, time evolution, recurrence |
| V11–V13 | State detection, closure, activation |
| V14–V15 | Resonance detection, dual-band structure |
| V15b | Gap stabilization → first loops + states |
| V16 | State graph + loop topology |
| V17 | Coupling metric (P × R × L) |
| V17b | Coupling heatmap (birth zones) |
| V21–V23 | Stable coupling regime + attractor phase |
| V24 | Noise activation → attractor breakdown |
| V25–V26 | Phase cycling → cyclic attractor |
| V29–V31 | Phase dynamics + resonance lock |
| V32 | Phase classifier (KKK / GH / CCC system) |
| V33 | GH Corridor + Flow Field |
| V34+ | Physical relevance tests (decoupling identified) |
| V14 (NEW) | Structural coupling + transition geometry |

---

## Key Results — IEEE 14 (Coupled System)

- Dual resonance peaks:
  - Band A ≈ 0.008  
  - Band B ≈ 0.84  

- Gap:
  - ≈ 0.832 (active interface)

- Emergent structure:
  - States: 2  
  - Loops: 6  

- Coupling metric:
  - C ≈ 0.0036  
  - P ≈ 0.47  
  - R ≈ 0.27  
  - L ≈ 0.028  

---

## Key Results — IEEE 9 (Diffuse System)

- Dual resonance peaks:
  - ≈ 0.007, ≈ 0.012  

- Gap:
  - ≈ 0.004  

- Structure:
  - States: 0  
  - Loops: 0  

---

## Fundamental Discovery

Both systems share a common decomposition:

→ **3 + 1 structure**

- Band A  
- Band B  
- Gap  
- Global flow field  

BUT:

| System | Behavior |
|--------|----------|
| IEEE 9 | latent structure (decoupled) |
| IEEE 14 | coupled system (active dynamics) |

---

## Coupling Metric

C = P × R × L  

Where:

- P → flow persistence  
- R → recurrence concentration  
- L → loop density  

Interpretation:

- C ≈ 0 → diffuse field  
- C > 0 → system formation  

---

## Phase System (V32)

| Phase | Meaning | Behavior |
|------|--------|----------|
| CCC | expansion field | high loops, high activity |
| KKK | collapse field | zero loops, absorbing |
| GH  | interface field | transition / coupling |

---

## Core Insight — Phase System

> The system does not live in CCC or KKK.  
>  
> It lives in GH.

---

## GH Corridor

GH is not a set of points.

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

→ GH behaves as a **band-like attractor**

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

→ Noise acts as an activation parameter

---

## New Layer — Structural Coupling (V14)

Recent experiments introduce explicit coupling between:

- θ (orientation)  
- C (field intensity)  
- loops (closure structure)  

Key additions:

- regime_separation = θ_std × c_std  
- c_struct = regime_separation × loops  

### Interpretation

- system no longer fully invariant  
- internal degrees of freedom begin to interact  
- structural measures grow with parameter changes  

⚠️ Important:

This represents **internal coupling only**  
→ not yet physical IEEE coupling

---

## Current Limitation

The system is still:

- internally consistent  
- structurally rich  

but:

- not yet coupled to real physical variables  
  (voltage, phase angle, imbalance)

---

## System Classification

1. Diffuse Field  
2. Activated Field  
3. Coupled Field  
4. Cyclic Field  
5. Phase-Coupled System  
6. Corridor System  

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

## Final Core Insight (Current)

> Stability is not a point.  
>  
> It is not even just a region.  
>  
> It is a structured corridor in phase space,  
> where motion is allowed, constrained, and sustained.  
>  
> Structure does not live in extremes —  
> it lives in the interface between them.  

---

## Repository Structure

APPLICATIONS/power_systems/stability_field_dynamics/
│
├── ieee_test_cases/
│   ├── pipeline/
│   ├── experiments/
│   ├── analysis/
│   ├── outputs/
│   ├── logs/
│   └── README.md
