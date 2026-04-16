# ⚡ NEXAH — Structural Navigation in Complex Systems

![Status](https://img.shields.io/badge/status-experimental-blue)
![Field Model](https://img.shields.io/badge/field-analysis-lightblue)
![Control](https://img.shields.io/badge/control-prototype-orange)

---

## 🧭 Abstract

NEXAH explores a structural approach to analyzing complex dynamical systems.

Instead of treating systems as binary (stable / unstable), NEXAH models them as evolving within:

> **structured dynamical landscapes**

This enables:

- representation of system dynamics as geometric structures  
- identification of regime transitions  
- trajectory-based system interpretation  
- exploration of navigation strategies within stability regions  

The framework is applied to power systems and reference dynamical systems, where it reveals consistent structural patterns in system evolution.

---

## 🧭 Overview

Classical system analysis focuses on:

→ threshold violations  
→ event detection  

NEXAH proposes a complementary perspective:

> systems evolve as **trajectories within structured state spaces**

This shifts the focus from:

→ "Is the system stable?"  

to:

→ **"How is the system evolving within its structure?"**

---

## 🚀 Start Here

👉 [START HERE — Run your first demo](START_HERE.md)

---

## 🎬 What you will see

- structured dynamics in chaotic systems  
- trajectories evolving in reduced state spaces  
- regime transitions preceding instability  
- geometry-based interpretations of system behavior  

---

## 🧭 Explore

- 🧠 [Framework](FRAMEWORK/README.md)  
- ⚡ [Applications](APPLICATIONS/README.md)  
- 🧭 [Navigator](NAVIGATOR/README.md)

---

## 📊 Example: Power System Dynamics

![IEEE Structure](APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

**Observation:**
- system trajectories organize into structured regions  
- similar geometric patterns appear across system sizes  

**Interpretation:**

> Power system dynamics can be interpreted as evolving within a  
> **low-dimensional structured landscape**

⚠️ Note:  
The figure illustrates qualitative structural behavior.  
Quantitative early-warning performance is currently under investigation.

---

## 🔁 Core Pipeline

```text
simulation → structure → geometry → dynamics → regimes
```

## 🔥 Core Insight

Classical control:

→ reacts to deviations  

NEXAH perspective:

→ analyzes trajectory evolution within structure  

👉 Stability becomes a question of:

- regime  
- trajectory  
- structural alignment  

---

## 📊 From Structure → Dynamics

---

### 🔹 Flow Field (IEEE Systems)

![Flow Field](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

**Observation:**
- trajectories follow structured flow patterns  
- system evolution is directional  

---

### 🔹 Trajectory-Based Control (Prototype)

![Control](APPLICATIONS/power_systems/nexah_ieee9/results/controller_v9/output_v9_plot.png)

**Observation:**
- control influences trajectory evolution  
- stabilization occurs in some scenarios  

**Interpretation:**

> Control can be interpreted as **trajectory shaping within system dynamics**

---

## 🧠 System Interpretation

NEXAH models systems as:

> **trajectories evolving within structured dynamical landscapes**

where:

- structure defines possible regimes  
- dynamics define transitions  
- analysis detects regime changes  

---

## ⚖️ Classical vs NEXAH

| Classical | NEXAH |
|----------|------|
| threshold-based | structure-based |
| event detection | regime analysis |
| reactive | trajectory-aware |
| state-focused | dynamics-focused |

---

## 🚀 Run Example

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v6.py
```

## 🧭 Status

| Component | Status |
|----------|--------|
| Structure Discovery | ✅ |
| Field Interpretation | ✅ |
| Regime Detection | ✅ (experimental) |
| Control | ⚠️ prototype |
| Navigation | 🚧 in development |

---

## ⚠️ Limitations

- no validated universal early-warning metric  
- sensitivity to system and dataset  
- limited evaluation on real-world grid dynamics  
- control layer is experimental  

---

## 🧠 Final Insight

Complex systems are not binary.

They evolve within:

> **structured dynamical regimes**

---

## 🌀 NEXAH

> dynamics → structure → geometry → regimes  

---

**Thomas K. R. Hofmann · 2026**

