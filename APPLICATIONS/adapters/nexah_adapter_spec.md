# NEXAH Adapter Specification

## Connecting External Systems to NEXAH

The NEXAH framework operates on **finite state graphs representing system regimes**.

External simulators and system models must therefore be translated into a **state graph representation** before they can be analyzed and navigated by NEXAH.

This document defines the **adapter interface** used to connect external systems to the NEXAH navigation engine.

---

# Conceptual Architecture

External systems produce system dynamics.

NEXAH operates on **abstract structural models** of these systems.

The adapter performs the translation.

External System / Simulator
↓
NEXAH Adapter
↓
State Graph
↓
NEXAH
↓
Policy
↓
Actions

Examples of external systems include:

- power grid simulators (MATPOWER, pandapower, PyPSA)
- infrastructure simulations
- supply chain models
- robotics simulations
- economic models
- distributed computing systems

NEXAH does not depend on a specific simulator.

Instead, systems are connected through **adapters that expose a structural state graph.**

---

# Core Requirement

An adapter must expose a **finite state graph representation** of the system.

The graph consists of:

- **states**
- **transitions**
- **optional regime annotations**

This representation forms the basis for all NEXAH operations.

---

# Minimal Adapter Interface

A minimal adapter should implement the following methods.

```python
class NexahAdapter:

    def states(self):
        """
        Return the set of system states.
        """
        raise NotImplementedError

    def transitions(self):
        """
        Return system transitions.

        Expected format:
        {
            state: [next_state_1, next_state_2]
        }
        """
        raise NotImplementedError

    def regimes(self):
        """
        Optional.

        Return regime classification for each state.
        Example:
        {
            "stable": "STABLE",
            "stress": "STRESS",
            "failure": "FAILURE"
        }
        """
        return None
```
Optional Adapter Extensions

Adapters may also expose additional information used by NEXAH.

Risk Targets

States that represent dangerous or unstable system conditions.


Example:

collapse
blackout
system_failure


Interface example:

def risk_targets(self):
    return ["collapse"]


Shock Events

External disturbances affecting system dynamics.

Example:

generator_failure
network_partition
traffic_spike


Control Actions

Actions that may modify system behavior.

Example:

start_reserve
shed_load
reroute_traffic
restart_service


Interface example:

def actions(self):
    return [
        "shed_load",
        "start_reserve",
        "reconfigure_grid"
    ]

Adapter Output Example

An adapter might produce the following graph:

states = ["stable", "stress", "failure"]

transitions = {
    "stable": ["stress"],
    "stress": ["failure", "stable"],
    "failure": ["collapse"]
}

regimes = {
    "stable": "STABLE",
    "stress": "STRESS",
    "failure": "FAILURE",
    "collapse": "COLLAPSE"
}

This representation becomes the structural input for the NEXAH navigation engine.

⸻

Role of the Adapter

The adapter performs three key tasks:
	1.	State Extraction

Convert simulator states into discrete system states.
	2.	Transition Mapping

Identify possible state transitions.
	3.	Regime Annotation

Label system states with stability classifications.

Once this structure is available, the NEXAH engine can perform:
	•	regime detection
	•	risk geometry analysis
	•	cascade modeling
	•	stabilization strategy planning
	•	policy-guided system navigation

⸻

Design Philosophy

Adapters allow NEXAH to remain system-agnostic.

Instead of hard-coding integrations for each simulator, the framework defines a generic structural interface.

Any system that can expose:

states
transitions
regimes

can be analyzed by NEXAH.

⸻

Example Adapter Locations

Adapters are expected to live in:
APPLICATIONS/adapters/

Example structure:
APPLICATIONS/
    adapters/
        nexah_adapter_spec.md
        base_adapter.py
        examples/
            energy_grid_adapter.py


Summary

The NEXAH adapter interface connects external systems to the NEXAH framework by exposing a finite structural representation of system dynamics.

System → Adapter → State Graph → NEXAH → Policy → Actions

This design enables NEXAH to function as a navigation layer for complex dynamical systems.


