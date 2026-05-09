# 🧠 NEXAH — Core Variable Map

## 🧭 Purpose

This document defines the **minimal operational variable set**
used throughout the NEXAH framework.

It serves as:

- the structural alphabet of NEXAH  
- the bridge between concepts and equations  
- the shared notation layer across modules  
- the semantic interface between dynamics, structure, and navigation  

---

# 🔤 Core Principle

NEXAH does not begin with isolated equations.

It begins with:

```text
observable relationships between motion,
structure,
transitions,
and control
```

The variables below represent the minimal operational quantities
currently used to describe these relationships.

---

# 🧭 Structural Grammar Overview

![NEXAH Structural Grammar](./visuals/NEXAH_STRUCTURAL_GRAMMAR_MAP.png)

---

## Interpretation

The structural grammar map visualizes how:

```text
dynamics
→ structure
→ coherence
→ transitions
→ navigation
```

emerge as interconnected layers.

It acts as the current operational atlas of the NEXAH variable system.

---

# 🌌 System Atlas

![NEXAH System Atlas](./visuals/NEXAH_SYSTEM_ATLAS.png)

---

## Interpretation

The atlas connects:

- flow fields  
- density structures  
- gates  
- transition manifolds  
- navigation paths  
- control mechanisms  

into a unified operational geometry.

It represents the current large-scale structural overview
of the NEXAH framework.

---

# 🧩 Core Variables

| Variable | Meaning | Role |
|---|---|---|
| $x$ | system state | local position in system space |
| $\dot{x}$ | state velocity | local motion |
| $F(x)$ | flow field | intrinsic system dynamics |
| $A(x)$ | acceleration / change dynamics | variation of motion |
| $\rho(x)$ | density field | occupancy / structural persistence |
| $\nabla \rho(x)$ | density gradient | structural drift direction |
| $C(x)$ | coherence | alignment with local flow |
| $R(x)$ | residence structure | local persistence behavior |
| $G(x)$ | gate score | transition susceptibility |
| $T(x)$ | transition tension | transition activation field |
| $J(x)$ | Janus field | coupled directional structure |
| $M(t)$ | mismatch | deviation from expected evolution |
| $I(t)$ | instability magnitude | local dynamical intensity |
| $\phi(t)$ | phase | rotational progression |
| $\omega(t)$ | phase velocity | temporal phase motion |
| $\hat{\omega}(t)$ | expected phase velocity | local structural expectation |
| $s(t)$ | control signal | external intervention |
| $\Delta(t)$ | structural change | observable transition proxy |
| $P(\text{IOTA})$ | transition probability | transition activation likelihood |

---

# 🔷 1. State Variable

## Definition

$$
x \in \mathbb{R}^n
$$

---

## Interpretation

```text
x describes the current local configuration of the system.
```

Examples:

- phase-space position  
- system configuration  
- trajectory coordinate  
- latent state  

---

# 🔷 2. Velocity

## Definition

$$
\dot{x} = \frac{dx}{dt}
$$

---

## Interpretation

```text
Velocity describes how the system moves locally.
```

It defines:

- direction  
- magnitude  
- temporal evolution  

---

# 🔷 3. Flow Field

## Definition

$$
\dot{x} = F(x)
$$

---

## Interpretation

```text
F(x) defines the intrinsic motion tendencies of the system.
```

It represents:

- local dynamics  
- directional structure  
- system evolution rules  

---

# 🔷 4. Acceleration / Change Dynamics

## Definition

$$
A(x) = \frac{d\dot{x}}{dt}
$$

---

## Interpretation

```text
A(x) measures how motion itself changes.
```

This includes:

- acceleration  
- curvature of motion  
- directional drift  
- transition buildup  

---

# 🔷 5. Density Field

## Definition

$$
\rho(x) = \mathrm{KDE}(\{x_t\})
$$

---

## Interpretation

```text
ρ(x) measures where the system tends to persist.
```

High density:

- stable structure  
- repeated motion  
- coherent occupancy  

Low density:

- weak structure  
- transition corridors  
- unstable regions  

---

# 🔷 6. Structural Gradient

## Definition

$$
\nabla \rho(x)
=
\left(
\frac{\partial \rho}{\partial x_1},
\dots,
\frac{\partial \rho}{\partial x_n}
\right)
$$

---

## Interpretation

```text
∇ρ(x) defines the local structural drift direction.
```

It represents:

- directional pull between structures  
- density flow  
- regime drift  
- transition corridors  

---

## Operational Meaning

```text
Systems tend to drift along structural gradients.
```

The gradient field acts as:

- a navigation bias  
- a transition indicator  
- a structural flow layer  

---

# 🔷 7. Coherence

## Definition

$$
C(x)
=
\frac{\dot{x} \cdot F(x)}
{\|\dot{x}\| \cdot \|F(x)\|}
$$

---

## Interpretation

```text
C(x) measures alignment between motion and local field structure.
```

Meaning:

| Value | Interpretation |
|---|---|
| $C(x) \approx 1$ | aligned / coherent |
| $C(x) \approx 0$ | transitional / ambiguous |
| $C(x) < 0$ | opposing structure |

---

# 🔷 8. Residence Structure

## Definition

$$
R(x)
=
\text{local persistence measure}
$$

---

## Interpretation

