# NEXAH Engine

Version 0.9 --- Finite Abstract Interpretation Core

The NEXAH Engine is the executable algebraic and analysis layer of the
NEXAH framework.

It operationalizes finite structural modeling and abstract
interpretation based on order theory and lattice semantics.

![NEXAH Engine --- Execution
Architecture](visuals/engine_architecture_execution_layer_dark.png)

------------------------------------------------------------------------

## 1. Architectural Position

The NEXAH architecture consists of three conceptual layers:

RESEARCH\
→ ENGINE\
→ STRUCTURAL OUTPUT

The Engine translates formal structural theory into executable algebraic
models and finite abstract interpretation systems.

------------------------------------------------------------------------

## 2. Core Operator Stack

The conceptual operator stack is now fully implemented:

FinitePoset\
→ LatticeOps\
→ Closure Operator (Γ)\
→ Interior Operator (Ι)\
→ Monotone Operators\
→ Regime Operator (Δ)\
→ Frame Projection (F)\
→ Fixpoint Structures\
→ Worklist Fixpoint Solver

### Implementation Status

✔ FinitePoset\
✔ LatticeOps (join/meet, distributivity, top/bottom)\
✔ Closure Operator (Γ)\
✔ Interior Operator (Ι)\
✔ Monotone Operators\
✔ Fixpoint-induced structures\
✔ Rank / height analysis\
✔ Hasse cover extraction\
✔ Regime Operator (Δ)\
✔ Frame Projection (F)\
✔ IN/OUT Worklist Fixpoint Solver\
✔ Application Layer (Mini IR + constant propagation)

Finite algebra core complete.\
Finite abstract interpretation operational.

------------------------------------------------------------------------

## 3. What the Engine Now Demonstrates

### Structural Layer

-   Finite partially ordered sets (validated)
-   Lattice construction and distributivity checks
-   Extremal element detection
-   Rank / height computation
-   Hasse cover extraction

### Stabilization Layer

-   Closure operators (extensive / monotone / idempotent)
-   Interior operators (contractive / monotone / idempotent)
-   Fixpoint extraction
-   Fixpoint-induced lattices

### Dynamic Layer

-   Monotone operators with iteration
-   Explicit IN/OUT worklist fixpoint solver
-   Regime restriction (Δ)
-   Frame projection (F)

### Application Layer

-   Finite constant propagation lattice
-   Product state lattice construction
-   Typed Mini IR
-   Linear CFG analysis
-   Branching CFG analysis with join conflict → ⊤

The engine now functions as a finite abstract interpretation kernel.

------------------------------------------------------------------------

## 4. Repository Structure

ENGINE/\
├── core/\
│ ├── poset.py\
│ ├── lattice.py\
│ ├── closure_operator.py\
│ ├── interior_operator.py\
│ ├── monotone_operator.py\
│ ├── fixpoint_lattice.py\
│ ├── worklist_fixpoint.py\
│ ├── rank.py\
│ ├── hasse.py\
│ ├── regime_operator.py\
│ └── frame_operator.py\
│\
├── applications/\
│ ├── constant_lattice.py\
│ ├── mini_ir.py\
│ ├── mini_ir_demo.py\
│ └── mini_ir_branch_demo.py\
│\
├── examples/\
│ └── example_stabilization.py\
│\
└── visuals/

------------------------------------------------------------------------

## 5. Running the Demos

From repository root:

Linear Mini IR:

    python -m ENGINE.applications.mini_ir_demo

Branching Mini IR (join conflict):

    python -m ENGINE.applications.mini_ir_branch_demo

Stabilization example:

    python -m ENGINE.examples.example_stabilization

------------------------------------------------------------------------

## 6. Quality Status

-   76 tests passing
-   Strict carrier enforcement
-   Deterministic IN/OUT semantics
-   `mypy --strict` clean
-   Finite scope intentionally enforced

------------------------------------------------------------------------

## 7. Design Philosophy

The engine is:

-   Finite
-   Deterministic
-   Algebraically validated
-   Explicit in structure
-   Type-safe
-   Extension-oriented

It is not a simulation engine.

It is a structural execution and finite abstract interpretation layer.

------------------------------------------------------------------------

## 8. Known Constraints (Intentional)

-   Finite structures only
-   No widening/narrowing operators yet
-   No infinite lattices
-   No performance scaling layer
-   No visualization export

------------------------------------------------------------------------

## 9. Development Roadmap

Phase A --- Finite Algebra Core ✔

Phase B --- Application Stabilization\
- Convert Mini IR demos into regression tests\
- CI integration (pytest + mypy gate)\
- Coverage threshold enforcement\
- API freeze candidate review

Phase C --- Extended Analysis Layer\
- Widening / narrowing operators\
- Guarded branch modeling\
- Loop analysis examples\
- Transition graph export\
- Visualization layer

------------------------------------------------------------------------

End of NEXAH Engine v0.9
