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

# 6. Transition Geometry & Basin Graph (NEW)

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

# 7. Control Methods (NEW)

NEXAH introduces **active control of transitions**.

## 7.1 Transition Control Objective

Control acts on transition probabilities:

$$
\max P(B_{source} \rightarrow B_{target})
$$

subject to:

$$
\sum_j P(B_{source} \rightarrow B_j) = 1
$$

---

## 7.2 Flow-Aligned Control

Control inputs are not arbitrary.

They must align with system dynamics:

- gradient direction  
- flow direction  
- structural constraints  

---

## 7.3 Pattern-Based Control

Control is applied as structured patterns:

- temporal gating  
- phase masks  
- adjacency constraints  

---

## 7.4 Control Propagation

Control effects propagate through system dynamics:

- local changes influence global trajectory  
- minimal intervention can yield large effects  

---

# 8. Navigation Methods (NEW)

Navigation treats the system as a **structured movement problem**.

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

The system is modeled as layered:

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

- first significant structural deviation from the stable manifold  

Baseline comparison:

- classical voltage threshold detection  

Measured result:

> NEXAH detects transitions ~43.9 seconds earlier (IEEE 300 system)

---

# 10. Robustness Evaluation

## 10.1 Noise Injection

Gaussian noise is added to system trajectories.

Evaluation:

- alignment of detected transition points  
- structural consistency across runs  

---

## 10.2 Multi-Run Stability

Repeated simulations show:

- stable transition patterns  
- preserved clustering of transition events  

---

## 10.3 Cross-System Validation

Tested on:

- Lorenz (oscillatory system)  
- IEEE grids (drift system)  

Observation:

- structure persists across system types  
- smoothing improves robustness  

---

# 11. Limitations

- results are empirical  
- no formal proof of generality  
- performance depends on system dynamics  
- sensitivity to sampling density  

---

# 12. Summary

NEXAH reconstructs:

```text
trajectory → field → geometry → stability → transitions → control → navigation
```

Key principle:

> structure is not imposed — it is extracted from dynamics

---

**Author:** Thomas K. R. Hofmann  
**Version:** v0.6.0
