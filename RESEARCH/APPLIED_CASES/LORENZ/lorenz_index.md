# 🧭 NEXAH — Lorenz Repository Index

Lorenz is used across NEXAH as a synthetic dynamical-system benchmark,
development example, and source of exploratory method studies. The repository
contains several independent Lorenz lineages; they should not be interpreted as
one fully validated pipeline.

## Current Entry Points

| Area | Role | Status |
|---|---|---|
| **[Validation](../../VALIDATION/lorenz/)** | Multi-run and noise experiments | Current validation material |
| **[Dynamical-systems application](../../../APPLICATIONS/dynamical_systems/lorenz/)** | Lorenz-specific analysis modules | Application experiments |
| **[Core demos](../../../APPLICATIONS/core_demos/lorenz/)** | Density, fields, regimes, navigation, and control demos | Experimental demo collection |
| **[Minimal Lorenz demo](../../../APPLICATIONS/demos/lorenz_demo/)** | Small user-facing example | Application demo |
| **[Discovery Engine](../../../EXPERIMENTAL/BUILDER_LAB/DISCOVERY_ENGINE/)** | Historical V4–V22 development series | Experimental lineage |
| **[Discovery observations](../../../EXPERIMENTAL/BUILDER_LAB/DISCOVERY_ENGINE/DISCOVERY_OBSERVATIONS.md)** | Evidence-aware interpretation of V4–V22 | Historical observation record |

## Recommended Reading Path

1. Start with the current validation results in `RESEARCH/VALIDATION/lorenz/`.
2. Use the application and demo directories for current runnable investigations.
3. Consult the Discovery Engine to understand how earlier probability, field,
   operator, and lag ideas developed.
4. Treat generated visuals as experiment artifacts, not standalone validation.

## Interpretation Boundary

The Lorenz system is valuable because its dynamics are known, inexpensive to
simulate, and structurally rich. Success on Lorenz can demonstrate that code or
a representation behaves as designed in a synthetic setting. It does not by
itself establish:

- cross-system generality
- physical equivalence to power-system dynamics
- predictive superiority
- operational control capability
- validation of every NEXAH mechanism

Power-system work has its own benchmark simulations and evidence paths under
**[APPLICATIONS/power_systems/](../../../APPLICATIONS/power_systems/)**.

---

**Last reviewed:** July 12, 2026
