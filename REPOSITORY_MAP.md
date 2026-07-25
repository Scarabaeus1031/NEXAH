# 🧭 NEXAH — Repository Map

This document maps the current repository structure and identifies the
recommended entry point for each type of reader.

NEXAH is an **evidence-bound orientation ecosystem** composed of six coordinated
subsystems: Research, Orientation Language, Implementations, Applications, the
Living Library, and the Editorial Operating System. Each has a separate
responsibility and authority. Supporting architecture, validation, prototype,
and historical areas make those responsibilities inspectable.

**Current-state review:** July 22, 2026

---

## 🚀 Start Here

| Goal | Entry point |
|---|---|
| Get the full overview | **[README.md](README.md)** |
| Read the published Orientation Language | **[ORIENTATION_LANGUAGE/README.md](ORIENTATION_LANGUAGE/README.md)** |
| Use or develop the current implementation | **[nexah/README.md](nexah/README.md)** |
| Enter the research layer | **[RESEARCH/README.md](RESEARCH/README.md)** |
| Evaluate applications and claims | **[APPLICATIONS/README.md](APPLICATIONS/README.md)** |
| Enter the visual Library | **[THE ATLAS OF ATLASES](docs/library/atlas-of-atlases/README.md)** |
| Inspect Library architecture and reader journeys | **[LIBRARY/README.md](LIBRARY/README.md)** |
| Understand editorial governance | **[EDITORIAL_OPERATING_SYSTEM/README.md](EDITORIAL_OPERATING_SYSTEM/README.md)** |
| Inspect non-canonical review instruments | **[Review Toolbox](EDITORIAL_OPERATING_SYSTEM/living_concepts/review/README.md)** |
| Inspect adopted governance and constitutional principles | **[GOVERNANCE/README.md](GOVERNANCE/README.md)** · **[Ecosystem Constitution v1.0](GOVERNANCE/ECOSYSTEM_CONSTITUTION.md)** |
| Inspect architecture and system state | **[ARCHITECTURE/README.md](ARCHITECTURE/README.md)** |
| Run the executable Demonstrator path | **[PROTO_CORE/NEXAH_DEMONSTRATOR/](PROTO_CORE/NEXAH_DEMONSTRATOR/README.md)** |

Recommended first path:

```text
README
→ choose a responsible subsystem
→ follow its local entry point
→ inspect evidence, authority, and boundaries
```

---

## 🗂️ Top-Level Structure

```text
NEXAH/
├── RESEARCH/                     hypotheses, experiments, evidence, findings
├── ORIENTATION_LANGUAGE/         canonical OLS specification and releases
├── nexah/                        maintained Orientation Kernel implementation
├── APPLICATIONS/                 domain and use-case realizations
├── LIBRARY/                      Works, Registry, Editions, reader journeys
├── EDITORIAL_OPERATING_SYSTEM/   review, explanation, governance, execution
│
├── ARCHITECTURE/                 relationships, state, methods, boundaries
├── GOVERNANCE/                   cross-system constitutional review
├── PROTO_CORE/                   demonstrators and prototype lineages
├── EXPERIMENTAL/                 active labs and historical systems
├── validation/                   reproducible validation campaigns and records
├── tests/                        automated repository verification
├── testkit/                      observed-evidence and outcome gates
├── assets/                       maintained public documentation assets
├── docs/                         cross-system and visual reader documentation
├── README.md           repository overview
├── REPOSITORY_MAP.md   directory and reader navigation
├── CONTRIBUTING.md     contribution and subsystem routing
├── CODE_OF_CONDUCT.md  participation expectations
└── SECURITY.md         security scope and reporting
```

The six primary areas are coordinated responsibilities, not one linear
pipeline:

```text
Research                 → evidence
Orientation Language     → semantics
Implementations          → executable behavior
Applications             → domain use and validation
Living Library           → editorial communication
Editorial Operating System → governance and controlled execution
```

Cross-cutting architecture, provenance, validation, security, and version
history support all six areas. `GOVERNANCE/` maintains the adopted
constitutional baseline and cross-system governance; it is not a seventh
subsystem and grants no authority by repository placement.

---

## 🧭 ORIENTATION_LANGUAGE/

**[ORIENTATION_LANGUAGE/](ORIENTATION_LANGUAGE/)** is the canonical subsystem
entry point for the published Orientation Language Specification. The current
immutable publication is
**[OLS-RELEASE-1.0.0](ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/PUBLICATION_SUMMARY.md)**.

