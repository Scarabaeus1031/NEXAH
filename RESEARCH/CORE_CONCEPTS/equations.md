## 🧭 Role in NEXAH

This document defines the **minimal operational layer**  
linking empirical observations to formal structure.

It translates:
```
validation → measurable quantities → control-relevant structure
```

# 🧮 NEXAH — Core Equations

This document defines the **minimal operational mathematical structure**  
underlying the NEXAH framework.

It formalizes the relationship between:

- phase dynamics  
- mismatch  
- transitions  
- control  

All quantities are derived from empirical system behavior.

---

# ⚠️ Scope

This is:

- not a complete theory  
- not a formal proof  

It is:

> a **minimal, empirically grounded equation system**

---

# 🧭 1. Dynamical System

We consider a continuous dynamical system:

$$
\dot{x}(t) = F(x(t)), \quad x(t) \in \mathbb{R}^n
$$

with trajectory:

$$
x(t)
$$

---

# 🌀 2. Phase Definition

Phase is defined via a projection onto a 2D subspace:

$$
\phi(t) = \arctan2(x_2(t), x_1(t))
$$

This defines a **scalar coordinate capturing rotational progression**.

---

# 🔁 3. Phase Velocity

Temporal derivative:

$$
\omega(t) = \frac{d\phi(t)}{dt}
$$

Discrete approximation:

$$
\omega(t) \approx \frac{\phi(t+\Delta t) - \phi(t)}{\Delta t}
$$

---

# 🧩 4. Expected Phase Dynamics

Define a local expectation operator:

$$
\hat{\omega}(t) = \mathcal{E}[\omega](t)
$$

where:

- $\mathcal{E}$ is a local smoothing operator  
- e.g. moving average, kernel smoothing, or low-pass filter  

Interpretation:

```text
ω̂(t) represents expected phase evolution under local consistency
```

---

# ⚠️ 5. Phase Mismatch

Core quantity:

$$
M(t) = |\omega(t) - \hat{\omega}(t)|
$$

Interpretation:

```text
M(t) small → coherent phase evolution  
M(t) large → disruption of phase consistency
```

---

# 🔥 6. Instability Measure

Define local dynamical magnitude:

$$
I(t) = \|\dot{x}(t)\|
$$

Interpretation:

```text
I(t) measures local dynamical intensity, not structural change
```

---

# ⚡ 7. Transition Events (IOTA)

Define transition activation probabilistically:

$$
P(\text{IOTA at } t) = f(M(t))
$$

with:

$$
\frac{dP}{dM} > 0
$$

---

## Threshold Approximation (Operational)

In practice:

$$
\text{IOTA} \;\Longleftrightarrow\; M(t) > \tau
$$

for threshold $\tau$.

---

# 🔬 8. Conditional Transition Law

Empirical observation:

$$
P(\text{IOTA} \mid M) \uparrow \quad \text{as } M \uparrow
$$

---

# 🧠 9. Interpretation of Mismatch

Mismatch measures deviation from expected rotational behavior:

```text
M(t) = deviation from locally consistent phase evolution
```

---

# 🎯 10. Control Law (Phase-Based)

Current control formulation:

$$
s(t) = s^*(φ(t), d)
$$

---

# ⚠️ Limitation

Phase-only control is insufficient to suppress transitions.

---

# 🚀 11. Extended Control Law

Proposed extension:

$$
s(t) = f(\phi(t), I(t))
$$

---

# 🔧 12. Control Objective

Primary objective:

$$
\min M(t)
$$

Equivalent:

$$
\omega(t) \rightarrow \hat{\omega}(t)
$$

---

# 🧭 13. Control Effectiveness

```text
effective control ⇔ M(t) small
```

---

# 🔁 14. Transition Mechanism (Core Result)

Empirical result:

```text
Transitions are not driven by instability alone.
```

Formally:

$$
\text{IOTA} \not\sim I(t)
$$

but:

$$
\text{IOTA} \sim M(t)
$$

---

# 🧬 15. Geometric Interpretation

```text
Stability:
→ M ≈ 0

Instability:
→ I large

Transition:
→ M large
```

---

# 🔄 16. Angular Structure (Empirical)

Observed dominant modes:

$$
k \in \{4, 32, 34, 2, 0\}
$$

Interpretation:

```text
Transitions exhibit structured angular signatures
```

---

# 🔑 System Summary

```text
φ → ω → ω̂ → M → transition probability
            ↑
         control
```

---

![Core Dynamical Variables](./visuals/nexah_phase_mismatch_control_mechanism.png)

---

# 🔥 Central Insight

```text
Transitions are caused by phase mismatch,
not by instability magnitude alone.
```

---

# 🚀 Operational Principle

```text
Control aligns phase dynamics,
rather than suppressing system energy.
```

---

# 🔬 17. Control Directionality (Extension)

Empirical results show:

```text
Control effectiveness depends on direction, not magnitude alone.
```

We extend the control law:

$$
s(t) = s^*(\phi(t), d)
$$

where:

- $d \in \{-1, +1\}$ represents control direction relative to phase flow

---

## 🔁 Directional Effect

Observed behavior:

```text
d aligned (+1)   → increases drift and transition activity  
d inverted (-1)  → reduces drift but may increase mismatch  
d damped         → suppresses transitions but retains instability  
d inverse        → minimizes drift AND suppresses transitions  
```

---

## 🧠 Interpretation

Control interacts with system dynamics as:

$$
\omega_{\text{eff}}(t) = \omega(t) - s(t)
$$

Mismatch becomes:

$$
M(t) = |\omega_{\text{eff}}(t) - \hat{\omega}(t)|
$$

---

## 🔑 Extended Control Objective

```text
Minimize mismatch via correct directional alignment.
```

---

## 🚀 Updated Principle

```text
Control does not reduce instability.

Control modifies phase dynamics through directional interaction.
```

---
# 🧭 Status

- empirically validated  
- cross-system consistent  
- causally supported  

---

**NEXAH Core Equation Layer**  
Minimal Phase–Mismatch–Control Framework  
Thomas K. R. Hofmann · 2026
