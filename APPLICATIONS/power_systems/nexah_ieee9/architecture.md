# 🧠 NEXAH IEEE9 — System Architecture (v9)

## 🧭 Overview

The NEXAH system is a **closed-loop stability framework** for power systems.

It transforms raw system simulation into:

```text
structure → risk → intervention → system evolution → phase dynamics
```

This creates a **dynamic stability navigation system** instead of static monitoring.

---

## ⚙️ Full Pipeline

```text
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
Adaptive Field Control (v3)
        ↓
Phase Dynamics Layer (v9)
        ↓
Closed Loop Feedback
        ↓
Updated System State
```

---

## 🔹 1. Simulation Layer

**Modules:**
- `simulation/nexah_solver_v2.py`
- `simulation/load_sweep.py`

**Role:**
- Simulates system response under load λ
- Applies intervention actions in closed loop

**Output:**
- Voltage vector `V`
- Phase angles `θ`
- Convergence flag

---

## 🔹 2. Feature Layer

**Module:**
- `features/structural_state.py`

**Extracted Features:**
- `c` → structural coherence
- `frag` → fragmentation
- `dc` → first derivative
- `d2c` → curvature (instability acceleration)

---

## 🔹 3. Manifold Layer

**Module:**
- `overlay/manifold_fit.py`

**Model:**

```text
log(d2c) = log(a) + p log(c) + q log(|dc|)
```

**Purpose:**
- Defines expected system behavior
- Establishes structural baseline

---

## 🔹 4. Overlay Field

**Module:**
- `overlay/residual_distance.py`

**Components:**
- `residual` → deviation from manifold
- `distance` → proximity to collapse boundary (rift)

**Interpretation:**
- Low residual → stable structure
- High residual → instability
- Distance encodes geometric collapse proximity

---

## 🔹 5. Clustering Layer

**Method:**
- KMeans on `(distance, residual)`

**Output:**
- Stable region
- Transition region
- Collapse region

---

## 🔹 6. Predictor Layer

**Module:**
- `analysis/predictor.py`

**Outputs:**
- `risk ∈ [0,1]`
- `warnings`
- `time-to-collapse (ttc)`

**Mechanism:**
Combines:
- geometry (distance)
- dynamics (`d2c`)
- regime structure

---

## 🔹 7. Policy Layer (Base Control)

**Module:**
- `decision/intervention_policy.py`

**Outputs:**
- continuous control signal
- discrete actions:
  - STABILIZE
  - PREEMPTIVE_STABILIZE
  - REDUCE_LOAD
  - EMERGENCY_SHED

---

## 🔹 8. Adaptive Field Control (v3) 🔥

**Module:**
- `decision/adaptive_policy_v3.py`

**Inputs:**
- `risk`
- `risk_slope`
- `d2c`
- `distance`
- `state_history`

---

### 🧠 Control Logic

The controller integrates:

1. **Trajectory Awareness**
   - reacts to direction of risk evolution

2. **Structural Awareness**
   - detects instability acceleration

3. **Geometric Awareness**
   - anticipates collapse via distance-to-rift

4. **Memory**
   - escalation based on persistence

---

### 🔄 Policy Evolution

| Version | Behavior |
|--------|--------|
| v1 | reactive |
| v2 | recovery + memory |
| v3 | **pre-emptive field control** |

---

## 🔹 9. Phase Dynamics Layer (v9) 🌀

**New Core Layer**

Introduces a **true dynamical system representation**.

**State Variables:**
- `λ` → load / stress parameter
- `ψ` → internal phase state

---

### 🧠 Dynamics

The system evolves as:

```text
(λ, ψ) → trajectory in phase space
```

**Observed Behavior:**
- Stable attractor formation
- Convergence to fixed point
- Phase coupling between control + system

---

### 🔬 Interpretation

This layer transforms NEXAH from:

- scalar control system

into:

- **2D dynamical phase system**

---

## 🔹 10. Closed Loop Control

```text
action → solver → new system → new features → new action
```

**Key property:**
- Control reshapes system trajectory
- Feedback modifies collapse geometry

---

## ⚡ System Behavior (v9)

The system now operates as:

- structure-aware  
- trajectory-aware  
- geometry-aware  
- **phase-aware**

---

## 🧭 Interpretation within NEXAH Framework

