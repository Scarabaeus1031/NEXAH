# 🏗️ NEXAH — Architecture

This directory explains how the current NEXAH repository is organized, how its
conceptual layers relate, and which parts are actually implemented.

NEXAH does not yet have one unified runtime architecture. The architecture is a
combination of:

- a conceptual research pipeline
- a verified reference demonstrator
- experimental method and application modules
- a minimal installable Python package
- historical development lineages

---

## 🧭 Start Here

| Question | Document |
|---|---|
| What is actually implemented? | **[SYSTEM_STATE.md](SYSTEM_STATE.md)** |
| Which computational methods are used? | **[METHODS.md](METHODS.md)** |
| What is the next concrete architecture plan? | **[Orientation Layer](orientation_layer/)** |
| What has been completed before Phase III? | **[Plateau A Closure](orientation_layer/PLATEAU_A_CLOSURE.md)** |
| How do repository areas relate? | Continue with this page |
| What can I run now? | **[NEXAH Demonstrator](../PROTO_CORE/NEXAH_DEMONSTRATOR/)** |
| Where is the empirical evidence? | **[Validation Portal](../RESEARCH/VALIDATION/)** |

`SYSTEM_STATE.md` is the source of truth for implementation maturity and known
limitations. Conceptual diagrams should not be read as proof that every layer
exists as an integrated software component.

---

## 🧠 Conceptual Architecture

The working NEXAH research pipeline is:

```text
dynamics
→ structure extraction
→ field reconstruction
→ geometric interpretation
→ stability and transition analysis
→ experimental control
→ exploratory navigation
```

An extended research model also investigates constraint behavior:

```text
geometry
→ observed admissible motion
→ candidate constraints
→ structure-aware intervention
```

This constraint layer is a hypothesis derived from experiments in which local
perturbations were absorbed and trajectories returned toward recurring
structure. It is not yet a formal manifold model or an implemented standalone
layer.

![NEXAH Architecture Flow](<archive/NEXAH_Architecture_Flow(Updated).png>)

The diagram is a conceptual map of the intended relationships. Some labels
reflect earlier development phases and do not correspond directly to current
root directories.

---

## 🛠️ Implemented Repository Architecture

```text
NEXAH/
├── nexah/                          minimal installable package and CLI
├── PROTO_CORE/
│   ├── NEXAH_DEMONSTRATOR/         verified reference pipeline
│   ├── FIELD_LAYER/                experimental methods laboratory
│   └── NEXAH_CORE/                 legacy development lineage
├── ARCHITECTURE/CORE/
│   ├── field_reconstruction/       experimental reconstruction studies
│   └── control_layer/              experimental control prototypes
├── RESEARCH/                       concepts, validation, and findings
├── APPLICATIONS/                   system-specific tools and studies
└── EXPERIMENTAL/                   labs and historical prototypes
```

There are no current root modules named `ARCHY`, `DISCOVERY_ENGINE`,
`FIELD_LAYER`, or `NAVIGATOR`. Those names describe earlier or conceptual
components and should be interpreted through the current paths above.

---

## 📊 Component Status

| Component | Current implementation | Status |
|---|---|---|
| Trajectory analysis | Demonstrator, package, research scripts | Implemented in multiple forms |
| Transition representation | Demonstrator and experimental pipelines | Empirical / demonstrator-level |
| Field reconstruction | Proto Core and Architecture prototypes | Experimental |
| Gate Operator | Demonstrator and historical experiments | Implemented as local-instability measure |
| Geometry extraction | Field and application scripts | Experimental, representation-dependent |
| Control | Prototype scripts and application experiments | Experimental |
| Navigation | Demonstrator and several prototype lines | Exploratory |
| Constraint layer | Observed absorption/re-alignment behavior | Theoretical interpretation of experiments |
| Unified runtime kernel | Not available | Open work |
| Stable cross-module API | Not available | Open work |

---

## 🧪 Verified Reference Path

The most reliable end-to-end implementation is the
**[NEXAH Demonstrator](../PROTO_CORE/NEXAH_DEMONSTRATOR/)**:

