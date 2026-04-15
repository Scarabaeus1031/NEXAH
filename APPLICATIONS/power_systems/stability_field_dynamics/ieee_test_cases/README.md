# ⚡ Stability Field Dynamics — IEEE Systems

> A geometric + dynamical + topological framework for predicting system collapse  
> using structure, flow, and manifold alignment.

---

## 🚀 What this is

This module reframes classical power system stability as:

- **Geometry** → collapse manifold  
- **Dynamics** → flow + acceleration  
- **Topology** → branching + multi-state collapse  

Validated on:

- IEEE 9  
- IEEE 14  
- IEEE 30  
- IEEE 57  
- IEEE 118  

---

## 🚀 Quick Entry

👉 Start here: [START_HERE.md](START_HERE.md)

### Recommended reading path

1. `results_summary.md` → empirical findings  
2. `theory_stability_field.md` → conceptual model  
3. `method_pipeline.md` → how everything is computed  
4. `logs/` → full discovery trace  

---

## 🧠 Core Discovery

> Collapse is not triggered —  
> it is approached along a structure.

Systems evolve toward:

→ a **low-dimensional manifold**  
→ align along a **collapse boundary (rift)**  
→ then **leave the structure**

---

## ⚡ What you can do here

- reproduce collapse dynamics from IEEE systems  
- extract the collapse manifold  
- identify the collapse boundary (rift)  
- measure stability as distance to structure  
- visualize collapse as geometry  

---

## 🧭 Mental Model

System evolution:

→ aligns with manifold  
→ moves along rift  
→ deviates (distance ↑)  
→ branches  
→ collapses  

![Collapse Geometry](outputs/ieee14_v52_residual_vs_distance.png)

---

## 🔬 Key Concepts

| Concept | Meaning |
|--------|--------|
| Manifold | collapse attractor in phase space |
| Rift | zero-residual boundary |
| Distance | stability metric |
| Residual | deviation from structure |
| Topology | branching collapse states |

---

# 🧱 Core Framework

## Geometry → Dynamics → Topology

- Geometry → manifold  
- Field → flow dynamics  
- Dynamics → recurrence  
- Structure → resonance  
- Boundary → rift  
- Metric → distance  
- Topology → branching  

---

## Collapse Manifold

All systems converge toward:

(c, dc, d²c) → (1, 1, α)

→ **low-dimensional attractor manifold**

**Properties:**

- stable under perturbations  
- invariant across systems  
- topology-independent  

---

## Manifold Equation

d²c ≈ a · c^p · (dc)^q  

**Interpretation:**

- dc → dominant driver  
- c → modulation  
- d²c → emergent instability  

---

## Rift — Collapse Boundary

Defined by:

residual ≈ 0  

Represents:

- structural alignment  
- collapse corridor  

---

## Stability Distance

distance = min || (c, dc) − rift ||

- small → stable  
- large → unstable  

---

## Collapse Strength

collapse_strength ≈ |residual| × τ  

→ local instability intensity  

---

# 📊 Results Summary

## Universal Behavior

Across all tested systems:

- identical manifold structure  
- identical collapse geometry  
- identical clustering behavior  

---

## Scaling Law

| System | p | q |
|--------|---|---|
| IEEE9 / 14 | ~0.44 | ~0.97 |
| IEEE30 / 57 / 118 | ~0.31 | ~0.89 |

→ parameters converge  

---

## Collapse Geometry

Projection into:

(distance, residual)

reveals:

| Region | Meaning |
|--------|--------|
| Core | stable |
| Triangle | deformation |
| Polygon | branching |
| Extremes | collapse |

---

## Cluster Structure

- stable cluster  
- pre-collapse cluster  
- transition noise  

→ identical across systems  

---

## Structural Transition Sequence

1. coherence  
2. fragmentation  
3. branching  
4. instability amplification  
5. collapse  

---

## Universal Collapse Signature

- curvature peak  
- divergence spike  
- fragmentation growth  
- manifold alignment  
- distance expansion  

→ scale-invariant precursor  

---

# 🌊 Field Perspective (V68–V69)

## Vector Field Representation

F(c, dc) → local flow direction  

→ trajectories follow structured flow  

---

## Key Insight

- dc → projection of flow  
- d²c → change of flow  
- manifold → preferred paths  

---

## Geodesic Interpretation

System follows:

→ minimal-energy paths in field  

---

## GH Corridor

→ coherent flow channel  

- aligned directions  
- stable propagation  

---

## Collapse (Field View)

Collapse occurs when:

→ trajectories enter divergence regions  

---

# 📊 Visual Evidence

## Phase Space

![Phase Space](outputs/ieee14_v50_field_separation.png)

## Manifold Fit

![Fit](outputs/ieee14_v43_fit.png)

## Vector Field

![Field](outputs/ieee14_v47_vector_field.png)

## Rift Boundary

![Rift](outputs/ieee14_v51_rift_boundary.png)

## Stability Distance

![Distance](outputs/ieee14_v52_stability_distance_map.png)

---

# 🌐 Fundamental Discovery

> Collapse is governed by a universal low-dimensional structure.

---

## 🧠 Theoretical Insight

> Stability = alignment with structure  
> Collapse = loss of alignment  

---

# 🧭 Final Insight

> Systems do not fail suddenly.  
>  
> They fragment, branch, and leave the structure  
> that sustains them.  

---

# 📂 Repository Structure

## Module Navigation

APPLICATIONS/power_systems/stability_field_dynamics/
└── ieee_test_cases/
    ├── core/         → definitions, field construction
    ├── pipeline/     → processing + feature extraction
    ├── experiments/  → V1–V52 experiments
    ├── analysis/     → evaluation + metrics
    ├── outputs/      → plots, data, visualizations
    ├── logs/         → research log (entries)
    ├── results_summary.md
    ├── theory_stability_field.md
    ├── method_pipeline.md
    └── README.md

---

# 🔥 Core Insight

The equations describe what happens.  

The field determines that it happens.
