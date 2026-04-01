# NEXAH Core Equations – iee_core_geometry

**Mathematical Foundations of the Regime Navigation System**

This document summarizes the core mathematical structures developed through the 2D and 3D phases.

### 1. State Vector
\[
\mathbf{x} = \begin{bmatrix} c \\ dc \\ \phi_{\text{idx}} \end{bmatrix}
\]
- \( c \): field coordinate
- \( dc \): drift
- \( \phi_{\text{idx}} \): discrete Phi regulator (0–4)

### 2. Core Regime ODE
\[
\begin{aligned}
\dot{c} &= dc \\
\dot{dc} &= \Big( f_{\text{field}} + p_{\text{drive}} + f_{\text{kuramoto}} + f_{\text{vdp}} + f_{\text{compass}} \Big) \cdot I(\phi) \\
\dot{\phi} &= g(\text{drift},\ \phi,\ \text{resonance})
\end{aligned}
\]

### 3. Key Terms (selected)
- Field Force, 5-Mode P-Drive, Kuramoto Coupling (Q-amplifier), Van der Pol, Compass Operator
- **Phi–π–√2 Resonance** (third dimension in 3D grid)
- Inversion (Bass-Schlüssel)
- Discrete pulse term (impulsive behavior between attractor clusters)

### 4. IEEE Load Ramp & Classical Benchmark
\[
p_{\text{ramp}}(t) = \lambda \cdot t, \quad V_{\text{classic}}(t) = \frac{1}{1 + \mu \cdot (\lambda t)^2}
\]

**Current status (3D Polar Grid phase)**  
The system shows multi-shell resonance structures, a clear central channel, and self-similar patterns across scales.

This set of equations is the **mathematical heart** of NEXAH and the basis for higher-dimensional navigation.
