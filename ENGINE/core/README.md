# NEXAH Engine – Core Layer

The core layer implements the structural primitives of the NEXAH Engine.

It provides a minimal, finite, deterministic execution model based on discrete order theory.

![Core Operator Stack](./ENGINE/visuals/core_operator_stack_structure.png)

---

## Scope

The core layer defines:

- Finite partially ordered sets
- Closure operators (Γ)
- Regime restriction operators (Δ)
- Frame projection operators (F)
- Fixpoint detection

All operations remain strictly within finite discrete structures.

No metric space.  
No topology.  
No time parameterization.

---

## Modules

### poset.py
Defines the `FinitePoset` class.

Implements:

- Element storage
- Order relation validation
- Reflexivity check
- Antisymmetry check
- Transitivity check
- Upper and lower set extraction

---

### closure.py
Implements monotone closure operators.

Defines stabilization through iterative application.

---

### regime.py
Defines constraint-based restriction operators.

Implements admissible subset extraction.

---

### frame.py
Defines projection operators for ranking and selection.

Separates structure from interpretation.

---

### fixpoint.py
Implements deterministic fixpoint detection.

Provides convergence verification.

---

## Design Principles

The core layer is:

- Minimal
- Explicit
- Deterministic
- Testable
- Structurally bounded

It is not a simulation engine.

It is a structural execution layer.
