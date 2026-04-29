# NEXAH — Methods

This document describes the computational methods used in NEXAH  
to extract structure, transitions, stability, and control behavior from dynamical systems.

The goal is not to impose models, but to reconstruct structure directly from system dynamics.

---

# Method Overview

NEXAH reconstructs system structure in six stages:

1. Field Reconstruction  
2. Geometry Extraction  
3. Transition Detection  
4. Stability Representation  
5. Transition Geometry & Basin Graph  
6. Control & Navigation  

---

# 1. Input Data

NEXAH operates on time-series data of dynamical systems:

$$
x(t) \in \mathbb{R}^n
$$

Examples:

- Lorenz system (synthetic)  
- IEEE power grid models (real-world simulation)  

The system does not require:

- labeled data  
- predefined failure states  
- external control signals  

---

# 2. Field Reconstruction

The system state trajectory is transformed into a continuous field representation.

## 2.1 Local Flow

The local flow is estimated as:

$$
F(x) = \frac{dx}{dt}
$$

using finite differences on the trajectory.

---

## 2.2 Probability Field

A probability density $p(x)$ is estimated over state space.

Implementation:

- kernel density estimation (KDE) or histogram-based approximation  
- normalized over the observed trajectory distribution  

---

## 2.3 Energy Landscape

An effective energy function is defined as:

$$
E(x) = -\log(p(x))
$$

Interpretation:

- high density → low energy  
- low density → high energy  

Transitions correspond to movements across energy gradients.

---

# 3. Geometric Structure Extraction

The reconstructed field is used to extract geometric structure.

## 3.1 Gradient Field

$$
\nabla E(x)
$$

indicates the direction of steepest ascent (instability direction).

---

## 3.2 Flow Geometry

The system identifies:

- **basins** → regions of convergence  
- **channels** → preferred transition paths  
- **separatrices** → boundaries between regimes  

These are derived from:

- density gradients  
- trajectory clustering  
- local flow alignment  

---

## 3.3 Rotational Dynamics

The curl of the flow field is approximated:

$$
\nabla \times F(x)
$$

Observation:

- rotational structure dominates in transition regions  
- coupled with divergence dynamics  

---

## 3.4 Divergence

$$
\nabla \cdot F(x)
$$

indicates:

- expansion (instability)  
- contraction (stability)  

---

## 3.5 Delayed Coupling

Empirical observation:

$$
\text{div}(t) \approx \text{curl}(t - \tau)
$$

with:

$$
\tau \approx 15
$$

This suggests a delayed feedback between expansion and rotation.

---

# 4. Transition Detection

Transitions are not defined by thresholds on system variables.

Instead, they are identified as:

> **geometric events within the reconstructed field**

Criteria:

- high curvature of trajectory  
- deviation from dominant manifold  
- crossing of low-density regions (greyspace)  
- alignment with separatrix structures  

These signals are combined into a transition score.

---

# 5. Stability Representation

Stability is not a scalar value.

It is represented as:

> **a spatial structure within the field**

Characteristics:

- basins → stable regions  
- boundaries → weakly stable regions  
- channels → transition corridors  

No explicit binary classification is used.

---

# 6. Transition Geometry & Basin Graph

Beyond continuous fields, NEXAH extracts a **discrete transition structure**.

## 6.1 Basin Decomposition

State space is partitioned into:

$$
\{B_1, B_2, ..., B_k\}
$$

Each basin represents a stable regime.

---

## 6.2 Transition System

Transitions are modeled as:

$$
P(B_i \rightarrow B_j)
$$

Estimated from observed trajectory transitions.

---

## 6.3 Gate Detection

Transitions do not occur uniformly.

They occur through structured regions:

> **Gates = directional transition corridors**

Detection signals:

- local stability weakening (Lyapunov peaks)  
- boundary curvature  
- transition density concentration  

---

## 6.4 Basin Graph

The system is represented as a graph:

