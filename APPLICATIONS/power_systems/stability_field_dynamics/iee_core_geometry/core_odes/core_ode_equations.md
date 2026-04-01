# NEXAH Core Equations – iee_core_geometry

**Mathematical Foundations of the Regime Navigation System**

This document summarizes the core mathematical structures developed through the 2D and 3D phases (v13–v3.8 + 3D Polar Grid).

### 1. State Vector
\[
\mathbf{x} = \begin{bmatrix}
c \\
dc \\
\phi_{\text{idx}}
\end{bmatrix}
\]
- \( c \): field coordinate (state variable)
- \( dc \): time derivative of \( c \) (drift)
- \( \phi_{\text{idx}} \): discrete Phi regulator state (0–4)

### 2. Core Regime ODE
\[
\begin{aligned}
\dot{c} &= dc \\
\dot{dc} &= \Big( f_{\text{field}} + p_{\text{drive}} + f_{\text{kuramoto}} + f_{\text{vdp}} + f_{\text{compass}} \Big) \cdot I(\phi) \\
\dot{\phi} &= g(\text{drift},\ \phi,\ \text{resonance})
\end{aligned}
\]

### 3. Individual Terms

**Field Force**
\[
f_{\text{field}} = -0.35\, c\,(c^2 - 1) + 0.92\, dc
\]

**5-Mode P-Drive**
\[
p_{\text{drive}}(\phi) = 
\begin{cases}
0.0   & \phi = 0 \quad (\text{Neutral}) \\
+0.85 & \phi = 1 \quad (\text{Forward1}) \\
+1.48 & \phi = 2 \quad (\text{Forward2}) \\
-1.0  & \phi = 3 \quad (\text{Reverse1}) \\
-1.7  & \phi = 4 \quad (\text{Reverse2})
\end{cases}
\]

**Kuramoto Coupling (Q-amplifier)**
\[
f_{\text{kuramoto}} = \sum_{i=0}^{4} K(Q) \cdot \sin\!\bigl(2\pi (\phi - i)/5\bigr), \quad K(Q) = 1 + \alpha Q
\]

**Van der Pol Term**
\[
f_{\text{vdp}} = \beta \, dc\,(1 - c^2)
\]

**Compass Operator**
\[
f_{\text{compass}} = \gamma \, \sin(\omega t + \phi \cdot \delta) \cdot \cos(\omega t + \phi \cdot \delta \cdot 1.618)
\]

**Phi–π–√2 Resonance (third dimension in 3D grid)**
\[
\text{resonance} = \sin(\phi \cdot \pi \cdot \sqrt{2}) \cdot \eta
\]

**Inversion**
\[
I(\phi) = 
\begin{cases}
1.0 & \phi < 3 \\
0.15 + 0.85 \tanh\bigl((\phi - 1.85) \cdot 5.8\bigr) & \phi \geq 3
\end{cases}
\]

**Phi-Regulator Update**
\[
\dot{\phi} = \text{resonance} + \text{pulse} + \text{threshold term}
\]

### 4. IEEE Load Ramp Integration
\[
p_{\text{ramp}}(t) = \lambda \cdot t, \quad \dot{dc} \leftarrow \dot{dc} + \kappa \cdot p_{\text{ramp}}(t)
\]

### 5. Classical Voltage Collapse Benchmark
\[
V_{\text{classic}}(t) = \frac{1}{1 + \mu \cdot (\lambda t)^2}
\]

**Current parameter set (v3.8 / 3D Polar Grid)**  
Q ≈ 1.62, λ ≈ 0.185 (118-Bus), strong discrete pulse and resonance term.

This set of equations forms the **mathematical heart** of the NEXAH instrument and is the basis for all higher-dimensional extensions (3D polar grid with Phi–π–√2 as third dimension).
