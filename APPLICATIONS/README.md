# NEXAH Applications  
**Structural Navigation in Real and Synthetic Systems**

---

## 🚀 Key Result

NEXAH enables:

→ **navigation within complex system stability fields**

instead of:

→ detection of collapse events

✔ early instability detection (~43.9s lead time)  
✔ no collapse (field-based navigation)  
✔ maximum safe utilization  

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

![NEXAH MicDrop](power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

*Voltage collapse detected ~43.9 seconds earlier than classical methods.*

![NEXAH Pipeline](power_systems/nexah_ieeeX/results/run_ieee300_20260413_015843/paper_figure.png)

*End-to-end pipeline: structure → risk → control → system evolution.*

### 🔥 Highlights

- scaling up to **9241-bus systems**  
- continuous **stability field reconstruction**  
- **predictive control via geometry**  
- integration with **real AC power flow (pandapower)**  

---

## 🧭 Entry Points

### 🔹 Quick Results (Start here)
👉 [`power_systems/nexah_ieeeX/`](power_systems/nexah_ieeeX/README.md)

- scaling results  
- real grid experiments  
- end-to-end pipeline  

---

### 🔹 Full System (Architecture)
👉 [`power_systems/`](power_systems/README.md)

- system layers  
- field interpretation  
- navigation logic  

---

### 🔹 Minimal System (Best for Code)
👉 [`power_systems/nexah_ieee9`](power_systems/nexah_ieee9/README.md)

- clean pipeline  
- easiest to understand  
- controller evolution (v7 → v11)  

---

### 🔹 Structural Theory
👉 [`power_systems/stability_field_dynamics`](power_systems/stability_field_dynamics/ieee_test_cases/README.md)

- collapse manifold  
- stability distance  
- topology & branching  

---

### 🔹 Geometric Control Experiments
👉 [`power_systems/ieee_xray_pipeline`](power_systems/ieee_xray_pipeline/README.md)

- reduced state space  
- attractor geometry  
- navigation structures  

---

## ⚡ Run Example

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieeeX/decision/main_ieee300.py
```

> NEXAH scales from small systems → to real-world grids  
> while preserving the same underlying structure  

---

# 🌀 2. Dynamical Systems — Geometry of Chaos

![Lorenz](../ENGINE/visuals/level37_20260321_193227/plot.png)

Reference systems:

- Lorenz attractor  
- gradient systems  
- drift systems  

> Chaos is not random — it is **structured and navigable**

👉 [`dynamical_systems/lorenz`](dynamical_systems/lorenz/README.md)

---

# 🧩 3. Structural Theory — Collapse Geometry

![Collapse Geometry](power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee14_v52_residual_vs_distance.png)

- manifold (expected dynamics)  
- rift (collapse boundary)  
- distance (stability metric)  

> Collapse is a **geometric transition**

---

# 🔵 4. Adapter Layer — System Integration

```text
System → Adapter → State Graph → NEXAH → Policy
```

Supports:

- power grids  
- dynamical systems  
- synthetic systems  

👉 [`adapters/`](adapters/README.md)

---

# 🧠 Core Insight

Across all modules:

> Systems evolve along structure.  
> Instability is a loss of alignment.  

NEXAH:

→ detects structure  
→ predicts transitions  
→ enables navigation  

---

# 🧭 Navigation Guide

| Goal | Start Here |
|------|-----------|
| Real-world validation | `power_systems/nexah_ieeeX/` |
| Understand system | `power_systems/` |
| Learn by code | `power_systems/nexah_ieee9/` |
| Theory | `power_systems/stability_field_dynamics/` |

---

# 🌀 NEXAH

> From dynamics → structure  
> From structure → geometry  
> From geometry → navigation  

---

**Scarabæus1033 · NEXAH**

