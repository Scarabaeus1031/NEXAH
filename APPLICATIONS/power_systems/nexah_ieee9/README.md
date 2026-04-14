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
- enables **closed-loop navigation along safe trajectories**

This transforms control from:

> reactive intervention → **predictive field navigation**

---

## 🔬 Problem Statement

Classical power system analysis operates on:

- static thresholds  
- discrete stability labels  
- post-event detection  

This leads to a fundamental limitation:

> The system reacts **after instability emerges**, not before.

---

## 💡 NEXAH Approach

NEXAH reframes the problem:

> A power system exists inside a **structured stability landscape**

Key idea:

- every system state has a **position in a field**
- instability is a **geometric property**
- control becomes **movement within that geometry**

---

## 🧱 System Pipeline

```text
Simulation → Features → Manifold → Field → Risk → Policy → Control → Navigation
```

---

## 🎬 Field Navigation (Prototype)

This animation shows the controller navigating toward the **stability boundary** without triggering collapse.

![Navigation GIF](results/visuals/nexah_navigation_v11.gif)

### Interpretation

- trajectory approaches critical region  
- stabilizes before instability  
- maintains maximum safe utilization  

👉 **Insight:**  
Control follows the **geometry of the field**, not just local state error.

---

**Note:**
- This visualization is based on **internal experimental versions (v7–v11)**  
- The latest **public, reproducible version is v6**  

---

# 📊 Field Reconstruction (v3)

## Voltage Collapse

![Voltage Collapse](results/run_20260412_223816/plot.png)

The voltage profile shows gradual degradation under increasing load.

👉 **Insight:**  
Collapse is not abrupt — it follows a **continuous trajectory in state space**.

---

## Risk Field

![Risk](results/run_20260412_223816/risk.png)

The risk function encodes system stability as a continuous scalar field.

- low values → stable region  
- sharp increase → collapse boundary  

👉 **Insight:**  
Instability appears as a **structured region**, not a threshold.

---

## Intervention Dynamics

![Intervention](results/run_20260412_223816/intervention.png)

The controller response evolves smoothly with system stress.

👉 **Insight:**  
Control becomes **trajectory-aware**, not event-triggered.

---

# 🔁 Closed-Loop Field Interaction

## Field Overlay

![Field Overlay](results/controller_runs/controller_replay_20260413_214411/field_overlay.png)

## Time Evolution

![Timeseries](results/controller_runs/controller_replay_20260413_214411/timeseries.png)

👉 **Insight:**  
The controller is not external — it is part of the **field dynamics itself**.

---

# 🌀 Dynamical System Layer (v7 → v9, experimental progression)

NEXAH evolves from static control to a true dynamical system.

---

## Phase Evolution

### v7 — Static Convergence
![v7](results/controller_v7_1/output_v7_1_phase.png)

→ gradient + drift  
→ fixed-point behavior  

---

### v8 — Perturbed Dynamics
![v8](results/controller_v8/output_v8_phase.png)

→ rotational component  
→ small oscillations  

---

### v9 — Phase System

![λ vs ψ](results/controller_v9/output_v9_phase_lambda_psi.png)

![Risk vs Distance](results/controller_v9/output_v9_phase_risk_distance.png)

![Timeseries](results/controller_v9/output_v9_plot.png)

👉 **Insight:**  
The system becomes a **coupled dynamical process**, not a static controller.

---

# 🔥 Field Geometry (v10 → v11, experimental)

The system is now analyzed as a **continuous stability surface**.

---

## Stability Surface

![Surface](results/controller_v10/output_v10_plot.png)

## Field Structure

![v10_3 Phase](results/controller_v10_3/output_v10_3_phase_lambda_psi.png)

![v10_3 Field](results/controller_v10_3/output_v10_3_phase_risk_distance.png)

---

## 🧠 Emergent Structure

Two regimes naturally appear:

### 🟡 Transition Region (~λ ≈ 0.8)

- first curvature  
- structural deformation  
- still stable  

---

### 🔴 Instability Region (~λ ≈ 1.25+)

- nonlinear amplification  
- rapid risk growth  
- collapse dynamics  

---

## ⚠️ Critical Insight

> Instability is NOT triggered by first curvature  
> but by **nonlinear amplification of the field**

---

# 🧭 Navigation Result

λ = 0.600 → 0.7717

→ just below critical boundary

👉 **Insight:**  
Maximum utilization without entering instability.

---

# 🧠 System Interpretation

The system now operates as:

> a trajectory evolving within a structured stability field

where:

- field = extracted from system physics  
- geometry = defines stability structure  
- navigation = movement along safe trajectories

# 🚀 Run (Public Version)

```bash
PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v6.py
```
Note:
	•	v6 is the latest stable and reproducible version in this repository
	•	newer iterations (v7–v11) are currently being consolidated and cleaned


---

# 🔥 Key Result

A complex physical system can be:

- mapped into a field  
- understood geometrically  
- navigated safely  
