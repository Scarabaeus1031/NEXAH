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

# 🎯 Core Claim (CRITICAL)

```text
For voltage-driven instability scenarios (IEEE14),
a curvature-based trajectory signal detects structural deviations
earlier than classical dv/dt-based indicators,
with observed lead times up to ~40–50 time units.
```

---

# ⚖️ Benchmark Definition

**Classical baseline:**

```text
t_classical = first sustained threshold crossing of dv/dt
```

**NEXAH detection:**

```text
t_nexah = first sustained increase in curvature κ(t)
```

**Evaluation metric:**

```text
Lead Time = t_collapse - t_detection
```

---

# 🧱 PART A — Core Validation Findings (Skeleton)

Reproducible via:

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
Instability manifests as a sequence of curvature events,
not as a single signal spike.
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

Derived from:

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

---

## B1. Early Warning Exists (Verified)

```text
NEXAH detects instability earlier than dv/dt-based indicators
in controlled IEEE collapse scenarios.
```

### Evidence (IEEE14 Collapse Sweep)

- collapse: ~60–75  
- warning: ~20–25  

```text
Observed lead time: ~40–50 time units
```

---

## B2. Instability is a Geometric Process

```text
Instability corresponds to deformation in trajectory geometry,
not a scalar threshold event.
```

---

## B3. Shape Space Exists

```text
Event shapes form a geometric space.
```

Using:

- resampling  
- PCA embedding  

---

## B4. Motion in Shape Space

```text
Events evolve as trajectories in shape space.
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

- loop deformation  
- directional drift  
- escape behavior  

---

## B6. Motion Metrics Detect Instability

### Speed

```text
magnitude of movement in shape space
```

### Angle

```text
directional change between steps
```

---

### Observed Behavior

- angle spikes → early warning  
- speed spikes → later confirmation  

---

## B7. Statistical Validation

- detection rate: 43 / 50 (~86%)  
- mean lead time: ~11.6 (synthetic baseline)  

---

## B8. IEEE System Validation

Observed:

- structured trajectories without collapse  
- persistent motion patterns in stable regime  
- consistent transition behavior under stress  

---

## B9. Collapse Dynamics (IEEE Sweep)

Observed progression:

```text
stable motion
→ geometric drift
→ directional escape
→ collapse
```

---

## 🔥 Critical Result

```text
Geometric drift consistently precedes voltage collapse.
```

---

# ❗ Failure Modes (IMPORTANT)

NEXAH shows limitations under certain conditions:

### Noise Sensitivity

```text
High noise levels produce spurious curvature spikes,
reducing detection reliability.
```

### Lack of Persistence Filtering

```text
Single spikes may not represent true structural transitions.
```

### Reduced Representation

```text
PCA projection may obscure higher-dimensional structure.
```

---

# 🧠 Unified Interpretation

```text
NEXAH does not detect collapse directly.

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

# 🚀 Implications

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
