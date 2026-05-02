# 🧩 NEXAH — Structural Quantities

## 🧭 Purpose

This document defines the **core structural quantities** of the NEXAH framework.

These quantities describe how structure emerges from trajectories and how
transition-relevant regions can be identified.

They extend the phase-based formulation (`equations.md`) with **spatial structure**.

---

# ⚠️ Scope

This is:

- empirically grounded  
- partially formalized  

It is NOT:

- a complete geometric theory  
- a proven manifold construction  

---

# 🔷 1. Density Field

Given trajectory samples:

$$
\{x(t_i)\}_{i=1}^N
$$

we define the density field:

$$
\rho(x) = \mathrm{KDE}(x)
$$

or more generally:

$$
\rho(x) \approx \text{empirical state density}
$$

---

## Interpretation

```text
ρ(x) measures where the system spends time.
```

- high ρ → stable regions (regimes)  
- low ρ → transition corridors  

---

# 🔷 2. Density Gradient

$$
\nabla \rho(x)
$$

---

## Interpretation

```text
∇ρ(x) defines the direction of increasing structural stability.
```

- points toward dense regions  
- used as a navigation / stabilization signal  

---

# 🔷 3. Flow Field

Given system dynamics:

$$
\dot{x} = F(x)
$$

---

## Interpretation

```text
F(x) describes how the system moves.
```

---

# 🔷 4. Coherence

Define coherence as alignment between trajectory and flow:

$$
C(x) =
\frac{\dot{x}(t) \cdot F(x)}{\|\dot{x}(t)\| \, \|F(x)\|}
$$

---

## Interpretation

```text
C(x) ≈ 1 → motion aligned with flow (stable)

C(x) low → directional conflict / instability
```

---

# 🔷 5. Normalized Quantities

To combine structural measures, define:

$$
\hat{\rho}(x), \quad \hat{C}(x), \quad \hat{R}(x)
$$

as normalized versions in $[0,1]$.

Where:

- $\hat{\rho}$ → normalized density  
- $\hat{C}$ → normalized coherence  
- $\hat{R}$ → optional residual / noise / variance measure  

---

# 🔷 6. Gate Function

Define:

$$
G(x) = (1 - \hat{\rho}(x))(1 - \hat{C}(x))(1 - \hat{R}(x))
$$

---

## Interpretation

```text
G(x) measures structural transition likelihood.
```

- high G → transition region  
- low G → stable region  

---

## Important Distinction

```text
ρ(x), C(x) → describe structure

G(x) → highlights breakdown of structure
```

---

# 🔷 7. Relation Between C(x) and G(x)

Conceptually:

```text
C high → coherent regime

C low → breakdown of alignment
        → contributes to G
```

BUT:

```text
G is NOT simply inverse(C)

G combines multiple failure modes:
- low density
- low coherence
- residual instability
```

---

## Insight

```text
C(x) describes "being inside structure"

G(x) describes "leaving structure"
```

---

# 🔷 8. Regimes

Define regime regions:

$$
\mathcal{R} = \{ x \mid \rho(x) \text{ high}, \; C(x) \text{ high} \}
$$

---

## Interpretation

```text
Regimes = coherent, stable regions of motion
```

---

# 🔷 9. Transition Regions (Gates)

Define:

$$
\mathcal{G} = \{ x \mid G(x) \text{ high} \}
$$

---

## Interpretation

```text
Gates = regions where transitions occur
```

---

# 🔷 10. Structural Flow Decomposition

System behavior can be decomposed into:

```text
ρ(x) → where system resides

F(x) → how system moves

C(x) → how consistent motion is

G(x) → where structure breaks
```

---

# 🔷 11. Link to Phase Dynamics

From `equations.md`:

- phase mismatch:
  $$
  M(t)
  $$

---

## Combined Interpretation

```text
G(x) → spatial transition potential

M(t) → temporal activation trigger
```

---

## Core Mechanism

```text
transition occurs when:

system enters high G(x)
AND
M(t) becomes large
```

---

# 🔷 12. Navigation Interpretation

Control uses:

$$
\nabla \rho(x), \quad G(x)
$$

---

## Conceptual Control Law

```text
move toward high ρ(x)
avoid high G(x)
align phase dynamics
```

---

# 🔷 13. Summary

```text
ρ(x) → structure (where)

F(x) → dynamics (how)

C(x) → coherence (consistency)

G(x) → transition field (breakdown)
```

---

# 🔥 Final Insight

```text
Structure is not defined explicitly.

It emerges from density and flow.

Transitions occur where structure weakens,
and are activated when phase coherence breaks.
```

---

**NEXAH Structural Quantities Layer**  
Spatial Structure & Transition Field Definition  
Thomas K. R. Hofmann · 2026
