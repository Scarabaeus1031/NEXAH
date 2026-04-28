# ⚡ NEXAH — Experiments Log

---

# 🧭 Purpose

Track all validation experiments in a reproducible and structured way.

Each experiment documents:

- goal
- script
- key result
- interpretation

---

# 🧪 Experiment 001 — Shape Validation

**Script:**
run_001_shape_validation.py

**Goal:**
Validate event extraction + shape space concept

**Key Results:**
- events extracted
- shape clusters visible

**Insight:**
Event shape encodes system dynamics

---

# 🧪 Experiment 002 — Shape Geometry

**Script:**
run_002_shape_geometry.py

**Goal:**
Analyze relationships between shape clusters

**Key Results:**
- crossings detected
- area differences between clusters

**Insight:**
Shape space has structure (not random)

---

# 🧪 Experiment 003 — Shape Dynamics

**Script:**
run_003_shape_dynamics.py

**Goal:**
Track movement through shape space

**Key Results:**
- trajectories visible
- ordered vs chaotic paths

**Insight:**
Instability is movement, not a point

---

# 🧪 Experiment 004 — Pre-Collapse Dynamics

**Script:**
run_004_pre_collapse_dynamics.py

**Goal:**
Compare pre vs post collapse behavior

**Key Results:**
- separation in shape space
- structural shift before collapse

**Insight:**
System transitions before observable collapse

---

# 🧪 Experiment 005 — Motion Instability Metric

**Script:**
run_005_motion_instability_metric.py

**Goal:**
Define motion-based instability metric

**Key Results:**
- angle spikes detected
- instability measurable

**Insight:**
Directional change encodes instability

---

# 🧪 Experiment 006 — Continuous Shape Flow

**Script:**
run_006_continuous_shape_flow.py

**Goal:**
Track continuous movement in shape space

**Key Results:**
- speed + angle signals
- early warning before collapse

**Insight:**
Instability = deviation in motion

---

# 🧪 Experiment 007 — Statistical Validation

**Script:**
run_007_statistical_validation.py

**Goal:**
Test robustness over multiple runs

**Key Results:**
- detection rate: 43 / 50
- mean lead time ~11.6

**Insight:**
Method is statistically stable

---

# 🧪 Experiment 008 — IEEE Bridge

**Script:**
run_008_ieee_bridge.py

**Goal:**
Apply method to real power system model

**Key Results:**
- shape flow visible in stable regime
- warnings without collapse

**Insight:**
System has structure even when stable

---

# 🧪 Experiment 009 — IEEE Collapse Sweep

**Script:**
run_009_ieee_collapse_sweep.py

**Goal:**
Test early warning under varying load

**Key Results:**
- collapse detected at high load_rate
- NEXAH warning ~40–50 time units earlier

**Insight:**
Geometric drift precedes voltage collapse

---

# 🧠 Summary

```text
signal → event → shape → geometry → motion → instability
