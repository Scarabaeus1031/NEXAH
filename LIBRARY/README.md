# NEXAH Library

**A human-readable visual library with a small canonical layer for orientation.**

> **The Library comes first. The Kernel learns from the Library—not the other
> way around.**

The Library is the human interface of NEXAH. The Registry provides stable
identity. The Kernel derives orientation from both.

`LIBRARY/` connects the visual NEXAH Library on Are.na with the research,
implementation, validation, and Orientation Kernel layers in this repository.

The project begins from a simple principle:

> The Library should remain understandable to people without software. The
> software should benefit from the structure without replacing the Library.

The Library is therefore not a database export and not a mirror of Are.na. It
is a curated architecture for stable identity, meaningful relationships, and
future navigation across NEXAH works.

```text
                 NEXAH

          Human Orientation
                  │
        ┌─────────┴─────────┐
        │                   │
     Are.na              GitHub
        │                   │
        └──── Canonical Registry ────┐
                                     │
                              Orientation Kernel
                                     │
                         Reading Paths · Search · Graphs
```

## Why this layer exists

NEXAH currently has three complementary knowledge surfaces:

```text
Are.na Library
→ books, atlases, visual essays, reports, notebooks, and visual sequences

GitHub Repository
→ code, research, validation, architecture, and applications

Orientation Kernel
→ structured representations, Operators, Orientation Reports, and graphs
```

Without a shared Library layer, future integration would risk becoming an
ad-hoc import pipeline based on titles and platform IDs. The Canonical Library
Registry establishes a small, human-reviewable contract before deeper
integration begins.

## Project goal

The long-term goal is a Library that supports both:

- human exploration through entry works, series, maps, and reading paths;
- machine-supported orientation through stable identity, controlled Operators,
  curated relationships, Editions, and provenance.

The Registry is intentionally small. Most knowledge remains inside the Works
themselves rather than being duplicated as metadata.

The intended relationship is:

```text
Human Work
    ↓
Stable NEXAH Identity
    ↓
Curated Classification and Relationships
    ↓
Addressable Edition and Structure
    ↓
Derived Kernel Views
```

Concepts such as Operators form a parallel vocabulary referenced by Works and,
later, selected pages or plates. Complete semantic annotation is not required
before a Work can participate in the Library.

## Four responsibilities

### Are.na — visual publication

Are.na remains authoritative for:

- visual content;
- channel descriptions;
- editorial sequence;
- the human experience of browsing and connecting works.

### Canonical Library Registry — identity and curation

The Registry is authoritative for:

- stable NEXAH IDs;
- Object Family, Type, Form, and Library Function;
- Publication and Edition state;
- controlled Core Operator references;
- curated relationships;
- canonical source resolution.

### GitHub — implementation and evidence

The repository remains authoritative for:

- Kernel and application code;
- technical architecture;
- research records;
- validation and claim boundaries;
- formal specifications.

### Orientation Kernel — derived orientation

The Kernel may read the Registry to produce:

- audience-aware Reading Paths;
- Operator queries across Works;
- relationship graphs;
- simple, explainable recommendations;
- later, provenance-bound retrieval and orientation reports.

Kernel inference is always an overlay. It may propose metadata or Concept
occurrences, but it may not silently overwrite canonical human-reviewed data.

## From Library to Reproducible Explanation

![NEXAH Editorial Explanation Layer — from reviewed knowledge to reproducible explanation](../EDITORIAL_OPERATING_SYSTEM/visuals/architecture/editorial_explanation_layer.png)

The Library provides the human-authored Works and editorial context from which
bounded Concept reviews and Answer Contracts may be developed. The separate
**[Editorial Explanation Layer](../EDITORIAL_OPERATING_SYSTEM/EDITORIAL_EXPLANATION_LAYER_STATUS.md)**
can reproduce an accepted, human-reviewed answer through a read-only Adapter.

```text
Works
→ Living Concept review
→ accepted Editorial Knowledge Contract
→ read-only resolution
→ Reader or Explain response
```

