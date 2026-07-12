# ⚙️ NEXAH — Builder Lab

The Builder Lab preserves experimental system simulators, navigation demos,
discovery work, and several earlier NEXAH implementation generations.

> **Status: mixed experimental workspace and development archive.** It is not a
> unified framework, current system core, or validated application suite.

For the verified repository quickstart, use the
**[NEXAH Demonstrator](../../PROTO_CORE/NEXAH_DEMONSTRATOR/)**. Use this directory
when investigating prototype lineages or testing individual experiments.

---

## 🧭 Start Here

| Goal | Entry point | Status |
|---|---|---|
| Run the minimal state-graph example | `python EXPERIMENTAL/BUILDER_LAB/demos/nexah_demo.py` | **Verified** on July 12, 2026 |
| List example system definitions | `python EXPERIMENTAL/BUILDER_LAB/nexah_cli.py systems-list` | **Verified** on July 12, 2026 |
| Understand the actual directory | **[Current Inventory](BUILDER_LAB_INVENTORY_INDEX.md)** | Current audit |
| Review early discovery work | **[DISCOVERY_ENGINE/](DISCOVERY_ENGINE/)** | Historical experiment lineage |
| Browse research and concept fragments | **[EXPLORATION/](EXPLORATION/)** | Mixed notebook and archive |
| Inspect older engine implementations | **[ARCHIVE_ENGINE/](ARCHIVE_ENGINE/)** | Archive |

The verified text demo uses only the Python standard library. It presents a
small synthetic state graph with fixed regimes, transitions, and policy rules;
it is not a power-system model or validation result.

---

## 🗺️ Current Structure

```text
BUILDER_LAB/
├── demos/              small synthetic demonstrations
├── engines/            system and cascade prototypes
├── models/             shared experimental model template
├── systems/            example JSON system definitions
├── dashboards/         prototype visual interfaces
├── visualizers/        graph and cascade renderers
├── data/               generated or example data
├── global_systems/     synthetic infrastructure definitions
├── DISCOVERY_ENGINE/   early field and transition experiments
├── EXPLORATION/        notes, fragments, and experimental branches
├── proto_models/       conceptual model proposals
├── ARCHIVE_KERNEL/     earlier kernel variants
├── ARCHIVE_ENGINE/     large historical engine lineage
├── tests/              stale tests for an earlier framework layout
└── visuals/            selected and generated visual artifacts
```

Several top-level directories are currently empty: `analysis/`, `app/`,
`core/`, `docs/`, `meta/`, and `navigation/`. They should not be interpreted as
implemented layers.

---

## 🧪 Entry-Point Status

| Entry point | Result | Notes |
|---|---|---|
| `demos/nexah_demo.py` | **Runs** | Standard-library synthetic transition and policy example |
| `nexah_cli.py systems-list` | **Runs** | Lists the three JSON examples in `systems/` |
| `demos/nexah_explorer.py` | **Dependency-blocked** | Requires undeclared `networkx` and `imageio`; writes frames relative to the working directory |
| `demos/nexah_graph_simulation.py` | **Dependency-blocked / interactive** | Same undeclared dependencies; includes pauses and a GUI display |
| `run_builder_lab.py` | **Not a verified suite** | Sequentially invokes all three demos, including the blocked visual demos |
| CLI `systems` / `simulate` | **Path-inconsistent** | Auto-loader and model/system paths no longer match the current directory layout |
| `tests/` | **Stale** | Imports an earlier `FRAMEWORK` and `APPLICATIONS/examples` structure |

The root project dependencies do not currently declare `networkx`, `imageio`,
or `cartopy`, although Builder Lab visual and geographic prototypes import them.
Do not add these packages to the main NEXAH installation solely to support
historical experiments; a separate experimental dependency definition would be
the cleaner future boundary.

---

## 🧩 What the Lab Demonstrates

The current non-archive prototypes explore:

- synthetic regime graphs and fixed transition policies
- cascade and infrastructure scenarios
- graph-based visualization
- multi-system and planetary-scale abstractions
- early structure, field, and transition discovery
- experimental control and navigation ideas

These are demonstrations of possible representations. Labels such as energy
grid, infrastructure, or planetary system do not imply domain validation or
use of operational data.

---

## 🚦 Promotion Priorities

The first two candidates were reviewed on July 12, 2026:

1. **Discovery observations** — remain experimental. The strongest next study
   is a controlled V22 lag reproduction; no current statement was promoted to
   `RESEARCH/FINDINGS/`.
2. **IEEE mapping note and IEEE_CASE script** — remain historical. The note is
   conceptual, while the script uses a synthetic scalar signal rather than an
   IEEE network. Neither should be copied into the current power application.
The next optional candidate is:

3. **Minimal state-graph demo** — decide whether its educational value justifies
   a small experimental-tool link from `APPLICATIONS/`; it should not be
   presented as a power-grid application in its current form.

The Symmetry Graph and archived multi-agent studies remain secondary candidates
because their code, data, and claims must first be reconstructed from the large
engine archive.

---

## 📏 Working Rules

- Treat each script as an individual experiment unless integration is proven.
- Keep archive trees intact when their historical context matters.
- Promote the smallest reproducible result, not an entire development lineage.
- Record dependencies, inputs, outputs, and limitations before exposing a tool.
- Use the current Gate distinction: a continuous local-instability field is not
  itself a discrete transition detector.
- Put verified findings in `RESEARCH`, stable reference implementations in
  `PROTO_CORE`, system-specific tools in `APPLICATIONS`, and maturity mappings
  in `ARCHITECTURE`.

---

## 🔗 Related Indexes

- **[Experimental Index](../README.md)**
- **[Builder Lab Inventory](BUILDER_LAB_INVENTORY_INDEX.md)**
- **[Discovery Engine](DISCOVERY_ENGINE/README.md)**
- **[Exploration Index](EXPLORATION/README.md)**
- **[Repository Map](../../REPOSITORY_MAP.md)**

---

**NEXAH Builder Lab**

Synthetic Demos · Experimental Engines · Discovery History · Archived Systems
