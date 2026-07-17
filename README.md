# NEXAH — The Orientation Ecosystem

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
| Understand the idea and principles | **[NEXAH Manifesto](MANIFESTO.md)** |
| Read the published specification | **[Orientation Language](ORIENTATION_LANGUAGE/README.md)** |
| Use or develop the software | **[Orientation Kernel](nexah/README.md)** |
| Inspect research and evidence | **[Research Portal](RESEARCH/README.md)** |
| Explore Works, journeys, or editorial practice | **[Living Library](LIBRARY/README.md)** · **[Editorial Operating System](EDITORIAL_OPERATING_SYSTEM/README.md)** |
| Evaluate a domain application | **[Applications](APPLICATIONS/README.md)** |

For the complete directory-level view, use the
**[Repository Map](REPOSITORY_MAP.md)**.

---

## Repository Organization

The six subsystems coordinate without sharing one authority:

| Subsystem | Responsibility | Authority boundary |
|---|---|---|
| **[Research](RESEARCH/README.md)** | Produces hypotheses, models, experiments, and evidence | Does not define released semantics or establish universality |
| **[Orientation Language](ORIENTATION_LANGUAGE/README.md)** | Defines published semantics and conformance rules | Does not execute implementations or establish domain validity |
| **[Implementations](nexah/README.md)** | Execute declared structures and produce inspectable behavior | Do not redefine semantics; conformance is explicit, never assumed |
| **[Applications](APPLICATIONS/README.md)** | Apply methods within declared domains and use cases | Do not generalize beyond admitted evidence or redefine the language |
| **[Living Library](LIBRARY/README.md)** | Communicates curated knowledge through Works and reader journeys | Its Registry governs editorial identity, not OLS semantics |
| **[Editorial Operating System](EDITORIAL_OPERATING_SYSTEM/README.md)** | Preserves human review, explanation, approval, and controlled execution | Editorial Governance does not replace Specification Governance |

The central distinction is simple: **the Orientation Language defines
semantics; implementations execute behavior; conformance must be demonstrated.**

The detailed responsibility and relationship map lives in
**[Architecture](ARCHITECTURE/README.md)**.

---

## Current State

- **Orientation Language 1.0** is published as the canonical semantic authority.
- **Orientation Kernel v0.7** is maintained as the current implementation track.
- **Research** remains active, scoped, and evidence-bound.
- **Reference applications** for Network Orientation and IEEE Geometry are maintained.
- **Library and Editorial infrastructure** operate within documented human-governance boundaries.

These are different maturity statements, not one repository-wide certification.

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
**[Applications](APPLICATIONS/README.md)**, or run the executable
**[Demonstrator Path](START_HERE.md)**.

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
└── EDITORIAL_OPERATING_SYSTEM/   governance and controlled execution
```

Supporting architecture, validation, prototype, and historical areas are
documented in the **[full Repository Map](REPOSITORY_MAP.md)**.

---

## Contributing, Citation, and License

Contributions should begin in the subsystem responsible for the proposed work
and preserve its local evidence, ownership, provenance, and review rules.
Architectural status belongs in **[Architecture](ARCHITECTURE/README.md)**;
normative language work belongs in
**[Orientation Language](ORIENTATION_LANGUAGE/README.md)**.

NEXAH is released under the **Apache License 2.0**. Canonical releases,
validation artifacts, research records, and Library Works may provide more
specific citation or provenance information in their responsible subsystem.

---

**Thomas K. R. Hofmann**

NEXAH Orientation Ecosystem · 2026
