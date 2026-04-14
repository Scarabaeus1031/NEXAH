# Lorenz Chaos Exploration

This module explores the **geometry of chaos** using the classical **Lorenz dynamical system**.

The Lorenz system serves as a **reference system for the NEXAH dynamical framework**, demonstrating how chaotic dynamics can be transformed into a **structured, navigable stability landscape**.

---

# 🔥 Chaos Navigation Map

![Lorenz Navigation Map](./visuals/lorenz_navigation_map.png)

This visualization summarizes the core idea:

- chaotic systems contain **hidden structure**
- transport follows **geometric pathways**
- navigation becomes possible through **field-aware intervention**

---

# 🧠 Core Idea

Instead of simulating trajectories, NEXAH reconstructs the **geometry that generates them**.

This reveals:

- attractor geometry  
- flow fields  
- Lyapunov instability  
- FTLE transport barriers  
- regime boundaries  
- navigation pathways  

The result is a **tomographic reconstruction of phase space**.

---

# Lorenz System

The Lorenz equations:

dx/dt = σ (y − x)  
dy/dt = x (ρ − z) − y  
dz/dt = xy − β z  

Typical parameters:

σ = 10  
ρ = 28  
β = 8/3  

---

# Structural Analysis Pipeline
```text
Lorenz Attractor
↓
Flow Field
↓
Lyapunov Field
↓
Stretching / Rotation
↓
FTLE Structures
↓
Filament Graph
↓
Chaos Density
↓
Topography
↓
Regime Boundaries
↓
Navigation
```

---

# Key Structural Layers

## Chaos Density Nebula

![Lorenz Density Nebula](./visuals/lorenz_density_nebula_20260313_210336.png)

Global density of chaotic transport.

---

## Chaos Topography

![Lorenz Topography](./visuals/lorenz_chaos_topography_20260313_202116.png)

Phase space interpreted as a **landscape**.

---

## FTLE Transport Structures

![Lorenz FTLE](./visuals/lorenz_ftle_lcs_20260313_213948.png)

Transport barriers (LCS) forming the **skeleton of chaos**.

---

## Filament Structure

![Lorenz Filament](./visuals/lorenz_filament_3d_20260313_204724.png)

Fine-scale chaotic structure.

---

## Separatrix Structure

![Lorenz Separatrix](./visuals/lorenz_separatrix_map_20260313_195544.png)

Fractal boundary between attractor regimes.

---

## Lyapunov Instability Map

![Lorenz Lyapunov](./visuals/lorenz_lyapunov_map_20260313_212407.png)

Regions of exponential divergence.

---

## Flow Field

![Lorenz Flow](./visuals/lorenz_flow_field_20260313_211152.png)

Underlying vector field of the system.

---

# Navigation Layer

The Lorenz system can be interpreted as a **navigation landscape**:

- stability valleys  
- instability ridges  
- transport channels  
- regime boundaries  

Navigation strategies:

- gradient descent toward stable regions  
- controlled regime switching  
- trajectory steering  
- barrier avoidance  

---

# 🧭 Core Mapping
```text
Field → Geometry → Operator → Navigation
```
- Field organizes motion  
- Geometry defines structure  
- Operator reshapes trajectories  
- Navigation becomes possible  

---

# Interpretation

The system decomposes into:

Attractor Geometry  
+ Instability Fields  
+ Transport Barriers  
+ Regime Boundaries  
+ Navigation Structure  

---

# Role within NEXAH

The Lorenz module serves as a **benchmark system** demonstrating:

- structural reconstruction of chaos  
- regime detection  
- transport geometry  
- navigation in dynamical systems  

---

# Final Insight

> The system is not defined by trajectories.  
> It is defined by the geometry that generates them.