Research may inform the language, but it does not define released semantics.
The Library communicates orientation, applications select declared semantics,
and implementations execute or support them without becoming semantic
authority.

---

## 🧭 EDITORIAL_OPERATING_SYSTEM/

**[EDITORIAL_OPERATING_SYSTEM/](EDITORIAL_OPERATING_SYSTEM/)** describes the
reusable coordination layer joining editorial knowledge, reader context,
orientation, human governance, controlled execution, and verification.

The Orientation Kernel is its reasoning core. The NEXAH Living Library is its
first reference implementation. Potential Wikipedia, museum, education,
research, enterprise, and personal-AI integrations remain application patterns
until an adapter, working demonstration, and domain-appropriate validation
exist.

Its main README carries the coherent architectural narrative. A separate
system-boundary document records changing implementation facts, while dated
visual snapshots preserve historical states without presenting them as current
forever.

The non-canonical **[Review Toolbox](EDITORIAL_OPERATING_SYSTEM/living_concepts/review/README.md)**
indexes five bounded review instruments for recurrence, independence, process,
model-space, and representation analysis. These reviews preserve
counterexamples and uncertainty; they do not create Registry, Operator, OLS,
Kernel, or Architecture authority.

---

## 📚 LIBRARY/

**[LIBRARY/](LIBRARY/)** contains the canonical, human-reviewable bridge to the
visual NEXAH Library on Are.na. It holds stable Entity IDs, Editions, controlled
Operator Concepts, and curated relationships for the initial ten-work pilot.

New readers enter through **[THE ATLAS OF ATLASES](docs/library/atlas-of-atlases/README.md)**,
the first-class visual onboarding module under `docs/library/`. It provides a
59-page approved reading sequence across six atlas fields and the Library
appendix while preserving 13 additional source pages as supplements.

Are.na remains authoritative for visual source content and live publication
state. The repository documentation is authoritative for this approved reader
sequence. The Registry is authoritative for NEXAH identity and classification.
Executable read-only queries live in `nexah/library/`.

---

## 🏗️ ARCHITECTURE/

**[ARCHITECTURE/](ARCHITECTURE/)** describes the current system model,
component relationships, methods, and implementation frontier.

Key documents:

- **[ARCHITECTURE/README.md](ARCHITECTURE/README.md)** — conceptual architecture
- **[ARCHITECTURE/SYSTEM_STATE.md](ARCHITECTURE/SYSTEM_STATE.md)** — current implemented state and limitations
- **[ARCHITECTURE/METHODS.md](ARCHITECTURE/METHODS.md)** — methods overview

The `archive/` subdirectory preserves earlier diagrams and architectural
snapshots. It is reference material, not the current implementation map.

Completed repository-level architecture reviews are preserved under
**[ARCHITECTURE/reviews/](ARCHITECTURE/reviews/)** rather than occupying the
repository root.

---

## ⚖️ GOVERNANCE/

**[GOVERNANCE/](GOVERNANCE/README.md)** contains the adopted
**[Ecosystem Constitution v1.0](GOVERNANCE/ECOSYSTEM_CONSTITUTION.md)** and the
cross-system Governance Index.

Governance is cross-cutting review material. It does not replace OLS
Specification Governance, Library or Registry authority, Editorial Governance,
Architecture decisions, or the responsibility of any primary subsystem.

The earlier
**[Constitution Review 01](GOVERNANCE/constitution_review_01/README.md)**
remains preserved as non-canonical historical review evidence.

---

## 🧪 PROTO_CORE/

**[PROTO_CORE/](PROTO_CORE/)** contains the main reference implementations.

| Area | Role |
|---|---|
| **[NEXAH_DEMONSTRATOR/](PROTO_CORE/NEXAH_DEMONSTRATOR/)** | Canonical hands-on demonstration |
| **[NEXAH_CORE/](PROTO_CORE/NEXAH_CORE/)** | Experimental transition and structural mechanisms |
| **[FIELD_LAYER/](PROTO_CORE/FIELD_LAYER/)** | Continuous field reconstruction and navigation geometry |

The demonstrator is the preferred executable entry. `NEXAH_CORE` and
`FIELD_LAYER` contain broader prototype material and should be read as research
implementations rather than a stable public API.

---

## 📦 nexah/

**[nexah/](nexah/)** is the installable Python package configured by
`pyproject.toml`.

