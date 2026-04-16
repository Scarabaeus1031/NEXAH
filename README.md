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

---

## ⚠️ Early Experiment — Misinterpreted Signal (“MicDrop”)

![NEXAH MicDrop](APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

**Context:**

This figure was generated during early experiments and initially interpreted as a strong early-warning signal.

The visual suggests a significant lead time between a detected structural event ("Phi-Split") and voltage collapse.

---

**Re-evaluation:**

Further analysis revealed that:

- the detected signal was **not consistently reproducible**
- results depended strongly on signal processing choices  
- similar lead times could not be confirmed across datasets  
- parts of the signal were artifacts of detection logic  

---

**Interpretation:**

> This result is now understood as an **interesting but misleading signal artifact**,  
> not as validated early-collapse detection.

---

**Why it is still included:**

- illustrates the **difficulty of early-warning detection**
- shows how **signal interpretation can be deceptive**
- motivated the transition toward:
  → regime detection  
  → structural analysis  
  → trajectory-based interpretation  

---

👉 In hindsight:

> “MicDrop” → **MicFlop — but a useful one**

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

