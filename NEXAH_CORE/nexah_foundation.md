# 📐 NEXAH — Mathematical Foundation  
## Field-Based Transition Detection, Prediction & Control

---

# 📍 Scope

This document defines the core mathematical structure of the NEXAH system.

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

Extended (v55):

```text
Transitions are state-dependent, structured, and controllable.
```

---

# 🔹 1. State Representation

We embed a time series $x(t)$ into phase space:

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

Interpretation:

```text
Trajectory in polar phase space
```

---

# 🔹 2. Derived Fields

---

## 2.1 Flow

$$
\frac{dr}{d\theta}
=
\frac{\frac{dr}{dt}}{\frac{d\theta}{dt}}
$$

---

## 2.2 Density Field

$$
\rho(r, \theta)
$$

Interpretation:

```text
High density → stable structure  
Low density → transition corridor
```

---

## 2.3 Greyspace

$$
G(r, \theta) = \frac{1}{\rho(r, \theta)}
$$

---

## 2.4 Risk Field

$$
P(\text{IOTA} \mid r, \theta)
$$

Interpretation:

```text
Continuous instability probability field
```

---

# 🔹 3. Structural Geometry

---

## 3.1 Ridge

$$
\nabla \rho(r,\theta) \approx 0
\quad \text{(local maxima)}
$$

---

## 3.2 Ridge Distance

$$
D(r,\theta) =
\min_{(r',\theta') \in \text{ridge}}
\| (r,\theta) - (r',\theta') \|
$$

---

## 3.3 Sheets

```text
Locally coherent flow layers
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

# 🔹 5. Basin Structure (v44+)

State space decomposes into discrete regions:

$$
B_i \subset (r, \theta)
$$

Each basin represents:

```text
stable dynamical regime
```

---

## Basin Assignment

$$
\text{basin}(s) = \arg\min_i \| s - c_i \|
$$

where $c_i$ are basin centroids.

---

# 🔹 6. Transition System

---

## 6.1 Transition Matrix

$$
P(B_i \rightarrow B_j)
$$

Estimated from observed transitions.

---

## 6.2 Transition Constraints

$$
\sum_j P(B_i \rightarrow B_j) = 1
$$

---

## Interpretation

```text
System behaves as a Markov transition process over basins
```

---

# 🔹 7. Prediction Model (v46)

Given current basin:

$$
B_t \rightarrow B_{t+1}
$$

Prediction:

$$
\hat{B}_{t+1} = \arg\max_j P(B_t \rightarrow B_j)
$$

---

# 🔹 8. Navigation Field

---

## 8.1 Risk Avoidance

$$
u_{\text{risk}} = -\nabla P(\text{IOTA})
$$

---

## 8.2 Target Attraction

$$
u_{\text{target}} = \nabla T(r,\theta)
$$

---

## 8.3 Combined Field

$$
u =
-\nabla P(\text{IOTA})
+
\nabla T
+
\nabla \rho
$$

---

# 🔹 9. Transition Control (v49+)

---

## 9.1 Control Objective

$$
\max \; P(B_s \rightarrow B_t)
$$

---

## 9.2 Control Input

$$
u =
\alpha \, u_{\text{base}}
+
\beta \, u_{\text{target}}
$$

---

## 9.3 Constrained System

$$
\sum_j P(B_s \rightarrow B_j) = 1
$$

---

## Interpretation

```text
Control redistributes transition probabilities
```

---

# 🔹 10. Temporal Control (v52–v53)

Control is time-dependent:

$$
u(t) = m(t) \cdot u
$$

where:

```text
m(t) ∈ {0,1}
```

or multi-phase:

```text
engage → lock → release → next
```

---

# 🔹 11. Topological Constraint (v54)

Allowed transitions:

$$
B_i \rightarrow B_j \quad \text{only if } j \in \text{Adj}(i)
$$

---

# 🔹 12. Resonance Control (v55)

Let natural distribution:

$$
P_{\text{nat}}(B_s \rightarrow B_j)
$$

Control aligns with:

$$
u \sim P_{\text{nat}}
$$

---

## Interpretation

```text
Control is most effective when aligned with natural dynamics
```

---

# 🔹 13. Transition Mechanism (Unified)

```text
1. density decreases        (ρ ↓)
2. greyspace increases      (G ↑)
3. flow destabilizes        (|dr/dθ| ↑)
4. IOTA events occur
5. system leaves ridge
6. enters basin transition regime
7. transition probabilities shift
8. new basin reached
```

---

# 🔹 14. Minimal Pipeline (Updated)

```text
Signal x(t)
→ Phase embedding (r, θ)
→ Density ρ
→ Greyspace G
→ Risk field P(IOTA)
→ Ridge / structure
→ Basin segmentation
→ Transition matrix P(B_i → B_j)
→ Prediction
→ Control
```

---

# 🔹 15. Key Properties (Updated)

---

## Field-based

```text
continuous instability representation
```

## Discrete structure

```text
basins + transitions
```

## Predictive

```text
future state estimation possible
```

## Controllable

```text
transition probabilities can be modified
```

---

# 🔹 Final Statement (v55)

$$
\text{Transition} =
\text{Loss of structural anchoring}
+
\text{Entry into instability field}
+
\text{Probabilistic transition between basins}
$$

---

# 🔹 Interpretation

```text
A system does not collapse.

It leaves one structured regime
and transitions into another.
```

---

© Thomas K. R. Hofmann  
NEXAH — 2026
