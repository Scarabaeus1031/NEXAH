# 📐 NEXAH — Mathematical Foundation  
## Field-Based Transition Detection, Prediction & Control

---

# 📍 Scope

This document defines the mathematical structure of the NEXAH system.

Goal:

```text
Provide a minimal, reproducible framework for detecting,
characterizing, predicting, and controlling transitions
in dynamical systems.
```

---

# 🧠 Core Principle

A dynamical system does not collapse randomly.

```text
Transitions occur when the system leaves a stable manifold
and enters a structurally unstable region of state space.
```

Extended:

```text
Transitions are state-dependent, structured, and controllable.
```

---

# 🔹 1. State Representation

Given a time series $x(t)$, we define a transformation into polar phase space:

---

## Phase Transformation

$$
r(t) = \sqrt{x(t)^2 + \dot{x}(t)^2}
$$

$$
\theta(t) = \arctan2(\dot{x}(t), x(t))
$$

---

## State Vector

$$
s(t) = (r(t), \theta(t))
$$

---

## Interpretation

```text
The system is mapped into a rotational state space:

- r(t)     → amplitude / energy
- θ(t)     → phase / rotation

This transformation defines the geometric domain
in which dynamics are analyzed.
```

---

## 🔥 Key Property

```text
θ is a rotational coordinate:

θ ∈ [0, 2π]

→ the system evolves on a circular / cylindrical geometry
```

---

# 🔹 1.1 Rotational Geometry and π

---

## Rotational Structure

$$
\theta(t + \Delta t) = \theta(t) + \omega(t)
$$

$$
\omega(t) = \frac{d\theta}{dt}
$$

---

## Interpretation

```text
The system is not only evolving in time,
but rotating in state space.

The coordinate θ introduces a continuous rotational symmetry.
```

---

## 🔥 Role of π

```text
π defines the geometry of rotation.

It is not causing instability,
but defining the space in which dynamics unfold.
```

---

## Key Insight

```text
π → perfect rotational symmetry

NEXAH → detects where this symmetry breaks
```

---

## Formal Observation

$$
P(\text{IOTA} \mid \theta) \neq \text{const}
$$

---

## Interpretation

```text
Instability is not isotropic.

It depends on phase → symmetry is broken.
```

---

# 🔹 2. Continuous Field Representation

---

## 2.1 Flow Field

$$
F(s) =
\left(
\frac{dr}{dt},
\frac{d\theta}{dt}
\right)
$$

Alternative:

$$
\frac{dr}{d\theta} =
\frac{\frac{dr}{dt}}{\frac{d\theta}{dt}}
$$

---

## 2.2 Density Field

$$
\rho(r, \theta)
$$

---

## Interpretation

```text
High density → stable manifold  
Low density → transition corridor
```

---

## 2.3 Greyspace (Instability Field)

$$
G(r, \theta) = \frac{1}{\rho(r, \theta)}
$$

---

## 2.4 Risk Field

$$
P(\text{IOTA} \mid r, \theta)
$$

---

## 🔥 Core Insight

```text
Instability is not an event

It is a continuous field
```

---

# 🔹 3. Structural Geometry

---

## 3.1 Ridge (Stable Structure)

$$
\nabla \rho(r,\theta) \approx 0
\quad \text{(local maxima)}
$$

---

## 3.2 Ridge Distance

