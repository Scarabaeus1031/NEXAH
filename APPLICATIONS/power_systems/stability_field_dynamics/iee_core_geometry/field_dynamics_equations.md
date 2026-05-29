# NEXAH Core Field Dynamics Equations

**Version 11.0**  
**Mathematical Foundations of Stability Field Dynamics**  
**NEXAH Framework – Power System Applications**

---

## Overview

This document defines the mathematical foundation of the NEXAH field-dynamics framework used for stability analysis, transition detection, and regime navigation in large-scale dynamical systems.

The framework combines multiple dynamical mechanisms into a unified field representation:

- Lorenz-inspired field dynamics
- Van der Pol oscillatory amplification
- Kuramoto synchronization coupling
- Compass modulation
- Winding-number topology detection
- Iota-ring periodic forcing
- Janus reversal dynamics
- Lyapunov rhythm modulation

Together, these components form the dynamical basis of the NEXAH Operator.

---

# 1. State Space

The system state is represented by

$$
\mathbf{x}
=
\begin{bmatrix}
c \\
dc \\
\phi
\end{bmatrix}
$$

where

| Variable | Description |
|-----------|-------------|
| $c$ | Field coordinate |
| $dc$ | Drift velocity |
| $\phi$ | Discrete regulator state |

---

# 2. Governing Equations

The field evolution is defined by

$$
\dot{c}
=
dc \cdot C(t)
$$

where $C(t)$ denotes the contraction function.

The drift evolution follows

$$
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
f_{\mathrm{winding}}
+
f_{\mathrm{iota}}
+
f_{\mathrm{janus}}
+
f_{\mathrm{lyapunov}}
\Big)
\cdot I(\phi)
\cdot S(t)
$$

where

$$
S(t)
=
\mathrm{slow\_start}(t)
$$

and

$$
I(\phi)
$$

is the regulator function.

The phase regulator evolves according to

$$
\dot{\phi}
=
g
\Big(
dc,
\phi,
\mathrm{resonance},
\mathrm{winding},
\mathrm{iota},
\mathrm{janus},
\mathrm{lyapunov}
\Big)
$$

---

# 3. Dynamic Components

## 3.1 Field Force

The field force provides the large-scale flow structure and acts as the primary attractor component.

$$
f_{\mathrm{field}}
=
\sigma (dc-c)
+
\rho c (1-\phi)
$$

---

## 3.2 Van der Pol Component

The Van der Pol component introduces nonlinear oscillatory amplification.

$$
f_{\mathrm{vdp}}
=
\beta \, dc \,(1-c^2)
$$

---

## 3.3 Kuramoto Coupling

The synchronization term measures collective phase alignment.

$$
f_{\mathrm{kuramoto}}
=
\sum_{i=0}^{4}
K(Q)
\sin
\left(
\frac{2\pi(\phi-i)}{5}
\right)
$$

with

$$
K(Q)
=
1+\alpha Q
$$

---

## 3.4 Compass Modulation

The compass operator introduces directional rotational guidance.

$$
f_{\mathrm{compass}}
=
\gamma
\sin(\omega t+\phi\delta)
\cos(\omega t+1.618\,\phi\delta)
$$

---

## 3.5 Phi Resonance

The resonance term couples phase dynamics to irrational-frequency modulation.

$$
\mathrm{resonance}
=
\eta
\sin(\phi\pi\sqrt{2})
$$

---

## 3.6 Winding Number Trigger

The winding-number term acts as a topological transition detector.

$$
f_{\mathrm{winding}}
=
\kappa
\cdot
W
$$

where $W$ denotes the current winding number.

---

## 3.7 Iota Ring

The Iota ring introduces periodic field modulation.

$$
f_{\mathrm{iota}}
=
0.35
\sin
\left(
2\pi
\frac{t-36}{19}
\right)
$$
