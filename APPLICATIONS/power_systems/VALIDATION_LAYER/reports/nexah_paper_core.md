# ⚡ NEXAH — Geometric Instability Detection from Time-Series Signals

---

# 🧾 Abstract

We introduce NEXAH, a geometry-based framework for analyzing instability in dynamical systems from observable signals.

Instead of defining instability as a threshold crossing in scalar measurements (e.g. voltage magnitude), NEXAH reconstructs a local state representation from time-series data and interprets system behavior as a trajectory in a geometric state space.

Using voltage time series from synthetic scenarios and IEEE14 test systems, we show that:

(1) instability manifests as a deformation of trajectory geometry before observable collapse,  
(2) curvature-derived events form structured objects with characteristic shapes,  
(3) these shapes define a low-dimensional geometric space, and  
(4) instability emerges as motion through this space, detectable via directional changes (angle) and displacement (speed).

In controlled collapse scenarios, NEXAH provides early warning signals up to 40–50 simulation steps before voltage threshold violation, while also revealing structural dynamics not accessible to classical indicators such as dv/dt.

These results suggest that instability detection can be reformulated as a problem of geometric trajectory analysis, enabling earlier and more informative diagnostics from existing measurements.

---

# ⚡ Contributions

This work makes the following contributions:

---

## 1. Geometric Reformulation of Instability

We show that instability can be interpreted as a **trajectory deformation in a reconstructed state space**, rather than a threshold crossing in scalar signals.

---

# 2. Method

---

## 2.1 Problem Setting

We consider a dynamical system observed through a scalar time series:

```text
V(t)
```

where $begin:math:text$ V\(t\) $end:math:text$ represents an observable quantity (e.g. voltage magnitude in a power system).

Classical approaches define instability as a threshold crossing in $begin:math:text$ V\(t\) $end:math:text$.  
In contrast, we assume that $begin:math:text$ V\(t\) $end:math:text$ is a projection of an underlying dynamical process:

```text
y(t) = h(x(t))
```

where $begin:math:text$ x\(t\) $end:math:text$ is the latent system state.

The objective is to reconstruct local system dynamics from $begin:math:text$ V\(t\) $end:math:text$ and detect instability **before observable collapse occurs**.

---

## 2.2 State Reconstruction

We construct a local state representation using temporal derivatives:

```text
x(t) = (V(t), dV/dt, d²V/dt²)
```

This embedding captures:

- position → $begin:math:text$ V\(t\) $end:math:text$  
- velocity → $begin:math:text$ dV\/dt $end:math:text$  
- acceleration → $begin:math:text$ d²V\/dt² $end:math:text$  

Numerical derivatives are computed using finite differences.

This results in a trajectory:

```text
x(t) ∈ ℝ³
```

representing system evolution in a reconstructed state space.

---

## 2.3 Curvature-Based Signal

To detect structural changes in the trajectory, we define a curvature-based signal:

```text
κ(t) = || d²x/dt² ||
```

This quantity measures the change of motion in the reconstructed state space.

Interpretation:

- low curvature → smooth, stable evolution  
- high curvature → structural deviation or transition  

---

## 2.4 Event Extraction

We define an event as a sustained increase in curvature:

```text
event = { t : κ(t) exceeds baseline threshold over a window }
```

Operationally:

- compute baseline statistics of $begin:math:text$ κ\(t\) $end:math:text$  
- detect contiguous segments where $begin:math:text$ κ\(t\) $end:math:text$ is elevated  

Each event corresponds to a localized deviation in system dynamics.

---

## 2.5 Shape Representation

Each extracted event is transformed into a normalized shape:

```text
shape = normalized κ(t) over event duration
```

Processing steps:

1. extract curvature segment  
2. resample to fixed length  
3. normalize amplitude  

This yields a representation:

```text
shape ∈ ℝⁿ
```

enabling comparison across events.

---

## 2.6 Shape Space Construction

All event shapes are embedded into a low-dimensional space using Principal Component Analysis (PCA):

```text
shape → vector → (PC1, PC2)
```

This defines a geometric space where:

- similar events cluster  
- different regimes occupy distinct regions  
- transitions appear as continuous trajectories  

---

## 2.7 Motion Analysis

