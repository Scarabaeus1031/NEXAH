# NEXAH Applications

This directory contains **applied system modules, benchmark analyses, and reference demonstrations** built with the NEXAH framework.

> NEXAH does not just simulate systems —  
> it reveals their **structure, flow, and stability landscape**.

---

# ⚡ Flagship Application — Power Grid Stability (IEEE)

## Key Result

NEXAH detects voltage collapse up to **43.9 seconds earlier** than classical methods across IEEE benchmark systems (118 → 9241 buses).

This result is consistent across system sizes and represents the first practical demonstration of **structure-based early instability detection** in power systems.

---

## 🔬 Detection vs Navigation (NEW)

NEXAH now operates on two distinct layers:

### ✔ Detection Layer (Solved)
- early instability detection  
- structural collapse prediction  
- validated across IEEE systems  

### ⚠ Navigation Layer (In Progress)
- orbit-based stabilization  
- phase-aware control  
- gate-based transitions  

→ implemented in:  
[`power_systems/ieee_xray_pipeline/`](power_systems/ieee_xray_pipeline/)

---

## ⚡ IEEE X-Ray Pipeline

The IEEE X-Ray Pipeline is the **next-generation application layer** of NEXAH.

It transforms classical simulation into a geometric control problem:

```text
simulation → structure → geometry → control → navigation
```

It introduces:

- reduced state space (coherence, switch)
- polar geometry (radius, phase)
- structural trajectories
- experimental controllers (v14.x → v36)

👉 Entry point:  
[`power_systems/ieee_xray_pipeline/`](power_systems/ieee_xray_pipeline/)

---

## 🔬 Applied IEEE Systems

NEXAH has been applied to:

- IEEE 9  
- IEEE 14  
- IEEE 30  
- IEEE 57  
- IEEE 118  
- IEEE 300  
- IEEE 1354  
- IEEE 9241 (PEGASE)  

---

## 🔬 Example — Field-Based Collapse Dynamics

![IEEE Field Flow](power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

This field representation reveals:

- structured trajectory flow  
- collapse along geometric paths  
- branching instability  
- non-random system evolution  

---

## Why this matters

Classical methods detect collapse late.

NEXAH instead:

- detects instability early  
- reveals *how* collapse develops  
- enables future navigation  

> From passive observation → to structural understanding → to control

---

# 🧭 From Framework to Applications

NEXAH follows a layered transition:

```text
Framework
    ↓
Structure Extraction
    ↓
System Models
    ↓
Applications
    ↓
Domain Integration
```

- **Framework** → structural operators and system logic  
- **Applications** → applied system analysis  
- **Integration** → real-world system connection  

---

## 🔬 Core Application Models

| Model | Description | Module |
|------|-------------|--------|
| **Stability Landscape** | Attractor basins and system stability | [STABILITY_LANDSCAPE](./dynamical_systems/STABILITY_LANDSCAPE) |
| **Gradient Systems** | Motion along potential gradients | [GRADIENT_SYSTEM](./dynamical_systems/GRADIENT_SYSTEM) |
| **Drift Systems** | Gradient + external forcing | [DRIFT_SYSTEM](./dynamical_systems/DRIFT_SYSTEM) |
| **Regime Systems** | Multi-attractor transitions | [REGIME_SYSTEM](./dynamical_systems/REGIME_SYSTEM) |

---

## 🤖 Multi-Agent Navigation Demonstrator

NEXAH enables agents to navigate **stability landscapes without reward functions**.

Agents:

- explore structure  
- detect stable regions  
- follow field directions  
- move along stable flows  

> Agents do not optimize —  
> they follow **geometry**

Run demo:

```bash
python ENGINE/run_agent.py
```

---

## 🌪 Lorenz System — Reference Demonstrator

The Lorenz system serves as a canonical nonlinear test case.

NEXAH reconstructs:

- attractor geometry  
- basin boundaries  
- separatrix structures  
- regime transitions  

> Chaos is not randomness —  
> it is **structured and navigable**

Run demo:

```bash
python -m APPLICATIONS.run_navigation_demo
```

---

## 🔌 External System Integration

NEXAH connects to simulators via an adapter layer:

```text
Simulator → Adapter → State Graph → NEXAH → Navigation
```

Target systems:

- MATPOWER  
- pandapower  
- PyPSA  
- infrastructure systems  
- traffic / logistics  
- supply chains  

Adapter location:

```text
APPLICATIONS/adapters/
```

---

## 🌐 From Structure to Application

<img src="visuals/From_Stucture_to_Application.png" width="900">

---

## 🧠 Core Idea

> Structure is not imposed —  
> it is extracted from dynamics.

---

## 🚀 What you can do here

- analyze real systems  
- detect instability early  
- visualize structure  
- explore stability landscapes  
- test control strategies  
- build new modules  

---

## 🔮 Outlook

The `APPLICATIONS` layer is evolving toward:

- real-world system integration  
- predictive stability control  
- autonomous navigation  
- cross-domain structure analysis  

---

**Scarabæus1033 · NEXAH**
