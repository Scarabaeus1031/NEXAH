# ⚡ NEXAH / Power Systems  
**Structural Field Analysis for Power System Stability and Regime Navigation**

---

## 🧭 Overview

NEXAH introduces a **geometry-based framework for analyzing power system stability**.

Rather than treating instability as a threshold violation, NEXAH interprets it as:

> a **structural transition in the system’s dynamical behavior**

This perspective enables:

- early detection of regime transitions  
- continuous stability assessment  
- trajectory-aware analysis  
- phase-space interpretation of system evolution  

---

## 🚀 Core Idea

Classical stability analysis focuses on:

→ scalar indicators (e.g. voltage magnitude)

NEXAH shifts the focus to:

→ **structure, flow, and geometry of system dynamics**

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

# 📊 System Insights

The following figures illustrate how stability emerges from structure and dynamics.

---

## 🔹 Figure 1 — Collapse Geometry

![Collapse Geometry](stability_field_dynamics/ieee_test_cases/outputs/ieee14_v52_residual_vs_distance.png)

**Observation:**
- system states organize into structured regions  
- collapse appears as a boundary between regions  

**Interpretation:**

> Stability can be interpreted as **geometric proximity within state space**

---

## 🔹 Figure 2 — Flow Field (Dynamics)

![Flow Field](stability_field_dynamics/ieee_test_cases/outputs/ieee118_v69_off_manifold_flow.png)

**Observation:**
- trajectories exhibit directional organization  
- system evolution is not random, but structured  

**Interpretation:**

> The system behaves like a **vector field**,  
> where stability corresponds to coherent flow.

---

## 🔹 Figure 3 — Geometric State Space

![Root Cube](ieee_xray_pipeline/results/v36b_good_final_3d.png)

**Observation:**
- high-dimensional dynamics can be mapped to geometric structures  

**Interpretation:**

> Stability becomes analyzable via **geometry rather than raw signals**

---

## 🔹 Figure 4 — Control Interaction

![Control](nexah_ieee9/results/controller_v9/output_v9_plot.png)

**Observation:**
- control modifies trajectory evolution  
- system stabilizes without suppressing dynamics  

**Interpretation:**

> Control acts on **trajectory shaping**, not only on state correction.

---

## 🔹 Figure 5 — Phase Dynamics

![Phase Lambda Psi](nexah_ieee9/results/controller_v9/output_v9_phase_lambda_psi.png)

**Observation:**
- structured trajectories appear in phase space  
- attractor-like behavior emerges  

**Interpretation:**

> Stability is a **dynamical structure**, not a static condition.

---

## 🔹 Figure 6 — Risk–Distance Field

![Risk Distance](nexah_ieee9/results/controller_v9/output_v9_phase_risk_distance.png)

**Observation:**
- risk correlates with geometric structure  

**Interpretation:**

> Risk can be viewed as a **projection of system geometry**

---

## 🔹 Figure 7 — Trajectory-Based Stabilization

![Navigation](nexah_ieee9/results/visuals/nexah_navigation_v11.gif)

**Observation:**
- trajectories are redirected near critical regions  
- collapse is avoided in this scenario  

**Interpretation:**

> Stabilization can be achieved by **guiding trajectories within the field**

---

## 🔹 Figure 8 — Scaling Behavior

![IEEE9241](nexah_ieeeX/results/run_ieee9241_20260413_021422/plot.png)

**Observation:**
- structural patterns persist across system sizes  

**Interpretation:**

> The framework shows **potential scalability**,  
> though further validation is required.

---

# 🔬 Regime Detection

A signal-based regime detection layer was introduced using:

- drift (dv/dt)  
- acceleration (d²v/dt²)  
- hybrid change score  
- adaptive thresholds  

---

## Key Observations

- regime transitions can be detected before collapse  
- lead time depends on system behavior  

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

The system can be interpreted as:

> a trajectory evolving within a structured dynamical landscape

where:

- structure defines possible regimes  
- dynamics govern transitions  
- analysis identifies regime changes  

---

# 🧮 Mathematical View

State vector:

x = (c, drift, acceleration, residual, distance, ψ)

Dynamics:

dx/dt = f(x)

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

---

# 🔮 Next Steps

- validation on real grid data  
- sensitivity analysis  
- probabilistic regime detection  
- comparison with existing early-warning indicators  

---

# 🧠 Final Insight

> Instability is not reliably captured by a single threshold.

It is better understood as:

→ a **transition between dynamical regimes**

---

# 🌀 NEXAH Principle

simulation → structure → flow → geometry → dynamics → regimes

---

**Author:** Thomas K. R. Hofmann  
April 2026
