# NEXAH Applications

![NEXAH Exploration
Hub](../EXPLORATION_HUB/visuals/NEXAH_Exploration_Map.png)

The **APPLICATIONS** layer contains practical system models built with
the **NEXAH framework**.

These modules demonstrate how the structural operators of NEXAH can be
applied to analyze **real dynamical systems**.

Applications translate theoretical structures into **simulation models,
analysis pipelines, and navigation strategies**.

------------------------------------------------------------------------

# Position within the NEXAH Architecture

The repository follows a layered architecture:

Framework ↓ Structural Operators ↓ System Models ↓ Applications ↓
Exploration Hub

-   **FRAMEWORK/** defines the mathematical and structural foundations\
-   **ENGINE/** implements the core computational architecture\
-   **APPLICATIONS/** demonstrates concrete dynamical systems\
-   **EXPLORATION_HUB/** extends the models to new domains

Repository navigation:

FRAMEWORK/ ENGINE/ APPLICATIONS/ BUILDER_LAB/ EXPLORATION_HUB/ RESEARCH/

------------------------------------------------------------------------

# From Structure to Application

`<img src="visuals/From_Stucture_to_Application.png" width="900">`{=html}

The NEXAH workflow connects **formal structural theory** with
**real-world system analysis**.

Conceptual layers:

Formal Core → Structural Semantics → System Models → Applications

-   **Formal Core** introduces the mathematical operators
-   **Structural Semantics** defines regimes and thresholds
-   **System Models** represent dynamical systems
-   **Applications** analyze real-world systems

------------------------------------------------------------------------

# Core Dynamical Models

The applications layer introduces several classes of dynamical systems.

  -------------------------------------------------------------------------------------------------
  Model           Description                        Module
  --------------- ---------------------------------- ----------------------------------------------
  **Stability     Fundamental representation of      [STABILITY_LANDSCAPE](./STABILITY_LANDSCAPE)
  Landscape**     system stability                   

  **Gradient      Systems evolving along stability   [GRADIENT_SYSTEM](./GRADIENT_SYSTEM)
  Systems**       gradients                          

  **Drift         Gradient systems with external     [DRIFT_SYSTEM](./DRIFT_SYSTEM)
  Systems**       forcing                            

  **Regime        Systems with multiple attractor    [REGIME_SYSTEM](./REGIME_SYSTEM)
  Systems**       regimes                            
  -------------------------------------------------------------------------------------------------

These models represent increasing levels of dynamical complexity:

Stability Landscape ↓ Gradient Systems ↓ Drift Systems ↓ Regime Systems

------------------------------------------------------------------------

# NEXAH Dynamical Framework

`<img src="visuals/nexah_dynamics_framework_overview.png" width="900">`{=html}

The NEXAH applications are built on a hierarchy of dynamical models
describing how systems evolve in structured state spaces.

------------------------------------------------------------------------

`<img src="visuals/nexah_dynamics_framework_detailed.png" width="900">`{=html}

This diagram summarizes the **four core dynamical models** used in the
NEXAH applications framework.

------------------------------------------------------------------------

# Application Navigation Map

`<img src="visuals/Applications_Navigation_Map.png" width="900">`{=html}

Applications follow a conceptual progression:

Stability Landscape ↓ Structural System Classes ↓ Example Applications

------------------------------------------------------------------------

# Case Study: Lorenz System

The **Lorenz system** serves as the first complete demonstration of the
**NEXAH dynamical analysis pipeline**.

This example reconstructs the structural geometry of a chaotic system
through:

-   basin boundary detection\
-   regime mapping\
-   resilience analysis\
-   potential landscape reconstruction\
-   gradient navigation\
-   separatrix analysis

Location:

APPLICATIONS/lorenz

Full documentation:

APPLICATIONS/lorenz/README.md

The Lorenz module includes:

-   attractor reconstruction\
-   FTLE analysis\
-   chaos energy landscapes\
-   filament networks\
-   navigation agents

and serves as the **primary benchmark system for NEXAH dynamical
analysis**.

------------------------------------------------------------------------

# External Simulator Integration

NEXAH can operate as a **navigation layer above existing simulation
software**.

Simulator ↓ Adapter ↓ State Graph ↓ NEXAH Navigator ↓ Policy ↓ Actions

Adapter implementations:

APPLICATIONS/adapters

Example compatible systems:

-   MATPOWER\
-   pandapower\
-   PyPSA\
-   traffic simulators\
-   supply chain systems\
-   cyber-physical infrastructure

Adapters translate simulator outputs into **finite state graphs** that
NEXAH can analyze.

------------------------------------------------------------------------

# From Applications to Exploration

While the application modules provide **reference implementations**, the
**Exploration Hub** enables open experimentation.

Location:

EXPLORATION_HUB/

Builders can extend NEXAH to domains such as:

-   infrastructure networks
-   ecosystems
-   cities
-   financial systems
-   planetary systems

Successful explorations may later evolve into **formal application
modules**.

------------------------------------------------------------------------

# Philosophy

NEXAH focuses on the **structure of stability in complex systems**.

Instead of predicting trajectories directly, NEXAH analyzes:

-   attractor structure
-   regime transitions
-   stability landscapes
-   navigation paths through state space

In short:

> **NEXAH explores the geometry of stability in dynamical systems.**
