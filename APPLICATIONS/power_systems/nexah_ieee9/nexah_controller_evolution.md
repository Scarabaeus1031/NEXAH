# ⚡ NEXAH — Structural Navigation in Complex Systems

![Status](https://img.shields.io/badge/status-active-success)
![Field Model](https://img.shields.io/badge/field-model-blue)
![Navigation](https://img.shields.io/badge/navigation-enabled-brightgreen)
![Dynamics](https://img.shields.io/badge/dynamics-v11-orange)

---

## 🧭 Overview

NEXAH transforms classical system analysis into:

> **a continuous stability field with closed-loop control and navigation**

Instead of binary classification:

> stable ❌ / unstable ❌  

systems are understood as existing within a:

> **structured stability landscape**

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
simulation → structure → field → geometry → navigation
```

---

## 🔥 Core Insight

Control is no longer:

→ reactive (based on error)

but:

→ predictive (based on geometry)

---

NEXAH does not react to instability.

It **reads the structure of the system** and moves within it.

👉 Stability becomes a **navigation problem**

---

# 📊 From Collapse → Field → Navigation

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

## 🔹 3. Field Navigation (v11_2)

![Navigation](APPLICATIONS/power_systems/nexah_ieee9/results/visuals/nexah_navigation_v11.gif)

*NEXAH actively navigates toward the stability boundary without triggering collapse.*

- smooth convergence  
- no oscillation  
- maximum safe utilization  

---

## 🔹 4. Closed-Loop Control (IEEE9)

![Control](APPLICATIONS/power_systems/nexah_ieee9/results/controller_v9/output_v9_plot.png)

*Control reshapes trajectories instead of reacting to states.*

- early intervention  
- structured escalation  
- trajectory-aware behavior  

---

## 🔹 5. Phase Dynamics (v9)

![Phase](APPLICATIONS/power_systems/nexah_ieee9/results/controller_v9/output_v9_phase_lambda_psi.png)

*System + controller form a dynamical system.*

- phase space: (λ, ψ)  
- attractor-based stability  
- coupling between system and control  

---

# 🧠 System Interpretation

The system now operates as:

> a trajectory evolving within a structured stability field

where:

- field = extracted from system physics  
- geometry = defines stability structure  
- navigation = movement along safe trajectories  

---

# 🔥 Key Result

A complex physical system can be:

- mapped into a field  
- understood geometrically  
- navigated safely without entering collapse  

---

# ⚖️ Classical vs NEXAH

| Feature | Classical | NEXAH |
|--------|----------|------|
| Static thresholds | ✅ | ❌ |
| Dynamic field | ❌ | ✅ |
| Early warning | ⚠️ | ✅ |
| Closed-loop control | ❌ | ✅ |
| Predictive behavior | ❌ | ✅ |
| Navigation | ❌ | ✅ |

---

# 🚀 Run

### Stability Scan

```bash
PYTHONPATH=APPLICATIONS/power_systems \
python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v11_0.py
```

### Navigation Controller

```bash
PYTHONPATH=APPLICATIONS/power_systems \
python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v11_2.py
```

---

# 📁 Results

```
APPLICATIONS/power_systems/nexah_ieee9/results/
```

Includes:

- field scans  
- controller evolution (v7 → v11)  
- navigation runs  
- replay logs  
- full system traces  

---

# 🧭 Status

| Component | Status |
|----------|--------|
| Structure Discovery | ✅ |
| Field Modeling | ✅ |
| Adaptive Control | ✅ |
| Dynamics Layer | ✅ |
| Field Geometry | ✅ |
| Navigation | ✅ |

---

# 🔮 Next Steps

- multi-agent navigation  
- real-time field estimation  
- higher-dimensional systems  
- real grid integration  

---

# 🧠 Final Insight

Power systems are not binary.

They exist within a:

> **structured stability landscape**

NEXAH makes this:

> **visible, measurable, and navigable**

---

# 🌀 NEXAH

> From dynamics → structure  
> From structure → geometry  
> From geometry → navigation  

---

**Thomas K. R. Hofmann · 2026**
