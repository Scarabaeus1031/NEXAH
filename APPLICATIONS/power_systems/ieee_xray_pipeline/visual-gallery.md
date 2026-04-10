# NEXAH IEEE57 — Visual Gallery

This gallery highlights the evolution of the NEXAH pipeline and controller system  
from raw signal extraction → geometric structure → control → orbit attempts.

---

# 1. Early Structure Discovery (v1–v6)

## Phase Space Emergence

![v3 detection](results/ieee57_pipeline_v3_detection.png)
![v3b detection](results/ieee57_pipeline_v3b_detection.png)

- first visible structure in (coherence, switch)
- non-random trajectories emerge

---

## Pre-Collapse Structure

![v4 precollapse](results/ieee57_pipeline_v4_precollapse.png)

- structure forms **before classical collapse**
- early instability becomes geometrically visible

---

## Multi-Band Formation

![v5 multiband](results/ieee57_pipeline_v5_multiband.png)

- multiple stability regions appear
- first indication of **band-like dynamics**

---

## Polar Geometry (Key Breakthrough)

![v6 polar morphology](results/ieee57_pipeline_v6_polar_morphology.png)
![v6 phase drift](results/ieee57_pipeline_v6_polar_phase_drift.png)

- transformation into (r, θ)
- reveals:
  - drift
  - rotation tendency
  - escape directions

---

# 2. Navigation Layer (v7–v9)

## Vector Field

![v7 vector field](results/ieee57_v7_navigation_vector_field.png)

- direction of motion becomes explicit
- system seen as **flow field**

---

## Escape Directions

![v8 escape polar](results/ieee57_v8_basin_escape_polar.png)

- identification of instability directions
- first "where will it fail?" insight

---

## Navigation Policy

![v9 policy](results/ieee57_v9_navigation_policy_polar.png)

- first attempt to steer trajectories
- still open-loop logic

---

# 3. Closed-Loop Control (v10–v13)

## Closed Loop Emerges

![v10 polar](results/ieee57_v10_closed_loop_polar.png)

- feedback control begins
- trajectories become constrained

---

## Phase Control

![v11 polar](results/ieee57_v11_phase_polar.png)

- introduction of θ reference
- partial angular alignment

---

## Adaptive Phase Lock

![v12 polar](results/ieee57_v12_adaptive_phase_polar.png)

- early gate-like behavior
- local phase locking attempts

---

## Stability Band (Orbit Idea Begins)

![v13 polar](results/ieee57_v13_band_polar.png)

- radius target introduced
- system moves toward **orbital concept**

---

# 4. NCS Controllers (v14 Series)

## Hybrid Controller

![v14 hybrid](results/ieee57_v14_hybrid_polar.png)

- combined radial + phase + velocity control
- strong stabilization

---

## Breathing NCS

![v14.4 polar](results/ieee57_v14_4_breathing_ncs_polar.png)

- dynamic radius ("breathing")
- smoother trajectories

---

## Orbital Gate Activation

![v14.5 polar](results/ieee57_v14_5_orbital_gate_polar.png)

- inner core + lift
- escape eliminated

⚠️ BUT:
- no orbit formation

---

# 5. Orbit Capture Attempts (v14.6–v14.7)

## Orbit Capture (v14.6)

![v14.6 polar](results/ieee57_v14_6_orbit_capture_polar.png)

- system reaches band intermittently
- orbit not sustained

---

## Forced Rotation (v14.7 Series)

![v14.7](results/v14_7_polar.png)
![v14.7b](results/v14_7b_polar.png)
![v14.7c](results/v14_7c_polar.png)

- explicit rotation injected
- partial angular motion visible

⚠️ Key issue:
- rotation unstable
- system falls back toward center

---

# 6. Key Observations

Across all visuals:

### ✔ Structure is real
- trajectories are not random
- stable regions and escape regions exist

### ✔ Control works
- escape states → eliminated
- coherence → improved

### ❌ Missing element: rotation
- no persistent orbit
- no stable angular motion

---

# 7. Core Insight

The system behaves like:

```text
strongly damped + weakly driven
```

Result:

- collapse to center dominates
- orbit must be **actively constructed**

---

# 8. Interpretation

These visuals support the hypothesis:

> instability appears first as structural deformation in phase space  
> before it appears in classical voltage metrics

---

# 9. Status

- Structure discovery: ✔
- Control (stabilization): ✔
- Orbit formation: ⚠
- Gate locking: ❌

---

# 10. Next Step

- stabilize rotation
- maintain band orbit
- enable real gate transitions
