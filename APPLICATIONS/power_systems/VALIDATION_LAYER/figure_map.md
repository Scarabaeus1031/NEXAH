# 📊 NEXAH — Figure Map
### (Validation Layer Visual Reference)

---

# 🧭 Purpose

This document defines the mapping between:

```text
generated figures → experiment outputs → report references
```

---

# 📁 Figure Directory

```text
APPLICATIONS/power_systems/VALIDATION_LAYER/figures/
```

---

# 📊 FIGURE INDEX

---

## 🔹 FIG 01 — Event Shape Overlay

![Fig01](figures/fig_01_overlay.png)

**File:**
```text
figures/fig_01_overlay.png
```

**Source:**
```text
run_001_shape_validation.py
```

---

## 🔹 FIG 02 — Shape Space (PCA)

![Fig02](figures/fig_02_shape_space.png)

**File:**
```text
figures/fig_02_shape_space.png
```

**Source:**
```text
run_001_shape_validation.py
```

---

## 🔹 FIG 03 — Shape Clusters

![Fig03](figures/fig_03_clusters.png)

**File:**
```text
figures/fig_03_clusters.png
```

**Source:**
```text
run_001_shape_validation.py
```

---

## 🔹 FIG 04 — Shape Geometry

![Fig04](figures/fig_04_geometry.png)

**File:**
```text
figures/fig_04_geometry.png
```

**Source:**
```text
run_002_shape_geometry.py
```

---

## 🔹 FIG 05 — Shape Trajectories

![Fig05](figures/fig_05_trajectory.png)

**File:**
```text
figures/fig_05_trajectory.png
```

**Source:**
```text
run_003_shape_dynamics.py
```

---

## 🔹 FIG 06 — Pre-Collapse Dynamics

![Fig06](figures/fig_06_pre_collapse.png)

**File:**
```text
figures/fig_06_pre_collapse.png
```

**Source:**
```text
run_004_pre_collapse_dynamics.py
```

---

## 🔹 FIG 07 — Motion Instability Metric

![Fig07](figures/fig_07_motion_metric.png)

**File:**
```text
figures/fig_07_motion_metric.png
```

**Source:**
```text
run_005_motion_instability_metric.py
```

---

## 🔹 FIG 08 — Continuous Shape Flow

![Fig08](figures/fig_08_shape_flow.png)

**File:**
```text
figures/fig_08_shape_flow.png
```

**Source:**
```text
run_006_continuous_shape_flow.py
```

---

## 🔹 FIG 09 — IEEE Shape Flow

![Fig09](figures/fig_09_ieee_flow.png)

**File:**
```text
figures/fig_09_ieee_flow.png
```

**Source:**
```text
run_008_ieee_bridge.py
```

---

## 🔹 FIG 10 — IEEE Collapse Sweep

![Fig10](figures/fig_10_ieee_sweep.png)

**File:**
```text
figures/fig_10_ieee_sweep.png
```

**Source:**
```text
run_009_ieee_collapse_sweep.py
```

---

# 🧠 Summary

```text
signal → event → shape → geometry → motion
```

---

# 🧭 Usage

In reports:

```text
Fig. 1 — Event Shape Overlay
Fig. 2 — Shape Space
...
```

---

# 📌 Notes

- Figures must exist in `/figures/`
- Use `export_figures.py` to populate this folder
- Missing figures indicate incomplete pipeline outputs

---

# ⚡ NEXAH

```text
structure is visible
before collapse is measurable
```