This does not make the Library a Knowledge Graph and does not grant the Adapter
authority to infer new meaning. A contract preserves its question, reviewed
answer, evidence, uncertainty, and boundaries. The audience may change; the
evidence and claim boundary may not.

The audience-specific renditions shown in the visual remain a bounded design
question. They are not part of the current X2 implementation.

## Current status — Living Library, Editorial Writer, and X2 pilot

The current pilot contains:

- **10 registered Works** representing Books, Guides, Atlases, a Research
  Report, and a large Compendium;
- **17 controlled Core Operators** with definitions and source Works;
- **Library Architecture v1.0**;
- a strictly read-only Are.na comparison client;
- a separate, approval-gated Are.na Editorial Writer;
- initial Reading Path, Operator, graph, and recommendation queries;
- six accepted pilot Answer Contracts and a read-only Concept Answer Adapter.

The ten pilot Works are:

1. THE VISITOR’S GUIDE
2. GEOMETRIA NOVA
3. THE OPERATOR’S HANDBOOK
4. THE LANGUAGE BOOK
5. THE LANGUAGE ATLAS
6. FIELD ATLAS I — WATER
7. THE CARTOGRAPHY LABORATORY
8. THE OPERATOR LIBRARY
9. THE ATLAS OF ATLASES
10. LIBRARYBOOK

These records are a work-level pilot, not a claim that the complete Are.na
Library has already been classified.

## Living Library Operations

Phase VII adds small reporting tools for one human editor. They expose structural
failures and editorial warnings without making editorial decisions.

Local-only commands:

```bash
python -m nexah.library health
python -m nexah.library reader-regression
python -m nexah.library series-validate
python -m nexah.library cleanup-status
python -m nexah.library release-check
```

Snapshot-based and public read-only commands:

```bash
python -m nexah.library source-snapshot
python -m nexah.library traversability --all
python -m nexah.library editorial-diff --all
python -m nexah.library editorial-diff NX-000002
python -m nexah.library editorial-diff arena:5404576
```

`source-snapshot` and `traversability` observe public Are.na state. Editorial
Diff compares a verified Source Snapshot with current public observations.
Missing links, unresolved Series, and pending cleanup are warnings; invalid
Registry data, collapsed Proposal isolation, Reader regression changes, or a
write-enabled connector are failures.

All Living Library reporting commands remain read-only. `cleanup-status` cannot
update its queue. The separate Phase IX Writer can execute only accepted Queue
Actions through an explicit Dry Run, matching Plan ID, `--apply`, write token,
and live fingerprint verification. Proposal data remains non-canonical unless a
human editor later approves an explicit Registry change.

## Phase IX Editorial Writer

The Writer is not a synchronizer or importer. It never changes the Registry,
identities, Operators, Proposal state, visibility, ownership, titles, or the
Action Queue. The original `arena.py` connector remains GET-only.

Batch 0 is an isolated API capability test in a private Channel:

```bash
python -m nexah.library editorial-sandbox
python -m nexah.library editorial-sandbox --apply
```

Batch 1 is always planned before it can be applied:

```bash
python -m nexah.library editorial-write --batch BATCH-01
python -m nexah.library editorial-write --batch BATCH-01 \
  --apply --plan-id <approved-plan-id>
```

Only Queue Actions with `review_state: accepted` are eligible. `pending`,
`deferred`, `rejected`, and `completed` Actions are reported as ignored. Batch 1
is restricted to `ACQ-001`, `ACQ-002`, `ACQ-006`, and `ACQ-013`.

The token is read only from the process environment:

```bash
export ARENA_WRITE_TOKEN="..."
```

Never place the token in this repository, YAML, a command argument, or a report.
See [Phase IX Editorial Writer](review/PHASE_IX_EDITORIAL_WRITER.md) for the
complete operational contract.

## What the project does not do

The current Library layer does not:

