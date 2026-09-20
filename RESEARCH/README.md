# NEXAH Research

NEXAH Research is the canonical home for the mathematical school, conceptual
foundations, system definitions, research synthesis, and open questions of
NEXAH.

It connects established mathematics, NEXAH representations, bounded
computational results, and historical sources without treating them as one
authority or one physical mechanism.

This is a maintained research corpus and framework, not a finalized theory.
Whether a research cycle is operationally active is decided by Mission
Control, not by the presence of material in this directory.

---

## 🧭 Start Here

Choose the entry that matches your goal:

| Goal | Start with |
|---|---|
| Understand NEXAH in a few minutes | **[ABSTRACT.md](ABSTRACT.md)** |
| Check the meaning of a mathematical term | **[Mathematical Foundations and Glossary](FOUNDATION/MATHEMATICAL_FOUNDATIONS_GLOSSARY.md)** |
| Navigate mathematics, models, experiments, and historical sources | **[MATHEMATICS_MAP.md](MATHEMATICS_MAP.md)** |
| Follow the recommended research path | **[RESEARCH_INDEX.md](RESEARCH_INDEX.md)** |
| Understand the conceptual direction | **[RESEARCH_VISION.md](RESEARCH_VISION.md)** |
| See how the central concepts connect | **[CORE_CONCEPT_MAP.md](CORE_CONCEPT_MAP.md)** |
| Check neutral definitions of studied systems | **[SYSTEM_MODELS/](SYSTEM_MODELS/)** |
| Locate bounded tests and evidence | **[VALIDATION/](VALIDATION/)** |
| Recover historical mathematical material | **[Historical pointers](HISTORY/CODEX_MATHEMATICS_POINTERS.md)** |
| Read the integrated manuscript | **[PAPER_DRAFT.md](PAPER_DRAFT.md)** |
| Run the reference implementation | **[NEXAH Demonstrator](../PROTO_CORE/NEXAH_DEMONSTRATOR/)** |

Recommended first reading:

```text
ABSTRACT
→ MATHEMATICAL FOUNDATIONS AND GLOSSARY
→ MATHEMATICS MAP
→ RESEARCH VISION
→ CORE CONCEPT MAP
→ VALIDATION
→ FINDINGS
```

For complete navigation through the research archive, use
**[RESEARCH_INDEX.md](RESEARCH_INDEX.md)**.

---

## Ownership and migration rule

```text
NEXAH Research  -> definitions, mathematical framing, synthesis, open questions
Science Lab     -> protocols, controls, evidence packages, bounded decisions
Applications    -> domain programs and implementations
ORION           -> certified deterministic engineering
Library / Books -> cultural, editorial, and narrative Works
Mission Control -> currentness, routing, activation, and source bindings
NEXAH-CODEX     -> frozen exploratory provenance
```

Material is not moved here merely because it is mathematically interesting.
Use the following rule:

- maintain a canonical definition or synthesis here;
- leave code, datasets, test reports, and outputs with their owning package;
- add a pointer when an existing topic becomes relevant;
- import a historical artifact only when a current research object genuinely
  depends on it;
- never promote visual similarity or symbolic language into a shared mechanism
  by directory placement alone.

Accordingly, Lorenz, Roessler, Halvorsen, Kuramoto, Mandelbrot/Julia,
prime-residue and CRT work, IEEE field reconstructions, QRT, grids, cuts,
projections, residuals, and invariants are now jointly navigable through the
Mathematics Map. Their evidence and implementation files remain where they are
owned.

---

## 🌌 Research Perspective

The current operational perspective is:

```text
dynamics
→ trajectory reconstruction
→ field structure
→ directional coherence
→ transition geometry
→ phase and mismatch
→ connectivity and topology
→ navigation and control
```

The framework studies whether observed system behavior contains recurring
organization such as:

- coherent regions and persistent trajectories
- transition corridors and bottlenecks
- phase-dependent activation
- directional transport structure
- aperture and shell-crossing geometry
- emergent connectivity and topology
- recovery pathways and navigable state-space atlases

![Interactive Navigation Map](./FOUNDATION/visuals/interactive_navigation_map.png)

---

## 🔬 Current Working Hypothesis

Across the systems investigated so far, transition behavior appears to be
associated with more than instability magnitude alone. Current experiments
study the interaction between:

```text
instability
→ transition potential

phase mismatch
→ possible activation mechanism

directional coherence
→ transport organization
```

Operational mismatch is currently represented as:

$$M(t)=|\omega(t)-\hat{\omega}(t)|$$

These relationships are empirical research findings under continued
validation. They are not presented as universal laws.

---

## 🪞 JANUS Transition Geometry

The **[JANUS Operator](CORE_CONCEPTS/JANUS_OPERATOR/)** is one of the central
exploratory mechanisms in NEXAH. It compares forward and backward local flow
organization to investigate:

- directional coherence
- aperture regions
- shell crossings
- transport corridors
- recursive orientation structure
- transition sensitivity

![JANUS Orientation Atlas](./CORE_CONCEPTS/JANUS_OPERATOR/outputs/janus_transition_orientation_atlas.png)

JANUS results currently suggest that detected transitions can concentrate
around structured directional regions. The strength and generality of this
observation remain active research questions.

