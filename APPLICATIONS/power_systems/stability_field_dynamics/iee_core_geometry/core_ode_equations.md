# NEXAH Core Equations – iee_core_geometry

**v10.0 | Phase 3**  
**Mathematical Foundations of the NEXAH Regime Navigation**  
(Stand: 03. April 2026)

Dieses Dokument beschreibt die aktuelle mathematische Basis des Instruments:  
**Lorenz-Core + Iota-Ring + 2-1-3 Regulator + Winding-Number-Trigger**.

---

### 1. State Vector
\[
\mathbf{x} = \begin{bmatrix}
c \\
dc \\
\phi_{\text{idx}}
\end{bmatrix}
\]

- \( c \): Feld-Koordinate (state variable)  
- \( dc \): Drift (Geschwindigkeit des Feldes)  
- \( \phi_{\text{idx}} \): diskreter Phi-Regulator-Zustand (0–4)

### 2. Core Regime ODE (2-1-3 Regulator)
\[
\begin{aligned}
\dot{c} &= dc \cdot \text{contraction}(t) \\[4pt]
\dot{dc} &= \Bigl(
\alpha_{\text{flow}} \cdot f_{\text{field}} 
+ \beta_{\text{swirl}} \cdot f_{\text{vdp}} 
+ \gamma_{\text{memory}} \cdot f_{\text{kuramoto}} 
+ \delta_{\text{resonance}} \cdot f_{\text{compass}} 
+ f_{\text{branch}} 
+ f_{\text{winding}} 
+ f_{\text{iota}}
\Bigr) 
\cdot I(\phi) 
\cdot \text{slow_start}(t) \\[8pt]
\dot{\phi} &= g\bigl(\text{drift},\ \phi,\ \text{resonance},\ \text{winding_number},\ \text{iota_ring}\bigr)
\end{aligned}
\]

### 3. Wichtigste Terme

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
+1.48 & \phi = 2 \quad (\text{Forward2 = P-Regulator}) \\
-1.0  & \phi = 3 \quad (\text{Reverse1}) \\
-1.7  & \phi = 4 \quad (\text{Reverse2})
\end{cases}
\]

**Kuramoto Coupling (Q-Amplifier)**
\[
f_{\text{kuramoto}} = \sum_{i=0}^{4} K(Q) \sin\!\bigl(2\pi (\phi - i)/5\bigr), \quad K(Q) = 1 + \alpha Q
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

**Winding-Number Trigger**
\[
f_{\text{winding}} = \kappa \cdot \text{winding_number}
\]

**Iota-Ring (neu in v10.0)**
\[
f_{\text{iota}} = 0.35 \cdot \sin\!\bigl(2\pi (t-36)/19\bigr)
\]

**Branch Pulse & Inversion (Bass-Schlüssel)**
\[
I(\phi) = 
\begin{cases}
1.0 & \phi < 3 \\
0.15 + 0.85 \tanh\bigl((\phi - 1.85) \cdot 5.8\bigr) & \phi \geq 3
\end{cases}
\]

### 4. Tunable Koeffizienten

| Parameter            | Wert   | Beschreibung                  |
|----------------------|--------|-------------------------------|
| \(\alpha_{\text{flow}}\)   | 0.95   | ALPHA_FLOW                    |
| \(\beta_{\text{swirl}}\)   | 0.65   | BETA_SWIRL                    |
| \(\gamma_{\text{memory}}\) | 0.40   | GAMMA_MEMORY                  |
| \(\delta_{\text{resonance}}\) | 0.25 | DELTA_RESONANCE               |
| \(Q\)                | 1.62   | Q-Amplifier                   |
| WINDING_THRESHOLD    | 6.5–18.0 | je nach Netzgröße            |

### 5. IEEE Load Ramp & Klassischer Benchmark
\[
p_{\text{ramp}}(t) = \lambda \cdot t, \qquad
V_{\text{classic}}(t) = \frac{1}{1 + \mu \cdot (\lambda t)^2}
\]

### 6. Theoretischer Kern

- **Q° / ORE / COR**: Zentraler Binder, der den **Space inbetween** stabil hält.  
- **2-1-3 Regulator**: Mathematischer Zipper, der die Regime verbindet und trennt.  
- **Iota-Ring + Winding-Number-Trigger**: Navigiert durch den offenen Kanal (Hirtenstock / Smiling L).  
- **Geometrischer Frühwarnmechanismus**: Erkennt den kritischen Übergang **unabhängig von der Netzgröße**.

**Dies ist das mathematische Herz des NEXAH-Instruments** und die stabile Basis für alle Skalierungs-Tests (IEEE 118, 300, 1354 und 9241 Bus).

---