- synchronize or import content into Are.na;
- autonomously decide or approve Are.na changes;
- rename or delete production Channels;
- import every Are.na block into GitHub;
- treat Are.na IDs as intellectual identity;
- infer scientific validity from publication status;
- treat recommendations as autonomous editorial decisions;
- require page-level semantic annotation;
- replace the visual sequence with a graph.

The canonical Are.na connector contains GET operations only. Phase IX writes are
isolated in `editorial_writer.py` and cannot mutate canonical Library data.

## Architecture

The complete frozen decision record is available in
**[Library Architecture v1.0](architecture/LIBRARY_ARCHITECTURE_V1.md)**.

The primary object model is:

```text
Library Entity
├── Work
│   └── Edition
│       └── Part / Chapter / Page / Plate
├── Environment
├── Navigation
├── Asset
└── Concept
    └── Operator
```

Important distinctions include:

- THE VISITOR’S GUIDE is a Work; it is not the future START navigation object.
- THE OPERATOR LIBRARY is a Reference Guide; it is not the future Operator
  Index.
- THE ATLAS OF ATLASES is a Meta Atlas; it is not the future Atlases Index.
- THE CARTOGRAPHY LABORATORY is currently registered as a published Laboratory
  Report; the ongoing Laboratory Environment will be a separate Entity.

## Repository structure

```text
LIBRARY/
├── README.md
├── architecture/
│   └── LIBRARY_ARCHITECTURE_V1.md
└── registry/
    ├── registry.yaml
    ├── entities/
    │   ├── NX-000001.yaml
    │   └── ...
    └── concepts/
        ├── NX-OP-0001.yaml
        └── ...

nexah/library/
├── arena.py       read-only Are.na client and comparison
├── editorial_writer.py  explicit editorial plans and guarded writes
├── registry.py    YAML loading and validation
├── kernel.py      derived paths, queries, graphs, and recommendations
└── cli.py         command-line interface

tests/library/
└── focused tests for Registry, connector, and queries
```

## Safe data flow

```text
Are.na
  │ read current metadata
  ▼
Read-only comparison
  │ report current or stale
  ▼
Human-reviewed Registry
  │ canonical Kernel input
  ▼
Derived paths, queries, graphs, and suggestions
```

Canonical Registry changes still flow only through human review. The separate
Editorial Writer acts in the other direction only for accepted operational
Queue Actions; it cannot alter Registry or Kernel state.

## Commands

From the repository root:

```bash
python -m nexah.library validate
python -m nexah.library compare --all
python -m nexah.library reading-path --audience newcomer
python -m nexah.library operators --operator NX-OP-0005
python -m nexah.library graph --format mermaid
python -m nexah.library recommend NX-000004 --limit 5
```

An Are.na token is optional for material that is not publicly readable. Keep it
outside the repository:

```bash
export ARENA_TOKEN="..."
```

## Editorial workflow

The conservative workflow is:

1. inspect the Are.na Work;
2. propose or update its Registry record;
3. validate controlled IDs, Operators, and relationships;
4. compare the record with current Are.na metadata;
5. review differences manually;
6. use the confirmed Registry as Kernel input.

The Registry never derives identity from a mutable title, slug, or platform ID.

## Next steps

The next work should remain focused on the ten-work pilot:

1. editorially confirm each Pilot Card and current Edition;
2. review the definitions and source Works of the 17 Core Operators;
3. curate the first official `Begin Here` Reading Path;
4. register the future START, Operator Index, and Atlases Index as separate
   Navigation Entities;
5. register the Cartography Laboratory as an Environment separate from its
   published Report;
6. add explicit mappings from selected Works to relevant repository modules;
7. evaluate the usefulness of the Kernel queries with real reader questions;
8. introduce page-level structure only for selected core or large Works after
   the work-level model is stable.

Any Are.na write remains a separately approved, plan-bound operation through
the guarded Editorial Writer. Automated reorganization remains outside the
Library architecture.

## Project success criterion

The project succeeds when a person can understand and navigate the Library
without the Kernel, while the Kernel can explain every recommendation, path, or
relationship through stable identities, curated metadata, and explicit
provenance.
