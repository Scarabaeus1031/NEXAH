# Hierarchical Resonance Grid for Navigation

Dieser Ordner enthält das **diskrete hierarchische Zustandsraum-Modell** für NEXAH-Navigation.

## Kernkonzepte

- **Mod-77 Basis-Gitter**: 77 eindeutige Zustände aus Mod-7 × Mod-11
- **2²-Erweiterung**: Jeder Zustand wird lokal in 4 feinere Sub-Zustände unterteilt → 308 Zustände
- **Root Shrinking**: Fibonacci-gesteuerte Verdichtung der Zustände
- **Meta-Layer**: Skalierung mit Faktor 3 (96 → 288 → 576)
- **Emergenter Exponent p ≈ 0.308**: Beschreibt den Übergang von zustands-dominiert zu fluss-dominiert bei wachsender Systemgröße

## Mathematische Grundlage

Jeder Zustand \( s \) ist definiert als:
\[
s = (r_7, r_{11}), \quad r_7 \in \{0..6\}, \quad r_{11} \in \{0..10\}
\]

Feinjustierung:
\[
s_{\text{fine}} = (r_7 \pm \delta, \, r_{11} \pm \delta), \quad \delta \approx 0.17
\]

Der Skalierungsexponent \( p \approx 0.308 \) ergibt sich aus der Relation:
\[
d^2 c \approx a \cdot c^p \cdot (dc)^q
\]

## Integration mit IEEE-Trajektorien

Siehe `ieee_mapping.py` für die Abbildung kontinuierlicher Spannungstrajektorien (V20) auf das Mod-77-Gitter.

## Verwendung

Dieses Gitter dient als Grundlage für:
- Ring-Layer Targeting
- Drift-Quantisierung
- Phi-Split und 3+1 Gate Logik
- Hierarchische Navigation in großen Systemen

---

**Status**: In aktiver Entwicklung – erste Prototyp-Implementierung vorhanden.
