# ⚡ NEXAH — IEEE9 Stability Field System (v3 → v11)

## 🧭 Overview

This module implements the NEXAH framework on a power system test case (IEEE 9-bus).

It transforms classical voltage stability analysis into a:

> **continuous stability field with adaptive, closed-loop control and navigation**

---

## 🔬 Core Idea

Instead of asking:

> "Will the system collapse?"

NEXAH answers:

> "Where are we in the stability field — and how can we navigate it safely?"

---

## 🧱 Pipeline Architecture

Simulation → Features → Manifold → Overlay → Prediction → Policy → Adaptive Control → Field Navigation

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

# 🧠 Dynamical Controller Layer (v7 → v9)

NEXAH evolved from static control into a **true dynamical system**.

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

### v8
![v8 Phase](results/controller_v8/output_v8_phase.png)

### v9 — TRUE PHASE SYSTEM

#### λ vs ψ (Phase Portrait)
![v9 Phase Lambda Psi](results/controller_v9/output_v9_phase_lambda_psi.png)

#### Risk vs Distance
![v9 Phase Risk Distance](results/controller_v9/output_v9_phase_risk_distance.png)

---

## 📈 Controller Time Evolution (v9)

![v9 Timeseries](results/controller_v9/output_v9_plot.png)

---

# 🆕 🔥 Field Geometry & Navigation (v10 → v11)

## 🔹 v10 — Stability Surface

- Continuous scan over λ
- Extraction of:
  - vmin (voltage stability)
  - loading (system stress)
  - risk (field function)

👉 Result:
> A **continuous stability surface**

---

## 🔹 v11 — Field Structure Detection

Two key regions emerge:

### 🟡 Structural Transition (~λ ≈ 0.8)

- First curvature appears  
- Field begins to deform  
- System still stable  

---

### 🔴 Instability Onset (~λ ≈ 1.25+)

- Strong nonlinear amplification  
- Rapid risk growth  
- Collapse region  

---

## ⚠️ Critical Insight

> Instability is NOT triggered by first curvature  
> but by **nonlinear amplification of the field**

---

## 🔹 v11_2 — Field Navigation Controller

Controller now operates on geometry:

```text
λ_target = λ_critical − Δ
```
## Behavior

✔ Smooth convergence to boundary  
✔ No oscillation  
✔ No collapse  
✔ Maximum safe utilization  

---

## 📈 Navigation Result

Example trajectory:

λ = 0.600 → 0.7717 (safe boundary tracking)

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

- mapped into a stability field  
- analyzed via geometry  
- navigated safely without entering collapse  

---

# 🧩 System Layer Separation

## 1. Application Layer (Power System)

- Voltage stability  
- Load dynamics  
- Physical constraints  

## 2. NEXAH Core Layer

- Field geometry  
- Risk dynamics  
- Navigation logic  

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
| Field navigation | ❌ | ✅ |

---

# 🚀 Run

### Stability Scan (v11)

PYTHONPATH=APPLICATIONS/power_systems \
python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v11_0.py

### Navigation Controller (v11_2)

PYTHONPATH=APPLICATIONS/power_systems \
python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v11_2.py

---

# 📁 Results

APPLICATIONS/power_systems/nexah_ieee9/results/

Includes:

- controller evolution (v7 → v11)  
- field scans  
- navigation runs  
- replay logs  
- full system state traces  

---

# 🧭 Status

| Component | Status |
|----------|--------|
| Field Model | ✅ |
| Adaptive Control | ✅ |
| Closed Loop | ✅ |
| Dynamics Layer | ✅ |
| Field Geometry | ✅ |
| Navigation | ✅ |

---

# 🔮 Next Steps

- Real-time field estimation  
- Multi-agent navigation  
- Higher-dimensional state spaces  
- Integration with real grid data (pandapower)  

---

# 🔥 Final Insight

Power systems are not binary (stable / unstable)

They exist within a:

> **structured stability landscape**

NEXAH turns this into something we can:

> **measure, understand, and navigate**
