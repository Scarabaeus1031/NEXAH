# 📐 NEXAH — Mathematical Foundation  
## Field-Based Transition Detection & Navigation

---

# 📍 Scope

This document defines the core mathematical structure of the NEXAH system.

Goal:

```text
Provide a minimal, reproducible framework for detecting,
characterizing, and navigating transitions in dynamical systems.
```

---

# 🧠 Core Principle

A dynamical system does not collapse randomly.

```text
Transitions occur when the system leaves a stable manifold
and enters a structurally unstable region of state space.
```

This framework is empirical and data-driven. It is not derived from first principles.

---

# 🔹 1. State Representation

We embed a time series $begin:math:text$x\(t\)$end:math:text$ into phase space:

$$
r(t) = \sqrt{x(t)^2 + \dot{x}(t)^2}
$$

$$
\theta(t) = \arctan2(\dot{x}(t), x(t))
$$

---

## State Vector

We define the system state as:

$$
s(t) = \big(r(t), \theta(t)\big)
$$

Interpretation:

```text
The system is represented as a trajectory in 2D state space.
```

- $begin:math:text$r\(t\)$end:math:text$ → energy / amplitude  
- $begin:math:text$\\theta\(t\)$end:math:text$ → phase position  

Optional higher-dimensional extension:

$$
s(t) = \big(r(t), \theta(t), \dot{r}(t), \dot{\theta}(t)\big)
$$

---

# 🔹 2. Derived Quantities

## 2.1 Flow

We define local flow along the trajectory as:

$$
\frac{dr}{d\theta}
=
\frac{\frac{dr}{dt}}{\frac{d\theta}{dt}}
$$

This captures how the radius changes relative to phase motion.

---

## 2.2 Density Field

We estimate a density over state space:

$$
\rho(r, \theta)
$$

Density is estimated empirically, for example by histogram approximation or kernel density estimation.

Interpretation:

- high density → stable manifold / recurrent structure  
- low density → unstable region / transition corridor  

---

## 2.3 Greyspace

Greyspace is defined as inverse density:

$$
G(r, \theta) = \frac{1}{\rho(r, \theta)}
$$

Interpretation:

```text
High G → structural gap / instability corridor
Low G  → stable region / dense manifold
```

---

## 2.4 Risk Field

We define a continuous instability field:

$$
P(\text{IOTA} \mid r, \theta)
$$

This estimates the probability of a transition event at a given state.

Empirically:

```text
P(IOTA | r, θ) is estimated from observed IOTA frequency
or instability scores in local neighborhoods of state space.
```

---

# 🔹 3. Structural Elements

## 3.1 Ridge

A ridge is a region of locally maximal density:

$$
\text{ridge}
=
\{(r,\theta) \mid \rho(r,\theta) \text{ is locally maximal}\}
$$

More formally:

$$
\nabla \rho(r,\theta) \approx 0
$$

with local maximum behavior in the density field.

Interpretation:

```text
Ridges approximate stable manifolds or attractor remnants.
```

---

## 3.2 Ridge Distance

Distance from a point to the nearest ridge:

$$
D(r,\theta)
=
\min_{(r',\theta') \in \text{ridge}}
\left\|
(r,\theta) - (r',\theta')
\right\|_2
$$

---

## 3.3 Sheets

Sheets are locally coherent flow layers:

```text
sheet = region with consistent directional flow
```

Multiple sheets may overlap in state space.

---

# 🔹 4. Event Definition

## 4.1 IOTA

An IOTA event is defined as a strong local transition event:

$$
\left|
\frac{dr}{d\theta}
\right|
> \tau
$$

where $begin:math:text$\\tau$end:math:text$ is a high empirical percentile threshold, for example the 98th percentile.

---

## 4.2 IOTA Classification

Each IOTA event is classified using:

- Greyspace $begin:math:text$G$end:math:text$
- Ridge distance $begin:math:text$D$end:math:text$

---

### Boundary Collapse

$$
G \leq G_c
\quad \text{and/or} \quad
D \leq D_c
$$

Interpretation:

```text
The system breaks along a structural boundary.
```

---

### Gap Escape

$$
G > G_c
\quad \text{and} \quad
D > D_c
$$

Interpretation:

```text
The system escapes into a low-density region.
```

---

# 🔹 5. Transition Condition

A transition region is characterized by:

$$
G(r,\theta) \text{ high}
$$

$$
\left|
\frac{dr}{d\theta}
\right|
\text{ high}
$$

$$
D(r,\theta) > 0
$$

Interpretation:

```text
Transition =
low density
+ unstable flow
+ separation from structure
```

---

# 🔹 6. Navigation Model

## 6.1 Risk Avoidance

Define steering away from instability:

$$
u_{\text{risk}}(r,\theta)
=
-\nabla P(\text{IOTA})
$$

---

## 6.2 Target Attraction

Let $begin:math:text$T\(r\,\\theta\)$end:math:text$ denote stable target regions.

$$
u_{\text{target}}(r,\theta)
=
\nabla T(r,\theta)
$$

---

## 6.3 Combined Steering

$$
u(r,\theta)
=
-\nabla P(\text{IOTA})
+
\nabla T(r,\theta)
$$

The control vector $begin:math:text$u$end:math:text$ is applied incrementally to the trajectory in discretized time steps.

---

# 🔹 7. Structure-Aware Navigation

Include structural alignment:

$$
u(r,\theta)
=
-\nabla P(\text{IOTA})
+
\nabla T(r,\theta)
+
\nabla \rho(r,\theta)
$$

Interpretation:

```text
Navigation balances:

- avoid instability
- move toward stable targets
- follow structural manifolds
```

---

# 🔹 8. Transition Mechanism

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

# 🔹 9. Minimal Pipeline

```text
Signal x(t)
→ Phase embedding (r, θ)
→ State vector s(t)
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

# 🔹 10. Key Properties

## Data-driven

```text
No explicit system model is required.
```

## Field-based

```text
Instability is represented as a continuous field.
```

## Structure-aware

```text
Geometry replaces pure threshold logic.
```

## Navigable

```text
The system can be guided away from instability regions
and toward stable structures.
```

---

# 🔹 Final Statement

$$
\text{Transition}
=
\text{Loss of structural anchoring}
+
\text{Entry into instability field}
$$

---

# 🔹 Interpretation

```text
A system does not collapse.

It leaves the manifold on which it was stable.
```

---
