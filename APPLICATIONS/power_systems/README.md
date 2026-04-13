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
- phase-space navigation (v9)

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

**Interpretation:**

> Stability is equivalent to proximity to a structural boundary (rift)

---

## 🔹 Figure 2 — Flow Field Dynamics (Underlying Physics)

![Flow Field](stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

**Interpretation:**

> The system is governed by a **continuous field**, not discrete transitions  

---

## 🔹 Figure 3 — Geometric State Space (Navigation Layer)

![Root Cube](ieee_xray_pipeline/results/v36b_good_final_3d.png)

**Interpretation:**

> Stability becomes a **navigation problem in state space**

---

## 🔹 Figure 4 — Closed-Loop Adaptive Control (IEEE9)

![Control](nexah_ieee9/results/controller_v9/output_v9_plot.png)

**Observation:**

- smooth intervention dynamics  
- no oscillatory instability  
- stable convergence  

**Interpretation:**

> Control operates on **trajectory behavior**, not static states  

---

## 🔹 Figure 5 — Phase Dynamics (NEW v9)

![Phase Lambda Psi](nexah_ieee9/results/controller_v9/output_v9_phase_lambda_psi.png)

**Observation:**

- system evolves in a structured phase space  
- converges toward a stable attractor  

**Interpretation:**

> Stability emerges as a **dynamical system in phase space (λ, ψ)**  

---

## 🔹 Figure 6 — Risk–Distance Field

![Risk Distance](nexah_ieee9/results/controller_v9/output_v9_phase_risk_distance.png)

**Interpretation:**

> Collapse risk is geometrically encoded in the field structure  

---

## 🔹 Figure 7 — Real-Scale Validation (9241-Bus PEGASE)

![IEEE9241](nexah_ieeeX/results/run_ieee9241_20260413_021422/plot.png)

**Interpretation:**

> NEXAH scales from small systems to **real grid size**

---

# ⚙️ System Pipeline

```text
Simulation → Features → Manifold → Field → Risk → Policy → Dynamics → Control
```

---

## 🧮 Mathematical View

System state:

```
x = (c, frag, d²c, residual, distance, ψ)
```

Dynamics:

```
dx/dt = f(x) + u(x, dx/dt)
```

Phase system (v9):

```
(λ, ψ) → trajectory in phase space
```

---

## 🔹 Stability Definition

```
S = { x : risk(x) < threshold }
```

becomes:

→ **geometric + dynamical containment**

---

## ⚖️ Classical vs NEXAH

| Feature                | Classical IEEE | NEXAH |
|----------------------|---------------|------|
| Static thresholds     | Yes           | No   |
| Dynamic risk field    | No            | Yes  |
| Early warning         | Limited       | Yes  |
| Closed-loop control   | No            | Yes  |
| Structural modeling   | No            | Yes  |
| Phase dynamics        | No            | **Yes (v9)** |

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

## 🔹 Control System (IEEE9)
→ [`nexah_ieee9`](nexah_ieee9/README.md)

## 🔹 Scaling & Real Grid
→ [`nexah_ieeeX`](nexah_ieeeX/README.md)

---

# ⚠️ Limitations

- full collapse prevention not yet achieved  
- actuator realism limited  
- attractor navigation still emerging (v9+)  
- validation vs classical methods ongoing  

---

# 🔮 Next Steps

- limit cycle formation (v10)  
- vector field extraction  
- stability basin mapping  
- trajectory navigation  
- real-world deployment  

---

# 🧠 Final Insight

> Instability is not a threshold event.  
> It is a **structural transformation in system dynamics**.

NEXAH now shows:

→ structure  
→ flow  
→ control  
→ **dynamics**

---

# 🌀 NEXAH

> From simulation → structure  
> From structure → navigation  
> From navigation → stability  
> From stability → **dynamical systems**

---

**Author:** Thomas K. R. Hofmann  
April 2026
