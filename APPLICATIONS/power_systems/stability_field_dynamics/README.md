# ⚡ Stability Field Dynamics

A collection of NEXAH-based experiments, applications, and validation studies for stability analysis, transition geometry, and navigation in complex dynamical systems.

---

## 📖 Overview

This directory contains the practical implementation, mathematical foundation, and validation environment of the NEXAH framework.

The project investigates whether instability in complex systems can be detected and navigated through geometric field structures before conventional collapse indicators become visible.

Current focus areas include:

- stability-field construction
- transition geometry
- regime detection
- navigation and intervention
- large-scale IEEE benchmark validation

---

## 📂 Main Components

| Folder | Description |
|----------|-------------|
| ieee_test_cases | Core validation environment containing experiments, analysis pipelines, state-field extraction, navigation research, and controller development across IEEE benchmark systems. |
| ieee_application | Application layer demonstrating practical NEXAH workflows, tutorials, loaders, and power-grid navigation examples. |
| iee_core_geometry | Mathematical foundations, field dynamics, operator theory, and scaling research. |
| data | Supporting datasets, generated inputs, and auxiliary resources used throughout the framework. |

---

# 🧩 CORE

Core implementation of the NEXAH framework.

Contains:

- ARCHY simulation layer
- Discovery Engine
- Stability Field Construction
- State Graph generation
- NEXAH Operator
- NEXAH Kernel
- Navigation and control logic

---

# 🌌 Mathematical Foundation

The current framework is built around the NEXAH Operator, a composite dynamical operator describing field evolution, regime transitions, and geometric instability detection.

Core documentation:

- NEXAH Operator
- Field Dynamics Equations

The operator combines:

- Lorenz-inspired field dynamics
- 2-1-3 regulator
- Kuramoto memory coupling
- Van der Pol oscillation
- Compass modulation
- Winding-number detection
- Iota-ring dynamics
- Janus reversal
- Lyapunov rhythm modulation

These components jointly generate the field structures used for transition detection and navigation.

---

# 🧩 IEEE Test Cases

Primary validation environment for NEXAH.

Contains:

- Benchmark power systems
- State-field extraction
- Controller development
- Navigation studies
- Experimental validation
- Generated results

➡️ Open: ieee_test_cases

---

# 📈 Large-Scale Scaling Validation

A dedicated scaling study investigates whether transition detection remains consistent across network size.

Current benchmark systems:

| Network | Status |
|----------|----------|
| IEEE 118 | ✅ |
| IEEE 300 | ✅ |
| IEEE 1354 | 🟡 Experimental |
| IEEE 9241 PEGASE | 🟡 Experimental |

Scaling experiments are located in:

➡️ ieee_scaling

Current observations suggest that geometric transition signatures emerge consistently across multiple network scales and often appear before classical voltage-collapse indicators.

Further validation is ongoing.

---

# 🧪 EXPERIMENTS

Research and validation studies.

Current experiment series:

| Experiment | Topic |
|------------|--------|
| EXP_01 | Phase Drift Validation |
| EXP_02 | Instability Phase Transitions |
| EXP_03 | Shell Crossing & Recursive Transport |
| EXP_04 | Control Direction & Stabilization |

---

# ⚙️ IEEE Applications

Application layer for practical usage.

Contains:

- Tutorials
- Example workflows
- Data loaders
- Stability analysis scripts
- Navigation demonstrations

➡️ Open: ieee_application

---

# 📊 OUTPUTS

Generated artifacts.

Examples:

- Stability maps
- Vector fields
- Transition graphs
- Animations
- Validation plots
- Experimental reports
- Scaling studies
- Regime transition visualizations

---

# 🌌 IEEE Core Geometry

Field geometry and theoretical research.

Contains:

- Stability fields
- Resonance maps
- Scaling studies
- ODE investigations
- Geometric field analysis
- NEXAH Operator development
- Transition dynamics

➡️ Open: iee_core_geometry

---

# 🏗 NEXAH Architecture

text Power System       ↓ ARCHY Simulation       ↓ Discovery Engine       ↓ Field Construction       ↓ NEXAH Operator       ↓ Regime Detection       ↓ State Graph       ↓ Navigation       ↓ Intervention 

---

# 🎯 Goal

The long-term goal of this project is to move from:

text Simulation     → Observation 

toward:

text Simulation     → Structure Discovery     → Navigation     → Intervention 

using the NEXAH framework.

---

# 📂 Current Structure

text stability_field_dynamics/ │ ├── ieee_test_cases/ │ ├── ieee_application/ │ ├── iee_core_geometry/ │   ├── field_dynamics_equations.md │   ├── nexah_operator.md │   ├── ieee_scaling/ │   └── ... │ └── data/ 

---

# 🔬 Main Research Areas

## Stability Geometry

Investigation of:

- Stability basins
- Collapse boundaries
- Transition corridors
- Attractor structures
- Field topology

---

## Early Warning Detection

Development of:

- Collapse indicators
- Transition probability estimators
- Stability distance metrics
- Adaptive warning systems
- Geometric transition detection

---

## Scaling and Universality

Investigation of:

- network-size independence
- transition timing consistency
- geometric invariants
- scaling behaviour
- benchmark transferability

---

## Navigation

Development of the NEXAH Kernel:

- State-space navigation
- Corridor following
- Stability seeking
- Regime transfer prediction

---

## Active Control

Current research focuses on:

- Field-aware controllers
- Corridor locking
- Predictive stabilization
- Phase-guided navigation
- Adaptive intervention

---

# 📈 Validation Systems

The framework is currently validated on:

| Test Case | Status |
|------------|---------|
| IEEE 9 Bus | ✅ |
| IEEE 14 Bus | ✅ |
| IEEE 30 Bus | ✅ |
| IEEE 57 Bus | ✅ |
| IEEE 118 Bus | ✅ |
| IEEE 300 Bus | ✅ |
| IEEE 1354 Bus | 🟡 Experimental |
| IEEE 9241 Bus | 🟡 Experimental |

---

# 📚 Documentation

Primary documentation:

- START_HERE
- Theory
- Method Pipeline
- Results Summary

Mathematical foundations:

- NEXAH Operator
- Field Dynamics Equations

Application examples:

- IEEE Application

Geometry studies:

- IEEE Core Geometry

---

# 🚀 Development Status

Current maturity level:

| Layer | Status |
|---------|---------|
| Mathematical Model | ✅ Mature |
| Simulation | ✅ Mature |
| Structure Discovery | ✅ Mature |
| Stability Fields | ✅ Mature |
| Scaling Validation | 🟡 Active Validation |
| Navigation | 🟡 Active Development |
| Intervention | 🟡 Active Development |
| Autonomous Agents | 🔬 Experimental |

---

# © NEXAH Framework

Developed as part of the NEXAH research program.

Focus areas:

- Stability Discovery
- Transition Geometry
- Dynamical Systems
- Power Grid Navigation
- Collapse Prevention
- Active Field Control
- Regime Detection
- Stability-Field Dynamics
