# NEXAH Engine

The `ENGINE` directory contains the **computational core and research execution layer** of NEXAH.

It is where structural operators, simulations, analysis tools, and experimental modules are implemented and executed.

> The engine does not merely simulate systems.  
> It extracts structure, analyzes dynamics, and supports the transition from system behavior to navigable models.

---

## What the Engine does

The NEXAH Engine provides the computational machinery for:

- structural computation
- simulation support
- regime analysis
- resonance and flow analysis
- experiment execution
- visualization support
- kernel bridging between experiments and framework logic

It acts as the main bridge between:

~~~text
formal ideas → executable analysis → structural outputs
~~~

---

## Position inside NEXAH

Within the broader NEXAH architecture:

~~~text
Research / Framework
        ↓
      ENGINE
        ↓
analysis / experiments / outputs
        ↓
applications / navigation
~~~

The engine is therefore the **execution layer for structural discovery**.

---

## Important New Development (April 2026)

### Hierarchical Resonance Grid

A central new component in the Engine is the **`navigation/hierarchical_grid/`** folder.

This module contains the **discrete hierarchical state space model** for NEXAH navigation:

- Mod-77 base grid (77 + 308 states)
- Emergent exponent p ≈ 0.308
- Phi-Split mechanism for controlled transitions
- Resonance pairs and Prime Leap Chain (13 + 16 = 29)
- Mapping of real IEEE trajectories with drift and transfer detection

**See:**
- [`navigation/hierarchical_grid/README.md`](./navigation/hierarchical_grid/README.md)
- [`navigation/hierarchical_grid/results.md`](./navigation/hierarchical_grid/results.md)
- [`navigation/hierarchical_grid/equations.md`](./navigation/hierarchical_grid/equations.md)

This module forms the bridge between structural analysis and concrete navigation in applications (e.g., Power Systems).

---

## Core Responsibilities

The `ENGINE` currently supports work in areas such as:

- order-theoretic structures
- finite structural computation
- dynamical systems analysis
- flow and field extraction
- resonance analysis
- multi-agent experimentation
- simulation-based structure discovery
- **hierarchical grid-based navigation** (new)

---

## Directory Overview

| Folder                          | Role |
|---------------------------------|------|
| `core/`                         | core structural and computational components |
| `kernel/`                       | kernel-level logic and integration |
| `research/`                     | research modules and experiment families |
| `navigation/hierarchical_grid/` | **discrete hierarchical navigation grid** (new) |
| `simulation/`                   | simulation logic |
| `analysis/`                     | analysis scripts and post-processing |
| `visualization/`                | plotting and visual output logic |
| `applications/`                 | engine-side application support |
| `examples/`                     | runnable examples |

---

## Architecture Notes

For more detailed architectural context, see:

- [ENGINE_MAP.md](./ENGINE_MAP.md)
- [NEXAH_Engine_v1.0.0_Release_Notes.md](./NEXAH_Engine_v1.0.0_Release_Notes.md)
- [`navigation/hierarchical_grid/README.md`](./navigation/hierarchical_grid/README.md)

---

## Research Execution Layer

A major role of the engine is to host **active experiment environments**.

These live primarily in:

~~~text
ENGINE/research/experiments/
~~~

Current experiment families include, among others:

- prime modular resonance
- structured oscillator networks
- symmetry graph experiments
- stability-driven multi-agent systems
- **hierarchical resonance navigation**

---

## Engine Philosophy

The engine follows a few consistent principles:

- structure is extracted, not imposed
- computation should remain inspectable
- experiments should be modular
- outputs should feed back into framework logic
- dynamics are treated as sources of geometry, topology, and flow

In this sense, the engine is not only a software layer, but also a **research instrument**.

---

## Key Entry Points

- [ENGINE_MAP.md](./ENGINE_MAP.md)
- [NEXAH_Engine_v1.0.0_Release_Notes.md](./NEXAH_Engine_v1.0.0_Release_Notes.md)
- [`navigation/hierarchical_grid/README.md`](./navigation/hierarchical_grid/README.md)
- [research/README.md](./research/README.md)
- [research/experiments/](./research/experiments/)

---

## Related Repository Layers

For broader context, see:

- [`../README.md`](../README.md)
- [`../FRAMEWORK/README.md`](../FRAMEWORK/README.md)
- [`../NAVIGATOR/README.md`](../NAVIGATOR/README.md)

---

## Summary

The NEXAH Engine is the part of the repository where:

- theoretical ideas become executable
- simulations become analyzable
- experiments produce structure
- structure becomes usable for navigation

It is the computational heart of NEXAH.

**New addition:** The Hierarchical Resonance Grid as a bridge between analysis and concrete navigation.
