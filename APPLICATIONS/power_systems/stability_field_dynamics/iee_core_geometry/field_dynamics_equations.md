# NEXAH Core Field Dynamics Equations

Version 11.0  
Mathematical Foundations of Stability Field Dynamics  
NEXAH Framework – Power System Applications

---

## Overview

This document defines the mathematical foundation of the NEXAH field-dynamics framework currently used for stability analysis, transition detection, and regime navigation in large-scale dynamical systems.

The framework combines:

- Lorenz-inspired field dynamics
- Van der Pol oscillatory behavior
- Kuramoto synchronization coupling
- Compass modulation
- Winding-number topology detection
- Iota-ring periodic forcing
- Janus reversal dynamics
- Lyapunov rhythm modulation

Together these components form the basis of the NEXAH Operator described in nexah_operator.md.

---

# 1. State Representation

The system state is represented by

[
\mathbf{x}
=
\begin{bmatrix}
c \
dc \
\phi
\end{bmatrix}
]

where

| Variable | Meaning |
|-----------|-----------|
| (c) | Field coordinate |
| (dc) | Field drift velocity |
| (\phi) | Discrete phase regulator state |

---

# 2. Core Field Dynamics

The evolution equations are

[
\dot c
=
dc \cdot \mathrm{contraction}(t)
]

[
\dot{dc}
=
\Big(
\alpha_{\mathrm{flow}} f_{\mathrm{field}}
+
\beta_{\mathrm{swirl}} f_{\mathrm{vdp}}
+
\gamma_{\mathrm{memory}} f_{\mathrm{kuramoto}}
+
\delta_{\mathrm{resonance}} f_{\mathrm{compass}}
+
f_{\mathrm{branch}}
+
f_{\mathrm{winding}}
+
f_{\mathrm{iota}}
+
f_{\mathrm{janus}}
+
f_{\mathrm{lyapunov}}
\Big)
\cdot I(\phi)
\cdot \mathrm{slow_start}(t)
]

[
\dot\phi
=
g(
dc,
\phi,
\mathrm{resonance},
\mathrm{winding},
\mathrm{iota},
\mathrm{janus},
\mathrm{lyapunov}
)
]

---

# 3. Dynamic Components

## 3.1 Field Force

Lorenz-inspired large-scale flow structure

[
f_{\mathrm{field}}
=
\sigma(dc-c)
+
\rho c(1-\phi)
]

---

## 3.2 Van der Pol Component

Nonlinear oscillatory amplification

[
f_{\mathrm{vdp}}
=
\beta , dc(1-c^2)
]

---

## 3.3 Kuramoto Coupling

Synchronization and collective phase alignment

[
f_{\mathrm{kuramoto}}
=
\sum_{i=0}^{4}
K(Q)
\sin
\left(
2\pi(\phi-i)/5
\right)
]

with

[
K(Q)
=
1+\alpha Q
]

---

## 3.4 Compass Modulation

Directional rotational guidance

[
f_{\mathrm{compass}}
=
\gamma
\sin(\omega t+\phi\delta)
\cos(\omega t+\phi\delta\cdot1.618)
]

---

## 3.5 Phi Resonance

[
\mathrm{resonance}
=
\eta
\sin(\phi\pi\sqrt2)
]

---

## 3.6 Winding Number Trigger

Topological transition detector

[
f_{\mathrm{winding}}
=
\kappa
\cdot
\mathrm{winding_number}
]

---

## 3.7 Iota Ring

Periodic field modulation

[
f_{\mathrm{iota}}
=
0.35
\sin
\left(
2\pi
\frac{t-36}{19}
\right)
]

---

## 3.8 Janus Reversal

Counter-rotational transition operator

[
f_{\mathrm{janus}}
=
J
\Big[
\cos(\omega t+\phi\delta)
-
\sin(\omega t+\phi\delta)
\Big]
\cdot
\mathrm{sign}(dc)
]

---

## 3.9 Lyapunov Rhythm

Local instability-sensitive modulation

[
f_{\mathrm{lyapunov}}
=
L(t)
\left[
\sin
\left(
2\pi\frac43 t
\right)
+
\sin
\left(
2\pi\frac32 t
\right)
\right]
]

with

[
L(t)
\approx
\kappa_L |dc|
]

---

# 4. Regulator Function

The regulator gate is

[
I(\phi)
=
\begin{cases}
1.0,
&
\phi < 3
\
0.15
+
0.85
\tanh
\big(
(\phi-1.85)\cdot5.8
\big),
&
\phi \ge 3
\end{cases}
]

This creates a nonlinear transition between stable and inversion-dominated regimes.

---

# 5. Tunable Parameters

| Parameter | Typical Value |
|------------|------------|
| (\alpha_{\mathrm{flow}}) | 0.95 |
| (\beta_{\mathrm{swirl}}) | 0.65 |
| (\gamma_{\mathrm{memory}}) | 0.40 |
| (\delta_{\mathrm{resonance}}) | 0.25 |
| (Q) | 1.62 |
| (J) | 0.8 – 1.2 |
| (\kappa_L) | 0.4 – 0.8 |
| Winding Threshold | 6.5 – 18.0 |

---

# 6. Classical Voltage-Collapse Benchmark

Reference load ramp

[
p_{\mathrm{ramp}}(t)
=
\lambda t
]

Classical voltage response

[
V_{\mathrm{classic}}(t)
=
\frac{1}
{1+\mu(\lambda t)^2}
]

---

# 7. Scaling Hypothesis

The NEXAH field-dynamics framework is designed to identify approaching regime transitions using geometric signatures rather than system size.

The central hypothesis is:

> Critical transition structures remain observable across network scales when represented in the NEXAH stability field.

Current validation systems:

- IEEE118
- IEEE300
- IEEE1354
- IEEE9241

---

# 8. Relation to the NEXAH Operator

The equations defined here provide the dynamical components used by the NEXAH Operator.

The operator itself is formally defined in:

text nexah_operator.md 

and represents the unified navigation field used for transition detection and stability guidance.
