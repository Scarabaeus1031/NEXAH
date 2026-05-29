# 🧭 NEXAH Field Navigation Findings

# EXP_01 — Stability Seeking

## Result

A field-guided trajectory was compared to an uncontrolled trajectory.

Observed:

- mean distance uncontrolled: **2.997**
- mean distance guided: **0.705**
- distance reduction: **76.46 %**

---

# 📊 Visual Evidence

## Figure 1 — Navigation Trajectory

![EXP01 Trajectory](./outputs/EXP_01_STABILITY_SEEKING/exp01_navigation_trajectory.png)

The field-guided trajectory remains close to the reconstructed rift structure,
while the uncontrolled trajectory drifts away.

---

## Figure 2 — Distance Evolution

![EXP01 Distance](./outputs/EXP_01_STABILITY_SEEKING/exp01_distance_comparison.png)

Distance to the stability corridor over time.

The guided trajectory maintains a significantly lower distance.

---

## Figure 3 — Summary Dashboard

![EXP01 Summary](./outputs/EXP_01_STABILITY_SEEKING/exp01_navigation_summary.png)

Combined overview of:

- trajectory navigation
- distance evolution
- quantitative comparison

---

## Interpretation

The controller successfully used the reconstructed field as a navigational object.

This demonstrates the feasibility of stability-seeking navigation within a reconstructed field structure.

---

## Status

✅ Passed

---

## Core Insight

```text
Instability is not merely detectable.

It is navigable.
```
# EXP_02 — Corridor Acquisition

![EXP02 Summary](outputs/EXP_02_CORRIDOR_ACQUISITION/exp02_summary_dashboard.png)

## Result

A field-guided controller successfully acquired a stability corridor from a distant initial condition.

Observed:

- Mean distance (uncontrolled): 7.798
- Mean distance (guided): 0.336
- Distance reduction: 95.70 %
- Acquisition step: 27

---

## Corridor Acquisition

![Corridor Acquisition](outputs/EXP_02_CORRIDOR_ACQUISITION/exp02_corridor_acquisition.png)

The guided trajectory starts far from the corridor,
approaches the structure, acquires it, and subsequently
follows the corridor.

---

## Distance Evolution

![Distance Evolution](outputs/EXP_02_CORRIDOR_ACQUISITION/exp02_distance_evolution.png)

The acquisition process becomes visible as a rapid
reduction in distance to the corridor, followed by
stable tracking.

---

## Distance Field Navigation

![Distance Field](outputs/EXP_02_CORRIDOR_ACQUISITION/exp02_distance_field.png)

The reconstructed corridor acts as a navigational
structure embedded within a stability-distance field.

The guided trajectory converges toward the minimum-distance
region and remains attached to the corridor.

---

## Interpretation

The controller successfully:

1. detected the corridor
2. approached the corridor
3. acquired the corridor
4. remained attached to the corridor

This demonstrates that reconstructed field structures can
function as navigational objects rather than passive observations.

---

## Status

✅ Passed
