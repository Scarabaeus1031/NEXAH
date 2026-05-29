# ⚡ NEXAH Applications for Power-System Stability

Application layer of the NEXAH framework.

This directory contains executable demonstrations, tutorials, workflows, and application-oriented studies showing how NEXAH can be used to analyze, detect, and navigate instability in real power-system environments.

---

# 📖 Overview

NEXAH approaches power-system stability from a geometric perspective.

Instead of monitoring only voltage magnitudes or convergence limits, NEXAH constructs a dynamic field representation of system evolution and investigates:

- transition geometry
- stability corridors
- regime changes
- early-warning signatures
- navigation opportunities

The goal is not merely to detect collapse.

The goal is to understand and navigate the transition process leading toward collapse.

---

## Current Scope

The current application layer focuses on:

- IEEE benchmark systems
- stability transition detection
- field-based collapse analysis
- regime navigation
- large-scale scaling validation

The implementation currently supports validation from IEEE 9-Bus systems up to IEEE 9241-Bus PEGASE networks.

---

# 📂 Contents

| Document | Description |
|-----------|-------------|
| [nexah_tutorial.md](./nexah_tutorial.md) | Step-by-step introduction to NEXAH workflows and concepts. |
| [NEXAH_App_Early_Collapse_Detection.md](./NEXAH_App_Early_Collapse_Detection.md) | Demonstration of predictive instability detection compared to classical indicators. |
| [results/](./results/) | Generated figures, plots, and application outputs. |
| [scripts/](./scripts/) | Example scripts and demonstration workflows. |

---

# 🚀 Demonstration Goals

The application layer focuses on demonstrating that NEXAH can:

- detect instability before classical collapse indicators
- identify transition regions inside the stability field
- locate critical operating points
- provide interpretable geometric information
- support future intervention strategies

---

# ⚡ Core Concepts

The application examples are based on four central ideas.

## 1. Field Representation

System trajectories are embedded into a continuous field representation.

Instead of observing isolated measurements, NEXAH studies the evolving geometric structure of the system.

---

## 2. Transition Detection

Instability is interpreted as a transition between dynamical regimes.

Typical indicators include:

- drift amplification
- loss of coherence
- field fragmentation
- geometric bifurcation
- topological restructuring

---

## 3. Critical Point Identification

NEXAH identifies locations where the system approaches instability.

These regions often appear before traditional collapse indicators become visible.

---

## 4. Navigation

Long-term development aims at active navigation.

```text
Detection
    →
Localization
    →
Prediction
    →
Navigation
    →
Intervention
```

---

# 🔬 Example Application Areas

The framework is designed for:

- transmission grids
- renewable integration studies
- microgrids
- distributed energy systems
- oscillatory infrastructure networks
- complex dynamical systems beyond power engineering

---

# 📊 Typical Outputs

Application runs may generate:

- stability trajectories
- field visualizations
- drift maps
- transition indicators
- collapse-warning metrics
- navigation maps
- intervention studies

---

# 🧪 Early Collapse Detection

One of the primary demonstrations compares:

## Classical Indicators

- minimum voltage
- voltage sensitivity
- power-flow convergence

against

## NEXAH Indicators

- field drift
- geometric curvature
- fragmentation
- transition metrics
- regime-change signatures

The central hypothesis is:

> Instability becomes visible in the field geometry before it becomes visible in voltage trajectories.

---

# 🏗 Relationship to the Framework

This directory represents the application layer of the larger NEXAH architecture.

```text
ARCHY Simulation
        ↓
Discovery Engine
        ↓
Field Construction
        ↓
NEXAH Operator
        ↓
Transition Detection
        ↓
Navigation
        ↓
Application Layer
```

The mathematical foundations are documented in:

- [iee_core_geometry/nexah_operator.md](../iee_core_geometry/nexah_operator.md)
- [iee_core_geometry/field_dynamics_equations.md](../iee_core_geometry/field_dynamics_equations.md)

---

# 📚 Recommended Reading Order

1. NEXAH Tutorial
2. NEXAH Operator
3. Field Dynamics Equations
4. Early Collapse Detection Demo
5. IEEE Scaling Validation

---

# 🎯 Current Status

| Component | Status |
|------------|---------|
| Demonstration Layer | ✅ Functional |
| Early Warning Detection | ✅ Functional |
| IEEE Validation | ✅ Functional |
| Scaling Studies | 🟡 Ongoing |
| Navigation Logic | 🟡 Active Development |
| Intervention Strategies | 🔬 Experimental |

---

# 🚀 Outlook

Future development focuses on:

- larger benchmark systems
- real-world operating profiles
- adaptive intervention strategies
- navigation-based control
- predictive stability management

The long-term objective is to transform instability analysis from a passive monitoring task into an active navigation problem.

---

# © NEXAH Framework

Application layer for stability-field analysis, transition geometry, and predictive navigation in complex dynamical systems.

---
