# NEXAH Applications  
**Structural Analysis and Regime Navigation in Complex Systems**

---

## 🧭 Overview

This directory contains **applied system modules** built with the NEXAH framework.

NEXAH explores how complex systems can be interpreted through:

→ structure  
→ flow  
→ geometry  
→ regime transitions  

Instead of focusing purely on event detection (e.g. collapse),  
NEXAH analyzes how systems evolve within **structured dynamical landscapes**.

---

## 🚀 Core Idea

NEXAH shifts the focus from:

→ discrete instability events  

to:

→ **continuous structural and regime-based analysis**

---

# 🌀 1. Dynamical Systems — Core Reference (Lorenz)

![Lorenz Core](core_demos/lorenz/outputs/lorenz_nexah_v12_final.png)

The Lorenz system serves as the **primary reference model** for NEXAH.

It demonstrates the full transformation:
```text
Dynamics → Structure → Symbols → Prediction → Control → Meta-Control → Memory → Switching → Behavior
```

---

## 🧠 What This Shows

Across the Lorenz demos:

- chaos is structured, not random  
- trajectories form symbolic states  
- patterns and sequences emerge  
- prediction becomes possible  
- control becomes anticipatory  
- behavior becomes adaptive  

---

## 🧭 Entry Point

👉 [`core_demos/lorenz/`](core_demos/lorenz/README.md)

Structure:

- `core/` → pipeline & field extraction  
- `analysis/` → structure & symbolic dynamics  
- `navigation/` → control & behavior  
- `meta/` → adaptive intelligence  
- `docs/` → theory & development logs  

---

## 🧠 Interpretation

> The Lorenz system is not just a toy model.  
> It is a **minimal working example of the NEXAH framework**.

---

# ⚡ 2. Power Systems — Structural Analysis

![NEXAH Overview](power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

![NEXAH Pipeline](power_systems/nexah_ieeeX/results/run_ieee300_20260413_015843/paper_figure.png)

---

## 🔍 Observations

- system trajectories exhibit **structured behavior**
- collapse appears as a **transition boundary**
- dynamics follow **flow-like evolution**
- patterns scale across system sizes  

---

## 🧠 Interpretation

> Power system stability can be interpreted as a  
> **trajectory evolving within a structured dynamical landscape**

---

## ⚙️ Current Capabilities

- structural analysis of IEEE test systems  
- trajectory-based stability interpretation  
- regime transition detection (experimental)  
- scaling up to **9241-bus systems**  

---

## ⚠️ Important Note

- early detection performance is **case-dependent**  
- no universal guarantee  
- current validation is limited  

---

## 🧭 Entry Points

### 🔹 Quick Results
👉 [`power_systems/nexah_ieeeX/`](power_systems/nexah_ieeeX/README.md)

### 🔹 Full System Overview
👉 [`power_systems/`](power_systems/README.md)

### 🔹 Minimal Pipeline
👉 [`power_systems/nexah_ieee9`](power_systems/nexah_ieee9/README.md)

### 🔹 Structural Theory
👉 [`power_systems/stability_field_dynamics`](power_systems/stability_field_dynamics/ieee_test_cases/README.md)

### 🔹 Geometric Analysis
👉 [`power_systems/ieee_xray_pipeline`](power_systems/ieee_xray_pipeline/README.md)

---

## ⚡ Run Example

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieeeX/decision/main_ieee300.py
```

# 🧩 3. Structural Theory — Collapse Geometry

![Collapse Geometry](power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee14_v52_residual_vs_distance.png)

---

## 🧠 Interpretation

Collapse is better understood as a:

→ **geometric transition within system structure**

---

# 🔵 4. Adapter Layer — System Integration

System → Adapter → State Graph → NEXAH → Analysis

Supports:

- power grids  
- dynamical systems  
- synthetic environments  

👉 [`adapters/`](adapters/README.md)

---

# 🧠 Core Insight

Across all modules:

> Systems evolve along structured trajectories.  
> Instability emerges as a **regime transition**, not a single event.

---

# 🧭 Navigation Guide

| Goal | Start Here |
|------|-----------|
| Core framework (Lorenz) | `core_demos/lorenz/` |
| Large system experiments | `power_systems/nexah_ieeeX/` |
| System understanding | `power_systems/` |
| Code entry point | `power_systems/nexah_ieee9/` |
| Theory | `power_systems/stability_field_dynamics/` |

---

# 🌀 NEXAH

> From dynamics → structure  
> From structure → navigation  

---

**Scarabæus1033 · NEXAH**


