# ⚡ NEXAH — IEEE9 Stability Field System

![Status](https://img.shields.io/badge/status-active-success)
![Field Model](https://img.shields.io/badge/field-model-blue)
![Navigation](https://img.shields.io/badge/navigation-enabled-brightgreen)
![Dynamics](https://img.shields.io/badge/dynamics-v11-orange)

---

## 🧭 Overview

NEXAH transforms classical power system analysis into:

> **a continuous stability field with closed-loop control and navigation**

Instead of binary stability:

> stable ❌ / unstable ❌  

the system operates inside a:

> **structured stability landscape**

---

## 🔬 Core Idea

Instead of asking:

> "Will the system collapse?"

NEXAH answers:

> "Where are we in the field — and how do we move safely?"

---

## 🧱 Pipeline

Simulation → Features → Manifold → Field → Risk → Policy → Control → Navigation

---

# 🎬 Navigation (v11_2)

![Navigation GIF](results/visuals/nexah_navigation_v11.gif)

✔ Smooth convergence to boundary  
✔ No oscillation  
✔ No collapse  
✔ Maximum safe utilization  

---

# 📊 Field Behavior (v3)

## Voltage Collapse
![Voltage Collapse](results/run_20260412_223816/plot.png)

## Risk Field
![Risk](results/run_20260412_223816/risk.png)

## Intervention
![Intervention](results/run_20260412_223816/intervention.png)

---

# 🔁 Controller Replay

## Field Interaction
![Field Overlay](results/controller_runs/controller_replay_20260413_214411/field_overlay.png)

## Time Evolution
![Timeseries](results/controller_runs/controller_replay_20260413_214411/timeseries.png)

---

# 🌀 Dynamical Layer (v7 → v9)

## Phase Evolution

### v7
![v7](results/controller_v7_1/output_v7_1_phase.png)

### v8
![v8](results/controller_v8/output_v8_phase.png)

### v9 — Phase System

![λ vs ψ](results/controller_v9/output_v9_phase_lambda_psi.png)

![Risk vs Distance](results/controller_v9/output_v9_phase_risk_distance.png)

![Timeseries](results/controller_v9/output_v9_plot.png)

---

# 🔥 Field Geometry (v10 → v11)

## Stability Surface
![Surface](results/controller_v10/output_v10_plot.png)

## Phase + Field Structure
![v10_3 Phase](results/controller_v10_3/output_v10_3_phase_lambda_psi.png)

![v10_3 Field](results/controller_v10_3/output_v10_3_phase_risk_distance.png)

---

## 🧠 Field Structure Insight

### 🟡 Transition (~λ ≈ 0.8)
- first curvature  
- deformation begins  
- still stable  

### 🔴 Instability (~λ ≈ 1.25+)
- nonlinear amplification  
- rapid risk growth  
- collapse zone  

---

# 🧭 Navigation Result

λ = 0.600 → 0.7717 (safe boundary tracking)

---

# 🧠 System Interpretation

The system now operates as:

> a trajectory evolving within a structured stability field

where:

- field = extracted from system physics  
- geometry = defines stability structure  
- navigation = safe movement within field  

---

# 🔥 Key Result

A complex physical system can be:

- mapped into a field  
- understood geometrically  
- navigated safely  

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

PYTHONPATH=APPLICATIONS/power_systems \
python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v11_0.py

### Navigation

PYTHONPATH=APPLICATIONS/power_systems \
python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v11_2.py

---

# 📁 Results

APPLICATIONS/power_systems/nexah_ieee9/results/

---

# 🧭 Status

Field Model        ✅  
Adaptive Control   ✅  
Closed Loop        ✅  
Dynamics           ✅  
Field Geometry     ✅  
Navigation         ✅  

---

# 🔮 Next

- Multi-agent navigation  
- Real-time field estimation  
- Higher-dimensional systems  
- Real grid integration  

---

# 🔥 Final Insight

Power systems are not binary.

They exist within a:

> **structured stability landscape**

NEXAH makes it:

> **navigable**

