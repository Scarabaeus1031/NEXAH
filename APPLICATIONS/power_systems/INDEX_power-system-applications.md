# ⚡ NEXAH — Power Systems Applications

This section contains the **applied NEXAH framework for power system dynamics**,  
including experimental pipelines, scalable system validation, and closed-loop control prototypes.

---

# 🧭 Overview

NEXAH introduces a new approach to power system stability:

> **Stability is a continuous, navigable field — not a binary condition.**

Across all modules, the core transformation is:

```text
Simulation → Features → Manifold → Field → Risk → Control → Navigation
```

The goal is to move from:

- ❌ collapse detection  
to  
- ✅ **geometry-aware stability navigation**

---

# 📦 Module Structure

## 🔬 1. IEEE X-Ray Pipeline

📂 `ieee_xray_pipeline/`

**Purpose:**
Core experimental pipeline for transforming classical simulations into  
a **low-dimensional geometric state space**.

**Focus:**
- Feature extraction & manifold construction  
- Structural analysis of instability  
- Experimental controllers  
- Root Cube & attractor dynamics  

**Status:**
- Detection layer: ✅ functional  
- Control/navigation: 🧪 experimental  

👉 Entry point:  
`ieee_xray_pipeline/README.md`

---

## ⚡ 2. NEXAH IEEE9 — Closed-Loop Control (Reference System)

📂 `nexah_ieee9/`

**Purpose:**
First **fully working closed-loop system** demonstrating:

- field reconstruction  
- risk modeling  
- trajectory-based control  

**Key Property:**
👉 **Reproducible baseline implementation**

**Highlights:**
- Flow field as central object  
- Early instability detection  
- Geometry-aware control  
- Stable operation near collapse boundary  

**Status:**
- Controller v6: ✅ stable & public  
- Higher versions: 🧪 experimental  

👉 Entry point:  
`nexah_ieee9/README.md`

---

## 🌍 3. NEXAH IEEE X — Scalable Systems

📂 `nexah_ieeeX/`

**Purpose:**
Demonstrates **scaling of NEXAH** from small systems to real grids:

- IEEE 118  
- IEEE 300  
- IEEE 1354  
- IEEE 9241 (PEGASE)

**Focus:**
- robustness across system size  
- emergence of nonlinear dynamics  
- large-scale field behavior  
- adaptive intervention  

**Key Result:**
👉 NEXAH scales from **toy systems → real-world grids**

**Status:**
- Large-scale validation: ✅ successful  
- Control strategies: 🧪 ongoing  

👉 Entry point:  
`nexah_ieeeX/README.md`

---

# 🧠 Conceptual Layers

Across all modules, NEXAH operates in three layers:

### 1. Detection
- identify structural precursors  
- map collapse as continuous trajectory  

### 2. Field Construction
- build low-dimensional state space  
- derive flow field & risk landscape  

### 3. Navigation
- shape trajectories  
- stabilize system dynamically  
- operate near optimal boundary  

---

# 🔁 Relationship Between Modules

```text
ieee_xray_pipeline
    ↓ (method + experiments)

nexah_ieee9
    ↓ (first stable closed-loop system)

nexah_ieeeX
    ↓ (scaling & real-world validation)
```

---

# 🚀 Recommended Entry Path

For new users:

1. **Start with IEEE9**
   → understand core idea + working system  

2. **Explore X-Ray Pipeline**
   → see experimental structure + controllers  

3. **Move to IEEE X**
   → understand scaling & real-world behavior  

---

# ⚠️ Current Limitations

- Navigation (true multi-attractor control) is not yet solved  
- Physical coupling to real grid variables is still evolving  
- Benchmarking vs classical methods is incomplete  

---

# 🧭 Direction

NEXAH is moving toward:

- real-time stability navigation  
- geometry-based grid control  
- integration with real-world power systems  

---

# 🌀 NEXAH

> From simulation to structure  
> From structure to field  
> From field to navigation  
> From navigation to stability
