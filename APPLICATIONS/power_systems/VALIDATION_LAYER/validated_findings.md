# ⚡ NEXAH — Validated Findings
### (Unified Results from Skeleton + Experiments)

---

# 🧭 Purpose

This document summarizes the validated insights of the NEXAH validation layer.

It integrates:

- core validation (`validation_skeleton.py`)  
- experimental extensions (`run_001 → run_019`)  
- synthetic and IEEE-based analysis  

---

# 🧱 PART A — Core Validation Findings (Skeleton)

---

## A1. Structural Detection Exists

```text
Curvature-based signals detect deviations
before classical threshold-based methods.
```

---

## A2. Events are Structured Objects

```text
Instability appears as a sequence of curvature events,
not as a single scalar signal.
```

---

## A3. Event Shapes Exist

```text
Each event can be represented as a normalized shape.
```

---

## A4. Shape Space Structure

```text
Shapes form clusters and trajectories in a low-dimensional space.
```

---

## 🔥 Core Insight (Skeleton)

```text
NEXAH detects structural changes in trajectories,
not just threshold crossings.
```

---

# 🧪 PART B — Motion & Shape Dynamics

---

## B1. Instability is a Geometric Process

```text
Instability = deformation of trajectory geometry
```

---

## B2. Motion in Shape Space

```text
Events move through shape space → forming trajectories
```

---

## B3. Motion Metrics

- angle → early directional change  
- speed → magnitude of motion  

---

## B4. Stable vs Pre-Collapse Behavior

| Regime        | Behavior              |
|--------------|----------------------|
| stable       | bounded motion       |
| pre-collapse | drift + deformation  |
| collapse     | escape trajectory    |

---

## 🔁 Transition Model

```text
stable motion
→ geometric drift
→ directional escape
→ collapse
```

---

# 🧪 PART C — Signal-Level Findings (CRITICAL)

---

## C1. No Single Signal is Sufficient

```text
κ(t)       → local event detection
angle(t)   → directional sensitivity
drift(t)   → global motion
```

---

## C2. Early Warning is Limited

- curvature → no global lead  
- drift → small lead (~2 steps)  
- angle → very early but noisy  

---

## 🔥 Signal Insight

```text
Signals capture different layers of instability,
but none alone defines it.
```

---

# 🧪 PART D — State Space & Structural Findings (NEW CORE)

---

## D1. Trajectories Form a Structured State Space

Using reconstruction:

```text
x(t) = (V, dV/dt, d²V/dt²)
```

Observed:

- trajectories are continuous curves  
- system evolves along a structured path  
- collapse follows this path  

---

## D2. Transition Region Exists

```text
A distinct transition phase occurs before collapse.
```

Detected consistently at:

```text
t_transition ≈ 23.85
t_collapse   ≈ 25.05
```

---

## D3. Transition is Invariant (CRITICAL RESULT)

Across multiple runs:

- identical transition time  
- identical region in state space  
- independent of perturbations  

---

### 🔥 Key Finding

```text
The transition is invariant across trajectories.
```

---

## D4. Instability is a Region, not a Point

```text
Instability is not triggered at a moment.

It occurs when the trajectory enters
a specific region in state space.
```

---

## D5. Collapse is a Consequence

```text
Transition → collapse

NOT

collapse → transition
```

---

# 🧠 Unified Interpretation

---

## Old View

```text
instability = threshold crossing
```

---

## NEXAH View

```text
instability = trajectory entering
a geometric transition region
```

---

## Final Model

```text
signal
→ event
→ shape
→ geometry
→ motion
→ transition region
→ collapse
```

---

# ⚠️ Limitations

- curvature sensitive to noise  
- PCA is reduced representation  
- limited system set (IEEE14)  
- synthetic scenarios dominate  
- no control/action layer yet  

---

# 🚀 Implications

NEXAH enables:

- detection of transition regions  
- trajectory-based monitoring  
- structural interpretation of instability  

---

# 🧭 Final Statement

```text
Power system instability is not a sudden event.

It is the result of a trajectory entering
an invariant geometric transition region
in reconstructed state space,
which consistently precedes collapse.
```

---

# 🔗 References

- `scripts/validation_skeleton.py`  
- `experiments/run_001 → run_019`  
- `outputs/`  
- `reports/`  

---

# ⚡ NEXAH

```text
instability is not a point

it is a movement through structure
```
