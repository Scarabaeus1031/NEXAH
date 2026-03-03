# NEXAH Framework

The official repository for the **NEXAH Framework** —  
a modular system for structural modeling, stabilization, and relational navigation.

![NEXAH Entry Diagram](./NAVIGATOR/visuals/Nexah_Entry_Diagram.png)

---

## Overview

NEXAH is a structured modeling framework designed to analyze and navigate complex systems through explicit relational order, stabilization logic, and transition modeling.

The repository consists of:

- A **finite executable algebra engine**
- A **formal conceptual framework**
- A **research and application layer**

The system is implementation-first and mathematically grounded.

---

# 🏗 Repository Structure

## ENGINE (Executable Core)

Location: `/ENGINE`

Implements finite order-theoretic structures:

- `poset.py` — Finite partially ordered sets (validated)
- `lattice.py` — Join/meet operations, lattice detection, distributivity
- `closure_operator.py` — Closure operators (Γ)
- `monotone_operator.py` — General monotone operators
- `fixpoint_lattice.py` — Induced fixpoint structures
- `worklist_fixpoint.py` — Finite worklist-based fixpoint propagation

Validated via pytest test suite located in `/tests`.

The ENGINE provides the executable backbone of the framework.

---

## FRAMEWORK (Conceptual Layer)

Defines the three structural layers:

- **META** — Relational order
- **ARCHY** — Stabilization logic
- **NEXAH** — Orientation and transition modeling

Includes axioms, operator definitions, system stack documentation, and structural principles.

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

Current state (v0.6):

- Finite algebra engine operational
- Closure and monotone operators validated
- Fixpoint structures supported
- Worklist propagation implemented
- Defensive validation enforced (carrier safety)
- Test suite active (pytest, positive + negative cases)

The system is finite by design and explicitly validated.

Public API boundaries are not yet frozen (pre-1.0).

---

# 📚 Theoretical Foundations

Core formal documents:

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

# 🚀 Development Direction

Current focus:

- Algebra completion (Hasse diagrams, rank/height)
- Robustness hardening (typing, API stabilization, CI)
- Visualization layer
- Regime (Δ) and Frame (F) operators
- Applied case demonstrations

---

# 📦 Versioning

The ENGINE follows semantic versioning principles:

- v0.x → Algebra under construction, API not frozen
- v1.0 → Core algebra stable, API frozen
- v1.x → Backward-compatible extensions
- v2.x → Structural changes

Current version: **v0.6 — Core algebra stabilized + monotone/worklist layer operational**

---

# License

Code: Apache License 2.0  
Documentation & Research: CC BY 4.0  

© 2026 Thomas Hofmann
