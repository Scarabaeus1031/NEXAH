# NEXAH Orientation Layer

This directory is the active planning area for the next NEXAH architecture. It
turns the repository's broader orientation concept into a small, typed, testable
software layer built around evidence and uncertainty.

The text specifications are normative. The diagrams summarize them; code and
tests must verify them.

## Read in this order

1. **[ORIENTATION_LAYER_SPEC.md](ORIENTATION_LAYER_SPEC.md)** — scope,
   responsibilities, contracts, and boundaries.
2. **[BUILDING_PLAN.md](BUILDING_PLAN.md)** — work packages and acceptance
   criteria.
3. **[CONCEPT_TRACEABILITY.md](CONCEPT_TRACEABILITY.md)** — relationship
   between established concepts and actual implementation.
4. **[DECISIONS/0001-janus-identities.md](DECISIONS/0001-janus-identities.md)** —
   separation of JANUS, Janus Bridge, and the scientific operator.
5. **[ADAPTER_LANDSCAPE.md](ADAPTER_LANDSCAPE.md)** — existing adapter lines,
   preservation decisions, and their relationship to WP2.
6. **[SOURCE_ADAPTER_CONTRACT.md](SOURCE_ADAPTER_CONTRACT.md)** — Phase III
   source boundary, invariants, leakage rules, and acceptance evidence.
7. **[IEEE_COUPLED_ADAPTER.md](IEEE_COUPLED_ADAPTER.md)** — coupled entity and
   load-campaign views, physical variables, failure policy, and D–F roadmap.
8. **[PLATEAU_A_CLOSURE.md](PLATEAU_A_CLOSURE.md)** — implemented status,
   Memory V2 evidence, scientific boundaries, and the Phase III gate.
9. **[archive/README.md](archive/README.md)** — rules for historical designs.


## Architecture at a glance

```text
Input + Context
→ Representation Backend
→ Q° Orientation Core
→ Orientation Report
→ Decision Support
→ Outcome + Learning
             ↘ feedback to context and orientation state
```

The current `nexah` package is one representation backend. It is not renamed
or reinterpreted as the complete Orientation Core.

## Visual overview

### Page 1 — System blueprint

![NEXAH Orientation Layer final blueprint](visuals/orientation-layer-final-blueprint.png)

### Page 2 — Implementation plan

![NEXAH Orientation Layer implementation plan](visuals/orientation-layer-implementation-plan.png)

## Current status — Plateau A closure

The following two pages record the implemented state after Memory
Generalization V2. They are status summaries, not substitutes for the linked
specifications, tests, and canonical result files.

### Status page 1 — Orientation Core and episodic path

![NEXAH Orientation Core status after Memory V2](visuals/orientation-core-memory-v2-status-page-1.png)

### Status page 2 — Memory V2 validation and Phase III gate

![NEXAH Memory Generalization V2 validation](visuals/memory-generalization-v2-validation-page-2.png)

The corresponding textual record is
**[PLATEAU_A_CLOSURE.md](PLATEAU_A_CLOSURE.md)**. Phase III begins with the
adapter contract and domain validation; it does not expand the frozen V1 or V2
claims retrospectively.

Visuals are explanatory artifacts. If a diagram and a normative text disagree,
the normative text governs until the discrepancy is reviewed.
