# NEXAH Kernel

Minimal navigation kernel for exploring and intervening in complex systems.

The NEXAH kernel provides a lightweight framework for analyzing structural systems,
identifying regime landscapes, and testing structural interventions.

It is designed as a **modular system navigation engine** that can operate on graphs
representing infrastructures, ecosystems, networks, or other complex systems.

---

# Core Idea

NEXAH models systems as **structural graphs embedded in regime landscapes**.

The kernel analyzes possible trajectories through the system and allows simulation
of structural modifications to explore system resilience.

Pipeline:

System Graph
↓
Regime Landscape
↓
Navigation Analysis
↓
Structural Intervention

---

# Kernel Architecture

The NEXAH kernel follows a simple layered structure:


System Graph
│
▼
Regime Landscape (MESO)
│
▼
Navigation Engine
│
▼
Action Engine (MEVA)
│
▼
Structural Intervention

This allows complex systems to be **analyzed, navigated, and structurally modified**.

---

# Kernel Components

The NEXAH kernel consists of a small set of modular layers:

| Layer | Role |
|------|------|
| `models.py` | Core data structures |
| `orientation.py` | System orientation |
| `archy.py` | Architecture representation |
| `meso.py` | Regime landscape construction |
| `navigation.py` | Navigation analysis |
| `meva.py` | Structural action simulation |
| `nexah_kernel.py` | Kernel interface |

---

# Minimal Example

```python
from ENGINE.nexah_kernel import StructuralGraph
from ENGINE.nexah_kernel import NexahKernel

graph = StructuralGraph(
    nodes={"A": {}, "B": {}, "C": {}},
    edges=[("A","B"),("B","C")],
    weights={}
)

landscape = {
    "attractors": ["C"],
    "basins": {"stable": ["B","C"], "unstable": ["A"]},
    "thresholds": ["B"]
}

kernel = NexahKernel(graph, landscape)

analysis = kernel.analyze_system()

print(analysis.trajectories)

