# 🧠 NEXAH IEEE9 — System Architecture

## 🧭 Overview

The NEXAH system is a **closed-loop stability framework** for power systems.

It transforms raw system simulation into:

```text
structure → risk → intervention → system evolution
```
This creates a dynamic stability navigation system instead of static monitoring.

⸻

## ⚙️ Full Pipeline

Load Sweep / Solver
        ↓
Feature Extraction
        ↓
Manifold Learning
        ↓
Residual + Distance Field
        ↓
Clustering (Regimes)
        ↓
Risk Prediction
        ↓
Intervention Policy
        ↓
Closed Loop Feedback
        ↓
Updated System State
``
---

## 🔹 1. Simulation Layer

**Module:**
simulation/nexah_solver_v2.py

**Role:**
- Simulates system response under load λ
- Applies intervention actions (feedback)

**Output:**
- Voltage vector V
- Phase angles θ
- Convergence flag


## 🔹 2. Feature Layer

**Module:**
features/structural_state.py

**Extracted Features:**
- c → structural coherence
- frag → fragmentation
- dc → first derivative
- d2c → second derivative (curvature)


## 🔹 3. Manifold Layer

**Module:**
overlay/manifold_fit.py

**Model:**
log(d2c) = log(a) + p log(c) + q log(|dc|)

**Purpose:**
- Define expected system behavior
- Establish structural baseline


## 🔹 4. Overlay Field

**Modules:**
overlay/residual_distance.py

**Components:**
- Residual → deviation from manifold
- Distance → proximity to collapse region (rift)

**Interpretation:**
- Low residual → stable structure
- High residual → instability / deviation


## 🔹 5. Clustering Layer

**Method:**
- KMeans on (distance, residual)

**Output:**
- System regimes:
  - Stable region
  - Transition zone
  - Collapse region


## 🔹 6. Predictor Layer

**Module:**
analysis/predictor.py

**Outputs:**
- risk ∈ [0,1]
- warnings (bool)
- time-to-collapse (ttc)

**Mechanism:**
- Combines:
  - distance
  - curvature (d2c)
  - cluster deviation


## 🔹 7. Policy Layer

**Module:**
decision/intervention_policy.py

**Inputs:**
- risk
- slope (drift)
- TTC urgency
- system state

**Outputs:**
- continuous control signal
- discrete actions:
  - STABILIZE
  - PREEMPTIVE_STABILIZE
  - REDUCE_LOAD
  - EMERGENCY_SHED


## 🔹 8. Closed Loop Control

action → solver → new system → new features → new action

**Key property:**
- Intervention changes system trajectory
- Feedback modifies collapse dynamics

