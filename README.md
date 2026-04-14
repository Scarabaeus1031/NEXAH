# ⚡ NEXAH — Structural Navigation in Complex Systems

![Status](https://img.shields.io/badge/status-active-success)
![Field Model](https://img.shields.io/badge/field-model-blue)
![Control](https://img.shields.io/badge/control-prototype-orange)

---

## 🧭 Overview

NEXAH transforms classical system analysis into:

> **a continuous stability field with closed-loop control and early-stage navigation**

Instead of binary classification:

> stable / unstable  

systems are understood as existing within a:

> **structured stability landscape**

---

## 📂 Entry Points

- ⚡ [Power Systems](APPLICATIONS/power_systems/README.md)  
- 🧠 [Framework](FRAMEWORK/README.md)

---

## 🔥 Key Result — Real Power Systems

![NEXAH IEEE Result](APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

*NEXAH detects voltage collapse up to **43.9 seconds earlier** than classical methods.*

👉 Demonstrated on IEEE benchmark systems up to **9241 buses**

---

## 🔬 Core Idea

Instead of asking:

> "Will the system collapse?"

NEXAH answers:

> "Where are we in the field — and how can we move safely?"

---

## 🔁 Core Pipeline

```text
simulation → structure → field → geometry → control → navigation
```

---

## 🔥 Core Insight

Control is no longer:

→ reactive (error-based)

but:

→ **trajectory-aware and geometry-informed**

👉 Stability becomes a **navigation problem in state space**

---

# 📊 From Field → Control

---

## 🔹 Flow Field Dynamics

👉 Source: [IEEE Field Analysis](APPLICATIONS/power_systems/stability_field_dynamics/)

![Flow Field](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

*System trajectories follow structured flow — not randomness.*

- motion is directional  
- instability follows field paths  

---

## 🔹 Closed-Loop Control (IEEE9)

👉 Source: [IEEE9 Controller](APPLICATIONS/power_systems/nexah_ieee9/)

![Control](APPLICATIONS/power_systems/nexah_ieee9/results/controller_v9/output_v9_plot.png)

*Control reshapes trajectories instead of reacting to states.*

- early intervention  
- structured escalation  
- trajectory-aware behavior  

---

# 🧠 System Interpretation

The system operates as:

> a trajectory evolving within a structured stability field

where:

- field = extracted from system physics  
- geometry = defines stability structure  
- control = trajectory shaping within the field  

---

## 🧭 Explore the Full System

The IEEE results shown here are one application.

NEXAH is a general framework for navigating structure in complex systems.

- 🧭 [NAVIGATOR](NAVIGATOR/README.md)  
- 🏗 [Architecture](NAVIGATOR/ARCHITECTURE.md)  
- 📊 [System Capabilities](NAVIGATOR/SYSTEM_CAPABILITIES.md)

👉 This README is a **showcase**  
👉 NAVIGATOR reveals the **full system**

---

## ⚖️ Classical vs NEXAH (Essence)

Classical:
→ threshold-based, reactive

NEXAH:
→ field-based, trajectory-aware

---

# 🚀 Run

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v6.py
```

---

# 🧭 Status

| Component | Status |
|----------|--------|
| Structure Discovery | ✅ |
| Field Modeling | ✅ |
| Early Detection | ✅ (43.9 s) |
| Adaptive Control | ⚠️ prototype |
| Field Navigation | 🚧 in development |

---

# 🧠 Final Insight

Power systems are not binary.

They exist within a:

> **structured stability landscape**

---

# 🌀 NEXAH

> dynamics → structure → geometry → control → navigation  

---

**Thomas K. R. Hofmann · 2026**