It currently provides:

- the frozen v0.7 trajectory and state-space baseline;
- typed source adapters, Orientation States, evidence-bound reports, and
  append-only episodic memory;
- Network Orientation and IEEE Geometry application modules;
- Living Library queries, health checks, snapshots, traversability reports,
  and the separately guarded Editorial Writer;
- a read-only Living Concepts Answer Adapter;
- the `nexah` command-line interface.

The package remains a bounded implementation collection rather than one unified
runtime for every repository lineage. Its Library and Living Concepts modules
do not acquire editorial or semantic authority merely by being executable, and
it does not integrate every research mechanism found in `PROTO_CORE`,
`RESEARCH`, or `APPLICATIONS`.

---

## 🔬 RESEARCH/

**[RESEARCH/](RESEARCH/)** is the conceptual and empirical research archive.

Recommended entry:

- **[RESEARCH/README.md](RESEARCH/README.md)** — concise research portal
- **[RESEARCH/RESEARCH_INDEX.md](RESEARCH/RESEARCH_INDEX.md)** — detailed navigation
- **[RESEARCH/ABSTRACT.md](RESEARCH/ABSTRACT.md)** — compact research summary
- **[RESEARCH/CORE_CONCEPT_MAP.md](RESEARCH/CORE_CONCEPT_MAP.md)** — concept relationships

Main areas:

| Area | Role |
|---|---|
| **[FOUNDATION/](RESEARCH/FOUNDATION/)** | Structural assumptions and vocabulary |
| **[CORE_CONCEPTS/](RESEARCH/CORE_CONCEPTS/)** | Field, phase, mismatch, geometry, and JANUS |
| **[VALIDATION/](RESEARCH/VALIDATION/)** | Empirical and cross-system validation |
| **[FINDINGS/](RESEARCH/FINDINGS/)** | Condensed observations |
| **[APPLIED_CASES/](RESEARCH/APPLIED_CASES/)** | System-specific research cases |
| **[FIGURES/](RESEARCH/FIGURES/)** | Curated research and paper figures |
| **[THEORETICAL_EXTENSIONS/](RESEARCH/THEORETICAL_EXTENSIONS/)** | Exploratory formalization |
| **[NEXAH_TRANSLATIONS/](RESEARCH/NEXAH_TRANSLATIONS/)** | Connections to adjacent disciplines |

`NEXAH_DEVELOPMENT/`, `HISTORY/`, and `NOTES/` contain legacy development,
historical context, and non-canonical working material.

---

## 🌍 APPLICATIONS/

**[APPLICATIONS/](APPLICATIONS/)** contains concrete demonstrations and applied
research programs.

Main entry points:

- **[APPLICATIONS/README.md](APPLICATIONS/README.md)** — application overview
- **[APPLICATIONS/orientation_translation/](APPLICATIONS/orientation_translation/)** — non-canonical application and methodological research program over fixed public knowledge sources
- **[APPLICATIONS/core_demos/lorenz/](APPLICATIONS/core_demos/lorenz/)** — compact Lorenz reference
- **[APPLICATIONS/dynamical_systems/](APPLICATIONS/dynamical_systems/)** — nonlinear-system studies
- **[APPLICATIONS/navigation/](APPLICATIONS/navigation/)** — navigation experiments
- **[APPLICATIONS/power_systems/](APPLICATIONS/power_systems/)** — most developed applied validation program

The power-systems branch includes field reconstruction, IEEE benchmark work,
atlas discovery, transition prediction, recovery analysis, and exploratory
atlas-guided control.

Orientation Translation remains physically part of Applications and includes
pilots, Reflections, Neighborhoods, comparisons, studies, and reviews. Its
methodological evidence participates conceptually in Research and Architecture;
it does not establish a canonical Method.

Its maintained local entry point distinguishes pilots, neighborhoods,
comparisons, reviews, studies, provisional methods, and audited visualization
packages without presenting them as one maturity ladder.

The current public-use plan is
**[IEEE_GEOMETRY_SHOWCASE_PLAN.md](APPLICATIONS/power_systems/IEEE_GEOMETRY_SHOWCASE_PLAN.md)**.
It translates the historical Tube concept into a parameterized IEEE state
family with explicit benchmark, simulation, observation, and outcome labels.

`APPLICATIONS/archive/` preserves superseded and historical application demos.

---

## ✅ Cross-Cutting Evidence and Verification

