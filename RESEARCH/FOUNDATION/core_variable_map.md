# 🧠 NEXAH — Core Variable Map

## 🧭 Purpose

This document defines the **minimal operational variable set**
used throughout the NEXAH framework.

It serves as:

- the structural alphabet of NEXAH  
- the bridge between concepts and equations  
- the shared notation layer across modules  

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

# 🧩 Core Variables

| Variable | Meaning | Role |
|---|---|---|
| $x$ | system state | local position in system space |
| $\dot{x}$ | state velocity | local motion |
| $F(x)$ | flow field | intrinsic system dynamics |
| $A(x)$ | acceleration / change dynamics | variation of motion |
| $\rho(x)$ | density field | occupancy / structural persistence |
| $C(x)$ | coherence | alignment with local flow |
| $G(x)$ | gate score | transition susceptibility |
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

# 🔷 6. Coherence

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

# 🔷 7. Gate Score

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
- structural breakdown  

---

## Conceptual Meaning

```text
G(x) does not represent force.

It represents structural weakness.
```

---

# 🔷 8. Janus Field

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

# 🔷 9. Phase

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

# 🔷 10. Phase Velocity

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

# 🔷 11. Expected Phase Velocity

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

# 🔷 12. Mismatch

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

# 🔷 13. Instability Magnitude

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

# 🔷 14. Structural Change

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

# 🔷 15. Control Signal

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

# 🔷 16. Transition Probability

## Definition

$$
P(\text{IOTA})
=
f(M(t), G(x), \Delta(t))
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
→ coherence
→ mismatch
→ gates
→ transitions
→ control
```

---

# 🧠 Operational Hierarchy

## Geometry Layer

```text
x, F(x), ρ(x), C(x), G(x)
```

Defines:

- structure  
- flow  
- transition regions  

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

**NEXAH — Core Variable Map**  
Thomas K. R. Hofmann · 2026



# Status

empirical / partial / open