```text
R(x) estimates how strongly trajectories remain locally bound.
```

High residence:

- stable basin behavior  
- persistent occupancy  
- local structural retention  

Low residence:

- rapid drift  
- transition tendency  
- weak local attachment  

---

# 🔷 9. Gate Score

## Definition

$$
G(x)
=
(1-\hat{\rho})
(1-\hat{C})
(1-\hat{R})
$$

---

## Interpretation

```text
G(x) estimates transition susceptibility.
```

High $G(x)$ indicates:

- low density  
- low coherence  
- weak residence structure  
- structural breakdown  

---

## Conceptual Meaning

```text
G(x) does not represent force.

It represents structural weakness.
```

---

# 🔷 10. Transition Tension

## Definition

$$
T(x)
=
w_1 A(x)
+
w_2 D(x)
+
w_3 G(x)
$$

---

## Interpretation

```text
T(x) represents accumulated transition pressure.
```

It combines:

- dynamical change  
- structural drift  
- gate susceptibility  

---

## Operational Meaning

```text
Transitions emerge when structural tension accumulates.
```

---

# 🔷 11. Janus Field

## Definition

$$
J(x)
=
F_{\text{forward}}(x)
+
F_{\text{backward}}(x)
$$

---

## Interpretation

```text
J(x) represents coupled directional structure.
```

The Janus field explores whether:

- forward evolution  
- backward constraints  
- and interface dynamics  

coexist within local structure.

---

## Status

```text
exploratory / partially formalized
```

---

# 🔷 12. Phase

## Definition

$$
\phi(t)
=
\arctan2(x_2(t), x_1(t))
$$

---

## Interpretation

```text
Phase measures rotational progression through system structure.
```

---

# 🔷 13. Phase Velocity

## Definition

$$
\omega(t)
=
\frac{d\phi(t)}{dt}
$$

---

## Interpretation

```text
ω(t) measures local phase evolution speed.
```

---

# 🔷 14. Expected Phase Velocity

## Definition

$$
\hat{\omega}(t)
=
\mathcal{E}[\omega](t)
$$

---

## Interpretation

```text
ω̂(t) represents locally expected phase behavior.
```

---

# 🔷 15. Mismatch

## Definition

$$
M(t)
=
|\omega(t)-\hat{\omega}(t)|
$$

---

## Interpretation

```text
Mismatch measures deviation from locally consistent evolution.
```

---

## Meaning

| Value | Interpretation |
|---|---|
| small $M(t)$ | coherent evolution |
| large $M(t)$ | structural inconsistency |

---

# 🔷 16. Instability Magnitude

## Definition

$$
I(t)
=
\|\dot{x}(t)\|
$$

---

## Interpretation

```text
I(t) measures local dynamical intensity,
not transition activation itself.
```

---

# 🔷 17. Structural Change

## Definition

$$
\Delta(t)
=
\text{frame-to-frame structural difference}
$$

---

## Interpretation

```text
Δ(t) acts as an observable proxy
for transition activity.
```

---

# 🔷 18. Control Signal

## Definition

$$
s(t)
=
f(\phi(t), I(t), M(t))
$$

---

## Interpretation

```text
Control modifies motion relative to structural dynamics.
```

NEXAH control is:

- geometry-aware  
- phase-sensitive  
- transition-oriented  

---

# 🔷 19. Transition Probability

## Definition

$$
P(\text{IOTA})
=
f(M(t), G(x), \Delta(t), T(x))
$$

---

## Interpretation

```text
Transition likelihood emerges from structural mismatch
and geometric instability.
```

---

# 🔗 Structural Relationships

The variables form an interconnected system:

```text
x
→ motion
→ flow
→ density
→ structural gradients
→ coherence
→ mismatch
→ gates
→ transition tension
→ transitions
→ control
→ navigation
```

---

# 🧠 Operational Hierarchy

## Geometry Layer

```text
x, F(x), ρ(x), ∇ρ(x), C(x), R(x), G(x)
```

Defines:

- structure  
- flow  
- persistence  
- transition regions  

---

## Transition Layer

```text
A(x), T(x), Δ(t), M(t)
```

Defines:

- drift buildup  
- transition pressure  
- mismatch accumulation  
- regime activation  

---

## Phase Layer

```text
φ, ω, ω̂, M
```

Defines:

- temporal consistency  
- mismatch dynamics  
- transition activation  

---

## Control Layer

```text
s(t), J(x)
```

Defines:

- directional intervention  
- coupled navigation structure  
- admissible navigation  

---

# ⚠️ Important Clarification

These quantities are currently:

```text
empirical
semi-formal
operational
```

They are NOT yet:

- mathematically complete  
- universally proven  
- physically fundamental  

---

# 🔥 Central Insight

```text
NEXAH describes systems through interacting structural quantities,
rather than isolated equations alone.
```

---

# 🧭 Final Perspective

```text
The variables of NEXAH are not independent objects.

They are relational measurements
describing how systems move through structured dynamics.
```

---

# 🔬 Current Direction

The current NEXAH foundation suggests:

```text
Dynamics generate structure.

Structure generates constraints.

Constraints generate transitions.

Transitions generate navigable geometry.
```

---

**NEXAH — Core Variable Map**  
Thomas K. R. Hofmann · 2026

---

# Status

empirical / partial / open
