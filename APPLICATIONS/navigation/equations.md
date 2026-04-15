# NEXAH Navigation – Mathematical Equations

## 1. Mod-77 Hierarchical Resonance Grid

**Basis states**
\[
77 = 7 \times 11
\]

**Fine states**
\[
308 = 77 \times 4
\]

**Voltage normalization**
\[
v_{\text{norm}} = \frac{V - 0.65}{0.40}, \quad V \in [0.65, 1.05]\ \text{p.u.}
\]

**State quantization**
\[
r_7 = \round(v_{\text{norm}} \cdot 6) \mod 7
\]
\[
r_{11} = \round(v_{\text{norm}} \cdot 10) \mod 11
\]

**State index**
\[
\text{index} = r_7 \cdot 11 + r_{11}
\]

**Drift between states**
\[
\Delta r_7 = (r_7^{(t+1)} - r_7^{(t)}) \mod 7
\]
\[
\Delta r_{11} = (r_{11}^{(t+1)} - r_{11}^{(t)}) \mod 11
\]

**Normalized drift magnitude**
\[
\text{drift\_magnitude} = \max\left( \left| \frac{\Delta r_7}{7} \right|, \left| \frac{\Delta r_{11}}{11} \right| \right)
\]

## 2. Event Detection

**Phi-Split**
\[
\text{Phi-Split} \quad \text{if} \quad \text{drift\_magnitude} > 0.25
\]

**Transfer Event**
\[
\text{Transfer Event} \quad \text{if} \quad \text{drift\_magnitude} > 0.7
\]

## 3. Scaling Exponent

**Emergent exponent**
\[
p \approx 0.308
\]

**Multiplication chain**
\[
p \times 1 = 0.308, \quad p \times 2 = 0.616, \quad p \times 3 = 0.924, \quad p \times 4 = 1.232
\]

**Geometric relation**
\[
p \approx \frac{27.692^\circ}{90^\circ} \approx 28^\circ = 4 \times 7^\circ
\]

## 4. IEEE Trajectory Mapping

In the current prototype (`ieee9_navigation.py`) a typical voltage collapse trajectory from 0.98 p.u. to 0.65 p.u. produces:

- 13 discrete time steps
- 9 Phi-Split events
- 9 Transfer events
- Final state: (0, 0)

---

**Status:** April 2026  
All equations are directly implemented and numerically verified in the current codebase.