Let $begin:math:text$ s\(t\_i\) $end:math:text$ denote the sequence of shapes in the embedded space.

We define two motion metrics:

### Speed

```text
speed(t_i) = || s(t_i) - s(t_{i-1}) ||
```

Measures displacement between consecutive states.

---

### Angle

```text
angle(t_i) = arccos( 
    (Δs_{i-1} · Δs_i) / (||Δs_{i-1}|| · ||Δs_i||)
)
```

Measures directional change between successive steps.

---

### Interpretation

- high speed → rapid change in system behavior  
- high angle → change in direction (structural transition)  

---

## 2.8 Detection Mechanism

### Classical Detection

```text
t_classical = first t where V(t) < threshold
```

or

```text
t_classical = first t where dV/dt < threshold
```

---

### NEXAH Detection

We define detection as the earliest occurrence of:

```text
sustained increase in curvature
OR
significant motion in shape space
```

Operational signals:

- curvature increase  
- angle spike  
- combined motion threshold  

---

## 2.9 Evaluation Metric

We measure performance using lead time:

```text
Lead Time = t_collapse - t_detection
```

where:

```text
t_collapse = first t where V(t) < threshold
```

All time measurements are expressed in **simulation steps**.

---

## 2.10 Interpretation Framework

The full transformation pipeline is:

```text
V(t)
→ x(t)
→ κ(t)
→ events
→ shapes
→ shape space
→ motion
→ instability detection
```

This reframes instability as:

```text
trajectory deformation in a geometric space
```

rather than a scalar threshold event.

---
## 2. Event-to-Shape Representation

We introduce a representation in which **curvature-derived events are treated as structured objects (shapes)**, enabling comparison, normalization, and clustering.

---

## 3. Shape Space Construction

We demonstrate that event shapes form a **low-dimensional geometric space**, where:

- clusters correspond to system regimes  
- transitions appear as continuous deformations  

---

## 4. Motion-Based Detection

We show that instability can be detected through **motion in shape space**, using:

- angle → directional change  
- speed → displacement magnitude  

---

## 5. Early Warning Capability

In IEEE14 collapse scenarios, NEXAH produces early warning signals:

```text
≈ 40–50 simulation steps before voltage collapse
```

This exceeds classical detection based on voltage thresholds and dv/dt.

---

## 6. Reproducible Validation Pipeline

We provide a fully reproducible validation layer, including:

- a minimal validation script (`validation_skeleton.py`)  
- a structured experiment suite (`run_001 → run_009`)  
- a complete figure mapping (`figure_map.md`)  

---

# 🧠 Definitions

---

## Observable Signal

```text
V(t)
```

Measured system quantity (e.g. voltage magnitude).

---

## Reconstructed State

```text
x(t) = (V(t), dV/dt, d²V/dt²)
```

Local embedding of system dynamics derived from observable signals.

---

## Curvature Signal

```text
κ(t) = || d²x/dt² ||
```

Measures change of motion in reconstructed state space.

---

## Event

```text
event = sustained increase in κ(t)
```

Represents a localized structural deviation in system dynamics.

---

## Shape

```text
normalized curvature profile over time
```

Each event is represented as a shape, enabling comparison across events.

---

## Shape Space

```text
shape → vector → PCA projection
```

Low-dimensional geometric embedding of event shapes.

---

## Motion Metrics

- speed = displacement in shape space  
- angle = directional change between steps  

---

## Collapse Definition (Reference)

```text
t_collapse = first t where V(t) < threshold
```

---

## Lead Time

```text
Lead Time = t_collapse - t_detection
```

Measured in **simulation steps**.

---

# ⚠️ Limitations

- sensitivity to noise (curvature amplification)  
- validation currently limited to IEEE14  
- PCA is a reduced representation  
- no persistence filtering applied  

---

# 🧭 Interpretation

Classical methods:

```text
Instability = threshold crossing in V(t)
```

NEXAH:

```text
Instability = geometric drift in trajectory space
```

---

# ⚡ Core Insight

```text
Instability is not a point.

It is a movement through structure.
```

---

# 🧭 Final Statement

```text
Power system instability emerges as a measurable geometric drift 
in reconstructed state space, preceding observable collapse.
```

---
