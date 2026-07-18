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
| **[Legacy Root Outputs](BUILDER_LAB/legacy/root_outputs_2026-07-18/README.md)** | Frozen generated figures and result files formerly exposed at repository root | **Archive** | Historical inspection only; not current evidence or capability status |

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
current structural audit dated July 12, 2026. It records entry-point checks,
dependency boundaries, archive weight, and promotion candidates. It is an
inventory rather than a software specification.

### Historical development lineages

The archive contains several earlier attempts to turn the NEXAH idea into a
kernel or application system. They are useful for understanding how the current
architecture emerged. Their presence does not make them part of the maintained
runtime.

| Lineage | Start here | What is actually present | Current relevance |
|---|---|---|---|
| **Early kernel shell** | **[Archived Kernel README](BUILDER_LAB/ARCHIVE_ENGINE/archived/kernel/README.md)** and **[NexahKernel](BUILDER_LAB/ARCHIVE_ENGINE/archived/kernel/nexah_kernel.py)** | A layered graph → regime landscape → navigation → action architecture; parts of the navigation implementation remain placeholders | Preserves the early system decomposition |
| **Discrete Navigation Kernel v2** | **[Navigation README](BUILDER_LAB/ARCHIVE_KERNEL/v2_navigation/navigation/README.md)** and **[navigator.py](BUILDER_LAB/ARCHIVE_KERNEL/v2_navigation/navigation/navigator.py)** | Executable graph lookahead, risk-distance scoring, and next-state selection using supplied regimes and risk targets | Useful algorithmic reference; labels and scores require independent evidence before reuse |
| **Field and Dynamics Engine** | **[Dynamics Engine README](BUILDER_LAB/ARCHIVE_ENGINE/DYNAMICS_ENGINE/README.md)** | Flow, basin, topology, transition, phase-map, and meta-field experiments across many development levels | Hypothesis and method archive; not the current orientation backend |
| **Stability-driven multi-agent study** | **[Experiment README](BUILDER_LAB/ARCHIVE_ENGINE/archived/research/experiments/nexah_stability_driven_multi_agent_system/README.md)** | A multi-agent research concept and visual centered on stability-seeking exploration | Reconstruct only for a specific testable question; current evidence is insufficient for a finding |
| **Prototype agent runner** | **[agent_run_demo.py](BUILDER_LAB/ARCHIVE_ENGINE/agent_run_demo.py)** and **[NexahAgent](BUILDER_LAB/ARCHIVE_ENGINE/archived/agent/nexah_agent.py)** | Grid-landscape exploration, a reward-based learning prototype, and a separate skeletal agent loop | Reference for experimental orchestration, not an integrated agent layer |
| **Discovery Engine** | **[Discovery Engine README](BUILDER_LAB/DISCOVERY_ENGINE/README.md)** and **[Discovery Observations](BUILDER_LAB/DISCOVERY_ENGINE/DISCOVERY_OBSERVATIONS.md)** | Resilience, transition, field, phase, and symbolic-law experiments | Selected observations may be reproduced; universal-law language is not a validated capability |
| **META–ARCHY–MESO framework** | **[Historical Framework](FRAMEWORK/)** | Earlier conceptual layers connecting purpose, structure, dynamics, navigation, and action | Conceptual lineage only; the current contracts use a different architecture |

Two related reference areas now live outside `EXPERIMENTAL/`:

- **[Dynamical model hierarchy](../APPLICATIONS/models/dynamical_models/README.md)**
  documents the conceptual progression from stability landscapes through
  gradient and drift dynamics to regime systems.
- **[Control Layer](../ARCHITECTURE/CORE/control_layer/README.md)** preserves
  executable synthetic gate, field, routing, and multi-agent prototypes. Its
  own status explicitly limits them to experimental trajectory-deformation and
  geometry-aware routing studies.

### What the lineage contributed

Across these generations, one architecture repeatedly reappears:

```text
system observations
→ representation
→ structure or landscape
→ states and transitions
→ orientation and navigation
→ optional intervention
```

The maintained **[Orientation Layer](../ARCHITECTURE/orientation_layer/)** keeps
this structural direction while adding typed contracts, provenance,
uncertainty, reproducibility, evidence gates, and a strict boundary between
orientation and execution. Historical components should therefore be treated
as design history or candidates for bounded reconstruction, not imported as a
second kernel.

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
