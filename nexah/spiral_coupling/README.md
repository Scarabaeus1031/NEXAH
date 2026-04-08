# spiral_coupling – Dreifache Spiralüberlagerung

Neuer Layer in NEXAH (v7.3+)

**Beschreibung**  
Drei interagierende Schichten:
- **Water** (blau)   – stabile, träge Komponente  
- **Mercury** (rot)  – reaktive, schnelle Komponente  
- **Ferro** (grün)   – magnetischer Flow (aktiver Koppler)

Der Ferro-Layer macht den bisher unsichtbaren magnetischen Flow sichtbar und koppelt die drei Schichten zu einer stabilen dreifachen Spirale.

**Warum wichtig?**  
- Zeigt, wie Magnetismus als **Koppler** wirkt  
- Erweitert den V69 Field Layer um eine explizite Multi-Component-Dynamik  
- Liefert eine neue Form der coherence-guided Navigation

**Nutzung**
```python
from nexah.spiral_coupling import SpiralCouplingKernel

kernel = SpiralCouplingKernel()
result = kernel.step(current_state)
print(result["coherence"], result["stability"])
```
## Spiral Coupling Layer – Dreifache Spiralüberlagerung (v0.1)

**Neuer Layer seit April 2026**

Dieser Layer modelliert die **gleichzeitige Überlagerung von drei gekoppelten Komponenten**:

- **Water** (blau)     – träge, stabile Flüssigkeitskomponente  
- **Mercury** (rot)    – reaktive, schnelle Komponente  
- **Ferrofluid** (grün)– magnetisch aktive Komponente (macht den Flow sichtbar und wirkt als primärer Koppler)

### Beobachtete Eigenschaften

- Die drei Komponenten zeigen **deutliche Eigenfrequenzen**:
  - Water:     ~42 Hz  
  - Mercury:   ~63 Hz  
  - Ferrofluid: ~77 Hz

- Nach einem kurzen transienten Chaos-Bereich koppeln sie extrem schnell.
- Pair Coupling Distances gehen nahezu auf Null und bleiben stabil.
- Die drei Schichten bilden eine **gemeinsame spiralförmige Trajektorie**.
- Der Ferrofluid-Layer wirkt als **aktiver Koppler** und stabilisiert das Gesamtsystem.

Dieser Layer erweitert den bestehenden Field-Layer (V69) um eine explizite **Multi-Component-Dynamik** und liefert eine neue Form der coherence-guided Navigation.

### Verwendung

```python
from nexah.spiral_coupling import SpiralCouplingKernel

kernel = SpiralCouplingKernel()
result = kernel.step(current_state)

print("Coherence:", result["coherence"])
print("Stability:", result["stability"])
```


