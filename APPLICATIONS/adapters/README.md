# NEXAH Adapter Layer

## Connecting External Systems to the NEXAH Framework

The **NEXAH framework** analyzes complex systems through **structural regime landscapes**.

Instead of directly coupling to specific simulators or models, NEXAH uses an **adapter layer** that converts external system dynamics into a **finite state graph representation**.

This allows NEXAH to operate as a:

> **navigation engine for complex dynamical systems**

independent of the underlying simulator.

---

# Conceptual Architecture

External systems produce system dynamics.

NEXAH operates on structural abstractions of those dynamics.

The adapter connects both layers.

```
External System / Simulator
            ↓
          Adapter
            ↓
        State Graph
            ↓
           NEXAH
            ↓
          Policy
            ↓
          Actions
```

---

# Core Requirement

An adapter must expose a **finite state graph representation**.

This representation contains:

- states  
- transitions  
- optional regime labels  
- optional control actions  
- optional risk targets  

The state graph is the input structure for the **NEXAH navigation engine**.

---

# 🔷 NEW: Internal Phase-Space Adapter (NEXAH Engine → Graph)

The adapter layer is not only used for external systems.

It now also connects **internal NEXAH dynamics** to the navigation framework.

---

## PhaseSpaceAdapter

The **PhaseSpaceAdapter** converts outputs of the NEXAH Dynamics Engine into a state graph.

### Input

- phase_map results  
- topology classifications  
- structural signatures  
- optional meta-fields  

### Output

- states (grid positions)  
- transitions (parameter adjacency + structure similarity)  
- metadata (system-level structure)  

---

## Interpretation

This enables NEXAH to:

- analyze its own simulations  
- detect structural regimes  
- construct transition graphs  
- navigate phase space  

---

## Result

> The NEXAH engine becomes **self-referential**

It can:

- simulate  
- extract structure  
- build graphs  
- navigate them  

---

# Minimal Adapter Interface

All adapters inherit from:

`base_adapter.py`

```python
class NexahAdapter:

    def states(self):
        raise NotImplementedError

    def transitions(self):
        raise NotImplementedError

    def regimes(self):
        return None
```

---

# Optional Extensions

```python
def risk_targets(self):
    return []

def actions(self):
    return []

def metadata(self):
    return {}
```

---

# Implemented Adapters

| Adapter | System Type |
|--------|------------|
| LorenzAdapter | chaotic system |
| KuramotoAdapter | oscillators |
| PowerGridAdapter | energy systems |
| SupplyChainAdapter | logistics |
| TrafficAdapter | traffic systems |
| PhaseSpaceAdapter | NEXAH internal |

---

# Running the Adapter Demo

```bash
python -m APPLICATIONS.adapters.run_adapter_demo
```

---

# Creating a New Adapter

```python
from APPLICATIONS.adapters.base_adapter import NexahAdapter

class MySystemAdapter(NexahAdapter):

    def states(self):
        return ["state_a", "state_b"]

    def transitions(self):
        return {
            "state_a": ["state_b"],
            "state_b": []
        }
```

---

# Adapter Categories

### A — External Systems
- power grids  
- infrastructure  
- traffic  
- supply chains  

### B — Dynamical Systems
- Lorenz  
- Kuramoto  
- attractor systems  

### C — Internal NEXAH Systems (NEW)
- phase maps  
- topology fields  
- meta fields  
- resonance structures  

---

# Design Philosophy

### System-agnostic
Works across domains.

### Structural abstraction
Only structure matters.

### Minimal interface
Adapters stay simple.

### Recursive capability (NEW)
NEXAH analyzes its own outputs.

---

# Role in Architecture

```
Simulator / Engine
        ↓
      Adapter
        ↓
   Structural Graph
        ↓
   NEXAH Navigation
        ↓
     Policy Layer
```

---

# 🔥 Key Insight

> Systems are not analyzed directly —  
> they are **converted into navigable state spaces**

---

# Summary

The adapter layer enables:

- system-independent modeling  
- structural abstraction  
- cross-domain compatibility  
- graph-based navigation  

And now also:

> **self-analysis of NEXAH-generated systems**

---

# 🚧 TO DO / NEXT STEPS

## 🔴 Phase System

- introduce instability / chaos into phase_map  
- create real phase transitions  
- improve classifier (reduce "Structured Network" dominance)  

## 🟠 Graph Construction

- replace linear connections with grid-neighbor topology  
- add transition weights  
- integrate flow direction into edges  
- detect real basins as nodes  

## 🔵 Meta Layer

- refine meta_field weighting  
- validate basin detection  
- identify stable vs unstable attractor regions  

## 🟢 Real-World Integration

- connect PowerGridAdapter to real simulation data  
- test stability navigation scenarios  
- simulate failure prevention strategies  

## 🟣 Control / Policy Layer (NEXT BIG STEP)

- implement action selection  
- build navigation policies  
- optimize transitions toward stable regimes  

---

# License

Apache 2.0