These areas support multiple subsystems without becoming additional subsystem
authorities:

| Area | Role |
|---|---|
| **[validation/](validation/)** | Reproducible validation campaigns, canonical results, summaries, and evidence records |
| **[tests/](tests/)** | Automated tests for the maintained package, applications, Library, Living Concepts, and repository contracts |
| **[testkit/](testkit/README.md)** | Observed-evidence admission and outcome-boundary instruments |
| **[assets/](assets/)** | Maintained public documentation visuals used by repository entry points |

Passing tests establishes software consistency within their declared scope. It
does not establish domain truth, scientific universality, operational safety,
or authority beyond the owning subsystem.

---

## 🧪 EXPERIMENTAL/

**[EXPERIMENTAL/](EXPERIMENTAL/)** is the exploration and prototype layer.

| Area | Role | Status |
|---|---|---|
| **[BUILDER_LAB/](EXPERIMENTAL/BUILDER_LAB/)** | Broad system-building and simulation environment | Experimental / historical mix |
| **[FRAMEWORK/](EXPERIMENTAL/FRAMEWORK/)** | Earlier conceptual framework | Reference / legacy |
| **[OBSERVER_GEOMETRY_LAB/](EXPERIMENTAL/OBSERVER_GEOMETRY_LAB/)** | Observer-relative and local/global geometry | Active exploration |

This area intentionally contains competing ideas, versioned scripts, and
unfinished mechanisms. New users should begin with the demonstrator or research
portal before entering these labs.

---

## 🧭 Navigation by Reader

### General visitor

```text
README.md
→ ARCHITECTURE/README.md
→ choose one responsible subsystem
```

### Specification reader

```text
ORIENTATION_LANGUAGE/README.md
→ OLS-RELEASE-1.0.0/PUBLICATION_SUMMARY.md
→ relevant OLS part
→ conformance and tests
```

### Researcher

```text
RESEARCH/README.md
→ RESEARCH/ABSTRACT.md
→ RESEARCH/CORE_CONCEPT_MAP.md
→ RESEARCH/VALIDATION/
→ RESEARCH/FINDINGS/
```

### Developer

```text
nexah/README.md
→ nexah/START_HERE.md
→ ARCHITECTURE/SYSTEM_STATE.md
→ PROTO_CORE/NEXAH_DEMONSTRATOR/
```

### Application evaluator

```text
APPLICATIONS/README.md
→ APPLICATIONS/power_systems/README.md
→ APPLICATIONS/power_systems/FIELD_NAVIGATION_VALIDATION/
```

For public-knowledge orientation:

```text
APPLICATIONS/README.md
→ APPLICATIONS/orientation_translation/
→ pilots or studies
→ Meta Review 01
```

See **[Meta Review 01](APPLICATIONS/orientation_translation/reviews/meta_review_01/META_REVIEW_REPORT.md)**.

### Library reader

```text
LIBRARY/README.md
→ docs/library/atlas-of-atlases/
→ six atlas fields and Library appendix
→ Registry and wider Works
→ editorial sequences
→ reader journeys
```

### Editorial contributor

```text
EDITORIAL_OPERATING_SYSTEM/README.md
→ governance and review
→ explanation contracts
→ controlled execution and verification
```

For bounded, non-canonical review instruments:

```text
EDITORIAL_OPERATING_SYSTEM/living_concepts/review/README.md
→ choose a review function
→ inspect its evidence, counterexamples, and disposition
```

### Principles and governance reviewer

```text
MANIFESTO.md
→ GOVERNANCE/constitution_review_01/
→ historical register and evidence map
→ provisional Constitution Candidate
```

The candidate does not become canonical by being linked here.

### Experimental exploration

```text
EXPERIMENTAL/README.md
→ EXPERIMENTAL/BUILDER_LAB/
or
→ EXPERIMENTAL/OBSERVER_GEOMETRY_LAB/
```

---

## ⚠️ Status and Scope

NEXAH currently combines:

- implemented demonstrations
- empirical and visual research
- partially reproducible validation pipelines
- exploratory navigation and control mechanisms
- semi-formal theory under active development
- historical prototypes and archived experiments

It is not yet a unified production framework or a finalized scientific theory.
Local documents distinguish results as empirical, experimental, theoretical,
or legacy where possible.

---

**NEXAH Repository Map**

Research · Language · Implementations · Applications · Library · Editorial OS
