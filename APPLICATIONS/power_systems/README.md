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

The following figures illustrate the transition from:

→ structure  
→ flow  
→ control  
→ dynamics  

---

## 🔹 Figure 1 — Collapse Geometry (Fundamental Structure)

![Collapse Geometry](stability_field_dynamics/ieee_test_cases/outputs/ieee14_v52_residual_vs_distance.png)

**Observation:**

- system states organize into structured regions  
- collapse emerges as a boundary (rift)  

**Interpretation:**

> Stability is not binary — it is **geometric proximity to a boundary**

---

## 🔹 Figure 2 — Flow Field Dynamics (Underlying Physics)

![Flow Field](stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

**Builds on Figure 1:**

Once structure is identified, we observe:

- trajectories are not random  
- motion follows directional flows  

**Interpretation:**

> The system evolves within a **continuous vector field**

---

## 🔹 Figure 3 — Geometric State Space (Navigation Layer)

![Root Cube](ieee_xray_pipeline/results/v36b_good_final_3d.png)

**Builds on Figure 2:**

The flow field can be embedded into a low-dimensional space:

- complex dynamics collapse into geometric structure  
- trajectories become navigable  

**Interpretation:**

> Stability becomes a **navigation problem in state space**

---

## 🔹 Figure 4 — Closed-Loop Adaptive Control (IEEE9)

![Control](nexah_ieee9/results/controller_v9/output_v9_plot.png)

**Builds on Figure 3:**

Navigation enables intervention:

- control modifies trajectory instead of state  
- system stabilizes without suppressing dynamics  

**Interpretation:**

> Control acts on **trajectory evolution**, not thresholds  

---

## 🔹 Figure 5 — Phase Dynamics (NEW v9)

![Phase Lambda Psi](nexah_ieee9/results/controller_v9/output_v9_phase_lambda_psi.png)

**Builds on Figure 4:**

Control + system interaction forms a dynamical system:

- trajectories evolve in phase space (λ, ψ)  
- convergence toward attractor  

**Interpretation:**

> Stability emerges as a **dynamical attractor**

---

## 🔹 Figure 6 — Risk–Distance Field

![Risk Distance](nexah_ieee9/results/controller_v9/output_v9_phase_risk_distance.png)

**Builds on Figure 5:**

Risk is not arbitrary:

- it is encoded in system geometry  
- aligned with phase evolution  

**Interpretation:**

> Risk is a **projection of field geometry**

---

## 🔹 Figure 7 — Real-Scale Validation (9241-Bus PEGASE)

![IEEE9241](nexah_ieeeX/results/run_ieee9241_20260413_021422/plot.png)

**Final validation:**

- same structure persists at scale  
- early warning remains intact  
- control remains effective  

**Interpretation:**

> NEXAH generalizes from toy systems to **real-world grids**

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
