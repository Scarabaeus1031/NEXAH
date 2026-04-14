# 🧠 NEXAH IEEE9 — System Architecture (v11)

## 🧭 Overview

The NEXAH system is a **field-driven closed-loop stability framework** for power systems.

It transforms system behavior into a navigable structure:

```text
simulation → field → geometry → navigation → system evolution
```

This enables:

> **stability navigation instead of reactive control**

---

## ⚙️ Full Pipeline

```text
Power Flow Solver
        ↓
Feature Extraction
        ↓
Risk Field Construction
        ↓
Field Geometry (∂risk, ∂²risk)
        ↓
Critical Region Detection
        ↓
Navigation Target Selection
        ↓
Navigation Controller (v11_2)
        ↓
Closed Loop System Evolution
```

---

## 🔹 1. Simulation Layer

**Module:**
- `simulation/powerflow_solver_real_v3.py`

**Role:**
- Computes system response for given λ
- Represents physical grid behavior

**Outputs:**
- `vmin` → voltage stability indicator  
- `line_loading` → system stress  
- `converged` → feasibility  

---

## 🔹 2. Feature Layer

**Extracted:**
- Voltage stability (`vmin`)
- Line loading (`loading`)

---

## 🔹 3. Risk Field

**Definition:**

```text
risk(λ) = max(0, 0.97 - vmin) + max(0, (loading - 80)/100)
```

**Interpretation:**
- Encodes proximity to instability
- Combines voltage + thermal stress
- Defines a continuous stability field

---

## 🔹 4. Field Geometry

Derived quantities:

```text
∂risk/∂λ   → slope (trajectory direction)
∂²risk/∂λ² → curvature (instability acceleration)
```

**Meaning:**
- Slope → how fast instability grows  
- Curvature → onset of nonlinear behavior  

---

## 🔹 5. Stability Field Structure

Two key regimes emerge:

### 🟡 Structural Transition (~λ ≈ 0.8)
- First curvature appears  
- Field begins to deform  
- System remains stable  

---

### 🔴 Instability Region (~λ ≈ 1.25+)
- Rapid nonlinear risk growth  
- Strong amplification  
- System approaches collapse boundary  

---

## 🔹 6. Critical Region Detection (v11_1)

**Method:**
- Detect first significant curvature increase  
- Identify transition into nonlinear regime  

**Output:**

```text
λ_critical ≈ 0.79
```

---

## 🔹 7. Navigation Target

Controller defines a safe operating point:

```text
λ_target = λ_critical - Δ
```

→ ensures operation near, but not inside instability region

---

## 🔹 8. Navigation Controller (v11_2) 🧭

**Core Principle:**

```text
dλ ∝ (λ_target - λ)
```

**Behavior:**
- Smooth convergence toward target  
- Adaptive step size  
- No oscillation  
- No overshoot  

---

### 📈 Observed Dynamics

- Stable trajectory  
- Continuous movement  
- No collapse interaction  

Example:

```text
λ=0.600 → 0.7717 (safe boundary approach)
```

---

## 🔹 9. Closed Loop System

```text
λ → solver → field → target → controller → λ_next
```

**Key Property:**
- System follows field geometry  
- Control emerges from structure  

---

## ⚡ System Behavior (v11)

The system is now:

- field-aware  
- geometry-aware  
- predictive  
- **navigation-driven**

---

## 🔬 Conceptual Transition

```text
State Control → Field Navigation
```

Control is no longer:

- reactive (based on state error)

but:

- predictive (based on field geometry)

---

## 🧠 System Interpretation

The system operates as:

> a trajectory evolving within a structured stability field

where:

- field = extracted from system physics  
- geometry = defines stability structure  
- navigation = movement along safe trajectories  

---

## 🔥 Key Result

A power system can be:

- mapped into a stability field  
- structurally analyzed  
- safely navigated near its limits  

---

## ⚡ Implication

- operation near stability boundary  
- maximum safe utilization  
- avoidance of collapse  

---

## 🔮 Next Steps

- Real-time field estimation (online NEXAH)  
- Adaptive safety margins  
- Multi-agent field navigation  
- Extension to multi-dimensional systems  
- Integration with real grid data  

---

## 🧭 Summary

NEXAH integrates:

- physics (power flow)
- field extraction (risk)
- geometry (curvature + slope)
- navigation (target-based control)

into a unified system capable of:

→ **navigating stability in complex dynamical systems**

---

## 📌 Note

Legacy architecture (v7–v9), including:
- manifold learning  
- residual fields  
- clustering  
- phase dynamics  

is documented separately and represents the **development path toward field-based navigation**.
