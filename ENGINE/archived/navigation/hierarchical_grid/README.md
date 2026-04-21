# Hierarchical Resonance Grid

**Diskreter hierarchischer Zustandsraum für NEXAH-Navigation**

Dieser Ordner enthält das mathematische Kernmodell für drift-aware und geometrisch-resonante Navigation in komplexen dynamischen Systemen. Es bildet kontinuierliche Trajektorien (z. B. IEEE-Spannungskurven) auf einen strukturierten, skalierbaren Gitter-Zustandsraum ab.

## Kernkonzepte

### Mod-77 Basis-Gitter
- 77 Zustände aus Mod-7 × Mod-11 (teilerfremd)
- Mod-7: zyklische, resonante Komponente
- Mod-11: asymmetrische, drift-erzeugende Komponente

### 2²-Erweiterung
- Jeder Basis-Zustand wird in 4 feinere Zustände (±δ) unterteilt → **308 feinere Zustände**
- Ermöglicht lokale Drift-Präzision

### Emergenter kritischer Exponent p ≈ 0.308
Aus der Skalierungsrelation:
\[
d^2 c \approx a \cdot c^p \cdot (dc)^q \quad \text{mit} \quad p \approx 0.308
\]

**Vergleich mit bekannten Exponenten**  
Der Wert liegt in der Nähe kritischer Exponenten der Renormalisierungsgruppe (z. B. β ≈ 0.326 im 3D-Ising-Modell). Er beschreibt den Übergang von **zustands-dominiert** zu **fluss-dominiert** bei wachsender Systemgröße.

### Phi-Split (mathematische Definition)

Der Phi-Split ist der zentrale Mechanismus für kontrollierte Übergänge:

\[
\text{Drift-Magnitude} = \max\left( \left| \frac{\Delta r_7}{7} \right|, \left| \frac{\Delta r_{11}}{11} \right| \right)
\]

Ein Phi-Split wird ausgelöst, wenn:

\[
\text{Drift-Magnitude} > \theta_{\text{Phi}} \quad (\text{typischerweise } \theta_{\text{Phi}} = 0.25)
\]

**Bedeutung bei IEEE-Anwendungen**  
- Erkennt strukturierte Sprünge in Spannungstrajektorien (z. B. V20 Local Instability)
- Dient als Trigger für Ring-Layer-Wechsel oder kontrollierte Navigation
- Ersetzt reaktive PID/MPC-Regelung durch **geometrisch informierte** Übergänge
- Ermöglicht frühe Intervention (vor klassischem Voltage Collapse)

### Prime Leap & Resonanz-Paare
Die feinen Zustände bilden komplementäre Paare, deren Summen auf relevante Zahlen verweisen:
- 7.83 + 8.17 = 16 (= 2⁴)
- 4.83 + 8.17 = 13 (6. Prime)
- 13 + 16 = **29** (nächster Prime)

Dies deutet auf eine rekursive Prime-generierende Struktur hin.

## Ziel der Navigation

Statt binärer Stabilitätsbewertung ermöglicht das Gitter eine **geometrisch-resonante Navigation**:
- Ring-Layer Targeting
- Quantisierte Drift-Nutzung
- Phi-Split als kontrollierte Übergänge
- Hierarchische Skalierung (fein → grob)

## Verbindung zu IEEE-Trajektorien

Kontinuierliche Spannungskurven (z. B. aus V20 oder Closed-Loop-Controllern) werden direkt auf das Mod-77-Gitter abgebildet. Phi-Split und Transfer Events entsprechen realen Instabilitäts-Sprüngen und können für frühe Stabilisierung genutzt werden.

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
- Integration mit realen IEEE-Testfällen (IEEE9, IEEE118, IEEE300+)
- Erweiterung der Prime-Leap- und Resonanz-Strukturen

---

**Autor:** Thomas K. R. Hofmann  
**Zweck:** Technischer Kern für skalierbare, drift-aware Navigation in komplexen Systemen.
