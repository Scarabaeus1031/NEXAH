# ⚡ NEXAH — IEEE9 Stability Field Navigation

![Status](https://img.shields.io/badge/status-active-success)
![Field Model](https://img.shields.io/badge/field-model-blue)
![Navigation](https://img.shields.io/badge/navigation-enabled-brightgreen)
![Dynamics](https://img.shields.io/badge/dynamics-v6_public_|_v11_dev-orange)

---

## 🧭 Abstract

NEXAH introduces a new paradigm for power system stability:

> **Stability is not a binary condition — it is a navigable field.**

Instead of detecting collapse after it occurs, NEXAH:

- reconstructs the **underlying stability geometry**
- defines a **continuous risk field**
- enables **closed-loop control along safe trajectories**

---

## 🔁 System Pipeline

```text
Simulation → Features → Manifold → Field → Risk → Policy → Control → Navigation
```

---

## 🧭 Version Map (Controller Evolution)

| Version | Status | Description |
|--------|--------|------------|
| v6 | ✅ public | stable closed-loop control (reproducible) |
| v7 | 🧪 experimental | dynamic response behavior |
| v8 | 🧪 experimental | rotational / oscillatory dynamics |
| v9 | 🧪 experimental | coupled phase system (λ, ψ) |
| v10 | 🧪 experimental | field surface reconstruction |
| v11 | 🧪 internal | early navigation behavior |

👉 **v6 is the current reproducible reference**  
👉 v7–v11 represent ongoing development toward full navigation

---

# 📊 Field Reconstruction

## 🔹 Voltage Collapse

![Voltage Collapse](results/run_20260412_223816/plot.png)

*Collapse is not abrupt — it follows a continuous trajectory in state space.*

---

## 🔹 Risk Field

![Risk](results/run_20260412_223816/risk.png)

- low values → stable region  
- sharp increase → collapse boundary  

👉 Instability appears as a **structured region**, not a threshold.

---

## 🔹 Flow Field Dynamics

![Flow Field](results/controller_runs/controller_replay_20260413_214411/field_overlay.png)

*System trajectories follow structured flow paths.*

- motion is directional  
- instability follows field geometry  

👉 This is the **core object of NEXAH**.

---

# 🔁 Closed-Loop Control

## 🔹 Controller Response

![Control](results/run_20260412_223816/intervention.png)

*Control reshapes trajectories instead of reacting to states.*

- early intervention  
- smooth response  
- geometry-aware behavior  

---

## 🔹 Time Evolution

![Timeseries](results/controller_runs/controller_replay_20260413_214411/timeseries.png)

👉 The controller is part of the **system dynamics**, not external to it.

---

# 🌀 Dynamical System Layer (v7 → v9)

NEXAH evolves from static control to a coupled dynamical system.

---

### v7 — Static Convergence
![v7](results/controller_v7_1/output_v7_1_phase.png)

---

### v8 — Perturbed Dynamics
![v8](results/controller_v8/output_v8_phase.png)

---

### v9 — Phase System

![λ vs ψ](results/controller_v9/output_v9_phase_lambda_psi.png)

![Risk vs Distance](results/controller_v9/output_v9_phase_risk_distance.png)

![Timeseries](results/controller_v9/output_v9_plot.png)

👉 System + controller form a **coupled dynamical process**

---

# 🔥 Field Geometry (v10 → v11, experimental)

## 🔹 Stability Surface

![Surface](results/controller_v10/output_v10_plot.png)

## 🔹 Field Structure

![v10_3 Phase](results/controller_v10_3/output_v10_3_phase_lambda_psi.png)

![v10_3 Field](results/controller_v10_3/output_v10_3_phase_risk_distance.png)

---

## 🧠 Emergent Structure

### 🟡 Transition Region (~λ ≈ 0.8)

- structural deformation  
- still stable  

### 🔴 Instability Region (~λ ≈ 1.25+)

- nonlinear amplification  
- collapse dynamics  

---

## ⚠️ Critical Insight

> Instability is NOT triggered by first curvature  
> but by **nonlinear amplification of the field**

---

# 🎬 Field Navigation (Prototype)

![Navigation GIF](results/visuals/nexah_navigation_v11.gif)

*Controller approaches the stability boundary without triggering collapse.*

- smooth convergence  
- reduced oscillation  
- near-critical operation  

⚠️ Based on internal experimental versions (v7–v11)

---

# 🧭 Navigation Result

λ = 0.600 → 0.7717  

→ operation close to critical boundary without collapse

---

# 🧠 System Interpretation

The system operates as:

> a trajectory evolving within a structured stability field

where:

- field = extracted from system physics  
- geometry = defines stability structure  
- control = trajectory shaping within the field  

---

# 🚀 Run (Public Version)

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v6.py
```

---

# 🔥 Key Result

A complex physical system can be:

- mapped into a field  
- understood geometrically  
- controlled via trajectory shaping  
- pushed toward optimal safe operation  
