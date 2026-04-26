# 🧭 NEXAH — Repository Map

This document provides a **practical orientation** for navigating the NEXAH repository.

It answers:

- where things are  
- what they do  
- where to start  

---

# 🧠 What NEXAH is

NEXAH is a framework for:

> **reconstructing, understanding, and navigating dynamical systems as structured fields**

Core transformation:

```text
Dynamics → Structure → Field → Geometry → Stability → Control → Navigation
```

---

# 📦 Repository Structure

## 🔷 1. ARCHITECTURE (System Definition)

ARCHITECTURE/

Defines:

- system design  
- layer structure  
- integration logic  

→ Start here if you want to understand the system

---

## 🔶 2. CORE (Implementation)

ARCHITECTURE/CORE/

The actual working system.

---

### 🌊 Field Reconstruction

ARCHITECTURE/CORE/field_reconstruction/

Builds structure from data:

- density fields  
- flow fields  
- boundary detection  
- validity regions  

→ transforms data → field

---

### 🎮 Control Layer

ARCHITECTURE/CORE/control_layer/

Enables system interaction:

- basin detection  
- separatrix extraction  
- gate extraction  
- gate tracking  
- trajectory steering  

→ operates on transition structure

---

## 🌊 3. FIELD_LAYER (Interpretation)

FIELD_LAYER/

Adds meaning to structure:

- geometry (basins, channels)  
- stability structure  
- energy landscape  
- flow decomposition  

→ transforms field → geometry + stability

---

## 🧭 4. NAVIGATOR (Execution)

NAVIGATOR/

Executes movement:

- trajectory shaping  
- path following  
- convergence behavior  

→ transforms structure → motion

---

## 🔬 5. DISCOVERY ENGINE

DISCOVERY_ENGINE/

Extracts structure from dynamics:

- transition detection  
- manifold discovery  
- divergence / curl  
- temporal structure  

→ transforms dynamics → structure

---

## 🌍 6. APPLICATIONS (Use Cases)

APPLICATIONS/

Real-world and demo systems:

- Lorenz system (reference)  
- power systems (IEEE)  
- experimental systems  

→ see the system in action

---

## 🧪 7. BUILDER LAB (Exploration)

BUILDER_LAB/

- rapid experiments  
- visual prototypes  
- exploratory models  

→ supports development and discovery

---

# 🔥 System Flow (Actual)

ARCHY (Simulation)  
→ Discovery Engine  
→ Field Reconstruction  
→ Field Layer  
→ Transition Geometry  
→ Control Layer  
→ Navigator  
→ Convergence  

---

# 🔹 Transition Geometry (Key Concept)

The system operates on:

- Basins → stable long-term behavior  
- Separatrix → boundary between regimes  
- Gates → minimal-cost transition points  

→ These define where control is possible

---

## 🔷 Advanced Transition Layer

Location:

```text
NEXAH_CORE/
```

Contains:

- transition system (v56–v80)
- gate geometry
- phase-aligned navigation
- flow-aligned control

---
# 🧭 Where to Start

## ⚡ Quick Start (Recommended)

Run a demo:

python APPLICATIONS/core_demos/lorenz/lorenz_meta_control_v6_switch.py

Observe:

- structure in chaos  
- transitions  
- controlled motion  

---

## 🧠 Understand the System

→ ARCHITECTURE/README.md

---

## 🔬 Understand Structure Extraction

→ DISCOVERY_ENGINE/

---

## 🌊 Understand Field Construction

→ ARCHITECTURE/CORE/field_reconstruction/

---

## 🎮 Understand Control

→ ARCHITECTURE/CORE/control_layer/

---

## 🧭 See Full Pipeline

→ FIELD_LAYER/  
→ NAVIGATOR/

---

# ⚡ What This Repository Enables

- structure extraction from dynamics  
- field reconstruction  
- geometric interpretation  
- stability analysis  
- transition detection  
- gate-based control  
- navigation through system structure  

---

# 🧠 Key Insight

> Systems are not random.  
>  
> They evolve within structured fields  
> that constrain motion, transitions, and outcomes.

---

# 🔥 Final Orientation

NEXAH is not a collection of scripts.

It is:

> a layered system that reconstructs, constrains, and navigates dynamical fields

---

Thomas K. R. Hofmann · NEXAH · 2026
