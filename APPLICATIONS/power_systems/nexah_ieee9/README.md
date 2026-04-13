# ⚡ NEXAH — IEEE9 Stability Field System (v3 + Dynamics Layer)

## 🧭 Overview

This module implements the NEXAH framework on a power system test case (IEEE 9-bus).

It transforms classical voltage stability analysis into a:

> **continuous stability field with adaptive, closed-loop control**

---

## 🔬 Core Idea

Instead of asking:

> "Will the system collapse?"

NEXAH answers:

> "Where are we in the stability field — and how can we navigate it?"

---

## 🧱 Pipeline Architecture

Simulation → Features → Manifold → Overlay → Prediction → Policy → Adaptive Control → System Evolution

---

# 📊 System Behavior (Field Layer — v3)

## ⚡ Voltage Collapse (Adaptive Closed Loop)

![Voltage Collapse](results/run_20260412_223816/plot.png)

✔ Collapse dynamics preserved  
✔ Adaptive stabilization in mid-regime  
✔ Structural transitions remain visible  

---

## ⚡ Collapse Risk Field

![Collapse Risk](results/run_20260412_223816/risk.png)

✔ Peak risk ≈ 0.77  
✔ Clean signal (low noise)  
✔ Structured collapse boundary  

---

## ⚡ Intervention Field

![Intervention](results/run_20260412_223816/intervention.png)

✔ Smooth control escalation  
✔ No saturation artifacts  
✔ Trajectory-aware behavior  

---

# 🆕 🔁 Controller Replay (Field Interaction)

## Field Overlay

![Field Overlay](results/controller_runs/controller_replay_20260413_214411/field_overlay.png)

## Time Series

![Timeseries](results/controller_runs/controller_replay_20260413_214411/timeseries.png)

---

# 🧠 NEW: Dynamical Controller Layer (v7 → v9)

NEXAH now includes a **true dynamical system layer**.

---

## 🔹 Evolution

| Version | Behavior |
|--------|---------|
| v7 | Gradient + drift (static convergence) |
| v8 | + rotation (perturbed convergence) |
| v9 | Phase coupling (2D dynamical system) |

---

## 🔁 Phase Space Evolution

### v7

![v7 Phase](results/controller_v7_1/output_v7_1_phase.png)

---

### v8

![v8 Phase](results/controller_v8/output_v8_phase.png)

---

### v9 — TRUE PHASE SYSTEM

#### λ vs ψ (Phase Portrait)

![v9 Phase Lambda Psi](results/controller_v9/output_v9_phase_lambda_psi.png)

#### Risk vs Distance

![v9 Phase Risk Distance](results/controller_v9/output_v9_phase_risk_distance.png)

---

## 📈 Controller Time Evolution (v9)

![v9 Timeseries](results/controller_v9/output_v9_plot.png)

---

## 🔬 Interpretation (Dynamics Layer)

The controller is no longer:

> a regulator

It is becoming:

> a **field-driven dynamical navigator**

---

## 🧩 System Layer Separation

The project now consists of two interacting layers:

### 1. Application Layer (IEEE System)
- Risk field  
- Collapse dynamics  
- Adaptive policy (v3)

### 2. NEXAH Core Layer
- Field dynamics  
- Phase coupling  
- Trajectory shaping  

---

## ⚠️ Current Limitation

The system is still:

- dissipative  
- converging to fixed points  
- not yet sustaining motion  

---

## 🔥 Next Target — v10

Goal:

> **self-sustained dynamics (limit cycles)**

---

## 🔮 Next Steps

- Establish limit cycles (v10)  
- Map vector fields (flow structure)  
- Identify stability basins  
- Enable trajectory navigation  
- Integrate with real AC power flow  

---

# ⚖️ Classical vs NEXAH

| Feature | Classical | NEXAH |
|--------|----------|------|
| Static thresholds | ✅ | ❌ |
| Dynamic risk field | ❌ | ✅ |
| Early warning | ⚠️ | ✅ |
| Closed-loop control | ❌ | ✅ |
| Structural modeling | ❌ | ✅ |
| Predictive behavior | ❌ | ✅ |
| Field navigation | ❌ | 🚧 |

---

# 🚀 Run

Synthetic:
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/decision/main_v2.py

Controller (latest):

PYTHONPATH=APPLICATIONS/power_systems
python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v9.py

---

# 📁 Results

APPLICATIONS/power_systems/nexah_ieee9/results/

---

# 🧭 Status

Field Model        ✅  
Adaptive Control   ✅  
Closed Loop        ✅  
Dynamics Layer     ✅ (v9)  
Navigation         🚧 (v10)  

---

# 🔥 Final Insight

Power systems are not binary (stable / unstable)

They exist inside a:

> **structured stability landscape**

NEXAH turns this into something we can:

> **measure, interpret, and navigate**
