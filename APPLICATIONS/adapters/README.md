# NEXAH Adapter Layer

## Connecting External Systems to the NEXAH Framework

The **NEXAH framework** analyzes complex systems through **structural
regime landscapes**.

Instead of directly coupling to specific simulators or models, NEXAH
uses an **adapter layer** that converts external system dynamics into a
**finite state graph representation**.

This allows NEXAH to operate as a **navigation engine for complex
systems**, independent of the underlying simulator.

------------------------------------------------------------------------

# Conceptual Architecture

External systems produce system dynamics.

NEXAH operates on structural abstractions of those dynamics.

The adapter connects both layers.

External System / Simulator\
↓\
Adapter\
↓\
State Graph\
↓\
NEXAH\
↓\
Policy\
↓\
Actions

Examples of external systems:

-   power grid simulators (MATPOWER, pandapower, PyPSA)
-   dynamical systems (Lorenz, Kuramoto)
-   supply chain models
-   traffic simulations
-   cyber-physical systems
-   distributed computing systems
-   infrastructure networks

NEXAH does **not depend on a specific simulator**.

Instead, systems are connected through **adapters that expose a
structural state graph**.

------------------------------------------------------------------------

# Core Requirement

An adapter must expose a **finite state graph representation**.

This representation contains:

-   states
-   transitions
-   optional regime labels
-   optional control actions
-   optional risk targets

The state graph is the input structure for the **NEXAH navigation
engine**.

------------------------------------------------------------------------

# Minimal Adapter Interface

All adapters inherit from the base class:

`base_adapter.py`

Minimal interface:

``` python
class NexahAdapter:

    def states(self):
        """Return the list of system states"""
        raise NotImplementedError

    def transitions(self):
        """Return system transitions"""
        raise NotImplementedError

    def regimes(self):
        """Optional regime classification"""
        return None
```

Optional extensions:

``` python
def risk_targets(self):
    return []

def actions(self):
    return []

def metadata(self):
    return {}
```

------------------------------------------------------------------------

# Implemented Example Adapters

Adapters included in the repository:

  Adapter              System Type
  -------------------- ----------------------------------
  LorenzAdapter        chaotic dynamical system
  KuramotoAdapter      oscillator synchronization model
  PowerGridAdapter     energy infrastructure network
  SupplyChainAdapter   logistics network
  TrafficAdapter       urban traffic network

Location:

    APPLICATIONS/adapters/examples/

------------------------------------------------------------------------

# Running the Adapter Demo

Run the demo runner:

    python -m APPLICATIONS.adapters.run_adapter_demo

This will:

1.  load each adapter
2.  construct the state graph
3.  display transitions and regimes
4.  show metadata for each system

------------------------------------------------------------------------

# Creating a New Adapter

To connect a new system to NEXAH:

1.  create a new adapter class
2.  inherit from `NexahAdapter`
3.  implement `states()` and `transitions()`
4.  optionally define regimes, risk targets, and actions

Example:

``` python
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

------------------------------------------------------------------------

# Design Philosophy

### System‑agnostic architecture

NEXAH does not assume a specific domain or simulator.

### Structural abstraction

Only the **structural dynamics** of a system are required.

### Minimal interface

Adapters remain simple and lightweight.

### Extensibility

Adapters can expose additional metadata and control actions.

------------------------------------------------------------------------

# Role in the NEXAH Architecture

Simulator → Adapter → Structural Model → NEXAH Navigation Engine

Adapters enable NEXAH to operate across many domains while maintaining a
simple core architecture.

------------------------------------------------------------------------

# Summary

The adapter layer allows external systems to connect to NEXAH through a
simple structural interface.

Adapters translate simulator dynamics into **finite state graphs**,
enabling NEXAH to perform:

-   regime detection
-   cascade analysis
-   stability navigation
-   risk geometry analysis
-   stabilization planning

This makes NEXAH a **general navigation engine for complex dynamical
systems**.
