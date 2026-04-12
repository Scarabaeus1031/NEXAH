# NEXAH / Power Systems
**Structural Field Navigation for Power System Stability**

This module applies NEXAH’s orientation-based approach to power system stability analysis.

The goal is to detect structural precursors of instability earlier than classical voltage-based methods and to explore **geometry-driven control of system dynamics**.

---

## 🧭 System Scope

NEXAH transforms power system analysis from:

→ static monitoring  

into:

→ **dynamic stability field navigation**

---

## ⚙️ Current System Layers (April 2026)

### 🔹 1. Detection Layer — Operational

NEXAH detects the onset of voltage collapse **~43.9 seconds earlier** than classical methods.

Based on structural indicators:
- coherence breakdown  
- geometric drift  
- state-space deformation  

| Network                  | Lead Time vs. Classical | Status     |
|--------------------------|------------------------|------------|
| IEEE 118-Bus             | ~43.9 s                | Confirmed  |
| IEEE 300-Bus             | ~43.9 s                | Confirmed  |
| IEEE 1354-Bus            | ~43.9 s                | Confirmed  |
| IEEE 9241-Bus (PEGASE)   | ~43.9 s                | Confirmed  |

---

### 🔹 2. Stability Field Layer — Operational

The system constructs a **continuous stability field**:

- manifold (expected dynamics)
- residual (structural deviation)
- distance (collapse proximity)

This enables:

- early instability detection  
- interpretable system states  
- regime separation  

---

### 🔹 3. Closed-Loop Control Layer — Functional

NEXAH now includes **closed-loop intervention**:

structure → risk → policy → action → system → structure

Capabilities:

- continuous risk field ∈ [0,1]  
- time-to-collapse estimation  
- dynamic intervention signal  

**Actions:**
- STABILIZE  
- PREEMPTIVE_STABILIZE  
- REDUCE_LOAD  
- EMERGENCY_SHED  

---

### 🔹 4. Adaptive Policy Layer (v3) — Experimental

The system has evolved into **trajectory-aware control**.

Key signals:
- risk  
- risk_slope (trajectory)  
- curvature (d2c)  
- distance (rift proximity)  

**Behavior:**

- anticipatory (not reactive)
- early intervention
- structured escalation

STABILIZE → PREEMPTIVE → REDUCE_LOAD → EMERGENCY_SHED

---

## 🧮 System Interpretation (Power Systems)

The NEXAH power system module can be interpreted as a controlled dynamical system in feature space.

The system state is defined as:

x = (coherence, frag, d2c, residual, distance)

The dynamics follow:

dx/dt = f(x) + u(x, dx/dt)

where:

- f(x) represents the underlying power grid physics  
- u(x, dx/dt) is the NEXAH intervention policy  

---

### Stability Definition

Stability is defined geometrically:

A system is stable if its trajectory remains within a region:

S = { x : risk(x) < threshold }

---

### Key Property

The system operates on:

→ trajectory-aware control  

instead of:

→ static voltage thresholds  

---

### 🔹 5. Real Grid Prototype — NEW ⚡

First integration with **pandapower-based AC solver**:

- real voltage dynamics
- physical load flow constraints
- action → system coupling

**Observed:**
- realistic system response  
- reduced artificial stability  
- control becomes physically constrained  

👉 Transition:
synthetic model → physical system interaction  

---

## 🔬 Structural Dynamics Layer (v40–v56)

A higher-level experimental layer introduces:

- OLGO shell structure (radial layering)
- hexagonal sector topology
- attractor-based dynamics
- controlled transitions (prototype)

**Key observations:**

- trajectories organize into **radial shells**
- motion constrained to **6-sector topology**
- system influenced by **boundary attractors**
- first controlled attractor transitions observed

> The system evolves from trajectory tracking  
> to **topology-driven attractor navigation**

---

## 📊 IEEE X-Ray Pipeline

Transforms high-dimensional system state into geometry:

- coherence (x)  
- switch signal (y)  
- radius (r)  
- phase (θ)  

---

## 📈 Visual Evolution

### Early Structure Discovery

![v3 detection](ieee_xray_pipeline/results/ieee57_pipeline_v3_detection.png)

---

### Polar Geometry

![v6 polar](ieee_xray_pipeline/results/ieee57_pipeline_v6_polar_morphology.png)

---

### Stability Band

![v13 band](ieee_xray_pipeline/results/ieee57_v13_band_polar.png)

---

### Root Cube Navigation

![v36 3D](ieee_xray_pipeline/results/v36b_good_final_3d.png)  
![v36 polar](ieee_xray_pipeline/results/v36b_good_final_polar.png)

---

### Attractor & Topology Layer

![v44 hexagon](ieee_xray_pipeline/results/v44_hexagon_loop_3d.png)  
![v53 attractor](ieee_xray_pipeline/results/v53_polar.png)  
![v56 topology](ieee_xray_pipeline/results/v56_hexa_topology.png)

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

## ⚠️ Current Limitations

- Full prevention of collapse ❌  
- Limited actuator realism  
- No sustained orbit / phase locking  
- Attractor dynamics still experimental  
- Requires validation vs:
  - PV curves  
  - eigenvalue analysis  
  - continuation power flow  

---

## 🔮 Next Milestones

1. Strengthen real grid coupling  
2. Multi-step prediction (lookahead)  
3. Adaptive λ control  
4. Stability basin mapping  
5. Multi-attractor navigation  
6. Scaling to large grids  

---

## 🧠 Summary

NEXAH provides a **geometry-based stability framework**:

- early detection ✔  
- structured state space ✔  
- adaptive control ✔  
- real grid prototype ✔  

but:

- full navigation ❌  
- full physical validation ❌  

remain open challenges.

---

## 🔥 Final Insight

> Instability is not only a voltage problem.  
> It is a **structural transformation in system dynamics**.

NEXAH makes this structure:

→ visible  
→ measurable  
→ partially controllable  

---

**Author:** Thomas K. R. Hofmann  
April 2026
