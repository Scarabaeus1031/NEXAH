# NEXAH — The Orientation Ecosystem

[![NEXAH CI](https://github.com/Scarabaeus1031/NEXAH/actions/workflows/ci.yml/badge.svg)](https://github.com/Scarabaeus1031/NEXAH/actions/workflows/ci.yml)
[![Public Experience](https://img.shields.io/badge/public_experience-nexah.de-0b2745)](https://nexah.de)
[![Code License: Apache 2.0](https://img.shields.io/badge/code-Apache--2.0-b48738)](LICENSE)

**Understanding before action.**

NEXAH is an **evidence-bound orientation ecosystem** for making relationships,
limits, and possible transitions between bounded representations inspectable
and navigable. It exists because knowledge is distributed across many maps,
models, disciplines, and forms—and moving responsibly between them is itself a
problem of orientation.

> NEXAH does not replace knowledge, domain expertise, or human judgment. It
> does not claim universal truth or authorize action.

![NEXAH — an evidence-bound orientation ecosystem with six coordinated responsibilities](assets/readme/nexah-orientation-ecosystem-hero.png)

---

## Choose Your Entry Point

| I want to… | Begin here |
|---|---|
| Enter the public Experience | **[nexah.de](https://nexah.de)** — the public entrance to NEXAH |
| Inspect deterministic navigation | **[NEXAH-ORION](https://github.com/Scarabaeus1031/NEXAH-ORION)** — navigation, reports, validation and LYRA |
| Inspect the Experience source | **[NEXAH-Experience](https://github.com/Scarabaeus1031/NEXAH-Experience)** — public presentation, Library, Living Atlas, Laboratory and Reading Spaces |
| Understand the purpose and principles | **[Ecosystem Constitution v1.0](GOVERNANCE/ECOSYSTEM_CONSTITUTION.md)** · **[Governance Index](GOVERNANCE/README.md)** · **[NEXAH Manifesto](MANIFESTO.md)** |
| Read the published specification | **[Orientation Language](ORIENTATION_LANGUAGE/README.md)** |
| Use or develop the software | **[Orientation Kernel](nexah/README.md)** |
| Inspect research and evidence | **[Research Portal](RESEARCH/README.md)** |
| Explore Works, journeys, or editorial practice | **[Begin with THE ATLAS OF ATLASES](docs/library/atlas-of-atlases/README.md)** · **[Public Library on Are.na](https://www.are.na/nexah-scarabaeus1031/channels)** · **[Library Architecture & Registry](LIBRARY/README.md)** · **[Editorial Operating System](EDITORIAL_OPERATING_SYSTEM/README.md)** |
| Evaluate a domain application | **[Applications](APPLICATIONS/README.md)** |
| Inspect Orientation Translation pilots and methodological evidence | **[Applications / Orientation Translation](APPLICATIONS/orientation_translation/)** |

For the complete directory-level view, use the
**[Repository Map](REPOSITORY_MAP.md)**. Cross-system reader documentation is
indexed under **[Documentation](docs/README.md)**.

---

## Repository Organization

The six subsystems coordinate without sharing one authority:

![NEXAH architecture — six coordinated subsystems with equal responsibility](assets/readme/nexah-orientation-ecosystem-front-door.png)

The diagram shows what each subsystem is responsible for. The table records
where its authority stops:

| Subsystem | Authority boundary |
|---|---|
| **[Research](RESEARCH/README.md)** | Does not define released semantics or establish universality |
| **[Orientation Language](ORIENTATION_LANGUAGE/README.md)** | Does not execute implementations or establish domain validity |
| **[Implementations](nexah/README.md)** | Do not redefine semantics; conformance is explicit, never assumed |
| **[Applications](APPLICATIONS/README.md)** | Do not generalize beyond admitted evidence or redefine the language |
| **[Living Library](LIBRARY/README.md)** | Its Registry governs editorial identity, not OLS semantics |
| **[Editorial Operating System](EDITORIAL_OPERATING_SYSTEM/README.md)** | Editorial Governance does not replace Specification Governance |

The central distinction is simple: **the Orientation Language defines
semantics; implementations execute behavior; conformance must be demonstrated.**

The detailed responsibility and relationship map lives in
**[Architecture](ARCHITECTURE/README.md)**.

The adopted **[Ecosystem Constitution v1.0](GOVERNANCE/ECOSYSTEM_CONSTITUTION.md)**
is the highest governance document. The six repository subsystems are concrete
responsibility areas beneath that constitutional baseline; they are not
additional constitutional Houses. Earlier candidate work remains preserved as
non-canonical historical evidence in
**[Constitution Review 01](GOVERNANCE/constitution_review_01/README.md)**.

---

## Current State

- **Orientation Language 1.0** is published as the canonical semantic authority.
- **Orientation Kernel v0.7** is maintained as the current implementation track.
- **Research** remains active, scoped, and evidence-bound.
- **Reference applications** for Network Orientation and IEEE Geometry are maintained.
- **Library and Editorial infrastructure** operate within documented human-governance boundaries.

These are different maturity statements, not one repository-wide certification.
The existing tags, public releases and current package version are explained in
**[Release and Version History](RELEASES.md)**; no version in one responsibility
area versions the entire ecosystem.
The unnamed next Framework package is prepared in
**[Framework Release Candidate](FRAMEWORK_RELEASE_CANDIDATE.md)**. Its final
release identity remains an explicit owner decision.

---

## Run NEXAH

Install the current Python implementation:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Run one declared Network Orientation case:

```bash
nexah orient-network APPLICATIONS/datasets/supply_chain.json \
  --focus normal_operation \
  --target system_disruption \
  --domain supply-chain \
  --recorded-at 2026-07-13T22:45:00+00:00 \
  --format brief
```

The result is an inspectable report over the supplied representation—not a
real-world risk judgment or authorization to intervene.

Continue with the **[Kernel Start](nexah/START_HERE.md)**, browse
**[Applications](APPLICATIONS/README.md)**, or inspect the executable
**[NEXAH Demonstrator](PROTO_CORE/NEXAH_DEMONSTRATOR/README.md)**.

---

## Evidence and Limits

NEXAH keeps the following states separate:

```text
representation
→ orientation
≠ recommendation
≠ authorization
≠ execution
≠ observed outcome
```

The current repository supports typed orientation contracts, inspectable
reference applications, explicit provenance and claim boundaries, deterministic
replay, and guarded evidence handling.

It does **not** currently claim:

- universal transition laws or a closed theory
- automatic OLS conformance for any implementation
- broad real-world validation or calibrated uncertainty across domains
- causal intervention guarantees or autonomous execution authority
- production readiness or one unified runtime for every repository lineage

Complete implementation status and limitations are maintained in
**[System State](ARCHITECTURE/SYSTEM_STATE.md)**. Before using sensitive,
personal, or operational data, read
**[Safety and Misuse Boundaries](nexah/SAFETY_AND_MISUSE.md)**.

---

## Repository Structure

```text
NEXAH/
├── RESEARCH/                     evidence
├── ORIENTATION_LANGUAGE/         semantics
├── nexah/                        implementations
├── APPLICATIONS/                 domain use
├── LIBRARY/                      editorial communication
├── EDITORIAL_OPERATING_SYSTEM/   governance and controlled execution
└── docs/                         cross-system reader documentation
```

Supporting architecture, validation, prototype, and historical areas are
documented in the **[full Repository Map](REPOSITORY_MAP.md)**. The
**[Governance Index](GOVERNANCE/README.md)** records the authority order from
Constitution through Governance and Architecture to implementation and derived
artifacts without changing the six-subsystem architecture.

---

## Contributing, Citation, and License

Begin with the **[Contribution Guide](CONTRIBUTING.md)** and the
**[Code of Conduct](CODE_OF_CONDUCT.md)**. Contributions should enter through
the subsystem responsible for the proposed work and preserve its local
evidence, ownership, provenance, and review rules.
Architectural status belongs in **[Architecture](ARCHITECTURE/README.md)**;
normative language work belongs in
**[Orientation Language](ORIENTATION_LANGUAGE/README.md)**.
Release and tag meanings are recorded in **[Release and Version
History](RELEASES.md)**.
Current public-launch execution state is recorded once in
**[Launch Status](LAUNCH_STATUS.md)**.

Software is released under the **[Apache License 2.0](LICENSE)**.
Original NEXAH documentation and repository research material are released
under **[CC BY 4.0](LICENSE-DOCS.md)**. Third-party and source-derived material
retains its stated license and provenance. See the complete
**[Licensing Scope](LICENSES.md)** and **[CITATION.cff](CITATION.cff)**.

---

**Thomas K. R. Hofmann**

NEXAH Orientation Ecosystem · 2026
