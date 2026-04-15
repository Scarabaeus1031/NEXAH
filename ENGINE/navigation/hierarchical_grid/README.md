# Hierarchical Resonance Grid

**Diskreter hierarchischer Zustandsraum für NEXAH-Navigation**

Dieser Ordner enthält das mathematische Kernmodell für drift-aware und geometrisch-resonante Navigation in komplexen dynamischen Systemen. Es bildet kontinuierliche Trajektorien (z. B. IEEE-Spannungskurven) auf einen strukturierten, skalierbaren Gitter-Zustandsraum ab.

## Kernkonzepte

- **Mod-77 Basis-Gitter**: 77 Zustände aus Mod-7 × Mod-11 (teilerfremd)
- **2²-Erweiterung**: 308 feinere Zustände für lokale Drift-Präzision
- **Emergenter kritischer Exponent p ≈ 0.308**: Beschreibt den Übergang von zustands-dominiert zu fluss-dominiert
- **Resonanz-Paare & Prime Leap**: Feine Zustände erzeugen Summen wie 13 und 16 → 13 + 16 = 29 (nächster Prime)
- **Phi-Split & Transfer Events**: Erkennung von strukturierten Drift-Sprüngen

## Mathematische Grundlage

### Skalierungsexponent p ≈ 0.308
Aus der Relation:
\[
d^2 c \approx a \cdot c^p \cdot (dc)^q \quad \text{mit} \quad p \approx 0.308
\]

Der Wert liegt in der Nähe kritischer Exponenten der Renormalisierungsgruppe (z. B. β ≈ 0.326 im 3D-Ising-Modell). Dies deutet auf skalierendes Verhalten nahe eines kritischen Punktes hin, bei dem große Systeme zunehmend fluss-dominiert werden.

### Phi-Split
Ein Phi-Split wird erkannt, wenn der normalisierte Drift eine Schwelle (z. B. 0.25) überschreitet. Dies dient als kontrollierter Übergang zwischen Ring-Layern (ähnlich einem geometrischen „Tor“).

### Prime Leap Chain
Die feinen Zustände bilden komplementäre Paare, deren Summen auf Prime-Zahlen und Potenzen verweisen:
- 7.83 + 8.17 = 16 (= 2⁴)
- 4.83 + 8.17 = 13 (6. Prime)
- 13 + 16 = **29** (nächster Prime)

Dies deutet auf eine rekursive Prime-generierende Struktur innerhalb des Gitters hin.

## Ziel der Navigation

Statt binärer Stabilitätsbewertung (stabil/instabil) ermöglicht das Gitter eine **geometrisch-resonante Navigation**:
- Ring-Layer Targeting
- Quantisierte Drift-Nutzung
- Phi-Split als kontrollierte Übergänge
- Hierarchische Skalierung (fein → grob)

## Ordnerstruktur

- `mod77_state_space.py` — Gitter + Fein-Zustände + Drift-Berechnung
- `scaling_exponent.py` — p ≈ 0.308 + Multiplikationskette + Prime Leap
- `drift_quantization.py` — Phi-Split- und Transfer-Event-Erkennung
- `ieee_mapping.py` — Abbildung realer IEEE-Trajektorien

**Siehe auch:** [`results.md`](results.md) für konkrete Analysen, Beispiele und Interpretationen.

## Status (April 2026)

In aktiver Entwicklung.  
Erste Prototyp-Implementierung mit V20-ähnlichen Trajektorien, Phi-Split-Erkennung und Prime-Leap-Beobachtungen vorhanden.

**Nächste Schritte:**
- Visualisierungen der Trajektorien und Phi-Split-Events
- Integration mit realen IEEE-Testfällen
- Erweiterung der Prime-Leap- und Resonanz-Strukturen

---

**Autor:** Thomas K. R. Hofmann  
**Zweck:** Technischer Kern für skalierbare, drift-aware Navigation in komplexen Systemen.
