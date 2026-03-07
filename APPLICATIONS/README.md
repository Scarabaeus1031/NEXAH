# NEXAH Applications

This directory contains practical system models and example applications
built with the **NEXAH framework**.

In addition to internal system models, this layer also contains the
**adapter interfaces** that allow external simulators to connect to
NEXAH.

------------------------------------------------------------------------

# Framework Navigation

  -------------------------------------------------------------------------------------------------
  Model           Description                        Module
  --------------- ---------------------------------- ----------------------------------------------
  **Stability     Conceptual foundation of system    [STABILITY_LANDSCAPE](./STABILITY_LANDSCAPE)
  Landscape**     stability                          

  **Gradient      Systems evolving along stability   [GRADIENT_SYSTEM](./GRADIENT_SYSTEM)
  Systems**       gradients                          

  **Drift         Gradient dynamics with external    [DRIFT_SYSTEM](./DRIFT_SYSTEM)
  Systems**       forces                             

  **Regime        Systems with multiple attractor    [REGIME_SYSTEM](./REGIME_SYSTEM)
  Systems**       regimes                            
  -------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# External System Integration

NEXAH can connect to **existing simulation ecosystems** through
adapters.

Instead of replacing existing simulators, NEXAH acts as a **navigation
layer above them**.

External systems describe **physical dynamics**, while NEXAH analyzes
**regime structure and system navigation**.

Simulator\
↓\
Adapter\
↓\
State Graph\
↓\
NEXAH Navigation\
↓\
Policy\
↓\
Actions

Examples of compatible systems include:

-   MATPOWER
-   pandapower
-   PyPSA
-   traffic simulations
-   cyber-physical system models
-   supply chain simulations
-   infrastructure network models

Adapters translate simulator output into **finite state graphs** that
NEXAH can analyze.

Adapter implementations live in:

APPLICATIONS/adapters

Structure:

adapters/ README.md nexah_adapter_spec.md base_adapter.py examples/
energy_grid_adapter.py

This layer allows NEXAH to remain **system-agnostic** while integrating
with many different simulation domains.

------------------------------------------------------------------------

# Modules

-   **Stability Landscape**\
    APPLICATIONS/STABILITY_LANDSCAPE

-   **Gradient Systems**\
    APPLICATIONS/GRADIENT_SYSTEM

-   **Drift Systems**\
    APPLICATIONS/DRIFT_SYSTEM

-   **Regime Systems**\
    APPLICATIONS/REGIME_SYSTEM

------------------------------------------------------------------------

While the core framework defines the formal operators and structural
semantics, the **applications demonstrate how these models can be used
to analyze real-world systems.**

In simple terms:

> **NEXAH helps understand where systems stabilize.**

Many complex systems evolve through different states and eventually
reach stable configurations.\
NEXAH provides tools to model these systems structurally and compute
their stable states.

------------------------------------------------------------------------

# From Structure to Application

`<img src="visuals/From_Stucture_to_Application.png" width="900">`{=html}

The NEXAH workflow connects formal structural theory with real-world
system analysis.

Formal Core → Structural Semantics → System Models → Applications

-   **Formal Core** defines the mathematical and logical operators\
-   **Structural Semantics** introduces regimes, frames, and thresholds\
-   **System Models** represent specific structural dynamics\
-   **Applications** demonstrate how these models analyze real systems

------------------------------------------------------------------------

# NEXAH Dynamical Framework

`<img src="visuals/nexah_dynamics_framework_overview.png" width="900">`{=html}

The NEXAH applications are built on a hierarchy of dynamical models
describing how systems evolve in structured state spaces.

Stability Landscape\
↓\
Gradient Systems\
↓\
Drift Systems\
↓\
Regime Systems

The following diagram summarizes the full dynamical hierarchy.

`<img src="visuals/nexah_dynamics_framework_detailed.png" width="900">`{=html}

------------------------------------------------------------------------

# 1. Stability Landscape

Defines the structural stability space of a system using a potential
function:

V(x)

This landscape determines attractors, ridges, and stability basins.

------------------------------------------------------------------------

# 2. Gradient Systems

Pure stability-driven dynamics:

dx/dt = -∇V(x)

Systems move along the gradient of the stability landscape and converge
toward attractors.

Typical examples include:

-   temperature gradients\
-   pressure systems\
-   energy landscapes\
-   ecological distributions

Application module:

[GRADIENT_SYSTEM](./GRADIENT_SYSTEM/README.md)

------------------------------------------------------------------------

# 3. Drift Systems

External forces modify gradient dynamics:

dx/dt = -∇V(x) + F(x,t)

Examples include:

-   ocean currents\
-   atmospheric transport\
-   particle drift in fluids\
-   migration flows

Application module:

[DRIFT_SYSTEM](./DRIFT_SYSTEM/README.md)

------------------------------------------------------------------------

# 4. Regime Systems

Regime systems describe systems with **multiple attractor basins** and
possible transitions between them.

dx/dt = -∇V(x) + R(x,t)

Regime systems may exhibit:

-   transition boundaries\
-   tipping points\
-   regime shifts

Examples include:

-   traffic flow vs congestion\
-   financial market regimes\
-   ecosystem state transitions\
-   infrastructure thresholds

Application module:

[REGIME_SYSTEM](./REGIME_SYSTEM/README.md)

------------------------------------------------------------------------

# Application Structure

`<img src="visuals/Applications_Navigation_Map.png" width="900">`{=html}

Stability Landscape\
↓\
Three structural system classes\
↓\
Example applications

The goal is to demonstrate how general system dynamics can be
represented, analyzed, and applied using the NEXAH framework.

------------------------------------------------------------------------

# Intro Model -- Stability Landscape

The **Stability Landscape** model introduces the central idea of NEXAH.

Systems evolve through possible states and eventually stabilize within
attractor regions of a stability landscape.

Directory:

[STABILITY_LANDSCAPE](./STABILITY_LANDSCAPE/README.md)

------------------------------------------------------------------------

# Builder Hub

Experimental ideas and community-built applications can be developed
within this framework.

Possible directions include:

-   new application domains\
-   prototype system models\
-   experimental simulations\
-   collaborative research extensions

------------------------------------------------------------------------

# Philosophy

NEXAH focuses on **structural stability in complex systems**.

Instead of predicting outcomes purely through statistical models, NEXAH
analyzes the **structure of possible system states** and determines
where systems stabilize.

In short:

> **NEXAH explores the stability landscape of complex systems.**
