# 🧭 NEXAH — Repository Map (Grounded)

This document provides a **practical orientation** for navigating the NEXAH repository.

It reflects the **actual structure and current development state**,  
not an idealized or fully validated system.

---

# 🧠 What NEXAH is

NEXAH is a framework for:

> **extracting and analyzing structure in dynamical systems**

Core transformation:

```text
dynamics → structure → field → geometry → transition structure → navigation behavior
```

---

# ⚠️ CURRENT STATUS

NEXAH is:

```text
✔ a working structural system (demonstrator level)
✔ capable of extracting transition structure
✔ capable of producing consistent geometric patterns
```

But:

```text
❗ not yet fully validated
❗ not yet unified into a kernel
❗ not yet a production system
```

---

# 📦 Repository Structure (Actual)

---

## 🔷 1. ARCHITECTURE (System Definition)

```text
ARCHITECTURE/
```

Defines:

- system structure  
- layer organization  
- integration logic  
- current system state  

👉 **Primary reference for system understanding**

---

## 🧪 2. NEXAH_DEMONSTRATOR (Entry Point)

```text
NEXAH_DEMONSTRATOR/
```

Contains:

- minimal working pipeline  
- reproducible experiments  
- transition structure extraction  
- navigation demonstrations  

👉 **Recommended starting point**

---

## 🔶 3. NEXAH_CORE (Transition + Control Logic)

```text
NEXAH_CORE/
```

Contains:

- transition structure models  
- basin / gate representations  
- control experiments  
- navigation logic  

👉 **Core system logic (partly experimental)**

---

## 🌊 4. FIELD_LAYER (Geometry + Stability)

```text
FIELD_LAYER/
```

Includes:

- field reconstruction outputs  
- stability structure  
- flow geometry  
- separatrix / basin structure  

👉 transforms:

```text
field → geometry → stability interpretation
```

---

## 🔧 5. ARCHITECTURE/CORE (Executable Components)

```text
ARCHITECTURE/CORE/
```

### Field Reconstruction

```text
field_reconstruction/
```

- density fields  
- flow fields  
- boundary detection  

---

### Control Layer

```text
control_layer/
```

- basin detection  
- gate extraction  
- trajectory shaping  

---

👉 connects structure → execution

---

## 📦 6. nexah/ (Kernel — in progress)

```text
nexah/
```

Contains:

- early runtime logic  
- navigation abstractions  

👉 **future unified system kernel**

---

## 🧪 7. BUILDER_LAB (Exploration Layer)

```text
BUILDER_LAB/
```

Contains:

- experimental systems  
- discovery experiments  
- early prototypes  
- dashboards and tools  

---

### 🔬 Experimental Mechanism Layer

```text
BUILDER_LAB/EXPLORATION/experimental/
```

Purpose:

- test structural hypotheses  
- analyze system behavior under perturbation  
- explore control interaction  

---

### Observations (Current)

```text
• structure appears consistent across runs
• control affects local behavior
• global transitions are hard to enforce
```

---

### Interpretation

```text
🟡 system appears constrained by its geometry
🔴 not yet validated
```

---

👉 used for:

```text
hypothesis generation, not validation
```

---

## 🌍 8. APPLICATIONS (Test Systems)

```text
APPLICATIONS/
```

Includes:

- Lorenz system  
- IEEE power systems  
- experimental demos  

👉 **testbed for structure extraction**

---

## 🧠 9. FRAMEWORK (Conceptual Layer)

```text
FRAMEWORK/
```

Contains:

- ARCHY (simulation layer)  
- conceptual system abstractions  
- experimental modeling ideas  

👉 **high-level modeling layer (not validated)**

---

## 🔬 10. RESEARCH (Theory + Validation Layer)

```text
RESEARCH/
```

Contains:

- conceptual models  
- structural claims  
- validation plans  
- notes and documentation  

👉 **bridge between experiments and core system**

---

# 🔥 System Flow (Actual)

```text
ARCHY (simulation / systems)
→ BUILDER_LAB (exploration)
→ field_reconstruction (data → field)
→ FIELD_LAYER (geometry)
→ NEXAH_CORE (transition structure)
→ control_layer (trajectory shaping)
→ nexah/ (kernel — in progress)
→ navigation behavior
```

---

# 🔹 Core Structural Concept

The system is interpreted in terms of:

```text
basins → stable regions
boundaries → transition zones
gates → structured transition regions
```

---

## Key Observation

```text
Transitions are not random —
they appear constrained by system geometry.
```

---

## Status

```text
🟡 plausible
❗ requires validation
```

---

# 🧭 Where to Start

## ⚡ Run a minimal system

```bash
python NEXAH_DEMONSTRATOR/scripts/run_demo.py
```

---

## 🧠 Understand system structure

→ `ARCHITECTURE/README.md`

---

## 🔬 Explore core logic

→ `NEXAH_CORE/`

---

## 🌊 Geometry & stability

→ `FIELD_LAYER/`

---

## 🎮 Control experiments

→ `ARCHITECTURE/CORE/control_layer/`

---

## 🧪 Exploration layer

→ `BUILDER_LAB/`

---

# ⚡ What This Repository Enables

- structure extraction from dynamics  
- field reconstruction  
- geometric interpretation of behavior  
- transition modeling  
- exploratory control interaction  
- trajectory analysis within structured fields  

---

# 🧠 Key Insight

```text
Systems do not evolve randomly.

They appear to move within structured fields
that constrain motion and transitions.
```

---

# 🔥 Final Orientation

NEXAH is not yet a finalized framework.

It is:

> a **structured system for discovering and validating geometry in dynamical behavior**

---

Thomas K. R. Hofmann · NEXAH · 2026
