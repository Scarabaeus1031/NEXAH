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
5. **[archive/README.md](archive/README.md)** — rules for historical designs.

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

Visuals are explanatory artifacts. If a diagram and a normative text disagree,
the normative text governs until the discrepancy is reviewed.

