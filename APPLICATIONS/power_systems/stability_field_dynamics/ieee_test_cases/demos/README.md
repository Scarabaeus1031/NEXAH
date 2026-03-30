# 🧭 IEEE Test Case Demos — Rift / Field Navigation Experiments

## Overview

This folder contains experimental scripts exploring **field-based dynamics, rift extraction, and control strategies**  
on IEEE-style test systems.

The goal is to move from:

- trajectory-based analysis  
→ toward  
- **field-consistent navigation and control**

---

## 🧠 Core Idea

The system is not governed by a single curve or manifold.

Instead, it exhibits:

- field structure (flow)
- layers (stable bands)
- channels (preferred transitions)
- temporal modes (frequency)

This leads to a new paradigm:

> Navigation is not about reaching a point  
>  
> but aligning with structure in space and time.

---

## ⚙️ Pipeline (Current)

### 1. Field Generation & Export
- `run_ieee_field_analysis_export.py`
- `run_ieee_field_visual.py`
- `run_ieee_field_topology_map.py`

→ generates state trajectories and field structure

---

### 2. Rift Extraction
- `extract_rift_curve.py`
- `rift_distance_analysis.py`

→ identifies collapse-aligned structures (rift)

---

### 3. Instability & Temporal Analysis
- `rift_instability_detector.py`
- `rift_fft_analysis.py`
- `rift_modal_map.py`

→ detects:
- instability events
- dominant frequencies
- temporal structure

---

### 4. Navigation & Control

#### Early Controllers
- `rift_projection_control.py`
- `rift_tangent_controller.py`

#### Adaptive Controllers
- `rift_adaptive_controller.py`
- `rift_adaptive_controller_v2.py`

#### Predictive Controllers
- `rift_predictor_v2.py`
- `rift_predictor_v3.py`
- `rift_predictor_v4.py`
- `rift_predictor_v5.py`

#### Layer / Field Controllers
- `rift_layer_aware_navigator.py`
- `rift_layer_lock_controller.py`
- `rift_adaptive_corridor_v6.py`

#### Final Controller
- `rift_final_controller_v7.py`

→ combines:
- rift attraction
- frequency synchronization
- event response
- layer locking

---

### 5. Evaluation
- `rift_controller_metrics.py`

→ measures:
- distance to rift
- stability
- improvement

---

## 📊 Current Status

### Achieved

- ✅ Stable trajectory control (no divergence)
- ✅ Detectable frequency structure (~0.0083)
- ✅ Layer identification (~0.69–0.80)
- ✅ Event-based instability detection
- ✅ Combined controller (V7)

### Performance (V7)

- ~7% improvement vs original trajectory
- stable behavior
- reduced drift

---

## 🔍 Key Insights

### 1. Rift is not the true target
The system stabilizes in **layers**, not on the rift.

---

### 2. Field is structured
The phase space contains:

- layers (horizontal bands)
- channels (vertical transitions)
- grid-like geometry

---

### 3. Time matters
The system has a **dominant frequency**:

→ ~0.0083 (≈ 1 / 120)

Instabilities occur at specific phases.

---

### 4. Control must be multi-component

Effective control requires:

- spatial alignment (rift / grid)
- layer alignment (stability)
- temporal alignment (frequency)
- event response (instability)

---

## 🚧 Open Problems

### 1. Stronger Convergence
Current improvement (~7%) is moderate.

→ goal: >15–25%

---

### 2. Global vs Local Control
Current controllers are mostly local.

→ need:
- long-range planning
- field-consistent trajectories

---

### 3. Generalization
Test on:

- other datasets
- higher dimensions
- non-IEEE systems

---

### 4. Field Representation

Current work is in **projected 2D space**.

→ next step:
- lift control back to higher dimensions

---

## 🚀 Next Steps

Potential directions:

- V8: adaptive gain / stronger control
- frequency-phase locking controllers
- grid-based navigation
- API / real-time control system

---

## 🧭 Summary

The system has evolved from:

- trajectory observation  
→ manifold interpretation  
→ field modeling  
→ **controlled navigation**

---

## Core Insight

> The system is not defined by states.  
>  
> It is defined by its field structure, layers, and temporal modes.
