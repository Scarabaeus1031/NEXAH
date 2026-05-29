# ⚡ Stability Field Dynamics

A collection of NEXAH-based experiments, applications, and validation studies for stability analysis, transition geometry, and navigation in complex dynamical systems.

---

## 📖 Overview

This directory contains the practical implementation and validation environment of the NEXAH framework.

The project is currently organized into three major areas:

| Folder | Description |
|----------|-------------|
| [ieee_test_cases](./ieee_test_cases/) | Core validation environment containing experiments, analysis pipelines, state-field extraction, navigation research, and controller development across IEEE benchmark systems. |
| [ieee_application](./ieee_application/) | Application layer demonstrating practical NEXAH workflows, tutorials, loaders, and power-grid navigation examples. |
| [ieee_core_geometry](./ieee_core_geometry/) | Geometric and field-theoretic research environment containing stability-field construction, resonance maps, regime dynamics, scaling studies, and visualization frameworks. |
| [data](./data/) | Supporting datasets, generated inputs, and auxiliary resources used throughout the framework. |

---

# 🧩 CORE

Core implementation of the NEXAH framework.

Contains:

- ARCHY simulation layer
- Discovery Engine
- Field Layer
- State Graph generation
- NEXAH Kernel
- Navigation and control logic

# 🧩 IEEE Test Cases

Primary validation environment for NEXAH.

Contains:

- Benchmark power systems
- State-field extraction
- Controller development
- Navigation studies
- Experimental validation
- Generated results

➡️ Open: [ieee_test_cases](./ieee_test_cases/)

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

# ⚙️ IEEE Applications

Application layer for practical usage.

Contains:

- Tutorials
- Example workflows
- Data loaders
- Stability analysis scripts
- Navigation demonstrations

➡️ Open: [ieee_application](./ieee_application/)

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

# 🌌 IEEE Core Geometry

Field geometry and theoretical research.

Contains:

- Stability fields
- Resonance maps
- Scaling studies
- ODE investigations
- Geometric field analysis

➡️ Open: [ieee_core_geometry](./ieee_core_geometry/)

---

# 🏗 NEXAH Architecture

```text
Power System
      ↓
ARCHY Simulation
      ↓
Discovery Engine
      ↓
Field Layer
      ↓
State Graph
      ↓
NEXAH Kernel
      ↓
Navigation
      ↓
Intervention
```

---

# 🎯 Goal

The long-term goal of this project is to move from:

```text
Simulation
    →
Observation
```

toward:

```text
Simulation
    →
Structure Discovery
    →
Navigation
    →
Intervention
```

using the NEXAH framework.

---

# 📂 Current Structure

```text
stability_field_dynamics/
│
├── ieee_test_cases/
│   ├── core/
│   ├── pipeline/
│   ├── analysis/
│   ├── controller_lab/
│   ├── experiments/
│   ├── outputs/
│   └── documentation/
│
├── ieee_application/
│   ├── scripts/
│   ├── results/
│   └── tutorials/
│
├── ieee_core_geometry/
│   ├── core_odes/
│   ├── phi_geometry/
│   ├── resonance_maps/
│   ├── ieee_scaling/
│   └── outputs/
│
└── data/
```

---

# 🔬 Main Research Areas

### Stability Geometry

Investigation of:

- Stability basins
- Collapse boundaries
- Transition corridors
- Attractor structures
- Field topology

---

### Early Warning Detection

Development of:

- Collapse indicators
- Transition probability estimators
- Stability distance metrics
- Adaptive warning systems

---

### Navigation

Development of the NEXAH Kernel:

- State-space navigation
- Corridor following
- Stability seeking
- Regime transfer prediction

---

### Active Control

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
| IEEE 1354 Bus | Experimental |
| IEEE 9241 Bus | Experimental |

---

# 📚 Documentation

Primary documentation:

- [START_HERE](./ieee_test_cases/START_HERE.md)
- [Theory](./ieee_test_cases/theory_stability_field.md)
- [Method Pipeline](./ieee_test_cases/method_pipeline.md)
- [Results Summary](./ieee_test_cases/results_summary.md)

Application examples:

- [IEEE Application](./ieee_application/README.md)

Geometry studies:

- [IEEE Core Geometry](./ieee_core_geometry/README.md)

---

# 🚀 Development Status

Current maturity level:

| Layer | Status |
|---------|---------|
| Simulation | ✅ Mature |
| Structure Discovery | ✅ Mature |
| Stability Fields | ✅ Mature |
| State Graphs | ✅ Mature |
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

---
