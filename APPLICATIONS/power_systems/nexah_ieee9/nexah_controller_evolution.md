# ⚡ NEXAH — Structural Navigation in Complex Systems

![Status](https://img.shields.io/badge/status-active-success)
![Field Model](https://img.shields.io/badge/field-model-blue)
![Control](https://img.shields.io/badge/control-prototype-orange)

---

## 🧭 Overview

NEXAH transforms classical system analysis into:

> **a continuous stability field with closed-loop control and emerging navigation**

Instead of binary classification:

> stable ❌ / unstable ❌  

systems are understood as evolving inside a:

> **structured stability landscape**

---

## 🔥 Key Result — Real Power Systems

![NEXAH IEEE Result](APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/ieee_scaling/NEXAH_MicDrop_IEEE300_Final.png)

*NEXAH detects voltage collapse up to **43.9 seconds earlier** than classical methods.*

✔ demonstrated on IEEE benchmark systems (up to 9241 buses)

---

## 🔁 Core Pipeline

```text
simulation → structure → field → geometry → control → navigation (in development)
```

---

## 🔥 Core Insight

Control is no longer:

→ reactive (based on error)

but:

→ predictive (based on system geometry)

---

# 📊 From Collapse → Field → Control

---

## 🔹 1. Collapse Geometry

![Collapse Geometry](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee14_v52_residual_vs_distance.png)

*Collapse is not a point — it is a boundary in a structured field.*

- system states organize into regions  
- collapse emerges as a geometric rift  

---

## 🔹 2. Flow Field Dynamics

![Flow Field](APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

*System trajectories follow structured flow — not randomness.*

- motion is directional  
- instability follows field paths  

---

## 🔹 3. Closed-Loop Control (IEEE9 Prototype)

![Control](APPLICATIONS/power_systems/nexah_ieee9/results/controller_v9/output_v9_plot.png)

*Control reshapes trajectories instead of reacting to states.*

- early intervention  
- trajectory-aware behavior  
- structured escalation  

---

## 🔹 4. Phase Dynamics (v9)

![Phase](APPLICATIONS/power_systems/nexah_ieee9/results/controller_v9/output_v9_phase_lambda_psi.png)

*System + controller form a dynamical system.*

- phase space: (λ, ψ)  
- attractor-based behavior  
- coupling between system and control  

---

## 🔹 5. Field Navigation (Experimental — in development)

![Navigation](APPLICATIONS/power_systems/nexah_ieee9/results/visuals/nexah_navigation_v11.gif)

*Prototype navigation toward stability boundary.*

- smooth convergence observed  
- no collapse triggered  
- navigation logic under active development  

---

# 🧠 System Interpretation

The system operates as:

> a trajectory evolving within a structured stability field

where:

- field = extracted from system physics  
- geometry = defines stability structure  
- control = movement shaped by the field  

---

# ⚖️ Classical vs NEXAH

| Feature | Classical | NEXAH |
|--------|----------|------|
| Static thresholds | ✅ | ❌ |
| Dynamic field | ❌ | ✅ |
| Early warning | ⚠️ | ✅ (43.9 s) |
| Closed-loop control | ❌ | ✅ (prototype) |
| Predictive behavior | ❌ | ✅ |
| Navigation | ❌ | 🚧 emerging |

---

# 🚀 Run

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v6.py
```

---

# 📁 Results

```
APPLICATIONS/power_systems/nexah_ieee9/results/
```

Includes:

- field scans  
- controller runs  
- trajectories  
- intervention logs  

---

# 🧭 Current Status

| Component | Status |
|----------|--------|
| Structure Discovery | ✅ |
| Field Modeling | ✅ |
| Early Detection | ✅ (43.9 s) |
| Adaptive Control | ⚙️ Prototype |
| Phase Dynamics | ⚙️ Experimental |
| Field Navigation | 🚧 In Development |

---

# 🔮 Next Steps

- scale adaptive control to IEEE118+  
- quantify stability gains  
- refine navigation controller  
- real-time field estimation  

---

# 🧠 Final Insight

Power systems are not binary.

They exist within a:

> **structured stability landscape**

NEXAH makes this:

> **visible, measurable, and controllable**

---

## 🌀 NEXAH

> From dynamics → structure  
> From structure → field  
> From field → geometry  
> From geometry → control  

---

**Thomas K. R. Hofmann · 2026**
