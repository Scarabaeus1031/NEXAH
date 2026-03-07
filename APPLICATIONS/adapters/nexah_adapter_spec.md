# NEXAH Adapter Specification

## Connecting External Systems to NEXAH

The NEXAH framework operates on **finite state graphs representing
system regimes**.

External simulators and system models must therefore be translated into
a **state graph representation** before they can be analyzed and
navigated by NEXAH.

This document defines the **adapter interface** used to connect external
systems to the NEXAH navigation engine.

------------------------------------------------------------------------

# Conceptual Architecture

External systems produce system dynamics.

NEXAH operates on **abstract structural models** of these systems.

The adapter performs the translation.

External System / Simulator ↓ NEXAH Adapter ↓ State Graph ↓ NEXAH ↓
Policy ↓ Actions

Examples of external systems include:

-   power grid simulators (MATPOWER, pandapower, PyPSA)
-   infrastructure simulations
-   supply chain models
-   robotics simulations
-   economic models
-   distributed computing systems

NEXAH does not depend on a specific simulator.

Instead, systems are connected through **adapters that expose a
structural state graph.**

------------------------------------------------------------------------

# Core Requirement

An adapter must expose a **finite state graph representation** of the
system.

The graph consists of:

-   states
-   transitions
-   optional regime annotations

This representation forms the basis for all NEXAH operations.

------------------------------------------------------------------------

# Minimal Adapter Interface

A minimal adapter should implement the following methods.

class NexahAdapter:

    def states(self):
        """Return the set of system states"""
        raise NotImplementedError

    def transitions(self):
        """Return system transitions in the form {state: [next_states]}"""
        raise NotImplementedError

    def regimes(self):
        """Optional regime labels for states"""
        return None

------------------------------------------------------------------------

# Optional Adapter Extensions

Adapters may expose additional information.

### Risk Targets

States representing dangerous system conditions.

Example:

collapse blackout system_failure

### Control Actions

Actions that may modify system behavior.

Example:

shed_load start_reserve reroute_traffic restart_service

------------------------------------------------------------------------

# Example Graph Output

states = \["stable", "stress", "failure"\]

transitions = { "stable": \["stress"\], "stress": \["failure",
"stable"\], "failure": \["collapse"\] }

regimes = { "stable": "STABLE", "stress": "STRESS", "failure":
"FAILURE", "collapse": "COLLAPSE" }

This structure becomes the input for the **NEXAH navigation engine**.

------------------------------------------------------------------------

# Adapter Role

The adapter performs three tasks:

1.  State extraction from simulator outputs
2.  Transition mapping between system states
3.  Regime classification of states

Once provided, NEXAH can perform:

-   regime detection
-   cascade modeling
-   risk geometry analysis
-   stabilization navigation

------------------------------------------------------------------------

# Repository Location

Adapters should live in:

APPLICATIONS/adapters/

Example:

APPLICATIONS/ adapters/ nexah_adapter_spec.md base_adapter.py examples/
energy_grid_adapter.py

------------------------------------------------------------------------

# Summary

System → Adapter → State Graph → NEXAH → Policy → Actions

Adapters make NEXAH **system‑agnostic** and allow integration with many
kinds of dynamical systems.
