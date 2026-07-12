# 🧪 NEXAH — Experimental Index

This directory preserves active laboratories, exploratory prototypes, and
historical development lineages of NEXAH.

It is a workspace for investigation, not a second operational core. Content in
this directory may be incomplete, duplicated, speculative, or superseded by
material in `RESEARCH/`, `PROTO_CORE/`, `ARCHITECTURE/`, or `APPLICATIONS/`.

---

## 🧭 How to Read This Directory

Each area is assigned one of four working statuses:

- **Active Lab** — a current, bounded experimental investigation
- **Experimental System** — runnable or partially runnable prototypes that
  require review before reuse
- **Historical Reference** — conceptually useful earlier architecture or theory
- **Archive** — preserved development history; not a current entry point

Experimental results are not automatically validated findings. Promotion into
another repository layer requires a clear claim, reproducible evidence, and an
explicit destination.

---

## 🗺️ Directory Map

| Area | What it contains | Status | Recommended use |
|---|---|---|---|
| **[OBSERVER_GEOMETRY_LAB/](OBSERVER_GEOMETRY_LAB/)** | Observer-relative geometry, projections, transport structures, and visual experiments | **Active Lab** | Best current experimental entry point |
| **[BUILDER_LAB/](BUILDER_LAB/)** | Demos, simulation engines, discovery work, exploration notes, and several archived systems | **Experimental System / Archive mix** | Enter through the guided map below |
| **[FRAMEWORK/](FRAMEWORK/)** | Earlier META → ARCHY → MESO → NEXAH → MEVA conceptual architecture | **Historical Reference** | Consult for conceptual lineage, not current implementation state |

The empty root `scripts/` and `visuals/` directories are not current entry
points.

---

## 👁️ Active Lab: Observer Geometry

**[OBSERVER_GEOMETRY_LAB/](OBSERVER_GEOMETRY_LAB/)** is the most clearly bounded
laboratory in this directory. It investigates:

- local and global representations
- observer-relative projection
- transport corridors and reinjection structures
- manifold slicing and orientation axes
- Mandelbrot–Julia contact visualizations

The lab includes its own README, documentation, scripts, and selected visuals.
Its claims remain exploratory and have not been promoted into the validated
Research layer.

---

## ⚙️ Builder Lab: Guided Map

`BUILDER_LAB/` contains most of the directory's material and should not be read
as one coherent runtime. It combines several development generations.

| Builder Lab area | Role | Current interpretation |
|---|---|---|
| **[demos/](BUILDER_LAB/demos/)** | Small state-graph and navigation demonstrations | Test before presenting as user tools |
| **[engines/](BUILDER_LAB/engines/)** | Synthetic infrastructure, cascade, planetary, and multi-system simulators | Application prototypes, not validated applications |
| **[systems/](BUILDER_LAB/systems/)** | Example system definitions | Inputs for Builder Lab experiments |
| **[dashboards/](BUILDER_LAB/dashboards/)** and **[visualizers/](BUILDER_LAB/visualizers/)** | Experimental interfaces and renderers | Prototype tooling |
| **[DISCOVERY_ENGINE/](BUILDER_LAB/DISCOVERY_ENGINE/)** | Early transition, resilience, field, and law-discovery experiments | Historical experimental lineage with promotion candidates |
| **[EXPLORATION/](BUILDER_LAB/EXPLORATION/)** | Control notes, symbolic work, fragments, older portals, and experimental scripts | Mixed research notebook; review item by item |
| **[proto_models/](BUILDER_LAB/proto_models/)** | Oval-membrane and time-knot conceptual models | Early concept models |
| **[ARCHIVE_KERNEL/](BUILDER_LAB/ARCHIVE_KERNEL/)** | Earlier field, navigation, and kernel variants | Archive |
| **[ARCHIVE_ENGINE/](BUILDER_LAB/ARCHIVE_ENGINE/)** | Large historical engine, research, navigation, and output tree | Frozen development archive |

The existing
**[Builder Lab Inventory](BUILDER_LAB/BUILDER_LAB_INVENTORY_INDEX.md)** is a
historical map. It contains useful observations, but some paths and maturity
labels no longer match the repository. Use it as an audit source rather than a
current specification.

### Experimental entry commands

The following entry points exist, but still require a dedicated runtime and
dependency check:

```bash
python EXPERIMENTAL/BUILDER_LAB/run_builder_lab.py
python EXPERIMENTAL/BUILDER_LAB/nexah_cli.py systems-list
python EXPERIMENTAL/BUILDER_LAB/demos/nexah_demo.py
```

