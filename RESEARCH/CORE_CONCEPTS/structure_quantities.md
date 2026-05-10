# 🧩 NEXAH — Structural Quantities

---

# 🧭 Purpose

This document defines the core structural quantities used in the NEXAH framework.

These quantities describe how:

- structure emerges from trajectories
- coherence organizes transport
- transition regions form
- geometry constrains movement
- instability localizes into gates and corridors

This layer extends:

- `equations.md`
- `field_model.md`
- `aperture_geometry.md`

with an operational spatial-geometry formulation.

---

# ⚠️ Scope

This framework is:

- empirically grounded
- operationally useful
- partially formalized

It is NOT:

- a complete geometric theory
- a rigorous manifold derivation
- a proven universal framework

---

# 🔁 Structural Pipeline

```text
trajectory
→ density
→ flow
→ coherence
→ mismatch
→ aperture geometry
→ transition routing
→ navigation
```

---

# 🔷 1. Density Field

Given trajectory samples:

```math
\{x(t_i)\}_{i=1}^{N}
```

define the density field:

```math
\rho(x)
=
\mathrm{KDE}(x)
```

or more generally:

```math
\rho(x)
\approx
\text{empirical state density}
```

---

## Interpretation

```text
ρ(x) measures where the system spends time.
```

Observed behavior:

```text
high ρ
→ stable coherent regions

low ρ
→ transition corridors
→ shell boundaries
→ transport apertures
```

---

# 🔷 2. Density Gradient

Density gradient:

```math
\nabla \rho(x)
```

---

## Interpretation

```text
∇ρ(x)
defines the direction
of increasing structural stability.
```

Observed properties:

- points toward coherent basins
- aligns with stabilization flow
- acts as geometric guidance signal

---

# 🔷 3. Flow Field

Given system dynamics:

```math
\dot{x} = F(x)
```

define the local flow field:

```math
F(x)
```

---

## Interpretation

```text
F(x)
describes how the system moves locally.
```

Observed:

- directional transport organization
- coherent circulation patterns
- recursive motion structure

---

# 🔷 4. Local Coherence

Define local coherence as alignment between observed motion and flow geometry:

```math
C(x)
=
\frac{
\dot{x}(t)\cdot F(x)
}{
\|\dot{x}(t)\|
\,
\|F(x)\|
}
```

---

## Interpretation

```text
high C(x)
→ motion aligned with flow geometry

low C(x)
→ directional conflict
→ coherence weakening
```

---

## Observed Role

Coherence acts as:

- structural consistency measure
- transport alignment indicator
- local organization metric

---

# 🔷 5. Directional JANUS Coherence

JANUS extends coherence into directional transport geometry.

Forward local flow:

```math
F_{\mathrm{forward}}(x)
```

Backward local flow:

```math
F_{\mathrm{backward}}(x)
```

Directional overlap operator:

```math
\mathcal{J}(x)
=
F_{\mathrm{forward}}(x)
\odot
F_{\mathrm{backward}}(x)
```

---

## Normalized JANUS Coherence

```math
J(x)
=
\frac{
\|\mathcal{J}(x)\|
}{
\|F_{\mathrm{forward}}(x)\|
\cdot
\|F_{\mathrm{backward}}(x)\|
+
\varepsilon
}
```

with:

```math
\varepsilon \ll 1
```

for numerical stability.

---

## Interpretation

```text
high J(x)
→ directional agreement
→ coherent transport organization

low J(x)
→ transport asymmetry
→ transition-sensitive geometry
```

---

# 🔷 6. Normalized Structural Quantities

To combine structural measures, define normalized quantities:

```math
\hat{\rho}(x),
\quad
\hat{C}(x),
\quad
\hat{J}(x),
\quad
\hat{R}(x)
```

where:

- `ρ̂(x)` → normalized density
- `Ĉ(x)` → normalized local coherence
- `Ĵ(x)` → normalized directional coherence
- `R̂(x)` → residual / noise / variance estimate

All normalized into:

```text
[0,1]
```

---

# 🔷 7. Gate Function

Define operational transition field:

```math
G(x)
=
(1-\hat{\rho}(x))
(1-\hat{C}(x))
(1-\hat{J}(x))
(1-\hat{R}(x))
```

---

## Interpretation

```text
G(x)
measures structural transition likelihood.
```

Observed:

```text
high G(x)
→ transition corridors
→ gates
→ apertures
→ shell crossings

low G(x)
→ coherent stable regions
```

---

# 🔷 8. Aperture Geometry

Define aperture score:

```math
A(x)
=
1-J(x)
```

---

## Interpretation

```text
high aperture score
→ directional thinning
→ transition bottlenecks
```

Observed structures:

