# ARCHY System Map

Layer: ARCHY  
Framework: NEXAH  
Purpose: Planetary System Interaction Map

---

# Overview

The **ARCHY System Map** describes the interacting subsystems modeled in
the planetary simulation layer of the NEXAH framework.

ARCHY represents the Earth as a **coupled complex system** composed of
multiple interacting domains such as climate, water, food production,
economy, infrastructure, population, and geopolitics.

The goal of this map is to clarify **how these subsystems influence each
other and generate large-scale system dynamics**.

---

# Core Planetary Subsystems

The ARCHY layer models the following primary domains.

### Climate System

Models long-term climate pressure on planetary systems.

Key dynamics:

- temperature increase
- extreme weather events
- climate stress accumulation
- regional climate variability

Primary outputs:

- climate stress index
- extreme event probability

---

### Water System

Models freshwater availability and drought dynamics.

Key dynamics:

- water scarcity
- drought pressure
- hydrological stress

Water availability strongly affects food production and migration.

---

### Food System

Models agricultural productivity and food security.

Key dynamics:

- climate-dependent crop productivity
- agricultural output variability
- food scarcity

Food systems are tightly coupled with climate and water systems.

---

### Energy System

Models global energy demand and energy infrastructure.

Key dynamics:

- energy demand growth
- energy network stress
- infrastructure dependence

Energy availability strongly influences economic stability.

---

### Population System

Models demographic growth and population stress dynamics.

Key dynamics:

- population growth
- urban concentration
- demographic pressure

Population growth increases demand for food, water, and energy.

---

### Migration System

Models population displacement caused by environmental and economic
pressures.

Key drivers:

- climate stress
- food shortages
- water scarcity
- geopolitical instability

Migration creates additional stress on urban systems.

---

### Financial System

Models global economic contagion and financial cascade events.

Key dynamics:

- debt accumulation
- financial network exposure
- economic cascade propagation

Economic instability often spreads through networked financial systems.

---

### Infrastructure Networks

Models the physical backbone of the global system.

Examples include:

- trade networks
- supply chains
- transportation systems
- logistics infrastructure

Infrastructure networks connect cities and enable global trade.

---

### Trade System

Models global trade flows and supply chain dependencies.

Trade networks propagate shocks between regions.

Trade disruptions can trigger economic cascades.

---

### Geopolitical System

Models conflict dynamics and geopolitical instability.

Key drivers include:

- resource competition
- economic stress
- migration pressure

Geopolitical escalation can disrupt trade and infrastructure networks.

---

# Coupling Structure

The planetary system is modeled as a **coupled network of interacting
subsystems**.

Example interaction pathways:

```
Climate → Water
Climate → Food
Climate → Migration

Water → Food
Water → Migration

Food → Migration
Food → Geopolitics

Energy → Economy
Energy → Infrastructure

Economy → Trade
Economy → Financial Stability

Infrastructure → Trade
Infrastructure → Economy

Trade → Economy
Trade → Geopolitics

Migration → Urban Systems
Migration → Geopolitics

Geopolitics → Trade
Geopolitics → Infrastructure
```

These couplings allow the system to generate **cascading failures and
system-wide feedback loops**.

---

# Cascade Dynamics

Because the subsystems are tightly coupled, disturbances can propagate
across the planetary system.

Example cascade:

```
Climate warming
→ agricultural decline
→ food shortages
→ migration waves
→ geopolitical tensions
→ trade disruption
→ economic instability
→ financial contagion
```

Such cascades are central to the ARCHY simulation experiments.

---

# System Representation

The planetary system can be represented as a **multilayer network**:

```
Layer 1  Climate Field
Layer 2  Resource Systems (Water / Food / Energy)
Layer 3  Population Systems
Layer 4  Economic Networks
Layer 5  Infrastructure Networks
Layer 6  Geopolitical Dynamics
```

Cities act as **nodes connecting these layers**.

---

# Simulation Role

The ARCHY layer simulates how these interacting subsystems evolve
through time.

Simulation approaches include:

- system dynamics models
- network cascade models
- stochastic event simulation
- Monte Carlo scenario exploration

---

# Purpose of the System Map

The ARCHY System Map provides a conceptual overview of the planetary
system structure.

It helps users understand:

- how subsystems interact
- how cascades propagate
- where instability can emerge

This map acts as the conceptual guide for the simulation models in the
ARCHY layer.

---

# NEXAH

Exploring planetary system dynamics through structural simulation.
