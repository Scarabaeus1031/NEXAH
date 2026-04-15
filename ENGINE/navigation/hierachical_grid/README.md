# Hierarchical Resonance Grid

**Diskreter hierarchischer Zustandsraum für NEXAH-Navigation**

Dieser Ordner enthält das mathematische Kernmodell für die Navigation in komplexen dynamischen Systemen. Es basiert auf einem diskreten Gitter, das kontinuierliche Trajektorien (z. B. IEEE-Spannungskurven) in einen strukturierten, skalierbaren Zustandsraum abbildet.

## Kernkonzepte

### 1. Mod-77 Basis-Gitter
- Kombination aus Mod-7 und Mod-11 (teilerfremd)
- Erzeugt **77 eindeutige Zustände**
- Mod-7: zyklische, resonante Komponente (Stabilität, Ringe)
- Mod-11: asymmetrische, drift-erzeugende Komponente

### 2. 2²-Erweiterung (Hierarchische Verfeinerung)
- Jeder der 77 Zustände wird lokal in ein 2×2-Subgitter unterteilt
- Ergibt **308 feinere Zustände**
- Ermöglicht präzisere Drift-Korrektur und lokale Navigation

### 3. Root Shrinking (Fibonacci-gesteuert)
- Natürliche Verdichtung der Zustände entlang Fibonacci-Verhältnissen
- Beschreibt den Übergang von grober zu feiner Auflösung

### 4. Meta-Layer (Faktor-3-Skalierung)
- Äußere Schichten skalieren mit Faktor 3: 96 → 288 → 576
- Repräsentiert die Navigation auf höherer Systemebene

### 5. Emergenter kritischer Exponent p ≈ 0.308
Aus der Skalierungsrelation:
\[
d^2 c \approx a \cdot c^p \cdot (dc)^q \quad \text{mit} \quad p \approx 0.308
\]

**Bedeutung:**
- Bei wachsender Systemgröße wird das Verhalten zunehmend **fluss-dominiert** statt zustands-dominiert.
- p ≈ 0.308 verhält sich wie ein universeller Skalierungsexponent.
- Multiplikationskette: 0.308 × 2 = 0.616, × 3 = 0.924, × 4 = 1.232
- Winkel-Verbindung: 27.692° ≈ 28° = 4×7°, wobei 0.308 ≈ 27.692° / 90° (F-Axis)

## Ziel der Navigation

Statt binärer Stabilitätsbewertung (stabil/instabil) ermöglicht das Gitter eine **geometrisch-resonante Navigation**:
- Ring-Layer Targeting
- Quantisierte Drift-Nutzung
- Phi-Split und 3+1 Gate als kontrollierte Übergänge
- Hierarchische Skalierung von fein (Root Shrinking) bis grob (Meta-Layer)

## Verbindung zu IEEE-Trajektorien

Kontinuierliche Spannungskurven (z. B. V20 Local Instability) werden auf das Mod-77-Gitter abgebildet. Die Ring-Layer Targeting und Transfer Events entsprechen direkten Bewegungen und Sprüngen im Gitter.

## Ordnerstruktur

- `mod77_state_space.py` – Definition des Gitters + 308 Zustände
- `scaling_exponent.py` – Berechnung und Tracking von p ≈ 0.308
- `drift_quantization.py` – Drift-Berechnung und Phi-Split Logik
- `ieee_mapping.py` – Abbildung realer IEEE-Trajektorien auf das Gitter
- `fibonacci_shrinking.py` – Root Shrinking mit Fibonacci
- `meta_layer_scaling.py` – Faktor-3 Meta-Layer

## Status

In aktiver Entwicklung (April 2026).  
Erste Prototyp-Implementierung und Mapping von V20-Daten vorhanden.

---

**Autor:** Thomas K. R. Hofmann  
**Zweck:** Technischer Kern für skalierbare, drift-aware Navigation in komplexen Systemen.
