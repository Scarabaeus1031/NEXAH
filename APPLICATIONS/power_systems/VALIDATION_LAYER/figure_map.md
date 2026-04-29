# 📊 NEXAH — Figure Map
### (Validation Layer Visual Reference — Pipeline + Core Results)

---

# 🧭 Purpose

This document maps all generated figures from the validation pipeline to:

```text
experiments → outputs → interpretation
```

It ensures:

- full reproducibility  
- correct file references  
- clean integration into reports  

---

# 📁 Source

All figures originate from:

```text
APPLICATIONS/power_systems/VALIDATION_LAYER/outputs/
```

---

# 📊 PART A — PIPELINE FIGURES (STRUCTURE DISCOVERY)

---

## 🔹 FIG 01 — Shape Geometry (Cluster Relations I)

![Fig01](outputs/pipeline_20260429_012000/run_002_shape_geometry/figure_01.png)

---

## 🔹 FIG 02 — Shape Geometry (Cluster Relations II)

![Fig02](outputs/pipeline_20260429_012000/run_002_shape_geometry/figure_02.png)

---

## 🔹 FIG 03 — Shape Space Trajectory

![Fig03](outputs/pipeline_20260429_012000/run_003_shape_dynamics/figure_01.png)

---

## 🔹 FIG 04 — Pre-Collapse Structural Shift

![Fig04](outputs/pipeline_20260429_012000/run_004_pre_collapse_dynamics/figure_01.png)

---

## 🔹 FIG 05 — Motion Instability Metric

![Fig05](outputs/pipeline_20260429_012000/run_005_motion_instability_metric/figure_01.png)

---

## 🔹 FIG 06 — Shape Flow (Speed)

![Fig06](outputs/pipeline_20260429_012000/run_006_continuous_shape_flow/figure_01.png)

---

## 🔹 FIG 07 — Shape Flow (Angle)

![Fig07](outputs/pipeline_20260429_012000/run_006_continuous_shape_flow/figure_02.png)

---

## 🔹 FIG 08–10 — IEEE Shape Flow

![Fig08](outputs/pipeline_20260429_012000/run_008_ieee_bridge/figure_01.png)

---

## 🔹 FIG 11–13 — IEEE Collapse Sweep

![Fig11](outputs/pipeline_20260429_012000/run_009_ieee_collapse_sweep/figure_01.png)

---

# 📊 PART B — SIGNAL LAYER (LIMITATION ANALYSIS)

---

## 🔹 FIG 14 — Hybrid Detection Timeline

![Fig14](outputs/run_016_hybrid_detector/figure_01_hybrid_detector.png)

**Key Insight:**
```text
Combining signals improves robustness, not lead time.
```

---

# 📊 PART C — STATE SPACE STRUCTURE (CORE RESULTS)

---

## 🔹 FIG 21 — State Region Map (CRITICAL)

![Fig21](outputs/run_017_state_region_map/figure_01_state_region_map.png)

**Key Insight:**
```text
State space partitions into stable / transition / collapse regions.
```

---

## 🔹 FIG 22 — Curvature Region Map

![Fig22](outputs/run_017_state_region_map/figure_02_curvature_map.png)

---

## 🔹 FIG 23 — Region Timeline

![Fig23](outputs/run_017_state_region_map/figure_03_region_timeline.png)

**Key Insight:**
```text
A consistent transition phase exists before collapse.
```

---

## 🔹 FIG 24 — 3D State Space Trajectory

![Fig24](outputs/run_018_state_space_3d/figure_01_state_space_3d.png)

**Key Insight:**
```text
Time series corresponds to a trajectory in state space.
```

---

## 🔹 FIG 25 — 3D State Space (Curvature Overlay)

![Fig25](outputs/run_018_state_space_3d/figure_02_state_space_curvature.png)

---

# 🚨 CORE RESULT (PAPER FIGURE)

---

## 🔹 FIG 26 — Multi-Trajectory State Space (MAIN RESULT)

![Fig26](outputs/run_019_multi_trajectory_map/figure_01_multi_trajectory.png)

**Key Insight:**
```text
All trajectories pass through the same transition region
at the same time (~23.85), independent of perturbations.
```

---

## 🔹 FIG 27 — Multi-Trajectory Curvature Comparison

![Fig27](outputs/run_019_multi_trajectory_map/figure_02_curvature_compare.png)

---

# 🧠 Updated Summary

```text
signal → event → shape → geometry → motion → transition region → collapse
```

---

# 🔥 Recommended Figures for Paper

Use only:

```text
Fig. 21 — State Region Map
Fig. 23 — Region Timeline
Fig. 24 — 3D State Space
Fig. 26 — Multi-Trajectory State Space (MAIN RESULT)
```

---

# ⚡ NEXAH

```text
instability is not a point

it is a movement through structure
```
