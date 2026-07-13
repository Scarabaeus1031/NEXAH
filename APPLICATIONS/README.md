# 🌍 NEXAH — Applications

The Applications Layer is where NEXAH methods meet concrete systems.

It contains runnable demonstrations, system-specific research programs,
integration tools, conceptual models, and experimental navigation prototypes.
These are not finished products. They are working environments for asking:

> Which parts of a dynamical system can be reconstructed, compared, and
> navigated using structural field methods?

---

## 🧭 What “Application” Means Here

In NEXAH, an application can be:

- a **runnable tool** that produces an analysis or visualization
- a **reference system** used to test a method
- an **applied research program** with experiments and evidence
- an **adapter** that translates another system into a NEXAH representation
- an **experimental prototype** exploring a possible future capability
- a **conceptual model** describing how a class of systems might be represented

The status of each area matters. A runnable script is not automatically a
validated method, and a promising experiment is not automatically a deployable
application.

---

## 🚀 Start Here

| You want to… | Start with |
|---|---|
| Run the verified visual reference pipeline | **[NEXAH Demonstrator](../PROTO_CORE/NEXAH_DEMONSTRATOR/)** |
| Orient a declared network and compare its structure | **[network_orientation/](network_orientation/)** |
| Explore a compact Lorenz application | **[demos/lorenz_demo/](demos/lorenz_demo/)** |
| Study Lorenz field and geometry analysis | **[dynamical_systems/lorenz/](dynamical_systems/lorenz/)** |
| Compare a different chaotic flow | **[dynamical_systems/halvorsen/](dynamical_systems/halvorsen/)** |
| Explore the most developed applied program | **[power_systems/](power_systems/)** |
| Connect another system to NEXAH | **[adapters/](adapters/)** |
| Inspect experimental navigation tools | **[navigation/](navigation/)** |
| Understand the conceptual model families | **[models/dynamical_models/](models/dynamical_models/)** |

If you are completely new to NEXAH, begin with the repository
**[START_HERE](../START_HERE.md)** before entering an application program.

---

## 🗂️ Application Map

| Area | What it offers | Current status |
|---|---|---|
| **[Network Orientation](network_orientation/)** | Typed graph topology, reachability, structural comparison, five read-only probes, and V1/V2 fixtures | Verified illustrative application |
| **[Power Systems](power_systems/)** | IEEE benchmark studies, stability fields, atlas discovery, prediction, recovery, and control experiments | Active applied research |
| **[Lorenz Research](dynamical_systems/lorenz/)** | Density, FTLE, Lyapunov, separatrix, regime, and navigation analysis | Active reference system |
| **[Halvorsen Research](dynamical_systems/halvorsen/)** | Distributed transport, transition graphs, residue models, reachability, and policy experiments | Experimental research |
| **[Lorenz Demo](demos/lorenz_demo/)** | Compact visual pipeline for geometry and transport structures | Runnable demonstration |
| **[Lorenz Core Demos](core_demos/lorenz/)** | Historical progression from pattern detection to navigation and meta-control | Reference / legacy series |
| **[Adapters](adapters/)** | Interfaces and examples for Lorenz, Kuramoto, grids, traffic, and supply chains | Experimental integration layer |
| **[Navigation](navigation/)** | Mod-77, drift quantization, Phi-Split, and IEEE9 navigation prototypes | Legacy / experimental prototype |
| **[Dynamical Models](models/dynamical_models/)** | Stability, gradient, drift, and regime model documents | Theoretical reference |
| **[Datasets](datasets/)** | Synthetic JSON system descriptions | Reference data; documentation incomplete |
| **[Archive](archive/)** | Superseded prototypes and former root demos | Archived |

---

## ⚡ Power Systems

**[APPLICATIONS/power_systems/](power_systems/)** is currently the most
developed applied research program in NEXAH.

It investigates whether simulated and benchmark power-system states can be
organized into structural representations containing:

- operating regions and basin-like territories
- transition corridors
- warning and critical regimes
- recovery pathways
- candidate anchors and bottlenecks
- atlas-guided intervention concepts

Primary environments include:

| Environment | Role |
|---|---|
| **[FIELD_NAVIGATION_VALIDATION/](power_systems/FIELD_NAVIGATION_VALIDATION/)** | Main atlas, prediction, recovery, and reconstruction experiment series |
| **[VALIDATION_LAYER/](power_systems/VALIDATION_LAYER/)** | Quantitative indicators and validation experiments |
| **[ieee_xray_pipeline/](power_systems/ieee_xray_pipeline/)** | Feature and geometry reconstruction pipeline |
| **[nexah_ieee9/](power_systems/nexah_ieee9/)** | Compact IEEE9 navigation and control environment |
| **[nexah_ieeeX/](power_systems/nexah_ieeeX/)** | Scaling studies across larger IEEE benchmark networks |
| **[stability_field_dynamics/](power_systems/stability_field_dynamics/)** | Broad stability-field and IEEE experiment archive |

Current questions include:

- Do warning regimes appear before simulated collapse?
- Which structural indicators remain stable across IEEE network sizes?
- Can recovery trajectories be grouped into recurring archetypes?
- How much of an atlas can be reconstructed from historical simulation artifacts?
- Which proposed control actions survive comparison with established
  power-system methods?
- What changes when repository experiments are tested against operational data?

This work uses IEEE benchmark models and repository-generated simulation
archives. It should not yet be interpreted as operational grid validation or a
production control system.

For detail, use the **[Power Systems README](power_systems/README.md)** and
**[Power Systems Index](power_systems/INDEX_power-system-applications.md)**.

---

## 🕸️ Network Orientation

