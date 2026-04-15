# Hierarchical Resonance Grid

**Diskreter hierarchischer Zustandsraum für NEXAH-Navigation**

Dieser Ordner enthält das mathematische Kernmodell für drift-aware Navigation in komplexen Systemen. Es bildet kontinuierliche Trajektorien (z. B. IEEE-Spannungskurven) auf einen strukturierten, skalierbaren Gitter-Zustandsraum ab.

## Kernkonzepte

- **Mod-77 Basis-Gitter**: 77 Zustände (Mod-7 × Mod-11)
- **2²-Erweiterung**: 308 feinere Zustände für präzise Drift-Navigation
- **Emergenter Exponent p ≈ 0.308**: Übergang von zustands- zu fluss-dominiert
- **Resonanz-Paare & Prime Leap**: 7.83+8.17=16, 4.83+8.17=13, 13+16=29
- **Phi-Split & Transfer Events**: Erkennung von strukturierten Sprüngen

## Ziel

Statt binärer Stabilitätsbewertung ermöglicht das Gitter eine **geometrisch-resonante Navigation**:
- Ring-Layer Targeting
- Quantisierte Drift-Nutzung
- Phi-Split und kontrollierte Übergänge
- Skalierung von fein (Root Shrinking) bis grob (Meta-Layer)

## Dateien

- `mod77_state_space.py` — Gitter-Definition + Fein-Zustände
- `scaling_exponent.py` — p ≈ 0.308 + Multiplikationskette + Prime Leap
- `drift_quantization.py` — Drift-Analyse + Phi-Split Erkennung
- `ieee_mapping.py` — Abbildung realer IEEE-Trajektorien

## Status (April 2026)

In aktiver Entwicklung.  
Erste Prototyp-Implementierung mit V20-ähnlichen Trajektorien und Phi-Split-Erkennung vorhanden.

**Siehe auch:** [`results.md`](results.md) für konkrete Analysen und Interpretationen.
