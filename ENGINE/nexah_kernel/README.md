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

```
System Graph
    ↓
Regime Landscape
    ↓
Navigation Analysis
    ↓
Structural Intervention
```

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
```

---

# Demo

A minimal runnable demo is included:

```
ENGINE/nexah_kernel/demo_navigation.py
```

Run from repository root:

```
python -m ENGINE.nexah_kernel.demo_navigation
```

---

# Testing

A minimal kernel test is included:

```
ENGINE/nexah_kernel/test_kernel.py
```

Run with:

```
python -m ENGINE.nexah_kernel.test_kernel
```

---

# Design Principles

The NEXAH kernel follows three principles:

**Minimal Core**

The kernel is intentionally small and modular.

**System-Oriented**

Focus on system structure, regimes, and navigation rather than data pipelines.

**Composable**

The kernel can be embedded into larger simulations, infrastructure models,
or decision-support systems.

---

# Status

Current status: **experimental kernel**

The API may evolve as the framework expands.

---

# NEXAH

NEXAH is part of the broader SCARABÆUS1033 research framework exploring
navigation and structural resilience in complex systems.