```text
Nodes: basins
Edges: feasible transitions (gates)
```

Constraints:

- only adjacent basins are reachable  
- transition probabilities are structured  

---

# 7. Control Methods

NEXAH introduces **active interaction with transition structure**,  
but not unconstrained control.

## 7.1 Control Objective

Control is formulated as influencing transition behavior:

$$
\max P(B_{source} \rightarrow B_{target})
$$

subject to:

$$
\sum_j P(B_{source} \rightarrow B_j) = 1
$$

---

## 7.2 Flow-Aligned Control

Control inputs must align with system structure:

- gradient direction  
- flow direction  
- transition geometry  

---

## 7.3 Pattern-Based Control

Control is applied as structured patterns:

- temporal gating  
- phase alignment  
- adjacency constraints  

---

## 7.4 Control Propagation

Local perturbations may propagate through system dynamics:

- local deformation of trajectories  
- alignment with flow channels  

However, propagation is constrained by field geometry.

---

# 🔒 7.5 Constraint Behavior (Experimental Update)

Recent experimental results (Builder Lab, runs 033–040) refine the control model.

## Observation

```text
perturbation → local deviation → absorption → re-alignment
```

- deviations remain localized  
- no persistent redirection occurs  
- no regime transitions achieved internally  

---

## Interpretation

```text
Control does not freely modify system dynamics.
```

Instead:

```text
Control interacts with a constraint structure.
```

---

## Structural Model

The system evolves on an implicit manifold:

```text
x(t) ∈ M
```

Control acts as:

```text
u(x) → deformation within M
```

NOT:

```text
u(x) → arbitrary trajectory change
```

---

## Key Result

```text
The system is navigable,
but not freely controllable from within.
```

---

## Updated Control Principle

```text
Do not force transitions.

Align with the geometry that permits them.
```

---

# 8. Navigation Methods

Navigation treats the system as a **structured movement problem**.

## Constraint Note

```text
Navigation does not represent free path selection.

It traces trajectories allowed by the field geometry.
```

---

## 8.1 Navigation Field

A composite navigation field is defined:

```math
u =
- ∇P(IOTA)
+ ∇T
+ ∇ρ
```

---

## 8.2 Phase-Aware Navigation

Transitions depend on phase:

$$
P(gate \mid \theta)
$$

This introduces:

- timing constraints  
- phase-dependent accessibility  

---

## 8.3 Sheet-Based Dynamics

The system is layered:

- core → stable motion  
- intermediate → oscillatory  
- outer → instability  

Transitions occur via:

- sheet interactions  
- switching behavior  

---

## 8.4 Path Planning

Navigation operates on:

- basin graph  
- gate structure  
- probability constraints  

---

# 9. Early Transition Detection (IEEE Systems)

In power system experiments:

- system trajectory is tracked in state space  
- field structure is reconstructed locally  
- transition indicators are monitored  

Detection point:

- first structural deviation from stable manifold  

Baseline:

- classical voltage threshold detection  

Result:

> NEXAH detects transitions earlier (empirical observation)

---

# 10. Robustness Evaluation

## 10.1 Noise Injection

- Gaussian noise applied  
- structural consistency evaluated  

---

## 10.2 Multi-Run Stability

- stable transition patterns  
- preserved clustering  

---

## 10.3 Cross-System Validation

Tested on:

- Lorenz  
- IEEE systems  

Observation:

- structure persists across systems  

---

# 11. Limitations

- empirical method  
- no formal proof of generality  
- sampling-dependent  
- finite-time approximations  

---

# 12. Summary

NEXAH reconstructs:

```text
trajectory → field → geometry → stability → transitions → constrained control → navigation
```

---

## Core Principle

> Structure is not imposed — it is extracted.

---

## Final Insight

```text
Systems do not offer arbitrary control.

They define constrained paths,
and control must align with them.
```

---

**Author:** Thomas K. R. Hofmann  
**Version:** v0.7.0
