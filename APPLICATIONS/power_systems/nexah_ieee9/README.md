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

Two regimes emerge:

### 🟡 Transition (~λ ≈ 0.8)
- first curvature
- deformation begins
- still stable

### 🔴 Instability (~λ ≈ 1.25+)
- nonlinear amplification
- rapid risk growth
- collapse zone

---

# 🧭 Navigation Controller (v11_2)

## Behavior

✔ Smooth convergence to boundary  
✔ No oscillation  
✔ No collapse  
✔ Maximum safe utilization  

---

## 📈 Navigation Result

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

> **navigable**| v7 | Gradient + drift (static convergence) |
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
