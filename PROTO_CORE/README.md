# ⚙️ NEXAH — Proto Core

`PROTO_CORE` contains reference implementations, experimental method layers,
and the development history from which several current NEXAH applications
emerged.

It is not one unified software core. Its three areas have different roles and
different levels of readiness.

---

## 🚀 Start Here

| You want to… | Start with |
|---|---|
| Run the verified reference pipeline | **[NEXAH_DEMONSTRATOR/](NEXAH_DEMONSTRATOR/)** |
| Study field reconstruction methods | **[FIELD_LAYER/](FIELD_LAYER/)** |
| Trace the IEEE gate/control development sequence | **[NEXAH_CORE/](NEXAH_CORE/)** |
| Browse the visual development history | **[visual_gallery.md](visual_gallery.md)** |

New users should begin with the Demonstrator. `FIELD_LAYER` and `NEXAH_CORE`
are research environments rather than stable public APIs.

---

## 🗂️ Structure and Status

```text
PROTO_CORE/
├── NEXAH_DEMONSTRATOR/   active verified reference tool
├── FIELD_LAYER/          experimental methods laboratory
└── NEXAH_CORE/           legacy/experimental development lineage
```

| Area | Primary role | Status |
|---|---|---|
| **[NEXAH_DEMONSTRATOR](NEXAH_DEMONSTRATOR/)** | Onboarding, reproducible visual pipeline, structural reference | Active and verified |
| **[FIELD_LAYER](FIELD_LAYER/)** | Field reconstruction, decomposition, geometry, and navigation methods | Experimental Method Lab |
| **[NEXAH_CORE](NEXAH_CORE/)** | Versioned IEEE-oriented gate, transition, and control experiments | Legacy / experimental lineage |

These labels indicate maintenance and evidence level. “Legacy” does not mean
irrelevant; it means the material is preserved as development history rather
than presented as the current canonical implementation.

---

## 🧪 NEXAH Demonstrator

The **[NEXAH Demonstrator](NEXAH_DEMONSTRATOR/)** is the canonical executable
entry to Proto Core.

It combines:

- trajectory simulation
- field and transition-structure reconstruction
- a continuous instability field
- discrete structural transitions
- navigation behavior
- generated figures and animation

From the repository root:

```bash
python PROTO_CORE/NEXAH_DEMONSTRATOR/scripts/run_demo.py
```

This complete sequence has been verified with Python 3.12. See the
**[Demonstrator README](NEXAH_DEMONSTRATOR/README.md)** for expected outputs and
scientific limitations.

The Demonstrator is both a reference implementation and a small application of
NEXAH methods. It remains in `PROTO_CORE` because its primary purpose is to
expose the structural pipeline rather than a domain-specific user workflow.

---

## 🌊 Field Layer

The **[FIELD_LAYER](FIELD_LAYER/)** is an experimental methods laboratory for
turning trajectories into continuous and discrete structural representations.

Research areas include:

- density and flow reconstruction
- gradient/rotation decomposition
- boundary and separatrix analysis
- Lyapunov overlays
- regime and transport maps
- transition concentration regions
- exploratory navigation and field control

Major subareas:

| Area | Role |
|---|---|
| **[FIELD_DECOMPOSITION/](FIELD_LAYER/FIELD_DECOMPOSITION/)** | Versioned field, boundary, transport, and regime experiments |
| **[NAVIGATION_ENGINE/](FIELD_LAYER/NAVIGATION_ENGINE/)** | Experimental geometry-aware navigation and control |
| **[LEGACY/](FIELD_LAYER/LEGACY/)** | Earlier equations, findings, and formulations |

`FIELD_LAYER` contains reusable method ideas, but they are not consolidated
into a stable library interface.

---

## 🔶 NEXAH Core Development Lineage

The **[NEXAH_CORE](NEXAH_CORE/)** directory records an extended sequence of
IEEE-oriented experiments, ranging from early gate detection to phase-aligned
navigation.

The script history includes work on:

- phase and transition localization
- sheet tracking
- transition density fields
- basin identity and transition matrices
- memory-guided and policy control
- stability and barrier fields
- flow-aligned channels
- gate-aware navigation

Most of this history appears as successive `ieee_gate_detection_v*` scripts.
The sequence is valuable for tracing how concepts developed, but it is not a
single current engine and does not expose a unified API.

Current applied power-system work lives in
**[APPLICATIONS/power_systems/](../APPLICATIONS/power_systems/)**.

---

## 🔁 Relationship to the Rest of NEXAH

```text
RESEARCH
→ concepts, validation, and findings

PROTO_CORE
→ reference implementations and experimental methods

APPLICATIONS
→ system-specific tools and applied research programs

nexah/
→ minimal installable Python package
```

The boundaries are intentionally permeable:

- the Demonstrator is also an application
- Field Layer methods support both research and applications
- NEXAH Core contains early applied IEEE experiments
- successful prototypes can migrate into maintained application programs or
  the installable package

Files should be interpreted according to their documented status, not only
their directory name.

---

## 🧭 Is Proto Core an Applications Area?

Partly:

| Area | Application role |
|---|---|
| Demonstrator | Yes — runnable reference application |
| Field Layer | Primarily methods used to build applications |
| NEXAH Core | Applied experiment history, especially for IEEE systems |

`APPLICATIONS/` remains the curated entry for domain-specific workflows.
`PROTO_CORE/` explains and preserves the methods and implementation lineage
behind those workflows.

---

## 🛠️ What Contributors Can Work On

Useful contributions include:

- reproducing a Field Layer experiment in a clean environment
- extracting reusable functions from versioned scripts
- comparing an older NEXAH Core result with the maintained Power Systems work
- separating representation artifacts from robust field structure
- adding quantitative evaluation to visual observations
- consolidating navigation methods behind a small interface
- documenting which historical experiment superseded another
- promoting a stable method into the installable `nexah` package

The open architecture is intentional: Proto Core shows both what works and what
still needs consolidation.

---

## ⚠️ Current Boundaries

Proto Core does not currently provide:

- a unified runtime across all three areas
- one stable public API
- a single reproducibility command for historical experiments
- production control guarantees
- complete statistical validation of all visual findings
- a direct replacement for established domain methods

The verified Demonstrator is the supported entry. Everything beyond it should
be treated as experimental, historical, or method-level research according to
its local documentation.

---

## 🔗 Related Entry Points

- **[Repository Overview](../README.md)**
- **[Applications Index](../APPLICATIONS/README.md)**
- **[Research Portal](../RESEARCH/README.md)**
- **[Validation Portal](../RESEARCH/VALIDATION/README.md)**
- **[Architecture](../ARCHITECTURE/README.md)**
- **[Installable Package](../nexah/README.md)**

---

**NEXAH Proto Core**

Reference Tool · Method Lab · Development Lineage
