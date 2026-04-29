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
