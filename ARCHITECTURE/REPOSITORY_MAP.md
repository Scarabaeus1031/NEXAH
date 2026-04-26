# 🧭 NEXAH — Repository Map (Grounded)

This document provides a **practical orientation** for navigating the NEXAH repository.

It reflects the **actual structure**, not the idealized one.

---

# 🧠 What NEXAH is

NEXAH is a framework for:

> **reconstructing, controlling, and navigating dynamical systems as structured fields**

Core transformation:

```text
Dynamics → Structure → Field → Geometry → Stability → Transition → Control → Navigation
```

---

# 📦 Repository Structure (Real)

---

## 🔷 1. ARCHITECTURE (System Definition)

```text
ARCHITECTURE/
```

Defines:

- system design  
- layer structure  
- integration logic  
- current system state  

👉 **Single source of truth for architecture**

---

## 🔶 2. NEXAH_CORE (Transition + Control Theory Layer)

```text
NEXAH_CORE/
```

Contains:

- full transition system (v1–v80)  
- basin / gate model  
- control evolution  
- phase-aware navigation  

👉 **Deep system logic (experimental + validated)**

---

## 🌊 3. FIELD_LAYER (Geometry + Stability Layer)

```text
FIELD_LAYER/
```

Includes:

- FIELD_DECOMPOSITION  
- NAVIGATION_ENGINE  
- stability + geometry extraction  

Defines:

- basins  
- separatrix  
- flow geometry  
- stability structure  

👉 transforms field → geometry + stability

---

## 🔧 4. ARCHITECTURE/CORE (Executable Core Components)

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

→ data → field  

---

### Control Layer

```text
control_layer/
```

- basin detection  
- gate extraction  
- trajectory control  

→ operates on transition geometry  

---

## 📦 5. nexah/ (Runtime Package)

```text
nexah/
```

Contains:

- core logic (in progress)  
- navigation modules  
- system abstraction  

👉 **future unified kernel / API**

---

## 🧪 6. BUILDER_LAB (Exploration + Integration)

```text
BUILDER_LAB/
```

Contains:

- demos  
- experimental systems  
- discovery experiments  
- proto models  
- dashboards  

Also includes:

- DISCOVERY_ENGINE (early research)  
- ENGINE (legacy computation)  
- EXPLORATION (concept systems)  

👉 **active development + experimental workspace**

---

## 🌍 7. APPLICATIONS (Use Cases)

```text
APPLICATIONS/
```

Includes:

- Lorenz system  
- IEEE power systems  
- datasets  
- demos  

👉 **real-world and test systems**

---

## 🧠 8. FRAMEWORK (Conceptual Layer)

```text
FRAMEWORK/
```

Contains:

- ARCHY  
- system abstractions  
- conceptual system layers  

👉 **higher-level system modeling layer**

---

## 🔬 9. RESEARCH (Theory + Documentation)

```text
RESEARCH/
```

Contains:

- theory documents  
- experiments  
- notes  
- visual galleries  

👉 **long-form thinking + documentation**

---

# 🔥 System Flow (Actual)

```text
ARCHY (simulation)
→ BUILDER_LAB / DISCOVERY_ENGINE
→ CORE/field_reconstruction
→ FIELD_LAYER
→ Transition Geometry (NEXAH_CORE)
→ CORE/control_layer
→ nexah/ (kernel in progress)
→ Navigation / Execution
```

---

# 🔹 Transition Geometry (Core Concept)

The system operates on:

- Basins → stable regions  
- Separatrix → boundaries  
- Gates → transition corridors  

👉 transitions are structured, not random  

---

# 🧭 Where to Start

## ⚡ Run something

```bash
python run_nexah_demo.py
```

or

```bash
python APPLICATIONS/core_demos/...
```

---

## 🧠 Understand system

→ `ARCHITECTURE/README.md`

---

## 🔬 Deep logic

→ `NEXAH_CORE/`

---

## 🌊 Geometry & stability

→ `FIELD_LAYER/`

---

## 🎮 Control

→ `ARCHITECTURE/CORE/control_layer/`

---

## 🧪 Explore

→ `BUILDER_LAB/`

---

# ⚡ What This Repository Enables

- structure extraction from dynamics  
- field reconstruction  
- geometry + stability analysis  
- transition modeling  
- gate-based control  
- navigation through system structure  

---

# 🧠 Key Insight

> Systems evolve within structured fields  
> that constrain motion, transitions, and outcomes.

---

# 🔥 Final Orientation

NEXAH is not a collection of scripts.

It is:

> a layered system for **understanding and controlling structured dynamical fields**

---

Thomas K. R. Hofmann · NEXAH · 2026
