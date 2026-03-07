
# NEXAH Applications

This directory contains practical system models and example applications built with the **NEXAH framework**.

---

## Framework Navigation

| Model | Description | Module |
|------|-------------|--------|
| **Stability Landscape** | Conceptual foundation of system stability | [STABILITY_LANDSCAPE](./STABILITY_LANDSCAPE) |
| **Gradient Systems** | Systems evolving along stability gradients | [GRADIENT_SYSTEM](./GRADIENT_SYSTEM) |
| **Drift Systems** | Gradient dynamics with external forces | [DRIFT_SYSTEM](./DRIFT_SYSTEM) |
| **Regime Systems** | Systems with multiple attractor regimes | [REGIME_SYSTEM](./REGIME_SYSTEM) |

### Modules

- **Stability Landscape**  
  `APPLICATIONS/STABILITY_LANDSCAPE`

- **Gradient Systems**  
  `APPLICATIONS/GRADIENT_SYSTEM`

- **Drift Systems**  
  `APPLICATIONS/DRIFT_SYSTEM`

- **Regime Systems**  
  `APPLICATIONS/REGIME_SYSTEM`

---

# External System Integration

NEXAH can connect to **existing simulators and system models** through an adapter layer.

Instead of replacing existing simulators, NEXAH acts as a **navigation layer above them**.

External simulators describe **system dynamics**, while NEXAH analyzes the **regime structure and navigation possibilities**.

Simulator
    ↓
Adapter
    ↓
State Graph
    ↓
NEXAH Navigator
    ↓
Policy
    ↓
Actions

Examples of compatible systems include:

- MATPOWER
- pandapower
- PyPSA
- traffic simulations
- cyber-physical systems
- supply chain simulations
- infrastructure models

Adapters translate simulator output into **finite state graphs** that NEXAH can analyze.

Adapter implementations live in:

APPLICATIONS/adapters

Structure:

adapters/
   README.md
   nexah_adapter_spec.md
   base_adapter.py
   examples/
      energy_grid_adapter.py

This architecture allows NEXAH to remain **system-agnostic** while integrating with existing simulation ecosystems.

---

While the core framework defines the formal operators and structural semantics, the **applications demonstrate how these models can be used to analyze real-world systems.**

In simple terms:

> **NEXAH helps understand where systems stabilize.**

Many complex systems evolve through different states and eventually reach stable configurations.  
NEXAH provides tools to model these systems structurally and compute their stable states.

---

# From Structure to Application

<img src="visuals/From_Stucture_to_Application.png" width="900">

The NEXAH workflow connects formal structural theory with real-world system analysis.

The process follows four conceptual layers:

Formal Core → Structural Semantics → System Models → Applications

- **Formal Core** defines the mathematical and logical operators  
- **Structural Semantics** introduces regimes, frames, and thresholds  
- **System Models** represent specific structural dynamics  
- **Applications** demonstrate how these models analyze real systems  

---

# NEXAH Dynamical Framework

<img src="visuals/nexah_dynamics_framework_overview.png" width="900">

The NEXAH applications are built on a hierarchy of dynamical models describing how systems evolve in structured state spaces.

The framework introduces increasing levels of dynamical complexity:

Stability Landscape  
↓  
Gradient Systems  
↓  
Drift Systems  
↓  
Regime Systems  

The following diagram summarizes the full dynamical hierarchy.

<img src="visuals/nexah_dynamics_framework_detailed.png" width="900">

This diagram summarizes the **four core dynamical models** used in the NEXAH applications framework.

---

# Application Structure

<img src="visuals/Applications_Navigation_Map.png" width="900">

The applications follow a conceptual progression:

Stability Landscape (intro model)  
↓  
Three structural system classes  
↓  
Example applications  

The goal is to demonstrate how general system dynamics can be represented, analyzed, and applied using the NEXAH framework.

---

# Intro Model – Stability Landscape

The **Stability Landscape** model introduces the central idea of NEXAH.

Systems evolve through possible states and eventually stabilize within attractor regions of a stability landscape.

Directory:

[STABILITY_LANDSCAPE](./STABILITY_LANDSCAPE/README.md)

---

# Core System Classes

NEXAH focuses on three fundamental classes of dynamical systems.

Each class represents a different structural mechanism governing system evolution.

---

## Gradient Systems

Gradient systems evolve along the slope of a stability landscape.

System dynamics follow the gradient of a potential function:

dx/dt = -∇V(x)

Typical examples include:

- temperature gradients  
- pressure systems  
- energy landscapes  
- ecological distributions  

Application module:

[GRADIENT_SYSTEM](./GRADIENT_SYSTEM/README.md)

---

## Drift Systems

Drift systems extend gradient dynamics by introducing external forces that influence system motion.

dx/dt = -∇V(x) + F(x,t)

Examples include:

- ocean currents  
- atmospheric transport  
- particle drift in fluids  
- migration flows  

Application module:

[DRIFT_SYSTEM](./DRIFT_SYSTEM/README.md)

---

## Regime Systems

Regime systems describe systems with **multiple attractor basins** and possible transitions between them.

dx/dt = -∇V(x) + R(x,t)

Examples include:

- traffic flow vs congestion  
- financial market regimes  
- ecosystem state transitions  
- infrastructure thresholds  

Application module:

[REGIME_SYSTEM](./REGIME_SYSTEM/README.md)

---

# Builder Hub

Experimental ideas and community-built applications can be developed within this framework.

Possible directions include:

- new application domains  
- prototype system models  
- experimental simulations  
- collaborative research extensions  

---

# Philosophy

NEXAH focuses on **structural stability in complex systems**.

Instead of predicting outcomes purely through statistical models, NEXAH analyzes the **structure of possible system states** and determines where systems stabilize.

In short:

> **NEXAH explores the stability landscape of complex systems.**
