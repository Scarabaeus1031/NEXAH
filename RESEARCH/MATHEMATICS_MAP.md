# NEXAH Mathematics Map

Status: research navigation; non-normative

Purpose: locate mathematical foundations, models, experiments, and historical
sources without merging their authority or duplicating their contents.

## Boundary

This map is not a new mathematical theory, a toolbox, or an additional research
program. It does not make a visual similarity into a shared mechanism and does
not promote historical NEXAH-CODEX claims into current research.

The repository responsibilities remain separate:

```text
NEXAH Research  -> concepts, mathematical framing, open questions, synthesis
Science Lab     -> bounded protocols, evidence, controls, and decisions
ORION           -> certified deterministic structural execution
Library / Books -> cultural, editorial, and narrative interpretation
NEXAH-CODEX     -> frozen exploratory source archive
```

A topic may be connected across these areas without transferring ownership or
authority.

## Common research question

The cross-cutting mathematical question is not whether all investigated systems
share one mechanism. It is:

> Under a declared transformation, what is preserved, transformed, lost,
> unresolved, or left as a residual, and where does the transformation cease to
> support an inference?

For representation-indexed spaces, a transformation may be written as

\[
F_{r\rightarrow s}:D_{rs}\subseteq X_r\longrightarrow X_s.
\]

If a reverse map is declared, the round trip

\[
x\xmapsto{F_{r\rightarrow s}}y
 \xmapsto{F_{s\rightarrow r}}\hat{x}
\]

can be inspected for preservation, information loss, ambiguity, and residual
difference. No inverse, equivalence, common physics, or universal geometry is
implied.

The current formal entry point is
[Evidence-Bound Orientation over Heterogeneous State-Transition Systems](FOUNDATION/STATE_TRANSITION_ORIENTATION_FRAMEWORK_V0_1.md).

The canonical vocabulary and foundations baseline is
[NEXAH Mathematical Foundations and Glossary](FOUNDATION/MATHEMATICAL_FOUNDATIONS_GLOSSARY.md).
Use it before interpreting historical labels or comparing unlike models.

## Reading status

| Code | Meaning |
|---|---|
| `M0` | Established mathematics or standard method |
| `M1` | NEXAH representation or synthesis of known objects |
| `M2` | Reproducible local computational result |
| `M3` | Open formal or empirical hypothesis |
| `S` | Symbolic, heuristic, or visual hypothesis generator |
| `H` | Historical, superseded, rejected, or retained for provenance |

Status applies to a particular statement or artifact, not automatically to an
entire directory. One document may contain several classes.

## System and topic map

| Topic | Standard mathematical object | NEXAH question | Current homes | Status boundary |
|---|---|---|---|---|
| Lorenz | nonlinear ODE, attractor, return map, Lyapunov/FTLE analysis | Which transition and boundary features persist across partitions, projections, and reconstructions? | `APPLIED_CASES/LORENZ/`, `VALIDATION/lorenz/`, `../APPLICATIONS/dynamical_systems/lorenz/` | Standard system `M0`; local reconstructions/results `M1-M2`; general mechanisms `M3` |
| Roessler | nonlinear ODE with rotational chaotic dynamics | Which features survive comparison with Lorenz and Halvorsen, and which are attractor-specific? | `APPLIED_CASES/ROSSLER/`, `APPLIED_CASES/COMPARISONS/`, `VALIDATION/lorenz/run_rossler_validation_suite.py` | `M0-M3` by claim |
| Halvorsen | symmetric chaotic flow | How do coarse graining, gates, reachability, flow decomposition, and residual alignment depend on the representation? | `APPLIED_CASES/HALVORSEN/`, `../APPLICATIONS/dynamical_systems/halvorsen/` | `M0-M3` by claim |
| Kuramoto | coupled phase-oscillator system | Can phase, synchronization, and field projections be compared across unlike systems without identifying their mechanisms? | `VALIDATION/systems/kuramoto/`, `FINDINGS/TRANSITION_PHASE_DYNAMICS/` | Standard model `M0`; cross-system projections `M1-M2`; transfer claims `M3` |
| Mandelbrot / Julia | complex iteration, parameter space, dynamical plane, escape behavior | How do paths through parameter space alter represented boundaries, topology, and transition measures? | `APPLIED_CASES/FRACTAL_SYSTEMS/`, `VALIDATION/fractal/`, `VALIDATION/fractal_tests/` | Standard iteration `M0`; NEXAH transition readings `M1-M3` |
| Prime residues | residue sequence, empirical transition kernel, directed weighted graph | Which sequential structures remain under modulus changes and declared null models? | `FINDINGS/PRIME_MODULAR_RESONANCE/`, `VALIDATION/prime_modular_residue_comparison_01/` | Definitions `M0`; bounded results `M2`; privileged-modulus claims unsupported or `H` |
| CRT and product spaces | Chinese remainder theorem, product and quotient representations | When does a multi-grid representation preserve identity, and what is lost on projection or attempted return? | `VALIDATION/wheel_product_reference_spaces_01/` | Standard theorem `M0`; representation study `M1-M2` |
| Winding and topology | winding number, quotient spaces, graph connectivity, topological invariants | Which invariants are preserved only under declared representation conditions? | `FINDINGS/TRANSITION_PHASE_DYNAMICS/winding_and_topology.md`, bounded controls referenced by the Evidence Atlas | `M0-M2`; universal topology claims excluded |
| Relation–Transition Trace Grid (`RTTG`; historical alias `Ghostgrid`) | multilevel grids, quotient maps, fibers/preimages, relation and transition ledgers, traces, provenance and typed residuals | Which relations persist, which transitions occurred, and which traces remain across changes of scale, carrier, cut, and representation? | `FOUNDATION/MATHEMATICAL_FOUNDATIONS_GLOSSARY.md`; historical 111×111 and visual-equation materials remain with their owning archives | Standard components `M0`; NEXAH composition `M1`; no physical medium or proven Hopf bundle |
| IEEE state spaces | continuation paths, feature spaces, graphs, interpolation, field reconstruction | Which structures are measured, constructed, interpolated, or display-dependent across the trajectory-to-field pipeline? | `../APPLICATIONS/power_systems/`, `../ARCHITECTURE/CORE/field_reconstruction/` | Bounded implementation/results `M1-M2`; physical-field or universal claims unestablished |

