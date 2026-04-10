# NEXAH IEEE X-Ray Pipeline

## Overview

The **NEXAH IEEE X-Ray Pipeline** is a structural analysis and control framework for power-system dynamics.

It transforms classical simulations into a **geometric state space**, where system behavior can be:

- observed  
- interpreted  
- and eventually controlled  

The pipeline follows the transformation:

```text
IEEE system → structure → field → channel → switch → decision → navigation
```

This repository contains:

- the full diagnostic pipeline (v1–v13)
- experimental controllers (v14.x)
- structural motif definitions
- quantitative evaluation on IEEE test systems

---

## 1. Current Status

The project has reached a critical transition point:

### ✔ Established

- low-dimensional state space (coherence, switch)
- field representation of dynamics
- channel and strand structure
- switch / transition detection
- measurable stability improvements (v14.x)

### ⚠ Emerging

- decision logic (state-dependent control)
- orbit-based stabilization
- phase-aware dynamics

### ❌ Not yet achieved

- stable orbit formation
- persistent gate locking
- physically grounded actuation mapping

---

## 2. Core Idea

The pipeline is not a simulator wrapper.

It implements:

> structural diagnosis and navigation of dynamical systems through geometry

Key principles:

- classical signals remain visible
- structure is primary
- motion defines stability
- control must align with geometry

---

## 3. Architecture

The pipeline consists of six layers:

---

### 3.1 Classical Baseline Layer

Reference system behavior:

- voltage magnitude  
- load evolution  
- collapse timing  

---

### 3.2 Field Layer

Geometric structure:

- attractors  
- basins  
- directional flow  
- coherence gradients  

---

### 3.3 Signal Layer

Extracted features:

- coherence  
- drift direction  
- radius (distance from center)  
- phase (θ)  
- phase velocity (dθ/dt)  

---

### 3.4 Channel & Switch Layer

Structural interpretation:

- grey channel detection  
- strand separation  
- switch regions  
- instability precursors  

---

### 3.5 Decision Layer

Emerging logic:

- HOLD / MONITOR / SWITCH / ALERT  
- band adherence  
- gate proximity  
- transition awareness  

---

### 3.6 Navigation / Control Layer (v14.x)

Experimental controllers:

- orbit capture logic  
- band stabilization  
- phase alignment  
- pulse / snap mechanisms  

This layer is under active development.

---

## 4. Controller Evolution (v14 Series)

### v14.5 — Stabilization Breakthrough

- coherence improved  
- escape states eliminated  
- strong damping achieved  

Limitation:

- system collapses toward center  
- no orbit formation  

---

### v14.6 — Orbit Capture + Gate Logic

- core escape mechanism  
- target band defined  
- phase-aware gate scoring  

Result:

- system reaches band intermittently  
- but fails to sustain orbit  

---

### v14.7 — Forced Rotation

- tangential forcing introduced  
- synthetic orbital motion attempted  

Result:

- partial rotation visible  
- unstable / discontinuous orbit  

---

### v14.8 — Two-Axis Control (P/Q split)

- radial control (P)
- tangential control (Q)

Goal:

- decouple radius and phase control

Result:

- improved controllability  
- but limited by physical coupling in system  

---

### v14.9 — Field Injection (Emerging)

- synthetic vector field added
- explicit rotation constructed in state space

Insight:

> orbit must be constructed, not extracted

---

## 5. Key Findings

### 5.1 Structural Representation Works

The mapping:

```text
simulation → geometry → dynamics
```

is valid and measurable.

---

### 5.2 Control is Effective (Quantitatively)

- coherence ↑  
- excursions ↓  
- escape states → 0  

---

### 5.3 System is Dissipative

Observed:

- strong inward pull
- natural collapse to center

Conclusion:

> the system lacks intrinsic orbital energy

---

### 5.4 Missing Rotation

Observed:

- phase clustering  
- no sustained angular motion  

Conclusion:

> stability requires rotation, not only position control

---

### 5.5 Control Dimensionality Problem

- P and Q both affect voltage magnitude  
- no clean orthogonal actuation  

Result:

> true 2D control is not physically available in current setup

---

## 6. Interpretation

The system currently supports:

### ✔ Structural Monitoring

- early instability detection  
- transition localization  

### ✔ Soft Control

- damping  
- stabilization  

### ⚠ Partial Navigation

- direction control emerging  
- orbit not stable  

### ❌ Full Navigation

- no persistent orbit  
- no reliable gate transitions  

---

## 7. Conceptual Model

The system structure can be summarized as:

```
CORE → GAP → BAND → FIELD → GRID
```

Dynamics:

```
drift + pulse + switch + (missing rotation)
```

---

## 8. Immediate Next Steps

### 1. Rotation Stabilization

- sustain angular motion
- prevent phase collapse

### 2. Gap Timing

- detect Breathing Gap entry
- apply trigger impulses

### 3. Control Redesign

- improve orthogonality
- test alternative actuation mappings

### 4. Validation

- multi-grid testing (IEEE 57, 118, ...)
- reproducible metrics

---

## 9. Practical Relevance

### Already usable

- anomaly detection  
- early warning signals  
- structural diagnostics  

### Not yet proven

- real-time grid control  
- industrial deployment  
- actuator mapping  

---

## 10. Summary

The NEXAH IEEE X-Ray Pipeline has evolved from:

```text
raw simulation → structure → field → controlled dynamics
```

Current state:

> a quantitatively validated structural control framework  
> with strong stabilization, but incomplete navigation capability  

Next milestone:

> transition from stabilization → orbit-based navigation

---

## Status

- Pipeline core: ✔ stable  
- Controller layer: ⚠ experimental  
- Navigation: ❌ not yet achieved  

---

## Entry Points

- `pipeline_versions/` → evolution of extraction + control  
- `results/` → generated plots and reports  
- `metrics.md` → quantitative evaluation  
- `breathing_gap_control_principles.md` → structural theory  

---

## Final Note

This project explores a fundamental hypothesis:

> instability appears first as structural deformation  
> before it appears in classical electrical metrics

If validated, this enables:

- earlier detection  
- better interpretation  
- new control strategies  

for complex dynamical systems.