```text
trajectory simulation
→ transition structure
→ continuous instability field
→ navigation behavior
→ generated outputs
```

The Demonstrator establishes a shared reference for discussing implementation
behavior. It does not validate every broader architectural claim.

---

## 🌊 Experimental Architecture Modules

### Field Reconstruction

**[ARCHITECTURE/CORE/field_reconstruction/](CORE/field_reconstruction/)**
contains visual and computational studies of:

- trajectory-to-field reconstruction
- boundaries and stability masks
- flow channels
- frame and noise sensitivity
- target-guided navigation prototypes

Its strongest architectural contribution is the explicit distinction between
well-supported regions and interpolation-dominated regions.

### Control Layer

**[ARCHITECTURE/CORE/control_layer/](CORE/control_layer/)** contains prototypes
for:

- basin and separatrix extraction
- gate-field analysis
- trajectory steering
- gate tracking and routing
- adaptive and multi-agent navigation

These scripts demonstrate possible interactions with reconstructed geometry.
They do not establish general controllability or a production control layer.

---

## 🪞 Current Gate Interpretation

Later Demonstrator experiments refined the Gate Operator interpretation:

```text
Gate Operator G(x)
→ continuous local-instability field

Structural transition
→ discrete change in a trajectory-derived representation
```

High instability can interact with transition behavior, but the Gate Operator
does not directly detect transition events. Architecture and method documents
should use this corrected distinction.

---

## 🔁 Relationship Between Repository Layers

```text
RESEARCH
→ asks questions, validates observations, and records findings

PROTO_CORE
→ exposes reference implementations and method development

ARCHITECTURE
→ explains relationships, implementation status, and system boundaries

APPLICATIONS
→ applies methods to concrete systems and user workflows

nexah/
→ provides the minimal installable package and CLI
```

The architecture is therefore repository-wide. `ARCHITECTURE/CORE` is only one
experimental implementation area, not the complete NEXAH runtime.

---

## 📏 Methods and Evidence

The **[Methods document](METHODS.md)** describes implemented techniques,
experimental heuristics, and theoretical interpretations. Individual methods
must be read together with their status and evidence path.

Primary evidence and application layers:

- **[Validation](../RESEARCH/VALIDATION/)**
- **[Findings](../RESEARCH/FINDINGS/)**
- **[Applications](../APPLICATIONS/)**
- **[Power Systems](../APPLICATIONS/power_systems/)**

IEEE work currently uses benchmark models and repository-generated simulation
archives. It is not yet operational grid validation.

---

## ⚠️ Current Architectural Boundaries

NEXAH does not yet provide:

- one integrated implementation of the complete conceptual pipeline
- a formal constraint or manifold layer
- generalized transition detection across domains
- validated system-independent control
- stable APIs between research, methods, and applications
- comprehensive independent reproduction
- production deployment guarantees

These gaps are explicit architecture work, not hidden implementation claims.

---

## 🛣️ Development Priorities

The active consolidation plan is the
**[Orientation Layer Bauplan](orientation_layer/)**. It defines typed contracts,
a characterized v0.7 backend adapter, evidence-aware orientation reports, and a
bounded validation path. Its specifications supersede broad capability diagrams
as implementation guidance.

Useful architecture work includes:

- consolidating a minimal runtime interface
- separating reusable methods from versioned experiments
- defining data contracts between field, transition, and application layers
- attaching quantitative evidence to architectural claims
- formalizing what “constraint” means operationally
- comparing navigation prototypes under shared metrics
- promoting stable methods into the installable package

---

## 🔗 Related Entry Points

- **[System State](SYSTEM_STATE.md)**
- **[Methods](METHODS.md)**
- **[Orientation Layer Bauplan](orientation_layer/)**
- **[Proto Core Index](../PROTO_CORE/README.md)**
- **[Applications Index](../APPLICATIONS/README.md)**
- **[Research Portal](../RESEARCH/README.md)**
- **[Repository Map](../REPOSITORY_MAP.md)**

---

**NEXAH Architecture**

Conceptual Pipeline · Implemented Modules · Experimental Boundaries
