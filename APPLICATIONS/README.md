# NEXAH Applications  
**Structural Navigation in Real and Synthetic Systems**

---

## 🧭 Overview

This directory contains **applied system modules** built with the NEXAH framework.

NEXAH transforms systems into:

→ structure  
→ flow  
→ geometry  
→ navigation  

> Systems are not simulated — they are **mapped and navigated**

---

# ⚡ 1. Power Systems — Real-World Validation (FLAGSHIP)

![IEEE Field](power_systems/nexah_ieeeX/results/run_ieee9241_20260413_021422/plot.png)

NEXAH applied to real power grids (up to **9241 buses**):

- early instability detection (~43.9s lead time)  
- structural risk fields  
- adaptive intervention policies  
- real AC power flow integration (pandapower)  

👉 Entry:  
[`power_systems/`](power_systems/README.md)

---

# 🌀 2. Dynamical Systems — Geometry of Chaos

![Lorenz](dynamical_systems/lorenz/../outputs/lorenz_navigation/lorenz_density_nebula_20260313_210336.png)

Reference systems for structural understanding:

- Lorenz attractor (chaos geometry)  
- gradient systems  
- drift systems  
- regime systems  

Key idea:

> Chaos is not random — it is **structured and navigable**

👉 Entry:  
[`dynamical_systems/lorenz`](dynamical_systems/lorenz/README.md)

---

# 🧩 3. Structural Theory — Collapse Geometry

![Collapse Geometry](power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee14_v52_residual_vs_distance.png)

NEXAH reveals universal collapse structure:

- manifold (expected dynamics)  
- rift (collapse boundary)  
- distance (stability metric)  
- branching topology  

> Collapse is a **geometric transition**

👉 Entry:  
[`power_systems/stability_field_dynamics`](power_systems/stability_field_dynamics/ieee_test_cases/README.md)

---

# 🔵 4. Adapter Layer — System Integration

NEXAH connects to external systems via structural abstraction:

```text
System → Adapter → State Graph → NEXAH → Policy
```
Supports:

- power grids  
- dynamical systems  
- internal NEXAH simulations  

👉 Entry:  
[`adapters/`](adapters/README.md)

---

# 🧠 Core Insight

Across all modules:

> Systems evolve along structure.  
> Instability is a loss of alignment.  
>  
> NEXAH detects and navigates this structure.

---

# 🧭 Navigation Guide

| Goal | Start Here |
|------|-----------|
| Real-world application | `power_systems/` |
| Chaos & theory | `dynamical_systems/lorenz/` |
| Mathematical structure | `power_systems/stability_field_dynamics/` |
| Integration | `adapters/` |

---

# 🚀 What this enables

- early instability detection  
- structural system understanding  
- trajectory-aware control  
- cross-domain modeling  

---

# 🌀 NEXAH

> From dynamics → structure  
> From structure → geometry  
> From geometry → navigation  

---

**Scarabæus1033 · NEXAH**
