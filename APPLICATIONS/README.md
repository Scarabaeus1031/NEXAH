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

# ⚡ 1. Power Systems — Real-World Validation (FLAGSHIP MODULE)

![NEXAH MicDrop](power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

*Voltage collapse detected ~43.9 seconds earlier than classical methods.*

![NEXAH Pipeline](power_systems/nexah_ieeeX/results/run_ieee300_20260413_015843/paper_figure.png)

*End-to-end NEXAH pipeline: voltage collapse, structural features, risk field, and adaptive control actions.*

NEXAH applied to real power grids (up to **9241 buses**):

- early instability detection (~43.9s lead time)  
- structural risk fields  
- adaptive intervention policies  
- real AC power flow integration (pandapower)  

---

## 🧭 Entry Points

### 🔹 Quick Overview (Results + Scaling)
👉 [`power_systems/nexah_ieeeX/`](power_systems/nexah_ieeeX/README.md)

- end-to-end pipeline  
- IEEE118 → 9241 scaling  
- real grid experiments  

---

### 🔹 Deep Dive (Full System Architecture)
👉 [`power_systems/`](power_systems/README.md)

- system layers (detection → control)  
- field interpretation  
- theoretical framework  

---

### 🔹 Structural Theory (Manifold / Rift / Geometry)
👉 [`power_systems/stability_field_dynamics`](power_systems/stability_field_dynamics/ieee_test_cases/README.md)

- collapse manifold  
- stability distance  
- topology & branching  

---

### 🔹 Experimental Control (Geometry → Navigation)
👉 [`power_systems/ieee_xray_pipeline`](power_systems/ieee_xray_pipeline/README.md)

- reduced state space  
- polar geometry  
- attractor-based control  

---

### 🔹 Minimal System (IEEE9 — Clean Pipeline)
👉 [`power_systems/nexah_ieee9`](power_systems/nexah_ieee9/README.md)

- simplest full pipeline  
- easiest to understand  
- best starting point for code  

---

## ⚡ How to Run

Example:

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieeeX/decision/main_ieee300.py
```

---

> NEXAH scales from small systems → to real-world grids  
> while preserving the same underlying structure.
---

# 🌀 2. Dynamical Systems — Geometry of Chaos

![Lorenz](../ENGINE/visuals/level37_20260321_193227/plot.png)

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