For the verified repository quickstart, use the
**[NEXAH Demonstrator](../PROTO_CORE/NEXAH_DEMONSTRATOR/)** instead.

---

## 🌐 Historical Framework

**[FRAMEWORK/](FRAMEWORK/)** documents an earlier layered model:

```text
META → ARCHY → MESO → NEXAH → MEVA
```

It provides conceptual background for coherence, risk fields, regimes,
transition geometry, and navigation. These layers are not the current software
architecture. For the implemented repository view, see the
**[Architecture Index](../ARCHITECTURE/)** and
**[System State](../ARCHITECTURE/SYSTEM_STATE.md)**.

---

## 🚦 Promotion Queue

The following items appear worth reviewing outside the archive. Inclusion here
means **candidate for assessment**, not accepted result.

| Candidate | Possible destination | Required review |
|---|---|---|
| **[Discovery Observations](BUILDER_LAB/DISCOVERY_ENGINE/DISCOVERY_OBSERVATIONS.md)** | Remain experimental | Reviewed July 12, 2026; V22 needs controlled reproduction before Findings promotion |
| **[Symmetry Graph result summary](BUILDER_LAB/ARCHIVE_ENGINE/archived/research/experiments/RESULT_SUMMARY_Symmetry_Graph_Experiment.md)** | `RESEARCH/FINDINGS/` | Verify code, data, metrics, and current terminology |
| **[Structured Oscillator Networks](BUILDER_LAB/ARCHIVE_ENGINE/archived/research/experiments/structured_oscillator_networks/)** | `RESEARCH/FINDINGS/` or `RESEARCH/CONCEPTS/` | Determine whether it contains evidence or only a model proposal |
| **[Stability-driven Multi-Agent System](BUILDER_LAB/ARCHIVE_ENGINE/archived/research/experiments/nexah_stability_driven_multi_agent_system/)** | `RESEARCH/FINDINGS/` | Reproduce the experiment and qualify the stability claim |
| **[Control Sensitivity Field](BUILDER_LAB/EXPLORATION/experimental/01_control/control_sensitivity_field.md)** | `RESEARCH/CONCEPTS/` or `ARCHITECTURE/METHODS.md` | Formalize definitions and establish relationship to current control prototypes |
| **[IEEE Mapping Module](BUILDER_LAB/EXPLORATION/experimental/03_mapping/ieee_mapping_module.md)** | Remain historical | Reviewed July 12, 2026; conceptual analogies are superseded by current power-system experiments |
| **[Oval Membrane Field](BUILDER_LAB/proto_models/oval_membrane_field/)** | `RESEARCH/CONCEPTS/` | Decide whether the model yields testable hypotheses |
| **[Time Knot Field](BUILDER_LAB/proto_models/time_knot_field/)** | `RESEARCH/CONCEPTS/` | Separate mathematical proposal from metaphorical interpretation |
| **[Builder Lab demos](BUILDER_LAB/demos/)** | `APPLICATIONS/` index | Test dependencies, outputs, and user value before exposing them as tools |
| **[Observer Geometry Lab](OBSERVER_GEOMETRY_LAB/)** | Remain here; later link from Research | Define validation questions before any promotion |

Promotion should normally copy or rewrite the smallest relevant unit and retain
a source link. Moving an entire historical tree would erase useful context and
carry obsolete assumptions into current documentation.

---

## 📏 Promotion Criteria

Before experimental material becomes a current finding, method, or application,
check that it has:

1. a precise question or claim
2. a runnable or otherwise inspectable method
3. identifiable inputs and generated outputs
4. limitations and failed cases
5. terminology consistent with the current Gate and transition interpretation
6. a clear owner directory: Research, Proto Core, Architecture, or Applications

If these conditions are not met, the material should remain here and be indexed
as an experiment or historical reference.

---

## 🔗 Current Repository Layers

```text
EXPERIMENTAL
→ generates prototypes, hypotheses, and exploratory evidence

RESEARCH
→ frames questions, records findings, and organizes validation

PROTO_CORE
→ develops and exposes reference implementations

ARCHITECTURE
→ explains system relationships and implementation maturity

APPLICATIONS
→ presents system-specific tools and studies
```

Related entry points:

- **[Repository Map](../REPOSITORY_MAP.md)**
- **[Research Portal](../RESEARCH/README.md)**
- **[Proto Core Index](../PROTO_CORE/README.md)**
- **[Architecture Index](../ARCHITECTURE/README.md)**
- **[Applications Index](../APPLICATIONS/README.md)**

---

**NEXAH Experimental**

Active Labs · Prototype Systems · Historical Lineages · Promotion Candidates
