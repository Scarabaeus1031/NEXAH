# ⚡ NEXAH — The Orientation Laboratory

![NEXAH Peak Preview](./ARCHITECTURE/archive/Peak_Preview_visual_2.png)

> Mapping structure. Preserving evidence. Supporting orientation.

NEXAH is an open research and software laboratory for evidence-bound
orientation in complex systems.

It turns declared observations into inspectable representations of states,
relationships, transitions, paths, boundaries, and uncertainty. The current
kernel helps a user ask:

- Where am I in the supplied representation?
- What is reachable, blocked, changed, or missing?
- Which relationships and boundaries are supported by the evidence?
- Which conclusions remain unjustified?
- What should be examined next?

```text
observe → represent → map → compare → orient → explain → learn
```

NEXAH began as a cartography laboratory. Cartography remains its method for
making structure visible; orientation is what those maps are for.

> **Cartography constructs the map. Orientation asks what may legitimately be
> inferred and done from a declared position, context, and evidence state.**

NEXAH does not replace established scientific models, decide what reality
means, or autonomously control a system. It supports inspection and learning
before consequential decisions or actions.

![Status](https://img.shields.io/badge/status-research--active-orange)
![Validation](https://img.shields.io/badge/validation-in%20progress-yellow)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![Focus](https://img.shields.io/badge/focus-orientation%20in%20complex%20systems-lightgrey)

> **Status:** The typed Orientation Layer, Network Orientation application,
> IEEE Geometry V1 benchmark case, episodic-memory boundary, validation paths,
> and public showcase are implemented. Real-world operational validation,
> calibrated uncertainty, causal intervention, and autonomous execution are not
> claimed.

---

## 🧭 Quick Navigation

| Goal | Entry point |
|---|---|
| Understand the central idea | **[START_HERE.md](START_HERE.md)** |
| Use the current kernel | **[NEXAH Kernel Start](nexah/START_HERE.md)** |
| Run the reference demonstration | **[NEXAH Demonstrator](PROTO_CORE/NEXAH_DEMONSTRATOR/)** |
| Explore the visual work | **[VISUAL_GALLERY.md](VISUAL_GALLERY.md)** |
| Enter the research layer | **[RESEARCH/README.md](RESEARCH/README.md)** |
| Explore tools and applications | **[APPLICATIONS/README.md](APPLICATIONS/README.md)** |
| Inspect implementation maturity | **[ARCHITECTURE/SYSTEM_STATE.md](ARCHITECTURE/SYSTEM_STATE.md)** |
| Understand the full repository | **[REPOSITORY_MAP.md](REPOSITORY_MAP.md)** |
| Browse experimental lineages | **[EXPERIMENTAL/README.md](EXPERIMENTAL/README.md)** |
| Review safety and misuse boundaries | **[Kernel Safety](nexah/SAFETY_AND_MISUSE.md)** |
| Enter the visual Atlas | **[NEXAH Atlas on Are.na](https://www.are.na/nexah-scarabaeus1031/channels)** |

Recommended first path:

```text
NEXAH Kernel Start
→ choose Network Orientation or IEEE Geometry
→ run a canonical case
→ inspect evidence and limits
→ enter Research or Architecture when needed
```

---

## 🧭 What the Kernel Can Do Today

The installable `nexah` package and maintained applications provide:

| Capability | Current output |
|---|---|
| Ordered numerical trajectories | local state representation, empirical transitions, scoped analysis |
| Directed networks | reachability, paths, components, dead ends, bottlenecks, structural comparison |
| IEEE/Pandapower campaigns | typed physical frames, sampled geometry, turning and boundary records |
| Multiple perspectives | five read-only probes with agreement and disagreement preserved |
| Explanation | typed Orientation Reports and human-readable Orientation Briefs |
| Reproducibility | frozen manifests, canonical artifacts, validation records, replayable workflows |
| Episodic context | append-only storage and retrieval after explicit evidence admission |

Two maintained user-facing applications demonstrate the current kernel:

- **[Network Orientation](APPLICATIONS/network_orientation/README.md)** reads
  and compares declared graph structure from an explicit focus.
- **[IEEE Geometry V1](APPLICATIONS/power_systems/ieee_geometry_v1/showcase/README.md)**
  reads ordered benchmark campaigns through a frozen geometry and evidence
  protocol.

For the complete user surface, begin with
**[Start with the NEXAH Kernel](nexah/START_HERE.md)**.

---

## 🚀 Quick Start — Use the Kernel

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\activate
```

Orient the illustrative supply-chain graph:

```bash
nexah orient-network APPLICATIONS/datasets/supply_chain.json \
  --focus normal_operation \
  --target system_disruption \
  --domain supply-chain \
  --recorded-at 2026-07-13T22:45:00+00:00 \
  --format brief
```

Replay the frozen IEEE Geometry evaluation:

```bash
python validation/ieee_geometry_v1/run_validation.py
```

These paths produce inspectable reports and validation artifacts. They do not
issue commands to a real system or turn a scenario into observed experience.

The visual reference Demonstrator remains available as a complementary entry:

```bash
python PROTO_CORE/NEXAH_DEMONSTRATOR/scripts/run_demo.py
```

It runs the compact sequence:

```text
trajectory
→ field representation
→ transition structure
→ instability field
→ navigation behavior
```

Generated figures and data are written to:

```text
PROTO_CORE/NEXAH_DEMONSTRATOR/visuals/
```

For the conceptual introduction, read **[START_HERE.md](START_HERE.md)**. For
the current kernel surface, read **[nexah/START_HERE.md](nexah/START_HERE.md)**
or run `nexah --help` after installation.

---

## 🗺️ From Cartography to Orientation

Modern science produces increasingly accurate models, simulations, predictions,
and measurements. NEXAH explores a complementary question:

```text
Can the structures generated by those models
be mapped, compared, and navigated?
```

The framework looks for organization across:

- dynamics and topology
- coherence and synchronization
- fields and geometric representations
- regimes and transitions
- intervention and control
- local and global observation

This is not a claim that all systems share one universal law. It is an
investigation into whether useful structural descriptions can travel between
representations and domains.

The repository therefore acts as a laboratory in which mapping techniques are:

```text
proposed
→ implemented
→ visualized
→ challenged
→ compared
→ promoted or archived
```

Cartography is therefore a representation practice inside the broader
Orientation Laboratory. The emphasis is not merely producing a map, but making
complex behavior visible enough to inspect, compare, question, and learn from
without hiding the map's evidential limits.

---

## 🛡️ Evidence and Authority Boundary

Orientation is dual-use. A map of paths and bottlenecks can support resilience
and learning, but the same map can expose targets or optimize disruption.
NEXAH therefore separates:

```text
orientation ≠ recommendation ≠ authorization ≠ execution ≠ outcome
```

The current public kernel has no execution authority. Its probes are read-only,
its reports preserve uncertainty and disagreement, and simulations or declared
scenarios cannot silently become observed experience.

> **NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE**

Real infrastructure, personal data, health, finance, security, and autonomous
systems require additional evidence, governance, access control, and explicit
authorization. Read the normative
**[Safety and Misuse Boundaries](nexah/SAFETY_AND_MISUSE.md)** before connecting
a sensitive or operational source.

---

## 🔥 Current Research Model

![NEXAH Transition Activation Framework](RESEARCH/FIGURES/main/nexah_transition_activation_framework.png)

NEXAH investigates systems as motion within structured dynamical
representations. A current working hypothesis is:

```text
field
→ structure
→ coherence
→ mismatch
→ transition
          ↑
   control(direction)
```

Experimental interpretation:

```text
instability = candidate transition potential
mismatch    = possible activation factor
```

Some investigated representations indicate that labeled transitions can be
associated with drift, phase mismatch, or competing local flow geometry rather
than instability magnitude alone. This comparison remains system- and
representation-dependent.

The working vocabulary includes:

- **trajectory** — observed or simulated system evolution
- **field** — a reconstructed continuous representation
- **coherence** — local alignment within a chosen representation
- **Gate Operator** — a continuous local-instability field
- **transition** — a separate discrete event derived from trajectory structure
- **navigation** — experimental movement relative to reconstructed geometry

The Gate Operator does not directly detect discrete transitions. This
distinction is part of the current reference architecture.

For the implementation boundary and method status, see:

- **[Architecture Index](ARCHITECTURE/README.md)**
- **[System State](ARCHITECTURE/SYSTEM_STATE.md)**
- **[Methods Catalogue](ARCHITECTURE/METHODS.md)**

---

## ⚡ Power-System Benchmark Application

The maintained **[IEEE Geometry V1](APPLICATIONS/power_systems/ieee_geometry_v1/showcase/README.md)**
case is the most complete system-specific application of the current
Orientation Layer. It turns ordered IEEE/Pandapower benchmark campaigns into:

- typed physical frames with bus and line provenance
- sampled displacement, drift, direction, and curvature records
- explicit solver-visible boundaries and missing states
- five read-only perspectives
- an evidence-bound Orientation Brief
- a frozen IEEE-9 development to IEEE-14 evaluation path
- byte-reproducible validation and public figures

![NEXAH Power Systems Current Status](APPLICATIONS/power_systems/FIELD_NAVIGATION_VALIDATION/outputs/diagrams/NEXAH_POWER_SYSTEMS_CURRENT_STATUS_vii.png)

The broader Power Systems program also retains experiments in:

- field and atlas construction
- IEEE benchmark comparison
- transition prediction
- early-warning analysis
- recovery navigation
- reconstruction from stored simulation artifacts
- exploratory atlas-guided control

These older and experimental lines span structure discovery, navigation,
prediction, recovery, and archive reconstruction. They provide hypotheses and
historical context; they do not inherit the maintained V1 case's validation
status.

Its current boundary is equally important:

> This is benchmark and simulation research. It is not broad operational-grid
> validation, a production controller, or a deployed decision-support system.

For a runnable entry, use the
**[IEEE Geometry Showcase](APPLICATIONS/power_systems/ieee_geometry_v1/showcase/README.md)**.
For the broader archive and research program, use the
**[Power Systems README](APPLICATIONS/power_systems/README.md)**.

---

## 🔬 Research and Evidence

The **[Research layer](RESEARCH/README.md)** organizes questions, concepts,
validation material, findings, and theoretical extensions.

Its major areas are:

| Area | Role |
|---|---|
| `FOUNDATION/` | Structural assumptions and vocabulary |
| `CORE_CONCEPTS/` | Field, phase, mismatch, geometry, and JANUS |
| `VALIDATION/` | Empirical and cross-system tests |
| `FINDINGS/` | Condensed observations with scoped claims |
| `APPLIED_CASES/` | System-specific research indexes and studies |
| `THEORETICAL_EXTENSIONS/` | Exploratory formalization |
| `NEXAH_TRANSLATIONS/` | Connections to adjacent disciplines |

Current validation material includes synthetic dynamical systems,
synchronization models, transition-control experiments, fractal parameter
studies, and grid-inspired benchmark work.

The repository uses three broad interpretation levels:

```text
validated
→ reproducible evidence within a stated scope

experimental
→ implemented or observed, but not yet generalized

theoretical
→ conceptual extension requiring further formalization
```

Historical and exploratory material is retained when it helps reconstruct how a
method or hypothesis developed. It is not automatically treated as current
evidence.

Recommended research path:

1. **[Research Portal](RESEARCH/README.md)**
2. **[Research Abstract](RESEARCH/ABSTRACT.md)**
3. **[Core Concept Map](RESEARCH/CORE_CONCEPT_MAP.md)**
4. **[Validation Portal](RESEARCH/VALIDATION/)**
5. **[Findings](RESEARCH/FINDINGS/)**

---

## 🔥 Highlight: Janus Operator

The **[Janus Operator](RESEARCH/CORE_CONCEPTS/JANUS_OPERATOR/)** is a central
exploratory mechanism in NEXAH.

It compares forward and backward local flow structure within a reconstructed
representation:

```text
high directional coherence
→ locally aligned motion

low directional coherence
→ candidate transition sensitivity or aperture
```

Experiments investigate whether transition samples cluster around structured
geometric regions such as corridors, shell crossings, spines, or recursive
apertures.

The Janus directory contains mathematical notes, code, visuals, and validation
experiments. It remains an experimental mechanism rather than a generalized
transition law.

---

## 🧱 Repository Layers

NEXAH now has a maintained Orientation Kernel and applications, while the
repository remains a broader research ecosystem rather than one runtime for
every historical and experimental module:

```text
NEXAH/
├── START_HERE.md                 guided conceptual entry
├── VISUAL_GALLERY.md             curated visual entry
├── nexah/                        kernel start, contracts, package, CLI, safety
├── PROTO_CORE/                   reference and prototype implementations
├── RESEARCH/                     questions, evidence, and findings
├── APPLICATIONS/                 tools and system-specific programs
├── ARCHITECTURE/                 relationships and maturity mapping
├── EXPERIMENTAL/                 active labs and historical lineages
└── REPOSITORY_MAP.md             complete navigation map
```

The areas relate approximately as follows:

```text
research question
→ experimental exploration
→ reference implementation
→ validation and findings
→ system-specific application
```

This is a development path, not a guarantee that every experiment progresses
through every stage.

### Kernel

**[nexah/](nexah/START_HERE.md)** contains the current installable kernel,
typed Orientation contracts, representation backends, reporting, memory,
domain components, CLI, and safety boundary. This is the preferred entry for
someone who wants to use the current software.

### Proto Core

**[PROTO_CORE/](PROTO_CORE/)** contains the verified Demonstrator, experimental
Field Layer, and an older NEXAH Core development lineage. The Demonstrator is
the preferred visual reference; the other modules are method-development areas.

### Applications

**[APPLICATIONS/](APPLICATIONS/)** presents concrete tools, demonstrations, and
system-specific studies. “Application” means that a method is applied to a
particular system or user task; it does not automatically mean production-ready
software.

### Experimental

**[EXPERIMENTAL/](EXPERIMENTAL/)** preserves active laboratories, prototypes,
and historical development trees. Its portal distinguishes active labs,
experimental systems, historical references, archives, and promotion
candidates.

For the directory-by-directory view, use the
**[Repository Map](REPOSITORY_MAP.md)**.

---

## 📊 Status and Boundaries

| Area | Current status |
|---|---|
| Reference Demonstrator | Verified executable entry |
| Python package and CLI | Installable research kernel; typed public contracts |
| Orientation Layer | Implemented from source adapter to report and bounded memory |
| Network Orientation | Verified illustrative graph application with V1/V2 gates |
| IEEE Geometry V1 | Phase V complete; frozen IEEE-9/IEEE-14 benchmark path |
| Orientation Brief | Implemented in JSON and human-readable Markdown |
| Episodic memory | Append-only and retrieval-capable; observed-outcome firewall required |
| Observed-evidence bridge | Documented; no external operational dataset admitted |
| Field reconstruction | Implemented in reference and experimental forms |
| Transition representation | Demonstrator-level and experiment-dependent |
| Gate Operator | Implemented as continuous local-instability measure |
| General geometry extraction | Experimental and representation-dependent |
| Navigation beyond supplied representations | Exploratory prototypes |
| Control and execution | Outside the public kernel; no execution authority |
| Cross-system comparison | Available in selected studies; not generalized |
| Power systems | Maintained IEEE Geometry case plus extensive experiment archive |
| Unified runtime for all repository concepts | Not available |
| Stable API across historical modules | Not available |
| Production readiness | Not claimed |

NEXAH currently provides:

- a typed, evidence-bound Orientation path
- maintained graph and IEEE benchmark applications
- reproducible Orientation Reports and Briefs
- explicit provenance, uncertainty, failure, and claim boundaries
- guarded episodic storage and retrieval
- reproducible reference demonstrations
- selected scoped empirical and computational observations
- geometry-oriented interpretations
- semi-formal structural models
- a large visual and experimental archive

It does not yet provide:

- universal proofs or generalized physical laws
- a closed mathematical formalization
- broad independent reproduction
- operational-grid validation
- production deployment guarantees
- autonomous action or causal intervention guarantees
- one integrated implementation of every conceptual layer

The authoritative maturity overview is
**[ARCHITECTURE/SYSTEM_STATE.md](ARCHITECTURE/SYSTEM_STATE.md)**.

---

## 🌀 Visual Atlas

![NEXAH Navigation Grammar](ARCHITECTURE/archive/NEXAH_NAVIGATION_GRAMMAR.png)

The repository contains the computational, documentary, and empirical layers of
NEXAH. The companion **[NEXAH Atlas on Are.na](https://www.are.na/nexah-scarabaeus1031/channels)**
contains visual essays, system atlases, research notebooks, and orientation
paths.

Current Atlas entry points include:

- Core Orientation
- The Visitor’s Guide
- The Operator’s Handbook
- System Atlases
- historical NEXAH Atlas volumes
- Design Orientation

The two surfaces have different roles:

```text
GitHub
→ code, methods, evidence, status, reproducibility

Are.na
→ visual orientation, editorial sequence, conceptual exploration
```

The long-term goal is not to make them identical, but to connect them through
explicit mappings between repository modules and Atlas channels.

---

## 🤝 How to Explore and Contribute

NEXAH benefits from collaboration across:

- dynamical systems
- topology and geometry
- synchronization research
- control theory
- network science
- scientific visualization
- statistical modeling
- scientific computing

Useful contributions include:

- reproducing a scoped experiment
- testing a representation under changed parameters
- comparing a method with an established baseline
- formalizing an experimental definition
- documenting failed or negative results
- improving a user-facing application
- connecting visual claims to exact evidence paths

Good starting points:

- **New visitor:** [START_HERE.md](START_HERE.md)
- **Kernel user:** [nexah/START_HERE.md](nexah/START_HERE.md)
- **Researcher:** [RESEARCH/README.md](RESEARCH/README.md)
- **Developer:** [ARCHITECTURE/SYSTEM_STATE.md](ARCHITECTURE/SYSTEM_STATE.md)
- **Applied-systems reader:** [APPLICATIONS/README.md](APPLICATIONS/README.md)
- **Experimental explorer:** [EXPERIMENTAL/README.md](EXPERIMENTAL/README.md)
- **Safety reviewer:** [nexah/SAFETY_AND_MISUSE.md](nexah/SAFETY_AND_MISUSE.md)

---

## ⚡ Final Perspective

NEXAH begins with a possibility:

```text
Complex systems may not transition randomly.

Their trajectories may pass through structured regions
that shape transition pathways,
recovery possibilities,
and potential intervention behavior.
```

The repository does not treat that possibility as settled theory. It turns it
into visualizations, implementations, benchmarks, and questions that can be
inspected.

Run the demonstrator. Follow the evidence. Compare representations. Challenge
the maps.

The goal is not certainty.

The goal is orientation within complexity.

---

**Thomas K. R. Hofmann · NEXAH · 2026**
