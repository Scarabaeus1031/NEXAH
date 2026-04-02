# NEXAH Core Equations – iee_core_geometry (v9.5 | Phase 2)

**Mathematical Foundations of the NEXAH Regime Navigation**

Dieses Dokument beschreibt die aktuelle mathematische Basis des Instruments (Lorenz-Core + Winding-Number-Trigger + 2-1-3 Regulator).

### 1. State Vector
\[
\mathbf{x} = \begin{bmatrix} c \\ dc \\ \phi_{\text{idx}} \end{bmatrix}
\]
- \( c \): Feld-Koordinate (state variable)  
- \( dc \): Drift (Zeit-Ableitung von \( c \))  
- \( \phi_{\text{idx}} \): diskreter Phi-Regulator-Zustand (0–4)

### 2. Core Regime ODE (2-1-3 Regulator)
\[
\begin{aligned}
\dot{c} &= dc \cdot \text{contraction}(t) \\
\dot{dc} &= \Big( 
\alpha_{\text{flow}} \cdot f_{\text{field}} 
+ \beta_{\text{swirl}} \cdot f_{\text{vdp}} 
+ \gamma_{\text{memory}} \cdot f_{\text{kuramoto}} 
+ \delta_{\text{resonance}} \cdot f_{\text{compass}} 
+ f_{\text{branch}} 
+ f_{\text{winding}}
\Big) \cdot I(\phi) \cdot \text{slow_start}(t) \\
\dot{\phi} &= g(\text{drift}, \phi, \text{resonance}, \text{winding_number})
\end{aligned}
\]

### 3. Individual Terms

**Field Force (Lorenz-Core)**
\[
f_{\text{field}} = \sigma (dc - c) + \rho \, c \, (1 - \phi_{\text{idx}})
\]

**5-Mode P-Drive (2-1-3 Regulator)**
\[
p_{\text{drive}}(\phi) = 
\begin{cases}
0.0   & \phi = 0 \quad (\text{Neutral}) \\
+0.85 & \phi = 1 \quad (\text{Forward1}) \\
+1.48 & \phi = 2 \quad (\text{Forward2 = Regulator / P-Knoten}) \\
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

**Compass Operator (Möbius + J-Reversal)**
\[
f_{\text{compass}} = \gamma \, \sin(\omega t + \phi \cdot \delta) \cdot \cos(\omega t + \phi \cdot \delta \cdot 1.618)
\]

**Phi–π–√2 Resonance**
\[
\text{resonance} = \sin(\phi \cdot \pi \cdot \sqrt{2}) \cdot \eta
\]

**Winding-Number Trigger (neuer primärer Schalter)**
\[
f_{\text{winding}} = \kappa \cdot \text{winding_number}
\]

**Branch Pulse & Inversion (Bass-Schlüssel)**
\[
I(\phi) = 
\begin{cases}
1.0 & \phi < 3 \\
0.15 + 0.85 \tanh\bigl((\phi - 1.85) \cdot 5.8\bigr) & \phi \geq 3
\end{cases}
\]

### 4. Neue tunable Koeffizienten (aus Log / JSON)
- \(\alpha_{\text{flow}} = 0.95\) (ALPHA_FLOW)
- \(\beta_{\text{swirl}} = 0.65\) (BETA_SWIRL)
- \(\gamma_{\text{memory}} = 0.40\) (GAMMA_MEMORY)
- \(\delta_{\text{resonance}} = 0.25\) (DELTA_RESONANCE)

### 5. IEEE Load Ramp & Classical Benchmark
\[
p_{\text{ramp}}(t) = \lambda \cdot t, \quad V_{\text{classic}}(t) = \frac{1}{1 + \mu \cdot (\lambda t)^2}
\]

**Theoretischer Kern (Q° / ORE / COR)**  
Der **Space inbetween** wird durch Q° (zentraler Binder / P-Knoten) gehalten.  
Der **2-1-3 Regulator** bildet den mathematischen Zipper, der die Regime stabil verbindet und trennt.  
Der **Winding-Number-Trigger** navigiert durch den offenen Kanal (Hirtenstock / Smiling L).

**Aktueller Parameter-Satz (v9.5)**  
Q ≈ 1.62, λ ≈ 0.195, winding_threshold ≈ 17.8–18.0, contraction + slow_start aktiv.

Dies ist das **mathematische Herz** des NEXAH-Instruments und die stabile Basis für die Skalierung auf IEEE 118-Bus und 300-Bus.