---

## ⚡ Emerging Atlas Perspective

The most developed application work increasingly interprets reconstructed
state spaces as atlases containing:

- Basin Territories
- Attractors
- Transport Corridors
- Gates and Bottlenecks
- Recovery Regions
- Recovery Anchors

```text
trajectory
→ field
→ geometry
→ atlas
→ navigation
→ recovery
→ control
```

Large-scale atlas experiments currently take place in the
**[Power Systems application](../APPLICATIONS/power_systems/)**. Whether similar
atlas structures generalize across broader classes of nonlinear systems
remains open.

---

## 🗂️ Research Structure

| Area | Role | Status |
|---|---|---|
| **[FOUNDATION/](FOUNDATION/)** | Assumptions, variables, structural grammar | Foundational |
| **[CORE_CONCEPTS/](CORE_CONCEPTS/)** | Field, phase, mismatch, geometry, JANUS | Current conceptual core |
| **[VALIDATION/](VALIDATION/)** | Reproducibility, robustness, and cross-system experiments | Evidence corpus |
| **[FINDINGS/](FINDINGS/)** | Condensed observations from experiments | Research synthesis |
| **[APPLIED_CASES/](APPLIED_CASES/)** | Concrete dynamical systems and scenarios | Applied research |
| **[FIGURES/](FIGURES/)** | Curated visual synthesis and paper figures | Visual evidence |
| **[NEXAH_TRANSLATIONS/](NEXAH_TRANSLATIONS/)** | Connections to adjacent disciplines | Interpretive layer |
| **[THEORETICAL_EXTENSIONS/](THEORETICAL_EXTENSIONS/)** | Operator, topology, and future formalization | Exploratory |
| **[NEXAH_DEVELOPMENT/](NEXAH_DEVELOPMENT/)** | Earlier prototypes and development tracks | Legacy / experimental |
| **[HISTORY/](HISTORY/)** | Historical context | Archive |
| **[NOTES/](NOTES/)** | Informal working notes | Non-canonical |
| **[SYSTEM_MODELS/](SYSTEM_MODELS/)** | Neutral system definitions and pointers | Navigation |

The directory names describe research roles, not confidence levels. Check the
status and limitations stated inside each experiment before treating a result
as established evidence. They also do not declare an operationally active
research cycle.

---

## 🧪 Evidence Path

Readers who want to inspect evidence rather than the conceptual overview
should proceed through:

1. **[Evidence Atlas](../docs/evidence/README.md)** — non-authoritative
   claim-level navigation to owning sources
2. **[VALIDATION/README.md](VALIDATION/README.md)** — validation program
3. **[FINDINGS/README.md](FINDINGS/README.md)** — condensed observations
4. **[APPLIED_CASES/README.md](APPLIED_CASES/README.md)** — system-specific cases
5. **[FIGURES/README.md](FIGURES/README.md)** — visual synthesis
6. **[PAPER_DRAFT.md](PAPER_DRAFT.md)** — integrated argument

The executable reference pipeline is maintained separately in the
**[NEXAH Demonstrator](../PROTO_CORE/NEXAH_DEMONSTRATOR/)**.

---

## ⚠️ Scientific Scope

The Research Layer contains:

- reproducible and partially reproducible experiments
- empirical observations
- exploratory mechanisms
- semi-formal structural models
- hypotheses requiring broader validation

It does not currently provide:

- a universal theory of dynamical systems
- general mathematical proofs of the proposed mechanisms
- production-grade control guarantees
- comprehensive real-world validation

Claims should therefore be read according to their local evidence and stated
status: **empirical**, **experimental**, or **theoretical**.

---

## 🧭 Related Methodological Research

Methodological research also occurs inside bounded application programs.
**[Orientation Translation](../APPLICATIONS/orientation_translation/)** studies
how fixed public representations are separated, compared, navigated, explained,
audited, and stopped. It remains physically owned by Applications; this link
records conceptual participation in Research rather than directory transfer,
semantic authority, or canonical Method status.

Its current reviews preserve open questions concerning reader effect,
analyst-independent reproduction, sequence necessity, and method stability.
See **[Meta Review 01](../APPLICATIONS/orientation_translation/reviews/meta_review_01/META_REVIEW_REPORT.md)**
and **[Method Archaeology 01](../APPLICATIONS/orientation_translation/studies/method_archaeology_01/STUDY_REPORT.md)**.

---

## 🔗 Related Entry Points

- **[Repository overview](../README.md)**
- **[Mission Control Research Atlas](https://github.com/Scarabaeus1031/NEXAH-Mission-Control/blob/codex/mission-control-status-sync/CURRENT/RESEARCH_ATLAS.md)**
- **[Science Lab](https://github.com/Scarabaeus1031/NEXAH-Science-Lab)**
- **[Architecture visual guide](../ARCHITECTURE/visuals/README.md)**
- **[Architecture](../ARCHITECTURE/README.md)**
- **[NEXAH Demonstrator](../PROTO_CORE/NEXAH_DEMONSTRATOR/)**
- **[Power Systems validation](../APPLICATIONS/power_systems/)**

---

**NEXAH Research Layer**

Transition Geometry · Directional Coherence · Systems Cartography

Thomas K. R. Hofmann · 2026
