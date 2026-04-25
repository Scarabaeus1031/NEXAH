# 📐 NEXAH — Mathematical Foundation  
## Field-Based Transition Detection & Navigation

---

# 📍 Scope

This document defines the **core mathematical structure** of the NEXAH system.

Goal:

```text
Provide a minimal, reproducible framework for detecting,
characterizing, and navigating transitions in dynamical systems
```

---

# 🧠 Core Principle

A dynamical system does not collapse randomly.

```text
Transitions occur when the system leaves a stable manifold
and enters a structurally unstable region of state space.
```

---

# 🔹 1. State Representation

We embed a time series $begin:math:text$ x\(t\) $end:math:text$ into phase space:

$$
r(t) = \sqrt{x(t)^2 + \dot{x}(t)^2}
$$

$$
\theta(t) = \arctan2(\dot{x}(t), x(t))
$$

---

---

## 🔹 2. Derived Quantities

---

### 2.1 Flow (Local Dynamics)

We define the local flow in phase space:

$$
\frac{dr}{d\theta}
$$

This quantity captures how the system evolves geometrically along its trajectory.

---

### 2.2 Density Field

We estimate a density over state space:

$$
\rho(r, \theta)
$$

Interpretation:

- high density → stable manifold  
- low density → unstable region  

---

### 2.3 Greyspace (Instability Proxy)

Defined as inverse density:

$$
G(r, \theta) = \frac{1}{\rho(r, \theta)}
$$

Interpretation:

```text
High G → structural gap (instability corridor)
Low G  → stable region
```

---

### 2.4 Risk Field (Probabilistic Instability)

We define a continuous instability field:

$$
P(\text{IOTA} \mid r, \theta)
$$

This represents the probability of a transition event at a given state.

---

## 🔹 3. Structural Elements

---

### 3.1 Ridge (Stable Structure)

Define ridge as regions of locally maximal density:

$$
\text{ridge} = \{(r, \theta) \mid \rho(r, \theta) \text{ is locally maximal}\}
$$

Interpretation:

```text
Ridges approximate stable manifolds / attractor remnants
```

---

### 3.2 Ridge Distance

Distance from a point to the nearest ridge:

$$
D(r, \theta) = \min_{(r', \theta') \in \text{ridge}} \| (r, \theta) - (r', \theta') \|
$$

---

### 3.3 Sheets (Flow Layers)

The system organizes into locally coherent flow layers:

```text
sheet = region with consistent directional flow
```

Multiple sheets may overlap in state space.

---

## 🔹 4. Event Definition

---

### 4.1 IOTA (Transition Event)

An IOTA event is defined as:

$$
\left| \frac{dr}{d\theta} \right| > \tau
$$

where:

- $\tau$ is a high percentile threshold (e.g. 98%)

---

### 4.2 IOTA Classification

Each event is classified via:

- Greyspace $G$
- Ridge distance $D$

---

#### Boundary Collapse

$$
G \leq G_c \quad \text{and/or} \quad D \leq D_c
$$

```text
Break occurs along structural boundary
```

---

#### Gap Escape

$$
G > G_c \quad \text{and} \quad D > D_c
$$

```text
System enters low-density region
```

---

## 🔹 5. Transition Condition

A transition region satisfies:

$$
G(r, \theta) \text{ high}
$$

$$
\left| \frac{dr}{d\theta} \right| \text{ high}
$$

$$
D(r, \theta) > 0
$$

---

### Interpretation

```text
Transition =
low density
+ unstable flow
+ separation from structure
```

---

## 🔹 6. Navigation Model

---

### 6.1 Risk Avoidance

Define steering via risk gradient:

$$
u_{risk}(r, \theta) = -\nabla P(\text{IOTA})
$$

---

### 6.2 Target Attraction

Let $T(r, \theta)$ denote stable target regions.

$$
u_{target} = \nabla T(r, \theta)
$$

---

### 6.3 Combined Steering

$$
u(r, \theta) =
- \nabla P(\text{IOTA})
+ \nabla T(r, \theta)
$$

---

## 🔹 7. Extended Navigation (Structure-Aware)

Include structural alignment:

$$
u =
- \nabla P(\text{IOTA})
+ \nabla T(r, \theta)
+ \nabla \rho(r, \theta)
$$

---

### Interpretation

```text
Navigation balances:

- avoid instability
- move toward stability
- follow structural manifold
```

---

## 🔹 8. Transition Mechanism (Unified)

A full transition unfolds as:

```text
1. density decreases        (ρ ↓)
2. greyspace increases      (G ↑)
3. flow destabilizes        (|dr/dθ| ↑)
4. IOTA events occur
5. system leaves ridge
6. trajectory reorganizes
```

---

## 🔹 9. Minimal Pipeline

```text
Signal x(t)
→ Phase embedding (r, θ)
→ Density field ρ
→ Greyspace G
→ Ridge detection
→ Ridge distance D
→ Flow derivative dr/dθ
→ IOTA detection
→ Risk field P(IOTA)
→ Navigation field u
```

---

## 🔹 10. Key Properties

---

### No explicit system model required

```text
Method is data-driven
```

---

### No fixed thresholds required (in principle)

```text
Fields can be continuous
```

---

### Structure emerges from data

```text
geometry replaces heuristics
```

---

## 🔹 Final Statement

$$
\text{Transition} =
\text{Loss of structural anchoring}
+ \text{Entry into instability field}
$$

---

## 🔹 Interpretation

```text
A system does not collapse.

It leaves the manifold on which it was stable.
```

---