**[Network Orientation](network_orientation/)** is the first maintained,
graph-native application of the typed Orientation Layer. It turns declared
nodes and directed edges into an evidence-bound structural report containing
paths, reachability, components, bottlenecks, missing information, and explicit
uncertainty.

Its Supply Chain and Ecosystem inputs are illustrative fixtures. Their authored
regime, risk, action, and shock fields are excluded. The application is designed
for learning how maps and paths change, not for issuing control commands.

---

## 🌀 Dynamical Systems

The **[Dynamical Systems](dynamical_systems/)** area provides reference systems
for developing and comparing NEXAH methods.

### Lorenz

**[dynamical_systems/lorenz/](dynamical_systems/lorenz/)** contains the broadest
non-power-system analysis environment:

- attractor and density reconstruction
- FTLE and Lyapunov analysis
- filament and separatrix extraction
- regime and switching maps
- flow-field visualization
- exploratory navigation

Lorenz is the main reference system for recognizable switching behavior and
well-known chaotic geometry.

### Halvorsen

**[dynamical_systems/halvorsen/](dynamical_systems/halvorsen/)** provides a
contrasting flow geometry with distributed rotational transport. It contains:

- transition and coarse-graining experiments
- graph connectivity and reachability
- candidate gate and policy studies
- residue-flow comparisons
- Lorenz/Halvorsen visual comparisons

The comparison asks which observed NEXAH structures depend on the system and
which recur across different representations.

---

## 🎬 Demonstrations

NEXAH currently has several demo layers with different roles:

| Demo | Role |
|---|---|
| **[PROTO_CORE/NEXAH_DEMONSTRATOR](../PROTO_CORE/NEXAH_DEMONSTRATOR/)** | Canonical, verified hands-on entry |
| **[demos/lorenz_demo](demos/lorenz_demo/)** | Compact application-level Lorenz visualization |
| **[core_demos/lorenz](core_demos/lorenz/)** | Historical development series and visual archive |

The existence of several Lorenz areas reflects the development history. New
users should choose the canonical demonstrator first.

---

## 🔌 Adapters and Integration

The **[Adapter Layer](adapters/)** explores a minimal translation boundary
between an external system and a structural NEXAH representation.

Examples currently cover:

- Lorenz
- Kuramoto
- power-grid abstractions
- supply chains
- traffic systems
- synthetic energy grids

These adapters are useful prototypes and starting points for contributors.
They are not yet a stable public integration API.

Questions for this layer:

- What is the minimum information a system must expose?
- Which state, transition, phase, or graph representation is appropriate?
- Can different domains share one adapter contract without losing essential
  dynamics?
- How should uncertainty and measurement noise enter the representation?

---

## 🧭 Experimental Navigation

The **[navigation/](navigation/)** directory contains an earlier experimental
navigation line based on Mod-77 state spaces, drift quantization, Phi-Split
events, and an IEEE9-style prototype.

It is preserved because it contains executable ideas and useful research
questions. It is not the canonical NEXAH navigation layer and is not integrated
with every current application.

---

## 🧠 Models and Synthetic Data

The **[Dynamical Models](models/dynamical_models/)** documents describe a
conceptual progression:

```text
stability landscape
→ gradient dynamics
→ drift dynamics
→ regime transitions
```

The **[datasets/](datasets/)** directory contains synthetic JSON descriptions
for energy grids, supply chains, ecosystems, and server clusters. The shared
`nodes`/`edges` subset used by the Supply Chain and Ecosystem fixtures now has a
typed consumer in **[Network Orientation V1](network_orientation/)**. Other
metadata and datasets remain historical reference material with inconsistent
schemas.

---

## 🧪 What Users Can Work On

This layer intentionally exposes open work. Useful contributions include:

- reproducing an experiment in a clean environment
- comparing structural indicators against standard baselines
- connecting a new system through an adapter
- documenting a synthetic dataset and its schema
- testing Lorenz-derived methods on another dynamical system
- evaluating IEEE results with power-system expertise
- replacing simulated archives with appropriate operational or public data
- separating representation artifacts from system-invariant behavior
- improving statistical treatment and uncertainty reporting

The goal is not to present every question as solved. The goal is to make the
current tools, evidence, and open problems inspectable.

---

## 📊 Status Language

| Status | Meaning |
|---|---|
| **Runnable demonstration** | A documented script or pipeline can be executed |
| **Active applied research** | Ongoing system-specific experiments and evidence |
| **Experimental** | Promising implementation with limited validation |
| **Theoretical** | Conceptual model or proposed mechanism |
| **Legacy / reference** | Historical work retained for context or reuse |
| **Archived** | Superseded material outside the current entry path |

Runnable does not mean validated. Experimental does not mean ineffective. The
labels tell readers what kind of evidence and maintenance level to expect.

---

## ⚠️ Current Boundaries

The Applications Layer does not yet provide:

- a unified application API
- production deployment guarantees
- comprehensive real-world operational validation
- one reproducibility command for every historical experiment
- stable interfaces across all adapters and navigation prototypes
- independent validation of the major application claims

These are collaboration opportunities, not hidden assumptions.

---

## 🔗 Related Entry Points

- **[Repository Overview](../README.md)**
- **[Research Portal](../RESEARCH/README.md)**
- **[Validation Portal](../RESEARCH/VALIDATION/README.md)**
- **[Findings Portal](../RESEARCH/FINDINGS/README.md)**
- **[Architecture](../ARCHITECTURE/README.md)**
- **[NEXAH Demonstrator](../PROTO_CORE/NEXAH_DEMONSTRATOR/)**

---

**NEXAH Applications**

Systems · Tools · Evidence · Open Questions
