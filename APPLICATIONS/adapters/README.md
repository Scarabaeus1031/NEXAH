# NEXAH Adapter Layer

## Connecting External Systems to the NEXAH Framework

NEXAH is designed to operate on **finite structural representations of
dynamical systems**.

Instead of integrating directly with specific simulators, NEXAH uses an
**adapter layer** that translates external system models into a **state
graph representation**.

This makes the framework **system‑agnostic** and allows it to work with
many different domains.

Examples include:

-   power grids
-   supply chains
-   cyber‑physical systems
-   traffic simulations
-   distributed computing systems
-   infrastructure networks

------------------------------------------------------------------------

# Integration Architecture

External simulators describe the **physical or operational dynamics** of
a system.

NEXAH focuses on **navigation through system regimes**.

The adapter connects the two layers.

    External Simulator
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

External simulators produce system behavior.

The adapter extracts:

-   system states
-   possible transitions
-   regime classifications

This structural representation becomes the input for the **NEXAH
navigation engine**.

------------------------------------------------------------------------

# Minimal Adapter Interface

All adapters implement the base interface defined in:

    base_adapter.py

The minimal interface contains three required methods:

``` python
class NexahAdapter:

    def states(self):
        pass

    def transitions(self):
        pass

    def regimes(self):
        pass
```

Optional methods may expose:

-   risk targets
-   available control actions
-   metadata

------------------------------------------------------------------------

# Example Adapter

An example adapter is provided:

    examples/energy_grid_adapter.py

This demonstrates how a power grid simulator could expose its system
structure to NEXAH.

Example states:

    stable
    frequency_drop
    congestion
    failure
    collapse

Example transitions:

    stable → frequency_drop
    frequency_drop → congestion
    congestion → failure
    failure → collapse

Once translated into this structure, NEXAH can perform:

-   regime detection
-   cascade analysis
-   risk geometry computation
-   stabilization navigation

------------------------------------------------------------------------

# Design Philosophy

NEXAH does **not replace simulators**.

Instead, it acts as a **navigation layer above them**.

Simulators describe system physics.

NEXAH analyzes the **regime landscape** and supports **decision making
within that landscape**.

This allows NEXAH to integrate with existing modeling ecosystems rather
than competing with them.

------------------------------------------------------------------------

# Summary

Adapters provide the bridge between:

    Simulator → Structural Model → Navigation Engine

This architecture allows NEXAH to operate across many domains while
remaining conceptually simple.
