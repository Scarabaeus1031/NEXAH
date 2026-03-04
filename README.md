# NEXAH Framework

The official repository for the **NEXAH Framework** —  
a modular system for structural modeling, stabilization, and relational navigation.

![NEXAH Entry Diagram](./NAVIGATOR/visuals/Nexah_Entry_Diagram.png)

---
---

## 🔎 Quick Navigation

| Section | Description |
|--------|-------------|
| 🏗 **ENGINE** | Finite algebra engine and abstract interpretation core |
| 📐 **FRAMEWORK** | Conceptual stack (META / ARCHY / NEXAH) |
| 🔬 **RESEARCH** | Theoretical models, stability regimes, and experiments |
| 🚀 **APPLICATIONS** | Real-world system modeling and use cases |
| 🧭 **NAVIGATOR** | Visual documentation and system maps |

---

### Explore the Repository

| Portal | Link |
|------|------|
| Framework Portal | [`NAVIGATOR/framework_portal.md`](./NAVIGATOR/framework_portal.md) |
| Research Portal | [`NAVIGATOR/research_portal.md`](./NAVIGATOR/research_portal.md) |
| Repository Navigator | [`NAVIGATOR/navigator.md`](./NAVIGATOR/navigator.md) |
| Applications Portal | [`NAVIGATOR/applications_portal.md`](./NAVIGATOR/applications_portal.md) |

---

## Overview

NEXAH is a mathematically grounded structural framework for modeling:

- relational order
- stabilization regimes
- orientation and transition systems

The framework integrates:

1. A validated **finite executable algebra engine**
2. A formal **conceptual system stack (META / ARCHY / NEXAH)**
3. A research and application layer

The system is **implementation-first and structurally verified**.

---

## System Pipeline

![NEXAH Research Pipeline](./NAVIGATOR/visuals/nexah_research_pipeline.png)

The NEXAH ecosystem follows a layered development process:

```
Axioms
↓
Principles
↓
Theorems
↓
Operators
↓
Framework
↓
Applications
```

Research concepts are transformed into executable models through the ENGINE and then applied to real-world systems.

---

# 🏗 Repository Structure

## ENGINE (Executable Core) — Stable (v1.0.0)

Location: `/ENGINE`

Implements finite order-theoretic structures and abstract interpretation.

### Structural Algebra
- `poset.py` — Finite partially ordered sets (validated)
- `lattice.py` — Join/meet, lattice checks, distributivity
- `hasse.py` — Cover extraction
- `rank.py` — Height analysis

### Stabilization Layer
- `closure_operator.py` — Closure operators (Γ)
- `interior_operator.py` — Interior operators (Ι)
- `monotone_operator.py` — Monotone maps + fixpoints
- `fixpoint_lattice.py` — Induced fixpoint structures

### Dynamic Layer
- `worklist_fixpoint.py` — Explicit IN/OUT worklist solver
- `regime_operator.py` — Regime restriction (Δ)
- `frame_operator.py` — Frame projection (F)

### Application Layer
- `constant_lattice.py` — Finite constant propagation lattice
- `mini_ir.py` — Typed Mini IR
- Linear and branching CFG analysis demos

Validated via pytest test suite (`/tests`).

---

## FRAMEWORK (Conceptual Stack)

Defines the three structural layers:

- **META** — Relational order (formalized in ENGINE)
- **ARCHY** — Stabilization regimes (formalized in ENGINE)
- **NEXAH** — Orientation and transition modeling

The ENGINE operationalizes large parts of META and ARCHY.

---

## RESEARCH

Applied cases and exploratory models including:

- stability detection
- regime shifts
- transition modeling
- multi-regime interaction
- prototype development

---

# 🧪 Implementation Status

Current release: **v1.0.0**

- finite algebra engine stable
- monotone + fixpoint structures validated
- IN/OUT worklist solver operational
- constant propagation application layer implemented
- **95% test coverage**
- `mypy --strict` clean
- API frozen for finite scope

The system is **finite by design and structurally verified**.

---

# 📚 Theoretical Foundations

- [Axioms](./axioms.md)
- [Theorems](./theorems.md)
- [Minimal Logic](./minimal_logic.md)
- [Relational Model](./relational_model.md)
- [Frame Operator](./frame_operator.md)
- [Regime Operator](./regime_operator.md)

---

# 🧩 Modules

→ [Modules Overview](./FRAMEWORK/modules.md)

---

# 🧠 Research & Applications

- [Research Papers](./research_papers.md)
- [Application Cases](./application_cases.md)

---

# 📦 Versioning

The ENGINE follows semantic versioning:

- v1.0 → Finite core stable, API frozen
- v1.x → Backward-compatible extensions
- v2.x → Structural changes

Current version: **v1.0.0**

---

# License

Code: Apache License 2.0  
Documentation & Research: CC BY 4.0  

© 2026 Thomas Hofmann- **NEXAH** — Orientation and transition modeling

The ENGINE operationalizes large parts of META and ARCHY.

---

## RESEARCH

Applied cases and exploratory models:

- Stability detection
- Regime shifts
- Transition modeling
- Multi-regime interaction
- Prototype roadmap

---

# 🧪 Implementation Status

Current release: **v1.0.0**

- Finite algebra engine stable
- Monotone + fixpoint structures validated
- IN/OUT worklist solver operational
- Constant propagation application layer implemented
- 95% test coverage (core modules)
- `mypy --strict` clean
- API frozen for finite scope

The system is finite by design and structurally verified.

---

# 📚 Theoretical Foundations

- [Axioms](./axioms.md)
- [Theorems](./theorems.md)
- [Minimal Logic](./minimal_logic.md)
- [Relational Model](./relational_model.md)
- [Frame Operator](./frame_operator.md)
- [Regime Operator](./regime_operator.md)

---

# 🧩 Modules

→ [Modules Overview](./FRAMEWORK/modules.md)

---

# 🧠 Research & Applications

- [Research Papers](./research_papers.md)
- [Application Cases](./application_cases.md)

---

# 📦 Versioning

The ENGINE follows semantic versioning:

- v1.0 → Finite core stable, API frozen
- v1.x → Backward-compatible extensions
- v2.x → Structural changes

Current version: **v1.0.0**

---

# License

Code: Apache License 2.0  
Documentation & Research: CC BY 4.0  

© 2026 Thomas Hofmann
