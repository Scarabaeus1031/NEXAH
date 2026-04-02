# NEXAH Core Equations – iee_core_geometry (v9.4 / Phase 2)

**Mathematical Foundations of the NEXAH Regime Navigation**

This document summarizes the current core mathematical structures (Lorenz-Core + Winding-Number-Trigger).

### 1. State Vector
\[
\mathbf{x} = \begin{bmatrix} c \\ dc \\ \phi_{\text{idx}} \end{bmatrix}
\]
- \( c \): state variable (field coordinate)  
- \( dc \): time derivative of \( c \) (drift)  
- \( \phi_{\text{idx}} \): discrete Phi regulator state (0–4)

### 2. Core Regime ODE (2-1-3 Regulator)
\[
\begin{aligned}
\dot{c} &= dc \cdot \text{contraction} \\
\dot{dc} &= \Big( \alpha_{\text{flow}} \cdot f_{\text{field}} 
+ \beta_{\text{swirl}} \cdot f_{\text{vdp}} 
+ \gamma_{\text{memory}} \cdot f_{\text{kuramoto}} 
+ \delta_{\text{resonance}} \cdot f_{\text{compass}} 
+ f_{\text{branch}} \Big) \cdot I(\phi) \cdot \text{slow_start} \\
\dot{\phi} &= g(\text{drift}, \phi, \text{resonance}, \text{winding})
\end{aligned}
\]

### 3. Individual Terms

**Field Force (Lorenz-Core)**
\[
f_{\text{field}} = \sigma (dc - c) + \rho \cdot c \cdot (1 - \phi_{\text{idx}})
\]

**5-Mode P-Drive (2-1-3 Regulator)**
\[
p_{\text{drive}}(\phi) = 
\begin{cases}
0.0   & \phi = 0 \quad (\text{Neutral}) \\
+0.85 & \phi = 1 \quad (\text{Forward1}) \\
+1.48 & \phi = 2 \quad (\text{Forward2 / Regulator}) \\
-1.0  & \phi = 3 \quad (\text{Reverse1}) \\
-1.7  & \phi = 4 \quad (\text{Reverse2})
\end{cases}
\]

**Kuramoto Coupling (Q-amplifier)**
\[
f_{\text{kuramoto}} = \sum_{i=0}^{4} K(Q) \cdot \sin\!\bigl(2\pi (\phi - i)/5\bigr), \quad K(Q) = 1 + \alpha Q
\]

**Van der Pol Oscillator**
\[
f_{\text{vdp}} = \beta \, dc\,(1 - c^2)
\]

**Compass Operator (Möbius-style + J-Reversal)**
\[
f_{\text{compass}} = \gamma \, \sin(\omega t + \phi \cdot \delta) \cdot \cos(\omega t + \phi \cdot \delta \cdot 1.618)
\]

**Phi–π–√2 Resonance**
\[
\text{resonance} = \sin(\phi \cdot \pi \cdot \sqrt{2}) \cdot \eta
\]

**Winding-Number Contribution (neuer Trigger)**
\[
f_{\text{winding}} = \text{winding_number} \cdot \kappa
\]

**Inversion (Bass-Schlüssel / J-Spiegel)**
\[
I(\phi) = 
\begin{cases}
1.0 & \phi < 3 \\
0.15 + 0.85 \tanh\bigl((\phi - 1.85) \cdot 5.8\bigr) & \phi \geq 3
\end{cases}
\]

**New tunable Coefficients (from log)**
- \(\alpha_{\text{flow}} = 0.95\) (ALPHA_FLOW)
- \(\beta_{\text{swirl}} = 0.65\) (BETA_SWIRL)
- \(\gamma_{\text{memory}} = 0.40\) (GAMMA_MEMORY)
- \(\delta_{\text{resonance}} = 0.25\) (DELTA_RESONANCE)

**Phi-Regulator Update**
\[
\dot{\phi} = \text{resonance} + f_{\text{winding}} + \text{pulse} + \text{threshold term}
\]

### 4. IEEE Load Ramp Integration
\[
p_{\text{ramp}}(t) = \lambda \cdot t, \quad \dot{dc} \leftarrow \dot{dc} + \kappa \cdot p_{\text{ramp}}(t) \cdot \text{slow_start}
\]

### 5. Classical Voltage Collapse (Benchmark)
\[
V_{\text{classic}}(t) = \frac{1}{1 + \mu \cdot (\lambda t)^2}
\]

**Current parameter set (v9.4)**  
Q ≈ 1.62, λ ≈ 0.195 (tuned), winding_threshold ≈ 17.8–18.0, strong contraction + slow_start.

**Theoretischer Kern (Phase 2):**  
Das System beschreibt den **Space inbetween** als Q°-Zentrum (P-Regulator), wobei der Winding-Number-Thread den Übergang navigiert. Die 2-1-3-Struktur ist der zentrale Regulator, der den Zipper (Keil) stabilisiert.

This set of equations constitutes the **mathematical heart** of the NEXAH instrument and is the basis for all higher-dimensional extensions (IEEE 118-Bus, 300-Bus, etc.).
