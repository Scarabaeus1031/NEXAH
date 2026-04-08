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