## Cross-system comparison spine

The existing work can be navigated through the following descriptive chain:

```text
declared source system
-> trajectory, iteration, or measurement sequence
-> coordinates, cut, partition, or embedding
-> grid, graph, density, phase, or reconstructed field
-> transition, boundary, gate, or residual measurement
-> controls and cross-system comparison
-> bounded interpretation
```

This chain describes recurring work. It is not a mandatory workflow or evidence
that the source systems are mathematically or physically equivalent.

Key comparison entry points:

- [Lorenz versus Halvorsen](APPLIED_CASES/COMPARISONS/lorenz_vs_halvorsen.md)
- [Lorenz versus Roessler versus Halvorsen](APPLIED_CASES/COMPARISONS/lorenz_vs_roessler_vs_halvorsen.md)
- [Transition Phase Dynamics](FINDINGS/TRANSITION_PHASE_DYNAMICS/README.md)
- [Kuramoto validation and cross-system projections](VALIDATION/systems/kuramoto/README.md)
- [Fractal systems](APPLIED_CASES/FRACTAL_SYSTEMS/README.md)
- [Prime Modular Resonance](FINDINGS/PRIME_MODULAR_RESONANCE/README.md)
- [Validation program](VALIDATION/README.md)

## Historical visual geometry

Euclid, Pythagoras, Geometria Nova, the Resonance Cathedral, and associated GLB
models belong to the frozen exploratory provenance of NEXAH. They may be useful
as visual reasoning and representation-history sources. They are not current
proofs, physical evidence, or ORION contracts.

See [Historical NEXAH-CODEX mathematics pointers](HISTORY/CODEX_MATHEMATICS_POINTERS.md).

## Contribution and evidence boundary

The current repository does not establish a new mathematical theorem or a
universal transition mechanism. Its defensible candidate contribution is a
strict, evidence-bound integration of representation, transformation, loss,
boundary, trace, interpretation, and Human authority. See:

- [Core Contribution Test](PAPER_READINESS_AUDIT_2026-08-30/04_CORE_CONTRIBUTION_TEST.md)
- [Novelty Boundary](PAPER_READINESS_AUDIT_2026-08-30/05_NOVELTY_BOUNDARY.md)
- [Evidence Ladder](PAPER_READINESS_AUDIT_2026-08-30/06_EVIDENCE_LADDER.md)

## Maintenance rule

Add a pointer when an existing topic becomes relevant. Do not import an archive
wholesale, duplicate experiment outputs, or promote a symbolic connection by
placement alone. Every new row should identify its owner, claim status,
evidence source, and non-implications.
