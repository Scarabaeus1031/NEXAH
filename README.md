# ⚡ NEXAH — Structural Navigation in Complex Systems

![Status](https://img.shields.io/badge/status-active-success)
![Field Model](https://img.shields.io/badge/field-model-blue)
![Control](https://img.shields.io/badge/control-prototype-orange)

---

## 🧭 Overview

NEXAH transforms classical system analysis into:

> **a continuous stability field with closed-loop control and early-stage navigation**

Instead of binary classification:

> stable ❌ / unstable ❌  

systems are understood as existing within a:

> **structured stability landscape**

NEXAH is a domain-independent framework — power systems are one validated example.

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

simulation → structure → field → geometry → control → navigation

---

## 🔥 Core Insight

Control is no longer:

→ reactive (error-based)

but:

→ **trajectory-aware and geometry-informed**

NEXAH does not react to instability.

It **reads the structure of the system** and adapts behavior accordingly.

👉 Stability becomes a **navigation problem in state space**

---

# 📊 From Collapse → Field → Control

---

## 🔹 1. Collapse Geometry

👉 Source: [Stability Field Dynamics](APPLICATIONS/power_systems/stability_field_dynamics/README.md)

![Collapse Geometry](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee14_v52_residual_vs_distance.png)

*Collapse is not a point — it is a boundary in a structured field.*

- system states organize into regions  
- collapse emerges as a geometric rift  

---

## 🔹 2. Flow Field Dynamics

👉 Source: [IEEE Field Analysis](APPLICATIONS/power_systems/stability_field_dynamics/)

![Flow Field](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

*System trajectories follow structured flow — not randomness.*

- motion is directional  
- instability follows field paths  

---

## 🔹 3. Closed-Loop Control (IEEE9)

👉 Source: [IEEE9 Controller](APPLICATIONS/power_systems/nexah_ieee9/)

![Control](APPLICATIONS/power_systems/nexah_ieee9/results/controller_v9/output_v9_plot.png)

*Control reshapes trajectories instead of reacting to states.*

- early intervention  
- structured escalation  
- trajectory-aware behavior  

---

## 🔹 4. Phase Dynamics (v9)

👉 Source: [Controller Phase Analysis](APPLICATIONS/power_systems/nexah_ieee9/)

![Phase](APPLICATIONS/power_systems/nexah_ieee9/results/controller_v9/output_v9_phase_lambda_psi.png)

*System + controller form a dynamical system.*

- phase space: (λ, ψ)  
- attractor-like convergence  
- coupling between system and control  

---

## 🔹 5. Field Navigation (Prototype)

👉 Source: [Navigation Prototype](APPLICATIONS/power_systems/nexah_ieee9/)

![Navigation](APPLICATIONS/power_systems/nexah_ieee9/results/visuals/nexah_navigation_v11.gif)

*Prototype behavior: controller approaches stability boundary without triggering collapse.*

- smooth convergence  
- reduced oscillation  
- improved safe utilization (qualitative)  

⚠️ Navigation layer currently under active development

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

The IEEE results shown here are one concrete application.

NEXAH itself is a **general framework for navigating structure in complex systems**.

Explore the full system:

- 🧭 [NAVIGATOR](NAVIGATOR/README.md) → system overview & orientation  
- 🏗 [Architecture](NAVIGATOR/ARCHITECTURE.md) → full system design  
- 📊 [System Capabilities](NAVIGATOR/SYSTEM_CAPABILITIES.md) → what NEXAH can actually do  

👉 This README is a **showcase**  
👉 The NAVIGATOR reveals the **full system behind it**

---

# 🧠 What This Means

A complex physical system can be:

- mapped into a field  
- understood geometrically  
- influenced via trajectory-aware control  

---

# ⚖️ Classical vs NEXAH

| Feature | Classical | NEXAH |
|--------|----------|------|
| Static thresholds | ✅ | ❌ |
| Dynamic field | ❌ | ✅ |
| Early warning | ⚠️ | ✅ |
| Closed-loop control | ❌ | ✅ |
| Predictive behavior | ❌ | ⚠️ emerging |
| Navigation | ❌ | ⚠️ prototype |

---

# 🚀 Run

### IEEE9 Controller (current stable)

PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v6.py

---

# 📁 Results

📂 [APPLICATIONS/power_systems/nexah_ieee9/results/](APPLICATIONS/power_systems/nexah_ieee9/results/)

Includes:

- field scans  
- controller evolution  
- replay logs  
- system trajectories  

---

# 🧭 Status

| Component | Status |
|----------|--------|
| Structure Discovery | ✅ |
| Field Modeling | ✅ |
| Early Detection | ✅ (43.9 s) |
| Adaptive Control | ⚠️ prototype |
| Phase Dynamics | ✅ |
| Field Navigation | 🚧 in development |
| Generalization (multi-domain) | ⚠️ emerging |

---

# 🔮 Next Steps

- quantitative evaluation of control gains  
- scaling to IEEE118+  
- real-time field estimation  
- stabilization limits & capacity increase  
- integration with real grid control  

---

# 🧠 Final Insight

Power systems are not binary.

They exist within a:

> **structured stability landscape**

NEXAH makes this:

> **visible, measurable, and influenceable**

---

# 🌀 NEXAH

> From dynamics → structure  
> From structure → geometry  
> From geometry → control  
> From control → navigation  

---

**Thomas K. R. Hofmann · 2026**