- transport throats
- shell boundaries
- coherence corridors
- transition spines

---

# 🔷 9. Orientation Geometry

Define orientation field:

```math
\Theta(x)
=
\arg(F(x))
```

---

## Root Alignment

Define orientation bias score:

```math
B(x)
=
\cos(
\Theta(x)
-
\Theta_{\mathrm{root}}
)
```

---

## Interpretation

```text
high B(x)
→ alignment with dominant transport orientation
```

Observed exploratory behavior:

- directional pull structures
- root-aligned transport
- orientation clustering
- coherence axis formation

---

# 🔷 10. Structural Regimes

Define coherent regime regions:

```math
\mathcal{R}
=
\{
x
\mid
\rho(x)\ \text{high},
\;
C(x)\ \text{high},
\;
J(x)\ \text{high}
\}
```

---

## Interpretation

```text
regimes
=
stable coherent transport regions
```

---

# 🔷 11. Transition Regions (Gates)

Define gate regions:

```math
\mathcal{G}
=
\{
x
\mid
G(x)\ \text{high}
\}
```

---

## Interpretation

```text
gates
=
localized transition geometry
```

Observed:

- shell crossings
- transition corridors
- compression regions
- directional apertures

---

# 🔷 12. Recursive Phase Geometry

Observed recursive decomposition:

| Quadrant | Interpretation |
|---|---|
| Q1 | Expansion |
| Q2 | Compression |
| Q3 | Memory |
| Q4 | Transition |

---

## Phase Partition

```math
Q(t)
=
\mathcal{Q}(\phi(t),\dot{\phi}(t))
```

---

## Interpretation

```text
phase structure recursively organizes transport geometry
```

---

# 🔷 13. Structural Flow Decomposition

System behavior decomposes into:

```text
ρ(x)
→ where system resides

F(x)
→ how system moves

C(x)
→ local consistency

J(x)
→ directional transport coherence

A(x)
→ aperture geometry

G(x)
→ transition organization
```

---

# 🔷 14. Link to Phase Dynamics

From `equations.md`:

Phase mismatch:

```math
M(t)
=
|\omega(t)-\hat{\omega}(t)|
```

---

## Combined Interpretation

```text
G(x)
→ spatial transition potential

M(t)
→ temporal transition activation
```

---

# 🔷 15. Unified Transition Mechanism

Operational interpretation:

```text
transition occurs when:

system enters
high G(x)

AND

phase mismatch
M(t)
becomes large
```

---

# 🔷 16. Navigation Interpretation

Navigation uses:

```math
\nabla \rho(x),
\quad
G(x),
\quad
J(x),
\quad
B(x)
```

---

## Conceptual Navigation Rule

```text
move toward:
high density
high coherence

avoid:
high aperture
high gate activation
```

---

# 🔷 17. Directional Transport Geometry

Observed transport organization:

```text
systems do not transition randomly.
```

Transitions appear constrained by:

- coherence corridors
- shell geometry
- orientation bias
- recursive phase organization

---

## Interpretation

```text
transition geometry acts
like a navigable transport network
inside the field.
```

---

# 🔷 18. Unified Structural Vector

Define combined structural state:

```math
\mathcal{S}(x)
=
(
\rho,
C,
J,
A,
B,
G
)
```

---

## Interpretation

```text
𝒮(x)
describes the local structural state
of the dynamical field.
```

---

# 🔥 Final Insight

```text
Structure is not imposed externally.

It emerges from:

- density
- flow
- coherence
- directional organization
- recursive phase geometry
```

Transitions occur where:

```text
coherence weakens,
directional symmetry breaks,
and aperture geometry forms.
```

---

# 🌌 Current Interpretation

```text
nonlinear systems appear to organize motion
through structured coherence geometry
rather than unconstrained randomness.
```

---

# 🔗 Relation to Other Modules

## → equations.md

- phase mismatch framework

## → field_model.md

- field interpretation layer

## → aperture_geometry.md

- gate & corridor structures

## → theory_to_field_mapping.md

- operator-level interpretation

## → JANUS_OPERATOR/

- directional coherence geometry
- recursive transport structures
- orientation manifolds

---

# ⚠️ Current Limitations

- empirical framework
- reconstruction-dependent
- incomplete formalization
- orientation geometry exploratory
- transport manifolds not rigorously derived

---

# 🧭 Status

```text
density structure:
validated

coherence geometry:
strong exploratory evidence

directional JANUS coherence:
experimental but reproducible

aperture geometry:
emerging framework

orientation bias:
early-stage exploratory
```

---

**NEXAH Structural Quantities Layer**  
Spatial Structure · Coherence · Aperture Geometry · Transition Organization  
Thomas K. R. Hofmann · 2026
