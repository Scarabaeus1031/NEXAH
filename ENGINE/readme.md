# NEXAH Engine

**Version 1.0 — Finite Abstract Interpretation Kernel**

The NEXAH Engine is the **executable algebraic and analysis layer** of the
NEXAH framework.

It operationalizes **finite structural modeling and abstract interpretation**
based on **order theory and lattice semantics**.

![NEXAH Engine — Execution Architecture](visuals/engine_architecture_execution_layer_dark.png)

For the full architectural report see:

`ENGINE_REPORT_v1.md`

---

# 1. Architectural Position

The NEXAH architecture consists of three conceptual layers:

RESEARCH (formal structure)
↓
ENGINE (structural execution)
↓
STRUCTURAL OUTPUT


The Engine translates formal structural theory into executable algebraic
models and finite abstract interpretation systems.

---

# 2. Core Operator Stack

The conceptual operator stack implemented by the engine:

FinitePoset
↓
LatticeOps
↓
Closure Operator Γ
↓
Interior Operator Ι
↓
Monotone Operators
↓
Regime Operator Δ
↓
Frame Projection F
↓
Fixpoint Structures
↓
Worklist Fixpoint Solver

### Implementation Status

✔ FinitePoset  
✔ LatticeOps (join/meet, distributivity, top/bottom)  
✔ Closure Operator (Γ)  
✔ Interior Operator (Ι)  
✔ Monotone Operators  
✔ Fixpoint-induced structures  
✔ Rank / height analysis  
✔ Hasse cover extraction  
✔ Regime Operator (Δ)  
✔ Frame Projection (F)  
✔ IN/OUT Worklist Fixpoint Solver  
✔ Application Layer (Mini IR + constant propagation)

The finite algebra core is complete and operational.

---

# 3. What the Engine Demonstrates

## Structural Layer

• Finite partially ordered sets (validated)  
• Lattice construction and distributivity checks  
• Extremal element detection  
• Rank / height computation  
• Hasse cover extraction  

## Stabilization Layer

• Closure operators (extensive / monotone / idempotent)  
• Interior operators (contractive / monotone / idempotent)  
• Fixpoint extraction  
• Fixpoint-induced lattices  

## Dynamic Layer

• Monotone operators with iteration  
• Explicit IN/OUT worklist fixpoint solver  
• Regime restriction (Δ)  
• Frame projection (F)

## Application Layer

• Finite constant propagation lattice  
• Product state lattice construction  
• Typed Mini IR  
• Linear CFG analysis  
• Branching CFG analysis with join conflict → ⊤

The engine therefore acts as a **finite abstract interpretation kernel**.

---

# 4. Repository Structure

ENGINE/
├ core/
├ applications/
├ examples/
├ visualization/
├ visuals/
├ ENGINE_REPORT_v1.md
└ readme.md

---

# 5. Running the Examples

From repository root:

### Linear Mini IR

python -m ENGINE.applications.mini_ir_demo

### Branching Mini IR

python -m ENGINE.applications.mini_ir_branch_demo

python -m ENGINE.examples.example_stabilization

---

# 6. Quality Status

• 89 tests passing  
• ~95% coverage  
• Strict carrier enforcement  
• Deterministic IN/OUT semantics  
• `mypy --strict` clean  
• Finite scope intentionally enforced  

---

# 7. Design Philosophy

The NEXAH Engine is designed to be:

• Finite  
• Deterministic  
• Algebraically validated  
• Explicit in structure  
• Type-safe  
• Extension-oriented  

It is **not a simulation engine**.

It is a **structural execution and finite abstract interpretation layer**.

---

# 8. Intentional Constraints

Version 1.0 intentionally restricts the system to finite domains:

• Finite structures only  
• No widening/narrowing operators yet  
• No infinite lattices  
• No probabilistic semantics  
• No performance scaling layer  
• No visualization export pipeline  

These constraints define the **v1.0 stability boundary**.

---

# 9. Development Path

### Phase A — Finite Algebra Core ✔

Completed.

### Phase B — Stabilization (v1.0)

• CI integration (pytest + mypy)  
• Coverage threshold enforcement  
• API freeze candidate review  

### Phase C — Extended Analysis

• Widening / narrowing operators  
• Guard-sensitive branch modeling  
• Loop analysis extensions  
• Transition graph export  
• Visualization layer  

---

**NEXAH Engine v1.0**

Finite. Deterministic. Structurally Verified.

