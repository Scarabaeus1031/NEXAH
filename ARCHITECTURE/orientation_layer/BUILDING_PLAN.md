# Orientation Layer Building Plan

This plan translates the specification into bounded work packages. Later work
does not begin by silently expanding the meaning of earlier components.

## WP0 — Reality baseline

Status: implemented in the v0.7 freeze; final verification is recorded in the
package baseline status and characterization suite.

Work:

- align package, CLI, and documentation version labels
- inventory the current public API and outputs
- add characterization fixtures for v0.7 behavior
- document local map scope, heuristic semantics, and known limitations
- correct confirmed indexing or reproducibility defects separately from the
  baseline record

Acceptance:

- deterministic fixtures exist
- current behavior and edge cases are documented
- no capability claim exceeds the evidence

## WP1 — Orientation language and contracts

Status: implemented and verified. The contracts are backend-independent; WP2
will populate them from the v0.7 baseline.

Work:

- define typed primitives
- implement `OrientationState` and `OrientationReport`
- support serialization and schema evolution
- make provenance and uncertainty mandatory

Acceptance:

- schema and round-trip tests pass
- optional and required fields are explicit
- invalid or unsupported claims fail visibly

## WP2 — v0.7 backend adapter

Status: implemented and verified. The adapter produces a scoped
`OrientationState`, typed empirical transitions, explicit embedding alignment,
and evidence carrying the unchanged v0.7 limitations.

Work:

- wrap the package without changing its internal scientific meaning
- translate backend output into scoped representation objects
- align embedded indices with source observations
- isolate random-state behavior and errors

Acceptance:

- local state identity is marked explicitly
- alignment and deterministic fixtures pass
- the adapter does not claim causal intervention or global maps

## WP3 — Orientation report generation

Status: implemented and verified for the v0.7 backend result. Reports expose
local position, representation-level change, empirical graph reachability,
missing information, assumptions, evidence, and uncalibrated uncertainty.

Work:

- generate position, change, regime, option, evidence, and uncertainty sections
- distinguish observed, inferred, assumed, and unavailable information
- provide a compact human-readable explanation

Acceptance:

- every conclusion references evidence or an explicit assumption
- uncertainty is represented, not hidden
- blocked and missing information are reportable results

## WP4 — Demonstrator validation

Work:

- connect one verified Demonstrator path
- compare the report with a declared baseline
- record reproducible runs and failure cases

Acceptance:

- a clean-environment run produces an `OrientationReport`
- methods, inputs, outputs, and environment are traceable
- limitations accompany the published result

## WP5 — Episodic learning

Work:

- store outcome-linked episodes
- retrieve similar episodes with declared similarity semantics
- feed retrieved context into a new orientation cycle

Acceptance:

- provenance survives storage and retrieval
- updates are inspectable and reversible
- no silent backend mutation occurs

## Later, outside the MVP

Connectors, persistent global maps, planners, execution services, agents, and
domain deployment remain later layers. They require their own validation and
authorization models.

## MVP definition of done

- v0.7 behavior is characterized without overclaiming
- typed contracts are implemented and documented
- provenance and uncertainty are mandatory
- the backend adapter passes fixtures
- one Demonstrator produces an Orientation Report
- baseline comparison and failure cases are published
- execution remains opt-in and outside the core
