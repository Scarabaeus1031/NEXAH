# NEXAH / power_systems

**Power System Stability & Structural Field Navigation**

NEXAH detects instability significantly earlier than classical voltage-based methods by analyzing structural transitions in system dynamics.

> **Stability is not a static state — it is a geometry evolving in time.**

---

# Current Status — Detection ✔ | Navigation ⚠ (April 2026)

NEXAH reliably detects voltage collapse **43.9 seconds earlier** than classical methods across multiple IEEE test systems.

| Network                | Lead Time vs. Classical Collapse | Status         |
|------------------------|----------------------------------|----------------|
| IEEE 118-Bus           | **43.9 s**                       | Confirmed      |
| IEEE 300-Bus           | **43.9 s**                       | Mic-Drop       |
| IEEE 1354-Bus          | **43.9 s**                       | Confirmed      |
| IEEE 9241-Bus (PEGASE) | **43.9 s**                       | Confirmed      |

---

## Why this matters

Classical methods detect collapse only after voltage degradation begins.

NEXAH detects:

- structural drift  
- coherence breakdown  
- resonance deformation  

→ **before collapse becomes electrically visible**

---

# System Architecture

The NEXAH pipeline follows:

```text
simulation → structure → field → channel → switch → decision → navigation
```

---

# IEEE X-Ray Pipeline (v1–v14.x)

The IEEE X-Ray Pipeline introduces a reduced structural state space:

- coherence (x)
- switch signal (y)
- radius (r)
- phase (θ)

This enables:

- geometric trajectory analysis  
- stability band detection  
- experimental control  

---

## Controller Status (v14 Series)

### Achieved

- ✔ strong stabilization  
- ✔ escape elimination (v14.5)  
- ✔ coherence improvement  
- ✔ stability band definition  

### Limitations

- ⚠ system collapses toward center  
- ⚠ no sustained orbit formation  
- ⚠ no stable phase locking  

### Key Insight

> The system behaves as a **dissipative field lacking intrinsic rotational energy**

---

# Root Cube Navigation (v31–v36)

Recent experiments extend the system into a higher-dimensional geometric representation.

### Contributions

- 3D projection:
  - radius
  - phase
  - distance to structural axis
  - NCS proximity  

- breathing + twisting control dynamics  
- smooth transition in control regime

### Observations

- trajectories leave previously constrained regions  
- system explores new regions of state space  
- control signal transitions between regimes  

### Interpretation

> high escape counts indicate a transition out of the original stability basin  
> and suggest a structural regime change in system dynamics

This behavior is currently **experimental and not yet fully understood**.

---

# Two Operational Layers

## 1. Detection Layer ✔
- early warning (Mic-Drop achieved)
- structural instability detection
- validated across multiple grids

## 2. Navigation Layer ⚠
- orbit control
- phase alignment
- gate logic

→ currently under development

---

# Key Insight

The grey channel represents:

> a structurally valid region of motion

Switch points represent:

> transitions between stability regimes

---

# Interpretation

NEXAH currently provides:

### ✔ Early Detection (Solved)
### ✔ Structural Mapping (Solved)
### ⚠ Control (Partial)
### ❌ Navigation (Open Problem)

---

# Next Milestones

1. stabilize angular motion (rotation)
2. maintain orbit within stability band
3. enable phase locking (gate transitions)
4. connect control to physical actuation

---

# Summary

NEXAH evolves from:

```text
signal → structure → geometry → early warning
```

toward:

```text
structure → control → navigation
```

Current state:

> **Early warning is solved. Navigation is the next frontier.**

---

# Entry Points

- `ieee_xray_pipeline/` → pipeline + controllers  
- `stability_field_dynamics/` → validated detection system  
- `results/` → generated plots and reports  

---

# Author

Thomas K. R. Hofmann  
April 2026

NEXAH is transitioning from geometric discovery to a  
**functional framework for navigation in complex dynamical systems.**
