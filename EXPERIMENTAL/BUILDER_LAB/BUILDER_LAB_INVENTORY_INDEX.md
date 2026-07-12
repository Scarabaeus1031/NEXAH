# 🧭 NEXAH Builder Lab — Current Inventory

This inventory maps the Builder Lab as it exists in the repository. It replaces
the earlier conceptual six-layer map, which referenced directories and maturity
levels that no longer matched the filesystem.

> **Audit date:** July 12, 2026
>
> **Scope:** structure, entry points, dependencies, and promotion relevance
>
> **Not assessed:** scientific validity of every archived experiment

---

## 📊 Inventory Summary

The Builder Lab contains roughly 2,300 files and occupies about 341 MB. Most of
that volume is historical material and generated imagery:

- `ARCHIVE_ENGINE/`: approximately 175 MB
- `EXPLORATION/`: approximately 115 MB
- `DISCOVERY_ENGINE/`: approximately 30 MB
- `visuals/`: approximately 20 MB

The top-level Builder Lab is therefore an archive-heavy laboratory, not one
software package.

---

## 🗺️ Area Classification

| Area | Contents | Status | Action |
|---|---|---|---|
| `demos/` | Three state-graph demos | Mixed: one verified, two dependency-blocked | Keep; review separately |
| `engines/` | Cascade, infrastructure, planetary, and system generators | Experimental prototypes | Keep; do not market as validated applications |
| `models/` | `NexahSystem` graph/visualization template | Experimental shared code | Repair only if visual demos are retained |
| `systems/` | Energy-grid, climate, and supply-chain JSON examples | Synthetic examples | Keep with prototype engines |
| `dashboards/` | Matplotlib/network interfaces | Experimental UI prototypes | Dependency and runtime audit needed |
| `visualizers/` | Graph, cascade, planetary renderers | Experimental visual tooling | Dependency and output-path audit needed |
| `data/` | Timeline and planetary-network JSON | Example/generated data | Identify provenance before reuse |
| `global_systems/` | Synthetic global/infrastructure definitions | Experimental inputs | Keep with engines |
| `DISCOVERY_ENGINE/` | Resilience, phase, field, law-discovery, and validation experiments | Historical experimental lineage | Review observations for Research promotion |
| `EXPLORATION/` | Current fragments, symbolic studies, experimental notes, and older portals | Mixed notebook/archive | Curate item by item |
| `proto_models/` | Oval-membrane and time-knot models | Concept proposals | Require testable definitions before promotion |
| `ARCHIVE_KERNEL/` | Field, navigation, and experimental kernel generations | Archive | Preserve; no current entry-point claims |
| `ARCHIVE_ENGINE/` | Engine, kernel, research, navigation, outputs, and nested archives | Archive | Preserve as a historical lineage |
| `legacy/` | Legacy index | Archive metadata | Retain if it improves traceability |
| `IEEE_CASE/` | One early IEEE gate-detection script and empty visuals directory | Historical experiment fragment | Compare against current power-system work |
| `tests/` | Three manual scripts for old paths | Stale | Do not treat as current automated tests |
| `visuals/` | Selected diagrams, outputs, GIFs, and one plotting script | Mixed generated evidence | Index selected artifacts; avoid broad claims |

---

## 🕳️ Empty Top-Level Placeholders

The following directories exist but contain no tracked working material:

```text
analysis/
app/
core/
docs/
meta/
navigation/
```

They are remnants or placeholders, not functional architectural layers. Removal
can be considered later, but is not required for preserving the current audit.

---

## ▶️ Entry-Point Audit

### Verified

```bash
python EXPERIMENTAL/BUILDER_LAB/demos/nexah_demo.py
python EXPERIMENTAL/BUILDER_LAB/nexah_cli.py systems-list
```

Both commands completed successfully in the repository environment on the audit
date. The demo uses only the standard library; the CLI command only enumerates
JSON filenames.

### Blocked or inconsistent

| Component | Finding |
|---|---|
| `demos/nexah_explorer.py` | Fails without undeclared `networkx` and `imageio` dependencies |
| `demos/nexah_graph_simulation.py` | Uses the same undeclared dependencies and interactive plotting |
| `run_builder_lab.py` | Calls the blocked visual demos and is therefore not a verified suite |
| `nexah_cli.py simulate` | Points to `auto_system_loader.py` at the wrong level |
| `engines/auto_system_loader.py` | Imports `system_template` and resolves `systems/` relative to `engines/`, while both live elsewhere |
| `tests/test_*.py` | Import obsolete `FRAMEWORK` modules and `APPLICATIONS/examples/energy_grid.json` |

### Dependency boundary

The main repository declares NumPy, Matplotlib, scikit-learn, and pandas. Builder
Lab scripts additionally use:

- `networkx`
- `imageio`
- `cartopy` in geographic prototypes

If these experiments are revived, define their dependencies separately instead
of silently expanding the stable package requirements.

---

## 🧠 Valuable Content by Destination

### Candidate for `RESEARCH/FINDINGS/`

- `DISCOVERY_ENGINE/DISCOVERY_OBSERVATIONS.md`
- archived Symmetry Graph result summary
- archived structured-oscillator study
- archived stability-driven multi-agent study

Each requires reproduction and scientific qualification before promotion.

### Candidate for `RESEARCH/CONCEPTS/`

- `EXPLORATION/experimental/01_control/control_sensitivity_field.md`
- `proto_models/oval_membrane_field/`
- `proto_models/time_knot_field/`

These currently read as proposals or interpretations, not established methods.

### Candidate for `APPLICATIONS/`

- the minimal state-graph demo, as an explicitly synthetic educational tool
- selected engines only after runtime, dependency, and domain-claim review

The energy-grid naming in the demo is illustrative and does not make it an IEEE
or operational power-system application.

### Candidate for comparison with existing power-system work

- `IEEE_CASE/scripts/ieee_gate_detection_v1.py`
- `EXPLORATION/experimental/03_mapping/ieee_mapping_module.md`

Compare these with `APPLICATIONS/power_systems/` before copying anything.

---

## 🚦 Recommended Sequence

Completed review decisions:

- Discovery observations remain experimental pending a controlled V22 study.
- The IEEE fragments remain historical and should not be merged into the
  current power-system application.

Optional next work:

1. Decide whether to retain and repair the visual state-graph demos.
2. If retained, add an isolated experimental dependency definition and stable
   output paths.
3. Reconstruct archived Symmetry Graph or multi-agent studies only when they
   support an active research question.
4. Leave `ARCHIVE_ENGINE` and `ARCHIVE_KERNEL` frozen until a specific artifact
   is requested.

---

## ⚠️ Interpretation Boundary

The Builder Lab documents how NEXAH evolved through many representations. It
does not demonstrate that all these representations form one integrated kernel.

The useful task is selective recovery:

```text
archived experiment
→ reproducible question
→ qualified result
→ current repository destination
```

For broader routing, return to the
**[Experimental Index](../README.md)** or the
**[Builder Lab README](README.md)**.
