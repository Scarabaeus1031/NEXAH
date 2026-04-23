# NEXAH — Methods

This document describes the computational methods used in NEXAH  
to extract structure, transitions, and stability from dynamical systems.

The goal is not to impose models, but to reconstruct structure directly from system dynamics.

---

# 1. Input Data

NEXAH operates on time-series data of dynamical systems:

$begin:math:display$
x\(t\) \\in \\mathbb\{R\}\^n
$end:math:display$

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

$begin:math:display$
F\(x\) \= \\frac\{dx\}\{dt\}
$end:math:display$

using finite differences on the trajectory.

---

## 2.2 Probability Field

A probability density $begin:math:text$ p\(x\) $end:math:text$ is estimated over state space.

Implementation:

- kernel density estimation (KDE) or histogram-based approximation  
- normalized over the observed trajectory distribution  

---

## 2.3 Energy Landscape

An effective energy function is defined as:

$begin:math:display$
E\(x\) \= \-\\log\(p\(x\)\)
$end:math:display$

Interpretation:

- high density → low energy  
- low density → high energy  

Transitions correspond to movements across energy gradients.

---

# 3. Geometric Structure Extraction

The reconstructed field is used to extract geometric structure.

## 3.1 Gradient Field

$begin:math:display$
\\nabla E\(x\)
$end:math:display$

indicates direction of steepest ascent (instability direction).

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

$begin:math:display$
\\nabla \\times F\(x\)
$end:math:display$

Observation:

- rotational structure dominates in transition regions  
- coupled with divergence dynamics  

---

## 3.4 Divergence

$begin:math:display$
\\nabla \\cdot F\(x\)
$end:math:display$

indicates:

- expansion (instability)  
- contraction (stability)  

---

## 3.5 Delayed Coupling

Empirical observation:

$begin:math:display$
\\text\{div\}\(t\) \\approx \\text\{curl\}\(t \- \\tau\)
$end:math:display$

with:

$begin:math:display$
\\tau \\approx 15
$end:math:display$

This suggests a delayed feedback between expansion and rotation.

---

# 4. Transition Detection

Transitions are not defined by thresholds on system variables.

Instead, they are identified as:

> **geometric events within the reconstructed field**

Criteria:

- high curvature of trajectory  
- deviation from dominant manifold  
- crossing of low-density regions  
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

# 6. Early Transition Detection (IEEE Systems)

In power system experiments:

- system trajectory is tracked in state space  
- field structure is reconstructed locally  
- transition indicators are monitored  

Detection point:

- first significant structural deviation from stable manifold  

Baseline comparison:

- classical voltage threshold detection  

Measured result:

> NEXAH detects transition ~43.9 seconds earlier (IEEE 300 system)

---

# 7. Robustness Evaluation

## 7.1 Noise Injection

Gaussian noise added to system trajectories.

Evaluation:

- alignment of detected transition points  
- structural consistency across runs  

---

## 7.2 Multi-Run Stability

Repeated simulations:

- transition patterns remain stable  
- peak clustering preserved  

---

## 7.3 Cross-System Validation

Tested on:

- Lorenz (oscillatory system)  
- IEEE grids (drift system)  

Observation:

- structure persists across system types  
- smoothing improves robustness  

---

# 8. Limitations

- results are empirical  
- no formal proof of generality  
- performance depends on system dynamics  
- sensitivity to sampling density  

---

# 9. Summary

NEXAH reconstructs:

```text
trajectory → field → geometry → stability → transitions
```

Key principle:

> structure is not imposed — it is extracted from dynamics

---

**Author:** Thomas K. R. Hofmann  
**Version:** v0.5.0  
