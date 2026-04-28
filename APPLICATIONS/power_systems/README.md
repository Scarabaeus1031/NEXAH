# ⚡ NEXAH / Power Systems  
**Structural Field Analysis for Power System Stability and Regime Navigation**

---

## 🧭 Overview

NEXAH introduces a **geometry-based framework for analyzing power system stability**.

Instead of treating instability as a threshold violation, NEXAH models the system as a:

> **trajectory evolving within a structured dynamical field**

This enables:

- early detection of regime transitions  
- continuous stability assessment  
- trajectory-aware analysis  
- geometric interpretation of system dynamics  

---

## ⚙️ Technical Context

- **Simulation:** AC power flow / dynamic voltage simulations (pandapower-based)  
- **Input signals:** voltage magnitude, derived temporal features  
- **Feature space:**  
  - coherence (c)  
  - drift (dv/dt)  
  - acceleration (d²v/dt²)  
  - residual structure  
  - geometric distance metrics  
  - phase variable (ψ)  

- **Dimensionality reduction:** custom low-dimensional embedding  
- **Output representation:**
  - geometric state space  
  - flow field (vector field)  
  - risk landscape  

---

## 🚀 Core Idea

Classical stability analysis focuses on:

→ scalar indicators (e.g. voltage thresholds)

NEXAH shifts the focus to:

→ **structure, flow, and geometry of system dynamics**

---

## 🔁 System Pipeline

```text
Simulation
    ↓
Feature Extraction
    ↓
Low-Dimensional State Embedding
    ↓
Flow Field Reconstruction
    ↓
Risk Mapping
    ↓
Trajectory Analysis / Control Experiments
```

---

## 🧠 Conceptual Paradigm

**Classical methods:**
- monitor voltage thresholds  
- detect instability after it manifests  

**NEXAH:**
- reconstructs the **underlying dynamical structure**  
- interprets instability as a **regime transition**  
- analyzes trajectories within a **stability landscape**

---

# 📊 Structural Observations

---

## 🔹 Collapse Geometry

![Collapse Geometry](stability_field_dynamics/ieee_test_cases/outputs/ieee14_v52_residual_vs_distance.png)

**Observation:**
- system states organize into structured regions  
- collapse appears as a boundary between regions  

**Interpretation:**

> Stability corresponds to **geometric proximity within state space**

---

## 🔹 Flow Field (Dynamics)

![Flow Field](stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

**Observation:**
- trajectories follow structured directions  
- system evolution exhibits coherent flow  

**Interpretation:**

> The system behaves as a **vector field**, not as independent state updates

---

## 🔹 Geometric State Space

![Root Cube](ieee_xray_pipeline/results/v36b_good_final_3d.png)

**Observation:**
- high-dimensional dynamics can be embedded into structured geometry  

**Interpretation:**

> Stability becomes analyzable via **geometry instead of raw signals**

---

## 🔹 Control Interaction (Experimental)

![Control](nexah_ieee9/results/controller_v9/output_v9_plot.png)

**Observation:**
- control modifies trajectory evolution  
- stabilization occurs without suppressing dynamics  

**Interpretation:**

> Control acts via **trajectory shaping in the field**

---

## 🔹 Phase Dynamics

![Phase Lambda Psi](nexah_ieee9/results/controller_v9/output_v9_phase_lambda_psi.png)

**Observation:**
- structured trajectories appear in phase space  
- attractor-like behavior emerges  

---

## 🔹 Risk–Distance Field

![Risk Distance](nexah_ieee9/results/controller_v9/output_v9_phase_risk_distance.png)

**Observation:**
- risk correlates with geometric structure  

**Interpretation:**

> Risk is a **projection of system geometry**

---

## 🔹 Trajectory-Based Stabilization

![Navigation](nexah_ieee9/results/visuals/nexah_navigation_v11.gif)

**Observation:**
- trajectories are redirected near critical regions  
- collapse can be avoided in controlled scenarios  

---

## 🔹 Scaling Behavior

![IEEE9241](nexah_ieeeX/results/run_ieee9241_20260413_021422/plot.png)

**Observation:**
- structural patterns persist across system sizes  

**Interpretation:**

> The framework shows **scalability across IEEE test systems**

---

# 🔬 Regime Detection

A signal-based detection layer is defined using:

- drift (dv/dt)  
- acceleration (d²v/dt²)  
- hybrid change score  
- adaptive thresholds  

---

## Key Observations

| Scenario           | Lead Time |
|------------------|----------|
| smooth decay     | high (20–35) |
| accelerated      | moderate |
| noisy systems    | moderate |
| sharp collapse   | low |

---

## Interpretation

> Instability is better described as a **transition between regimes**,  
> not a single event.

---

# 🧠 System View

The system can be modeled as:

> a trajectory evolving within a structured dynamical landscape

where:

- structure defines possible regimes  
- dynamics govern transitions  
- analysis identifies regime changes  

---

# 🧮 Mathematical View

State vector:

```text
x = (c, drift, acceleration, residual, distance, ψ)
```

Dynamics:

```text
dx/dt = f(x)
```

NEXAH focuses on:

- trajectory structure  
- geometric organization  
- regime transitions  

---

# ⚖️ Classical vs NEXAH

| Feature                | Classical IEEE | NEXAH |
|----------------------|---------------|------|
| Static thresholds     | Yes           | Yes |
| Dynamic analysis      | Limited       | Yes |
| Regime detection      | No            | Yes |
| Structural modeling   | No            | Yes |
| Phase interpretation  | No            | Yes |
| Predictive capability | Limited       | Case-dependent |

---

# ⚠️ Limitations

- early-warning performance depends on scenario  
- parameter sensitivity not fully explored  
- limited validation on real-world datasets  
- no probabilistic confidence model yet  

> This framework is currently **experimental** and focuses on  
> structural insight and early-stage validation,  
> not yet on guaranteed stability control.

---

# 🔮 Next Steps

- validation on real grid data  
- sensitivity analysis  
- probabilistic regime detection  
- comparison with classical stability methods  

---

# 🌀 NEXAH Principle

```text
simulation → structure → flow → geometry → dynamics → regimes
```

---

**Author:** Thomas K. R. Hofmann  
April 2026
