# Spiral Coupling Layer – Dreifache Spiralüberlagerung

**Neuer Layer in NEXAH (April 2026)**

Dieser Layer modelliert die **gleichzeitige Überlagerung und Kopplung von drei unterschiedlichen Komponenten**:

- **Water** (blau)      – träge, stabile Flüssigkeitskomponente (~42 Hz Eigenfrequenz)  
- **Mercury** (rot)     – reaktive, schnelle Komponente (~63 Hz Eigenfrequenz)  
- **Ferrofluid** (grün) – magnetisch aktive Komponente (~77 Hz Eigenfrequenz)

Der **Ferrofluid-Layer** wirkt als primärer Koppler und macht den magnetischen Flow sichtbar.

![Triple Spiral Coupling Overview](visuals/triple_spiral_coupling_overview.png)

### Wichtige Eigenschaften

- Nach einem kurzen transienten Chaos-Bereich koppeln die drei Schichten sehr schnell und stabil.  
- Pair Coupling Distances gehen nahezu auf Null und bleiben stabil.  
- Die Komponenten bilden eine gemeinsame **spiralförmige Trajektorie**.  
- Der Ferrofluid-Layer stabilisiert das Gesamtsystem durch magnetische Kopplung.

### Span-Gurt / Elastic Dual Lock

Der **Grey Channel** wird als zentrale **Dual-Strand-Struktur** mit einer elastischen Achse (Span-Gurt) modelliert.  
Diese Achse wirkt als direkte Kopplungslinie zwischen den beiden Grey Strands und ermöglicht schnelle, phasengesteuerte Übergänge (Switch-Verhalten).  

Sie entspricht dem magnetischen Flow, der die drei Komponenten verbindet und stabilisiert.  
Aus Beobachterperspektive erscheint dieser Bereich als „stiller Raum“, da die schnelle Bewegung des Feldes dort kohärent und geordnet verläuft.

*(Siehe auch: NEXAH v8.9 – Dual-Strand Grey Channel + Phase Feedback und v9.0 – Switch Layer on Dual-Strand Grey Channel)*

### Warum dieser Layer wichtig ist

- Erweitert den bestehenden V69 Field Layer um eine explizite **Multi-Component-Dynamik mit Switch-Verhalten**.  
- Zeigt, wie Magnetismus als **aktiver Koppler** zwischen unterschiedlichen Schichten wirkt.  
- Liefert eine neue Form der **coherence-guided Navigation** mit elastischer Dual-Lock-Struktur.

### Verwendung

```python
from nexah.spiral_coupling import SpiralCouplingKernel

kernel = SpiralCouplingKernel()
result = kernel.step(current_state)

print("Coherence:", result["coherence"])
print("Stability:", result["stability"])
print("Avg Coupling Distance:", result["layer_state"]["avg_coupling_dist"])
