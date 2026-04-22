# NEXAH — Core Equations (Field Layer)

## Overview

This document defines the **minimal mathematical foundation** of the NEXAH Field Layer.

It provides:

- core system definitions  
- field representation  
- operators  
- coordinate transformation  
- transition signals  

---

# 1. Dynamical System

State:

```text
x(t) ∈ ℝⁿ
```

Dynamics:

```text
dx/dt = F(x)
```

---

# 2. Probability Field

From trajectory data, a probability density is estimated:

```text
p(x)
```

Interpretation:

- high p(x) → frequently visited states  
- low p(x) → rare / transitional states  

---

# 3. Energy Representation

Energy is defined as:

```text
E(x) = -log(p(x))
```

Interpretation:

- low energy → stable regions  
- high energy → barriers / transitions  

---

# 4. Field Operators

## Divergence

```text
div F = ∇ · F
```

Meaning:

- positive → expansion (source)  
- negative → contraction (sink)  

---

## Curl

```text
curl F = ∇ × F
```

Meaning:

- rotational structure  
- circulation of flow  

---

# 5. Temporal Coupling (Empirical)

Observed relationship:

```text
div(t) ≈ curl(t - τ)
curl(t) ≈ div(t + τ)
```

with:

```text
τ ≈ 15
```

Interpretation:

- delayed feedback between expansion and rotation  
- phase-shifted coupling  

---

# 6. Field-Aligned Representation

State decomposition:

```text
x(t) = α(t) · e₁ + β(t) · e₂ + γ(t) · e₃
```

Where:

- e₁ = dominant flow direction (PCA / FQ axis)  
- e₂, e₃ = orthogonal deviation directions  

---

## Interpretation

| Component | Meaning |
|----------|--------|
| α(t) | motion along flow (system progression) |
| β(t), γ(t) | deviation from structure |

---

# 7. Signals

## Deviation Magnitude

```text
D(t) = sqrt(β(t)² + γ(t)²)
```

Interpretation:

- small D → aligned / stable  
- large D → deviation / instability  

---

## Coherence

```text
C(t) = alignment(x(t), F(x(t)))
```

(implementation-dependent)

---

## Risk

```text
R(t) ∝ D(t)
```

Interpretation:

- higher deviation → higher risk  

---

# 8. Transition Indicator

Simple condition:

```text
D(t) ↑  ⇒ transition likelihood ↑
```

Optional refinement:

```text
dD/dt > threshold
```

---

# 9. Structural Summary

The system transforms:

```text
dynamics → probability → energy → field → coordinates → signals
```

---

# 10. Key Principle

> Stability is not a state,  
> but alignment with the system’s intrinsic flow.

---

# ⚠️ Scope

This formulation is:

- empirical  
- derived from simulations  
- not a fundamental physical theory  

---

# 🧠 Role in NEXAH

These equations define the **operational core** of:

- Discovery Engine → extracts structure  
- Field Layer → encodes structure  
- Navigator → acts on structure  

---

# 🔗 Extended Formulation

This document defines the minimal operational equations of the Field Layer.

For a structural and conceptual interpretation (including connections to dynamical systems, energy landscapes, and control), see:

→ `field_layer_core_formulation.md`

---
---

**Status:** Active  
**Scope:** Minimal working formulation  
