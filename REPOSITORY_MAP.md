# 🧭 NEXAH — Repository Map

This document maps the current repository structure and identifies the
recommended entry point for each type of reader.

NEXAH is an active research ecosystem for reconstructing and navigating
structure inside complex dynamical systems. The repository contains a small
Python package, reproducible demonstrators, application programs, research
evidence, and historical experimental environments.

---

## 🚀 Start Here

| Goal | Entry point |
|---|---|
| Understand the central idea | **[START_HERE.md](START_HERE.md)** |
| Get the full overview | **[README.md](README.md)** |
| Run the reference demonstration | **[PROTO_CORE/NEXAH_DEMONSTRATOR/](PROTO_CORE/NEXAH_DEMONSTRATOR/)** |
| Explore the visual work | **[VISUAL_GALLERY.md](VISUAL_GALLERY.md)** |
| Enter the research archive | **[RESEARCH/README.md](RESEARCH/README.md)** |
| Inspect the current architecture | **[ARCHITECTURE/README.md](ARCHITECTURE/README.md)** |
| Explore the most developed application | **[APPLICATIONS/power_systems/](APPLICATIONS/power_systems/)** |

Recommended first path:

```text
START_HERE
→ README
→ NEXAH_DEMONSTRATOR
→ RESEARCH or APPLICATIONS
```

---

## 🗂️ Top-Level Structure

```text
NEXAH/
├── ARCHITECTURE/       current architecture and system state
├── PROTO_CORE/         reference implementations and field layers
├── nexah/              installable minimal Python package
├── RESEARCH/           concepts, evidence, findings, and theory
├── APPLICATIONS/       demonstrations and applied validation
├── EXPERIMENTAL/       active labs, prototypes, and historical systems
├── outputs/            selected generated repository-level artifacts
├── README.md           repository overview
├── START_HERE.md       guided visual introduction
└── VISUAL_GALLERY.md   curated visual entry point
```

The conceptual flow across these areas is approximately:

```text
research questions
→ experimental exploration
→ reference implementation
→ validation and findings
→ applied systems
```

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

- trajectory preprocessing and embedding
- clustered regime representation
- transition and stability summaries
- simple structural comparison
- exploratory navigation and intervention heuristics
- the `nexah` command-line interface

This package is a minimal operational kernel. It does not yet integrate every
research mechanism found in `PROTO_CORE`, `RESEARCH`, or `APPLICATIONS`.

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
- **[APPLICATIONS/core_demos/lorenz/](APPLICATIONS/core_demos/lorenz/)** — compact Lorenz reference
- **[APPLICATIONS/dynamical_systems/](APPLICATIONS/dynamical_systems/)** — nonlinear-system studies
- **[APPLICATIONS/navigation/](APPLICATIONS/navigation/)** — navigation experiments
- **[APPLICATIONS/power_systems/](APPLICATIONS/power_systems/)** — most developed applied validation program

The power-systems branch includes field reconstruction, IEEE benchmark work,
atlas discovery, transition prediction, recovery analysis, and exploratory
atlas-guided control.

`APPLICATIONS/archive/` preserves superseded and historical application demos.

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

## 📊 outputs/

**[outputs/](outputs/)** contains selected generated artifacts used by root
documentation and demonstrations.

Most experiment-specific results live next to their producing research or
application module. Output files are evidence and presentation artifacts, not
the primary implementation source.

---

## 🧭 Navigation by Reader

### New visitor

```text
START_HERE.md
→ README.md
→ VISUAL_GALLERY.md
→ PROTO_CORE/NEXAH_DEMONSTRATOR/
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
ARCHITECTURE/SYSTEM_STATE.md
→ nexah/
→ PROTO_CORE/NEXAH_DEMONSTRATOR/
→ PROTO_CORE/NEXAH_CORE/
→ PROTO_CORE/FIELD_LAYER/
```

### Applied-systems reader

```text
APPLICATIONS/README.md
→ APPLICATIONS/power_systems/README.md
→ APPLICATIONS/power_systems/FIELD_NAVIGATION_VALIDATION/
```

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

Architecture · Demonstration · Research · Validation · Applications
