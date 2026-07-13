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

Status: implemented as `orientation-mvp-validation-v1`. The canonical Lorenz
Demonstrator produces a report, declared null-baseline comparison, repeated
byte-identical outputs, and committed failure cases. The reference is explicitly
a constructed radial-sheet proxy, not external ground truth.

Work:

- connect one verified Demonstrator path
- compare the report with a declared baseline
- record reproducible runs and failure cases

Acceptance:

- a clean-environment run produces an `OrientationReport`
- methods, inputs, outputs, and environment are traceable
- limitations accompany the published result

## WP5 — Episodic learning

Status: implemented and verified as an initial transparent memory loop. Episodes
link State, Report, and externally observed Outcome; append-only JSONL history is
inspectable and reversible, and similarity retrieval does not mutate the backend.

Work:

- store outcome-linked episodes
- retrieve similar episodes with declared similarity semantics
- feed retrieved context into a new orientation cycle

Acceptance:

- provenance survives storage and retrieval
- updates are inspectable and reversible
- no silent backend mutation occurs

## Post-MVP Plateau A — Memory generalization

Status: V1 and V2 are implemented as separate frozen benchmarks. V1 records
11/12 Top-1 retrievals from one reference per family. V2 uses five references
per family, separates method selection from a held-out test, and reaches 6/6
held-out Top-1 with the selected sequence profile. Its minimum margin is only
0.003172 and its objective remains synthetic family retrieval, not semantic
Outcome relevance.

## Post-MVP Plateau B — Adapter ecosystem

Status: next. Define a small adapter protocol around independent data sources,
domain context, representation features, and traceable outcomes. New adapters
must preserve the Orientation contracts and receive their own validation; they
must not encode domain identity as a similarity shortcut.

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