Two coupled systems now exist:

### 1. Application Layer (Power System)
- Risk field
- Collapse dynamics
- Adaptive control

### 2. NEXAH Core Layer
- Field geometry
- Phase dynamics (λ, ψ)
- Trajectory shaping

---

## 🔬 Conceptual Transition

The controller is no longer:

a regulator

It is becoming:

a **field-driven dynamical navigator**

---

## ⚠️ Current Limitations

- Solver is still partially synthetic
- Control not yet fully mapped to physical grid actions

---

## 🔮 Next Steps

- Integrate real AC power flow (pandapower)
- Map actions to physical interventions
- Identify stability basins
- Extract vector fields
- Enable trajectory navigation
- Establish limit cycles (v10)

---

## 🔥 Final Insight

Control is no longer applied *to* the system.

It emerges *from*:

**the geometry and dynamics of the field itself**

---

## 🧭 Summary

NEXAH integrates:

- structure (manifold)
- dynamics (risk + curvature)
- geometry (distance field)
- phase space (λ, ψ)
- control (adaptive policy)

into a unified system capable of:

→ **navigating stability in complex dynamical systems**## 🔹 3. Manifold Layer

**Module:**
- `overlay/manifold_fit.py`

**Model:**

```text
log(d2c) = log(a) + p log(c) + q log(|dc|)
```

**Purpose:**
- Define expected system behavior
- Establish structural baseline

---

## 🔹 4. Overlay Field

**Module:**
- `overlay/residual_distance.py`

**Components:**
- `residual` → deviation from manifold
- `distance` → proximity to collapse region (rift)

**Interpretation:**
- Low residual → stable structure
- High residual → instability
- High distance → approach to collapse boundary

---

## 🔹 5. Clustering Layer

**Method:**
- KMeans on `(distance, residual)`

**Output:**
- Structural regimes:
  - Stable region
  - Transition band
  - Collapse region

---

## 🔹 6. Predictor Layer

**Module:**
- `analysis/predictor.py`

**Outputs:**
- `risk ∈ [0,1]`
- `warnings (bool)`
- `time-to-collapse (ttc)`

**Mechanism:**
Combines:
- distance (geometry)
- curvature (`d2c`)
- cluster structure

---

## 🔹 7. Policy Layer (Base Control)

**Module:**
- `decision/intervention_policy.py`

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

---

## 🔹 8. Adaptive Field Control (v3) 🔥

**Module:**
- `decision/adaptive_policy_v3.py`

**New Inputs:**
- `risk_slope` → trajectory direction
- `d2c` → instability curvature
- `distance` → proximity to collapse manifold
- `state_history` → memory / persistence

---

### 🧠 Control Logic

The system now integrates:

1. **Trajectory Awareness**
   - reacts to rising risk (not just level)

2. **Structural Awareness**
   - detects instability acceleration (curvature)

3. **Geometric Awareness**
   - anticipates collapse via distance-to-rift

4. **Memory-Based Escalation**
   - persistent instability triggers stronger control

---

### 🔄 Control Transition

| Layer | Behavior |
|------|--------|
| Policy v1 | reactive |
| Policy v2 | recovery + memory |
| Policy v3 | **pre-emptive field control** |

---

## 🔹 9. Closed Loop Control

```text
action → solver → new system → new features → new action
```

**Key property:**
- Intervention modifies system trajectory
- Feedback reshapes collapse dynamics

---

## ⚡ System Behavior (v3)

The system now operates as:

- **structure-aware**
- **trajectory-aware**
- **anticipatory**

instead of:

- state-triggered
- reactive

---

## 🔬 Interpretation

NEXAH is no longer a monitoring system.

It is a:

**field-driven control architecture for dynamic stability navigation**

---

## ⚠️ Current Limitation

- Solver is still synthetic (not physical AC power flow)
- Control acts on abstract system, not real grid equations

---

## 🔮 Next Step (Critical)

- Replace solver with real AC power flow (pandapower)
- Enable physical intervention (load / generation control)

---

## 🧭 Summary

NEXAH integrates:

- structure (manifold)
- dynamics (risk + slope)
- geometry (distance field)
- control (adaptive policy)

into a unified system capable of:

→ **navigating stability in complex dynamical systems**
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

