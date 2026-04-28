# ⚡ NEXAH — Power Systems Applications

This section contains the **applied NEXAH framework for power system dynamics**,  
including experimental pipelines, system-level validation, and early-stage control experiments.

---

# 🧭 Overview

NEXAH introduces a geometry-based perspective on power system stability:

> **Stability is modeled as a trajectory evolving within a structured dynamical field.**

Instead of treating instability as a threshold violation, the system is interpreted as:

- a continuous dynamical process  
- evolving across structured regions (regimes)  
- with transitions between stable and unstable behavior  

---

# ⚙️ Technical Context (Condensed)

- **Simulation basis:** AC power flow / dynamic simulations (pandapower)  
- **Input signals:** voltage magnitude and derived temporal features  
- **Feature space:** coherence, drift, acceleration, residual structure, distance metrics, phase  
- **Representation:** low-dimensional geometric state space  
- **Derived objects:**
  - flow field (vector field)
  - risk landscape
  - regime structure  

---

# 🔁 Core Transformation

```text
Simulation → Features → State Embedding → Field → Risk → Analysis / Control
```

Goal:

- ❌ detect collapse after it occurs  
- ✅ **analyze and anticipate structural regime transitions**

---

# 🧠 System Architecture

NEXAH consists of three conceptual layers:

### 1. Extraction Layer
- simulation → feature generation  
- transformation into structured state representation  

### 2. Representation Layer
- construction of geometric state space  
- flow field and risk landscape  

### 3. Navigation / Application Layer (Experimental)
- trajectory analysis  
- early-stage control strategies  
- stability navigation experiments  

---

# 📦 Module Structure

## 🔬 1. IEEE X-Ray Pipeline

📂 `ieee_xray_pipeline/`

**Role:**
Core **extraction and representation pipeline**

**Purpose:**
Transforms classical simulations into a **low-dimensional geometric state space**

**Includes:**
- feature extraction  
- manifold construction  
- structural analysis  
- experimental controller designs  

**Status:**
- Detection: ✅ functional  
- Control: 🧪 experimental  

👉 Entry point:  
`ieee_xray_pipeline/README.md`

---

## ⚡ 2. NEXAH IEEE9 — Reference System

📂 `nexah_ieee9/`

**Role:**
First **reproducible closed-loop prototype**

**Purpose:**
Demonstrates:

- field reconstruction  
- risk modeling  
- trajectory-based intervention  

**Key property:**
👉 Minimal working system with reproducible behavior

**Status:**
- v6: ✅ stable baseline  
- later versions: 🧪 experimental  

👉 Entry point:  
`nexah_ieee9/README.md`

---

## 🌍 3. NEXAH IEEE X — Scaling Experiments

📂 `nexah_ieeeX/`

**Role:**
System-level validation across increasing grid size

**Systems:**
- IEEE 118  
- IEEE 300  
- IEEE 1354  
- IEEE 9241 (PEGASE)

**Focus:**
- structural consistency across scales  
- emergence of nonlinear dynamics  
- behavior under increasing complexity  

**Observed:**
- stable behavior at large scale  
- increased sensitivity in nonlinear regimes  

👉 Entry point:  
`nexah_ieeeX/README.md`

---

# 🔁 Relationship Between Modules

```text
ieee_xray_pipeline
    ↓ (method + representation)

nexah_ieee9
    ↓ (minimal working system)

nexah_ieeeX
    ↓ (scaling & system-level validation)
```

---

# 🚀 Recommended Entry Path

1. **Start with IEEE9**
   → understand core mechanism in a minimal system  

2. **Explore X-Ray Pipeline**
   → understand feature extraction and geometry construction  

3. **Move to IEEE X**
   → analyze scaling behavior and system-level effects  

---

# ⚠️ Current Limitations

- control remains experimental (no stability guarantees)  
- sensitivity to parameters not fully explored  
- limited validation on real-world datasets  
- benchmarking vs classical methods is ongoing  

---

# 🧭 Direction

Ongoing work focuses on:

- quantitative validation vs classical stability methods  
- robustness across scenarios and perturbations  
- improved mapping to physical grid variables  
- development of reliable control strategies  

---

# 🌀 NEXAH Principle

```text
simulation → structure → field → geometry → dynamics → regimes
```

---

# 🧠 Positioning

This framework is currently **experimental** and aims to:

- provide structural insight into power system dynamics  
- explore geometry-based representations  
- evaluate early-stage navigation concepts  

It is **not yet a production-ready control system**.

---

# 🌀 NEXAH

> From simulation to structure  
> From structure to field  
> From field to navigation  
> From navigation to stability
