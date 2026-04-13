# ⚡ NEXAH / Power Systems
**Structural Field Navigation for Power System Stability**

---

## 🧭 Overview

NEXAH introduces a **geometry-based framework** for power system stability.

Instead of modeling instability as a threshold violation, NEXAH interprets it as:

> a **structural transformation in system dynamics**

This enables:

- early detection of instability  
- continuous stability assessment  
- trajectory-aware intervention  

---

## 🧠 Core Paradigm

Classical methods:

→ monitor voltage thresholds  
→ react after instability  

NEXAH:

→ reconstructs **structure + flow + geometry**  
→ detects instability as **loss of alignment**  
→ enables **navigation within stability fields**

---

# 📊 System Highlights

## 🔹 Figure 1 — Collapse Geometry (Fundamental Structure)

![Collapse Geometry](stability_field_dynamics/ieee_test_cases/outputs/ieee14_v52_residual_vs_distance.png)

**Observation:**

- collapse is not random  
- system states organize into structured regions  
- distinct regimes emerge (core, transition, collapse)

**Interpretation:**

> Stability is equivalent to proximity to a structural boundary (rift)

---

## 🔹 Figure 2 — Flow Field Dynamics (Underlying Physics)

![Flow Field](stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

**Observation:**

- trajectories follow structured vector fields  
- deviations are directional, not random  

**Interpretation:**

> The system is governed by a **field**, not discrete transitions  

---

## 🔹 Figure 3 — Geometric State Space (Navigation Layer)

![Root Cube](ieee_xray_pipeline/results/v36b_good_final_3d.png)

**Observation:**

- high-dimensional system collapses into low-dimensional structure  
- trajectories become geometrically interpretable  

**Interpretation:**

> Stability becomes a **navigation problem in state space**

---

## 🔹 Figure 4 — Adaptive Control (Closed-Loop System)

![Control](nexah_ieee9/results/run_20260412_223816/plot.png)

**Observation:**

- control actions adapt continuously  
- system avoids collapse without suppressing dynamics  

**Interpretation:**

> Control operates on **trajectory behavior**, not static states  

---

## 🔹 Figure 5 — Real-Scale Validation (9241-Bus PEGASE)

![IEEE9241](nexah_ieeeX/results/run_ieee9241_20260413_021422/plot.png)

**Observation:**

- system remains stable at real-world scale  
- early risk detection persists  
- intervention stabilizes trajectory  

**Interpretation:**

> NEXAH scales from small systems to **real grid size**

---

# ⚙️ System Pipeline

*Simulation → Features → Manifold → Risk → Policy → Actions*


### Components

- AC power flow solver (pandapower)
- structural feature extraction
- manifold fitting
- residual + distance field
- risk prediction
- adaptive intervention policy

---

## 🧮 Mathematical View

System state:

*x = (coherence, frag, d²c, residual, distance)*


Dynamics:

*dx/dt = f(x) + u(x, dx/dt)*


- **f(x)** → physical grid dynamics  
- **u(x, dx/dt)** → NEXAH control  

---

### Stability Definition

*S = { x : risk(x) < threshold }*


Stability becomes:

→ **geometric containment in state space**

---

## ⚖️ Classical vs NEXAH

| Feature                | Classical IEEE | NEXAH |
|----------------------|---------------|------|
| Static thresholds     | Yes           | No   |
| Dynamic risk field    | No            | Yes  |
| Early warning         | Limited       | Yes  |
| Closed-loop control   | No            | Yes  |
| Structural modeling   | No            | Yes  |
| Adaptive control      | No            | Yes  |

---


# 📈 Scaling Results

| System   | Behavior |
|----------|----------|
| IEEE 118 | baseline collapse structure |
| IEEE 300 | nonlinear dynamics emerge |
| IEEE 1354 | distributed stability field |
| IEEE 9241 | real-scale validation |


---

# 🧩 Module Structure

## 🔹 Structural Theory
→ [`stability_field_dynamics`](stability_field_dynamics/ieee_test_cases/README.md)

## 🔹 Geometric Pipeline
→ [`ieee_xray_pipeline`](ieee_xray_pipeline/README.md)

## 🔹 Control System (Small Scale)
→ [`nexah_ieee9`](nexah_ieee9/README.md)

## 🔹 Scaling & Real Grid
→ [`nexah_ieeeX`](nexah_ieeeX/README.md)

---

# ⚠️ Limitations

- full collapse prevention not yet achieved  
- actuator realism limited  
- attractor navigation still experimental  
- requires validation vs classical methods:
  - PV curves  
  - eigenvalue analysis  
  - continuation power flow  

---

# 🔮 Next Steps

- multi-step prediction (lookahead)  
- adaptive λ control  
- stability basin mapping  
- multi-attractor navigation  
- real-world data integration  

---

# 🧠 Final Insight

> Instability is not a threshold event.  
> It is a **structural transformation in system dynamics**.

NEXAH makes this transformation:

→ visible  
→ measurable  
→ partially controllable  

---

# 🌀 NEXAH

> From simulation → structure  
> From structure → navigation  
> From navigation → stability  

---

**Author:** Thomas K. R. Hofmann  
April 2026
