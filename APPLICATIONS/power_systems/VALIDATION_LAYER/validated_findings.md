# ⚡ NEXAH — Validated Findings
### (Unified Results from Skeleton + Experiments)

---

# 🧭 Purpose

This document summarizes the validated insights of the NEXAH validation layer.

It integrates:

- core validation (`validation_skeleton.py`)  
- experimental extensions (`run_001 → run_009`)  
- IEEE system validation  

---

# 🧱 PART A — Core Validation Findings (Skeleton)

These findings are directly reproducible from:

```text
validation_skeleton.py
```

---

## A1. Structural Detection Exists

```text
Curvature-based signals detect deviations
before classical threshold-based methods.
```

### Evidence

- smooth → strong early detection  
- nonlinear → slight early detection  
- noisy → degraded performance  

---

## A2. Events are Structured Objects

```text
Instability does not appear as a single signal,
but as a sequence of curvature events.
```

---

## A3. Event Shapes Exist

Each event can be represented as:

```text
normalized curvature profile over time
```

---

## A4. Shape Distributions Differ by Regime

| Scenario   | Behavior |
|------------|----------|
| smooth     | multiple shapes |
| nonlinear  | single dominant shape |
| noisy      | fragmented shapes |

---

## A5. Alignment Metric Separates Regimes

```text
alignment = deviation from mean shape
```

### Interpretation

- low → coherent structure  
- medium → mixed dynamics  
- high → noise  

---

## A6. Classification Emerges from Geometry

```text
STRUCTURAL / AMBIGUOUS / NOISE
```

→ derived from:

- alignment  
- number of events  

---

## 🔥 Core Insight (Skeleton)

```text
NEXAH detects structural changes in system trajectories,
not just threshold crossings.
```

---

# 🧪 PART B — Extended Experimental Findings

These findings extend the skeleton into a full structural interpretation.

---

## B1. Early Warning Exists (Verified)

```text
NEXAH detects instability significantly earlier than classical methods.
```

### Evidence (IEEE14 Collapse Sweep)

- collapse: ~60–75  
- warning: ~20–25  

```text
Lead time: ~40–50 time units
```

---

## B2. Instability is a Geometric Process

```text
Instability is not a threshold,
but a deformation in trajectory geometry.
```

---

## B3. Shape Space Exists

```text
event shapes form a geometric space
```

Using:

- resampling  
- PCA embedding  

---

## B4. Motion in Shape Space

```text
events are not isolated
they move through shape space
```

Observed:

- ordered trajectories (nonlinear)  
- fragmented clouds (noise)  
- multi-path transitions (smooth)  

---

## B5. Stable vs Pre-Collapse Motion

### Stable regime

- loop structures  
- cyclic motion  
- bounded trajectories  

### Pre-collapse regime

- deformation of loops  
- directional drift  
- escape from stable region  

---

## B6. Motion Metrics Detect Instability

Two key quantities:

### Speed

```text
magnitude of movement in shape space
```

### Angle

```text
change of direction between steps
```

---

### Observed Behavior

- angle spikes → early warning signal  
- speed spikes → later confirmation  
- both occur before collapse  

---

## B7. Statistical Validation

From repeated runs:

- detection rate: ~86% (43 / 50)  
- mean lead time: ~11.6 (synthetic baseline)  

---

## B8. IEEE System Validation

Observed:

- structured trajectories even without collapse  
- persistent motion patterns in stable regime  
- clear transition behavior under stress  

---

### Key Observation

```text
NEXAH produces warnings even when
no classical collapse is detected.
```

---

## B9. Collapse Dynamics (IEEE Sweep)

At increasing load:

- no collapse → structured motion persists  
- collapse onset → strong geometric drift  
- post-threshold → rapid trajectory escape  

---

### Critical Result

```text
geometric drift consistently precedes voltage collapse
```

---

# 🧠 Unified Interpretation

```text
NEXAH does not detect collapse.

It reconstructs how instability emerges
as motion through a geometric structure.
```

---

# 🔁 Final Model

Before:

```text
stable → threshold → collapse
```

Now:

```text
stable motion
→ geometric drift
→ directional escape
→ collapse
```

---

# ⚠️ Limitations

- curvature sensitive to noise  
- single IEEE system (IEEE14)  
- no persistence filtering yet  
- PCA is a reduced representation  

---

# 🚀 Implications

NEXAH enables:

- early warning systems  
- trajectory-based monitoring  
- structural interpretation of dynamics  

---

# 🧭 Final Statement

```text
Power system instability appears as geometric drift
in reconstructed state space,
well before observable collapse occurs.
```

---

# 🔗 References

- `scripts/validation_skeleton.py`  
- `experiments/run_001 → run_009`  
- `reports/validation_report_v1.md`  
- `reports/validation_report_v2.md`  
