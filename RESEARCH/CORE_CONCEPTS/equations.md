# 🧮 NEXAH — Core Equations

This document defines the **minimal mathematical structure**  
underlying the NEXAH validation and control framework.

All equations are directly derived from simulation behavior  
and correspond to implemented analysis pipelines.

---

# ⚠️ Scope

This is:

- not a complete theory  
- not a formal proof  

It is:

> a **minimal operational system of equations**  
> describing phase dynamics, transitions, and control

---

# 🧭 1. State Representation

Given a dynamical system:

```text
dx/dt = F(x)
```

We analyze motion in projected phase space:

```text
x = (x₁, x₂, x₃, ...)
```

---

# 🌀 2. Phase Definition

Phase is defined in a 2D projection:

```text
φ(t) = arctan2(x₂(t), x₁(t))
```

---

# 🔁 3. Phase Velocity

```text
ω(t) = dφ/dt
```

Computed numerically:

```text
ω ≈ ∇φ
```

---

# 🧩 4. Expected Phase Dynamics

A smoothed reference:

```text
ω̂(t) = smooth(ω(t))
```

(e.g. moving average)

---

# ⚠️ 5. Phase Mismatch

Core quantity:

```text
M(t) = |ω(t) - ω̂(t)|
```

Interpretation:

- low M → aligned dynamics  
- high M → phase disruption  

---

# 🔥 6. Instability Measure

Local dynamical magnitude:

```text
I(t) = ||dx/dt||
```

---

# ⚡ 7. IOTA Event Definition

Transition events occur when mismatch exceeds threshold:

```text
IOTA ⇔ M(t) > M_threshold
```

Equivalent interpretation:

```text
IOTA ⇔ phase alignment breaks
```

---

# 🔬 8. Conditional Transition Law

Empirical law:

```text
P(IOTA | M) ↑ as M ↑
```

→ transition probability increases with mismatch

---

# 🧠 9. Mismatch Interpretation

Mismatch reflects misalignment between:

```text
M(t) ≈ I(t) − control_alignment
```

More precisely:

```text
M(t) = deviation from expected rotational consistency
```

---

# 🎯 10. Control Law (Phase-Based)

Current control:

```text
s(t) = s*(φ(t))
```

Where:

- s = control strength  
- φ = phase  

---

# ⚠️ Limitation

Phase-only control cannot fully suppress transitions.

---

# 🚀 11. Extended Control Law

Required extension:

```text
s(t) = f(φ(t), I(t))
```

Goal:

- adapt control to both phase and instability  

---

# 🔧 12. Control Objective

Control aims to minimize mismatch:

```text
minimize M(t)
```

Equivalent:

```text
align ω(t) with ω̂(t)
```

---

# 🧭 13. Control Effectiveness Condition

```text
effective control ⇔ M(t) → small
```

---

# 🔁 14. Transition Mechanism (Core Result)

Transitions are not driven by instability alone:

```text
IOTA ⇔ M(t) ≫ 0
```

Expanded:

```text
IOTA ⇔ phase–control mismatch
```

---

# 🧬 15. Geometric Interpretation

```text
Stability:
→ M ≈ 0

Instability:
→ I high

Transition:
→ M high
```

---

# 🔄 16. Angular Structure (Empirical)

Observed dominant modes:

```text
k ∈ {4, 32, 34, 2, 0}
```

Indicating:

```text
non-uniform angular transition structure
```

---

# 🔑 Core System Summary

```text
φ → ω → ω̂ → M → IOTA
           ↑
         control
```

---

![Core Dynamical Variables](./visuals/nexah_phase_mismatch_control_mechanism.png)

---

# 🔥 Central Insight

```text
Transitions are not caused by instability magnitude.

They are caused by mismatch
between actual and expected phase dynamics.
```

---

# 🚀 Operational Principle

```text
Control does not reduce instability.

Control aligns the system
with its intrinsic phase structure.
```

---

# 🧭 Status

- empirically validated  
- multi-system consistent  
- causally supported  

---

**NEXAH Core Equation Layer**  
Minimal Phase–Mismatch–Control Framework  
© Thomas K. R. Hofmann · 2026