$$
D(r,\theta) =
\min_{s' \in \text{ridge}} \| s - s' \|
$$

---

## 3.3 Sheets (Layered Dynamics)

$$
\mathcal{S}_i = \{ (r,\theta) \mid r \approx r_i \}
$$

---

## Sheet Index

$$
\text{sheet}(r) = \arg\min_i |r - r_i|
$$

---

## Interpretation

```text
Each sheet = locally coherent flow regime
```

---

# 🔹 4. Event Definition

---

## 4.1 IOTA Event

$$
\left|\frac{dr}{d\theta}\right| > \tau
$$

---

## 4.2 Transition Region

```text
low density + high flow + structural separation
```

---

# 🔹 5. Discrete Structure (Basins)

---

## Basin Decomposition

$$
B_i \subset (r, \theta)
$$

---

## Basin Assignment

$$
\text{basin}(s) = \arg\min_i \| s - c_i \|
$$

---

## Interpretation

```text
Each basin represents a stable dynamical regime
```

---

# 🔹 6. Transition System

---

## 6.1 Transition Matrix

$$
P(B_i \rightarrow B_j)
$$

---

## Constraint

$$
\sum_j P(B_i \rightarrow B_j) = 1
$$

---

## Interpretation

```text
System behaves as a Markov process over basins
```

---

# 🔹 7. Prediction

---

## Next-State Prediction

$$
\hat{B}_{t+1} =
\arg\max_j P(B_t \rightarrow B_j)
$$

---

# 🔹 8. Control Field (Continuous)

---

## 8.1 Risk Avoidance

$$
u_{\text{risk}} = -\nabla P(\text{IOTA})
$$

---

## 8.2 Structure Attraction

$$
u_{\text{structure}} = \nabla \rho
$$

---

## 8.3 Target Field

$$
u_{\text{target}} = \nabla T(r,\theta)
$$

---

## Combined Field

$$
u =
-\nabla P(\text{IOTA})
+
\nabla \rho
+
\nabla T
$$

---

# 🔹 9. π-Consistency (Rotational Control)

---

## Turning Rate

$$
\Delta \theta_t = \theta_{t+1} - \theta_t
$$

---

## Control

$$
u_{\pi} = -k_{\theta} \cdot \Delta \theta
$$

---

## Interpretation

```text
π enforces smooth rotational flow
```

---

# 🔹 10. Sheet Control

---

## Radial Transition

$$
u_{\text{sheet}} \sim (r_{\text{next}} - r)
$$

---

## Insight

```text
Instability correlates with sheet switching
```

---

# 🔹 11. Multi-Operator Control

---

## Combined Control

$$
u =
w_{\pi} u_{\pi}
+
w_{\text{risk}} u_{\text{risk}}
+
w_{\text{sheet}} u_{\text{sheet}}
+
w_{\text{target}} u_{\text{target}}
$$

---

## Interpretation

```text
Control is state-adaptive and multi-dimensional
```

---

# 🔹 12. Gate Navigation

---

## Gate Direction

$$
u_{\text{gate}} \sim \nabla d_{\text{gate}}
$$

---

## Insight

```text
Gates are directional structures, not static targets
```

---

# 🔹 13. Discrete Control (Transition Layer)

---

## Control Objective

$$
\max P(B_s \rightarrow B_t)
$$

---

## Interpretation

```text
Control redistributes transition probabilities
```

---

# 🔹 14. Temporal Control

---

$$
u(t) = m(t) \cdot u
$$

---

## Interpretation

```text
Control effectiveness depends on timing and phase
```

---

# 🔹 15. Transition Mechanism (Unified)

```text
1. density decreases        (ρ ↓)
2. greyspace increases      (G ↑)
3. flow destabilizes        (|dr/dθ| ↑)
4. trajectory loses alignment
5. ridge structure breaks
6. basin transition occurs
7. system reconfigures
```

---

# 🔹 16. NEXAH Kernel

---

## System Decomposition

```text
ARCHY   → system dynamics
FIELD   → continuous geometry
GRAPH   → basin structure
KERNEL  → navigation
```

---

---

# 🔹 17. Unified Field Control (v38+)

---

## 🧠 Motivation

Previous control layers operate on:

```text
- local gradients (∇P, ∇ρ)
- structural alignment (π, sheets)
- directional gates
```

However:

```text
control is still fragmented
```

We now define a **unified control formulation**.

---

## 🔹 17.1 Full Control Field

$$
u(s) =
- \nabla P(\text{IOTA})
+ \nabla \rho
+ u_{\pi}
+ u_{\text{sheet}}
+ u_{\text{gate}}
+ u_{\text{graph}}
$$

---

## Components

### Risk Avoidance

$$
-\nabla P(\text{IOTA})
$$

→ repels trajectory from instability regions  

---

### Structure Attraction

$$
\nabla \rho
$$

→ pulls trajectory toward stable manifolds  

---

### Rotational Consistency

$$
u_{\pi} = -k_{\theta} \cdot \Delta \theta
$$

→ enforces smooth angular evolution  

---

### Sheet Alignment

$$
u_{\text{sheet}} \sim (r_{\text{target}} - r)
$$

→ controls radial layer transitions  

---

### Gate Direction

$$
u_{\text{gate}} \sim v_{\text{gate}}(s)
$$

→ aligns trajectory with transition direction  

---

### Graph Control (NEW)

$$
u_{\text{graph}} \sim \nabla P(B_i \rightarrow B_j)
$$

→ shapes transition probabilities between basins  

---

## 🔥 Core Insight

```text
Control is not a single force.

It is a composition of:

geometry + probability + topology + direction
```

---

# 🔹 17.2 Gate Formalization (NEW)

---

## Definition

A gate is defined as a **directed transition manifold**:

$$
\mathcal{G} =
\{ (s, v) \mid
\text{alignment}(v, F(s)) > 0
\ \land \
\text{barrier}(s) \text{ minimal}
\}
$$

---

## Interpretation

```text
Gate ≠ point in space

Gate = (position + direction + local flow condition)
```

---

## Alignment Condition

$$
\text{alignment} =
\frac{v_{\text{current}} \cdot v_{\text{gate}}}
{\|v_{\text{current}}\| \|v_{\text{gate}}\|}
$$

---

## 🔥 Core Insight

```text
Transitions require directional agreement with system flow
```

---

# 🔹 17.3 Trajectory as Optimization Problem

---

## Objective

Trajectory is defined as minimizing a global functional:

$$
\mathcal{J} =
\int
\Big(
\alpha \, P(\text{IOTA})
+ \beta \, D_{\text{ridge}}
+ \gamma \, (1 - \text{alignment})
\Big)
dt
$$

---

## Terms

- $P(\text{IOTA})$ → instability exposure  
- $D_{\text{ridge}}$ → distance from structure  
- alignment → directional mismatch  

---

## Interpretation

```text
Optimal trajectory balances:

- low risk
- structural alignment
- directional consistency
```

---

## 🔥 Critical Insight

```text
Trajectory is not simulated.

It is optimized within a structured field.
```

---

# 🔹 17.4 Field–Graph Duality

---

## Continuous Layer

$$
(r, \theta) \rightarrow \rho, P(\text{IOTA}), F(s)
$$

---

## Discrete Layer

$$
B_i \rightarrow B_j
$$

---

## Coupling

$$
P(B_i \rightarrow B_j) =
\int_{\mathcal{G}_{ij}} P(\text{IOTA} \mid s) \, ds
$$

---

## Interpretation

```text
Discrete transitions emerge from continuous field structure
```

---

## 🔥 Core Insight

```text
Field and graph are dual representations
of the same system
```

---

# 🔹 17.5 Final Control Interpretation

---

```text
System evolution = navigation through:

- continuous field (geometry)
- transition graph (topology)
- directional gates (flow constraints)
```

---

## Final Unified Law

$$
\text{Trajectory} =
f(
F(s),
\nabla P,
\nabla \rho,
\mathcal{G},
P(B_i \rightarrow B_j)
)
$$

---

## 🔥 Final Insight

```text
Control does not push the system.

It aligns it with the structure
through which it must move.
```

---

## Unified Control Law

$$
u =
-\nabla P(\text{IOTA})
+
\nabla \rho
+
u_{\pi}
+
u_{\text{sheet}}
+
u_{\text{gate}}
$$

---

## 🔥 Core Insight

```text
A system does not evolve in time

It navigates a structured state space
```

---

# 🔹 Final Statement

$$
\text{Transition} =
\text{Field Navigation}
+
\text{Loss of Structural Alignment}
+
\text{Discrete Basin Transition}
$$

---

# 🧭 Final Summary

```text
Signal
→ Phase
→ Geometry
→ Density
→ Greyspace
→ Flow
→ Sheets
→ Basins
→ Transitions
→ Probability field
→ Control field
→ π-consistency
→ Sheet alignment
→ Gate alignment
→ NEXAH Kernel
```

---

## 🔥 Closing Statement

```text
We do not simulate systems.

We navigate them.
```

---

# 🔹 Theorem Layer (Working)

The structural behavior of the NEXAH system is further formalized in:

📄 `RESEARCH/FOUNDATION/structural_theorems.md`

This includes:

- coherence-based stability conditions  
- transition structure theorems  
- flow and geometry constraints  

⚠️ These statements are currently:

- empirically supported  
- structurally consistent  
- not yet formally proven  

They define the **emerging theoretical layer** of NEXAH.

---

© Thomas K. R. Hofmann  
NEXAH — 2026
