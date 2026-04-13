# ⚡ NEXAH / Power Systems
**Structural Field Navigation for Power System Stability**

---

## 🧭 Overview

This module implements the **NEXAH framework for power systems**:

> A geometry-based approach to detect, interpret, and navigate instability  
> in complex electrical grids.

Instead of treating collapse as a threshold event, NEXAH models it as:

→ a **structural transformation in system dynamics**

---

## 🧠 Core Idea

Classical approach:

→ monitor voltage thresholds  
→ react after instability  

NEXAH:

→ reconstructs system **geometry + flow structure**  
→ detects **early structural drift**  
→ enables **trajectory-aware control**

---

## 🧩 Module Architecture

This repository is organized into three complementary layers:

---

### 🔹 1. Structural Theory & Geometry

📁 `stability_field_dynamics/ieee_test_cases`

- collapse manifold (low-dimensional attractor)
- rift (collapse boundary)
- distance (stability metric)
- residual (structural deviation)
- topology (branching states)

📌 Deep dive:  
→ [`ieee_test_cases/README.md`](stability_field_dynamics/ieee_test_cases/README.md)

---

### 🔹 2. Geometric Pipeline & Navigation

📁 `ieee_xray_pipeline`

- low-dimensional state space (c, dc, d²c)
- polar / 3D projections
- Root Cube navigation
- attractor + topology experiments

📌 Deep dive:  
→ [`ieee_xray_pipeline/README.md`](ieee_xray_pipeline/README.md)

---

### 🔹 3. Closed-Loop Control Systems

#### Small-scale system (development)

📁 `nexah_ieee9`

- full NEXAH pipeline
- adaptive control (v3)
- synthetic + real grid prototype

📌 Deep dive:  
→ [`nexah_ieee9/README.md`](nexah_ieee9/README.md)

---

#### Large-scale validation (NEW 🚀)

📁 `nexah_ieeeX`

- scaling across IEEE systems
- pandapower-based AC solver
- real grid dynamics + intervention

📌 Deep dive:  
→ [`nexah_ieeeX/README.md`](nexah_ieeeX/README.md)

---

## 📊 Experimental Results (Scaling)

### 🔹 IEEE 118 — Baseline

![IEEE118](nexah_ieeeX/results/run_ieee118_20260413_004449/overview.png)

- clean collapse structure  
- early risk detection  
- pipeline baseline validated  

---

### 🔹 IEEE 300 — Nonlinear Regime

![IEEE300](nexah_ieeeX/results/run_ieee300_20260413_015843/plot.png)

- nonlinear structural dynamics  
- manifold + risk activation  
- adaptive control required  

---

### 🔹 IEEE 1354 — Large Grid

![IEEE1354](nexah_ieeeX/results/run_ieee1354_20260413_020204/plot.png)

- distributed voltage field  
- stable large-scale behavior  
- controllable regime  

---

### 🔹 IEEE 9241 (PEGASE) — Real Scale

![IEEE9241](nexah_ieeeX/results/run_ieee9241_20260413_021422/plot.png)

- real-world scale system  
- early risk spike detection  
- stable post-intervention regime  
- no full collapse observed  

---

## ⚙️ System Pipeline

*Simulation → Features → Manifold → Risk → Policy → Actions*

### Core Components

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

## ⚡ Key Result

NEXAH scales across:

*IEEE 9 → 118 → 300 → 1354 → 9241*

while maintaining:

- structural detection ✔  
- interpretable geometry ✔  
- adaptive control ✔  

---

## 🔬 System Behavior

Three regimes emerge:

1. **Stable regime**
   - high coherence
   - low risk

2. **Transition regime**
   - fragmentation
   - curvature increase

3. **Collapse regime**
   - divergence
   - manifold departure

---

## ⚠️ Current Limitations

- full collapse prevention ❌  
- actuator realism limited  
- no sustained attractor navigation  
- requires validation vs:
  - PV curves  
  - eigenvalue analysis  
  - continuation power flow  

---

## 🔮 Next Milestones

- multi-step prediction (lookahead)
- adaptive λ control
- stability basin mapping
- multi-attractor navigation
- real grid data integration

---

## 🧠 Final Insight

> Instability is not a voltage problem.  
> It is a **structural transformation in system dynamics**.

NEXAH makes this transformation:

→ visible  
→ measurable  
→ partially controllable  

---

## 🌀 NEXAH

> From simulation → structure  
> From structure → navigation  
> From navigation → stability  

---

**Author:** Thomas K. R. Hofmann  
April 2026

