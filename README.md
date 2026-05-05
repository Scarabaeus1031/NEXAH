# ⚡ NEXAH — A Geometric Framework for Dynamical Systems

![Status](https://img.shields.io/badge/status-research--active-orange)
![Validation](https://img.shields.io/badge/validation-in%20progress-yellow)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![Focus](https://img.shields.io/badge/focus-dynamical%20systems-lightgrey)

> A framework for discovering and navigating structure in dynamical systems.

> **Status:** Active research system — validation and kernel integration in progress

---

> NEXAH reconstructs structure, transitions, and stability  
> directly from system dynamics.

> It reveals how systems move, where transitions occur, and when they are triggered.

> Complex systems are not random.  
> They evolve within **structured fields that constrain motion, transitions, and outcomes**.

---

## 🧭 Conceptual Overview

![NEXAH Core System](ARCHITECTURE/archive/NEXAH_Regime_Atlas.png)

*NEXAH connects continuous dynamics with discrete transition structure across regimes.*

---

## 🧠 What NEXAH Does

NEXAH reconstructs **latent structure from dynamical systems**.

It transforms:

```text
raw trajectories → continuous field → structured regions → transition dynamics
```

into a representation that makes systems:

```text
observable → structurally interpretable → navigable
```

This enables:

- detection of transition regions (gates, boundaries)  
- identification of stable regimes (basins)  
- reconstruction of system geometry  
- simulation of motion within learned structure  

---

## 🔬 Research & Findings

📂 [`RESEARCH/`](RESEARCH/)

NEXAH is grounded in a structured research layer:

- empirical findings across systems  
- structural models (field, vessel, transitions, phase)  
- cross-system invariance analysis  

👉 Start here:

- [`RESEARCH/RESEARCH_INDEX.md`](RESEARCH/RESEARCH_INDEX.md)  
- [`RESEARCH/CORE_CONCEPT_MAP.md`](RESEARCH/CORE_CONCEPT_MAP.md)  

Then:

- [`RESEARCH/FOUNDATION/`](RESEARCH/FOUNDATION/)  
- [`RESEARCH/CORE_CONCEPTS/`](RESEARCH/CORE_CONCEPTS/)  
- [`RESEARCH/VALIDATION/`](RESEARCH/VALIDATION/)

---

## 🔬 Core Idea

Traditional approaches model:

```text
state → next state
```

NEXAH instead models:

```text
motion within a structured field
```

Where:

- stability = alignment with field structure  
- instability = drift into low-density or conflicting regions  
- transitions = movement across structured regions  
- **phase mismatch = trigger of transitions**

---

### 🔁 Phase & Control Extension (New)

Recent validation results show:

```text
Transitions are not only triggered by phase mismatch,
but can be causally influenced through phase-aligned control.
```

Key empirical result:

```text
Control effectiveness depends on direction relative to phase dynamics.
```

Observed behavior:

- phase-aligned control → amplifies drift and transition activity  
- phase-opposed control → suppresses drift and transitions  
- inverse control → stabilizes system near zero-drift regime  

This leads to an extended mechanism:

```text
phase → mismatch → transition
            ↑
        control (directional)
```

Interpretation:

- instability defines potential  
- phase mismatch triggers transitions  
- control direction determines whether dynamics amplify or stabilize  

This establishes a closed-loop causal structure:

```text
system dynamics ↔ phase ↔ control
```

and introduces a new control principle:

> effective control is achieved by opposing intrinsic phase-aligned instability,  
> not by reducing system magnitude.

---

---

## 🧪 Demonstrator (Reproducible Core)

📂 [`NEXAH_DEMONSTRATOR/`](NEXAH_DEMONSTRATOR/)  

The demonstrator provides a **minimal, reproducible implementation** of the core pipeline  
and serves as the recommended entry point.

It includes:

- field construction from trajectories  
- Gate Operator (continuous instability field)  
- Transition Structure (discrete sheet dynamics)  
- Navigation Kernel (geometry-aware motion)  

👉 Start here:  
- [`NEXAH_DEMONSTRATOR/README.md`](NEXAH_DEMONSTRATOR/README.md)

👉 Core components:  
- `gate_operator.md`  
- `transition_structure.md`  
- `navigation_kernel.md`  

---

## 🌊 Field Reality (Example)

![Off-Manifold Flow](FRAMEWORK/NEXAH/geometry/visuals/ieee57_v69_off_manifold_flow.png)

*System motion follows a constrained flow field — transitions occur only along admissible paths.*

---

## 🎯 Structure-Aware Field (Control View)

![Structure-Aware Target Field](NEXAH_CORE/outputs/ieee_gates/v37_structure_field.png)

*Control emerges from alignment with system geometry rather than external forcing.*

---

## 🧪 Validation (Empirical Layer)

📂 [`RESEARCH/VALIDATION/`](RESEARCH/VALIDATION/)

NEXAH has been tested across:

- chaotic systems (Lorenz, Halvorsen)  
- controlled experiments (transition modulation)  
- real-world inspired systems (power grids)  

Key observations (validated across tested systems):

- early detection of transition behavior before instability  
- structure remains robust under noise  
- transition geometry persists across systems  

These results indicate that transition structure is not system-specific,  
but an emergent property of dynamical systems.

👉 See:
- [`RESEARCH/VALIDATION/validation_summary.md`](RESEARCH/VALIDATION/validation_summary.md)

### 🔬 Fractal Transition Extension

![Fractal Transition Validation](RESEARCH/VALIDATION/visuals/Nexah-Fractal_Transition_Validation.png)

```text
parameter motion → mismatch → transitions
Δ(t) ≈ M(t)
```

→ Demonstrates externally induced transitions in structured systems.

---

## 🧠 Structural Insight (Unified View)

![NEXAH Core Structure](RESEARCH/FINDINGS/visuals/nexah_core_structure_diagram.png)

*Unified structural hierarchy: field dynamics, transition geometry, phase dynamics, and control layer.*

---

## 🧩 Core Modules

### 🔷 Field & Transition System

```text
NEXAH_CORE/
```

Implements:

- field reconstruction  
- transition detection (gates, basins)  
- probabilistic instability modeling  
- structure-aware trajectory analysis  

---

### 🔷 Demonstrator (Reference Implementation)

```text
NEXAH_DEMONSTRATOR/
```

- minimal working system  
- reproducible experiments  
- empirical validation layer  

---

## 🔷 System Perspective

NEXAH integrates:

```text
Field (continuous)
↔ Geometry (structure)
↔ Graph (transitions)
↔ Phase (causal dynamics)
↔ Control (trajectory navigation)
```

Interpretation:

- field → defines motion  
- geometry → defines constraints  
- graph → encodes transition structure  
- phase → defines transition activation  
- control → navigates trajectories within these constraints  

---

## 🔬 Current Capabilities

✔ field reconstruction from data  
✔ stability as spatial structure  
✔ transition detection (gates, basins)  
✔ probabilistic transition modeling  
✔ trajectory simulation within learned fields  

---

## ⚠️ Current Limitations

❌ no unified runtime kernel  
❌ limited large-scale validation  
❌ early-stage control integration  
❌ not production-ready  

---

## 🚀 Quick Start

```bash
pip install -e .
# or
pip install -r requirements.txt

python run_nexah_demo.py
```

---

## 📚 Documentation

- 📊 [System State](ARCHITECTURE/SYSTEM_STATE.md)  
- 🔬 [Methods](ARCHITECTURE/METHODS.md)  
- 🧭 [Architecture](ARCHITECTURE/README.md)  
- 🌀 [Visual Gallery](VISUAL_GALLERY.md)  
- 🧠 [Research Vision](RESEARCH/RESEARCH_VISION.md)

---

## 🧠 Learn More

👉 [START_HERE.md](START_HERE.md)

---

## ⚡ Core Insight

```text
Stability is not a scalar value.

It is a region within a structured field.
```

---

## 🧭 Final Statement

```text
A system does not fail randomly.

It moves through structured transition regions
that constrain what outcomes are possible.
```

---

## 🔬 Try It Yourself

NEXAH is designed to be explored.

Run the demonstrator, test different systems,  
and observe how structure emerges from dynamics.

→ The system is not just described — it can be experienced.

---

**Thomas K. R. Hofmann · NEXAH · 2026**
