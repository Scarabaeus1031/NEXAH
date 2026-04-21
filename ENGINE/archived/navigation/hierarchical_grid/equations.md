# Equations & Mathematical Definitions

## 1. Mod-77 State Space

Basis-Zustand:
\[
s = (r_7, r_{11}), \quad r_7 \in \{0,1,\dots,6\}, \quad r_{11} \in \{0,1,\dots,10\}
\]

Feine Zustände (2²-Erweiterung):
\[
fine_r7 = (r7 + dr7) \% 7, \quad fine_r11 = (r11 + dr11) \% 11, \quad dr \in \{-0.17, +0.17\}
\]

## 2. Skalierungsexponent

\[
d^2 c \approx a \cdot c^p \cdot (dc)^q \quad \text{mit} \quad p \approx 0.308
\]

Multiplikationskette:
- p × 2 = 0.616
- p × 3 = 0.924
- p × 4 = 1.232

## 3. Phi-Split Algorithmus

Drift-Magnitude:
\[
\text{Drift-Magnitude} = \max\left( \left| \frac{\Delta r_7}{7} \right|, \left| \frac{\Delta r_{11}}{11} \right| \right)
\]

Phi-Split Trigger:
\[
\text{Drift-Magnitude} > 0.25 \quad \Rightarrow \quad \text{Phi-Split \& Transfer Event}
\]

## 4. Prime Leap Chain

Beobachtete Resonanz-Paare:
- 7.83 + 8.17 = 16 (= 2⁴)
- 4.83 + 8.17 = 13
- 13 + 16 = **29** (nächster Prime)

Dies deutet auf eine rekursive Prime-generierende Struktur hin.

## 5. Weitere Konstanten

- α ≈ 63/64 ≈ 0.984375 (Kompressionsfaktor)
- 1/63 ≈ 0.01587 (Feinheitsfaktor)
- 28° = 4 × 7° → p ≈ 27.692° / 90° (F-Axis)

---

**Ziel:** Alle zentralen Formeln an einer Stelle sammeln für spätere Referenz (Applications, Papers, Dokumentation).
