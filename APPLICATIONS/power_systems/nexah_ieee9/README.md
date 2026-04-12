# ⚡ NEXAH — IEEE9 Stability Field System (v3)

## 🧭 Overview

This module implements the NEXAH framework on a power system test case (IEEE 9-bus).

It transforms classical voltage stability analysis into a:

continuous stability field with adaptive, closed-loop control

---

## 🔬 Core Idea

Instead of asking:

"Will the system collapse?"

NEXAH answers:

"Where are we in the stability field — and how can we navigate it?"

---

## 🧱 Pipeline Architecture

Simulation → Features → Manifold → Overlay → Prediction → Policy → Adaptive Control → System Evolution

---

## 📊 System Behavior (Latest Run — Synthetic)

### Run ID

run_20260412_223816

---

### Voltage Collapse (Adaptive Closed Loop)

![Voltage Collapse](results/run_20260412_223816/plot.png)

✔ Collapse dynamics preserved (no artificial suppression)  
✔ Adaptive stabilization in mid-regime  
✔ Structural transitions remain visible  

---

### Collapse Risk Field

![Collapse Risk](results/run_20260412_223816/risk.png)

✔ Peak risk ≈ 0.77  
✔ Fewer warnings (~3 vs ~37 in unstable runs)  
✔ Cleaner, more stable signal (less noise)  

---

### Intervention Field

![Intervention](results/run_20260412_223816/intervention.png)

✔ Controlled intervention (no overreaction)  
✔ Smooth transition between regimes  
✔ Reduced saturation effects  

---

## ⚡ Real Grid Prototype (NEW)

### Example Run

run_real_20260412_231904

Key Observations:

- Smooth voltage degradation with realistic oscillations
- Structured transition:
  SAFE → WARNING → CRITICAL
- Risk peak ≈ 0.77
- Adaptive control escalates to:
  PREEMPTIVE_STABILIZE
  REDUCE_LOAD

✔ No artificial stabilization  
✔ Physical constraints respected  
✔ Control remains effective but limited  

---

## 🧠 Interpretation (v3)

The system now behaves as:

adaptive field controller instead of reactive trigger system

---

## 🔄 Evolution Across Versions

v1 → reactive control  
v2 → recovery + memory  
v3 → pre-emptive field control  

---

## 🔍 What Changed in v3

- Risk becomes stable and interpretable  
- Warnings reduced to meaningful events  
- Control avoids oscillation and saturation  
- System reacts to trajectory, not just state  

---

## ⚖️ Classical vs NEXAH

Static thresholds     → Classical: Yes | NEXAH: No  
Dynamic risk field    → Classical: No  | NEXAH: Yes  
Early warning         → Classical: Limited | NEXAH: Yes  
Closed-loop control   → Classical: No  | NEXAH: Yes  
Structural modeling   → Classical: No  | NEXAH: Yes  
Adaptive control      → Classical: No  | NEXAH: Yes  

---

## 🚀 Run

Synthetic:

PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/decision/main_v2.py

Real Grid:

PYTHONPATH=. python APPLICATIONS/power_systems/nexah_ieee9/decision/main_real_v2.py

---

## 📁 Results Folder

APPLICATIONS/power_systems/nexah_ieee9/results/

Each run contains:

- plot.png  
- risk.png  
- intervention.png  
- states.txt  
- actions.txt / actions_adaptive.txt  
- meta.json  

---

## 🧭 Status

Baseline        DONE  
Manifold        DONE  
Predictor       DONE  
Policy          DONE  
Closed Loop     DONE  
Adaptive v3     DONE  
Real Grid       PROTOTYPE  

---

## ⚠️ Important Note

Two execution modes exist:

Synthetic Solver:
- Controlled environment  
- Smooth dynamics  
- Used for development  

Real Grid (pandapower):
- Nonlinear AC power flow  
- Convergence constraints  
- Realistic instability  

---

## 🔮 Next Step

- Trajectory control (path shaping)  
- Physical intervention mapping  
- Multi-step predictive control  

---

## 🔥 Final Insight

Power systems are not binary (stable / unstable)

They exist inside a structured stability landscape

NEXAH turns this into something we can:

measure, interpret, and actively navigate
