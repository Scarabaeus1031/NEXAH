# NEXAH Editorial Explanation Layer — Plateau X2 Status

**Status date:** 2026-07-16  
**Technical state:** implemented and repository-validated pilot  
**Editorial state:** ready for human review  
**General Kernel integration:** deferred  
**Canonical Concept Graph:** not implemented

![NEXAH Editorial Explanation Layer — from reviewed knowledge to reproducible explanation](visuals/architecture/editorial_explanation_layer.png)

> **CURRENT ARCHITECTURE · X2 PILOT.** The visual documents the implemented
> relationship between Works, Living Concepts, accepted Answer Contracts, and
> the read-only Adapter. The three audience renditions are the next bounded
> design question; they are not implemented in X2.

## Plateau statement

X2 establishes a new repository plateau:

> **NEXAH can preserve a human-reviewed explanation as a machine-readable
> contract and reproduce it in Reader and Explain modes without inferring new
> meaning.**

The achievement is deliberately narrower than a Knowledge Graph or general
reasoning engine. It proves controlled explanation, not autonomous
understanding.

## Development path

```text
Books
    ↓
Living Library
    ↓
Editorial Structure
    ↓
Governance
    ↓
Reader Orientation
    ↓
Living Concepts
    ↓
Accepted Editorial Knowledge Contracts
    ↓
Read-only Concept Answer Adapter
```

The ordering matters. Identity, provenance, human review, and claim boundaries
were established before runtime access was introduced.

## Architecture reached

```text
Works and Research
        ↓ document
Living Concept reviews
        ↓ preserve as
Accepted Concept Overlay v0.1
        ↓ contains
Six Editorial Knowledge Contracts
        ↓ resolved by
Read-only Concept Answer Adapter
        ↓ returns
Reader response or Explain response
```

This creates three distinct knowledge levels:

| Level | Governing question | Current implementation |
|---|---|---|
| Canonical Registry | What exists stably? | 10 Work identities and 17 controlled Operators |
| Living Concepts | How does an idea develop through sources? | Non-canonical dossiers, occurrences, family reviews, and Concept paths |
| Editorial Knowledge Contracts | How is the reviewed idea explained reproducibly? | Six accepted pilot contracts and a read-only resolver |

These levels do not inherit authority automatically. A reviewed Concept handle
does not become a canonical identity, and an accepted answer does not become a
universal scientific claim.

## What X2 implemented

### Accepted Overlay baseline

- seven reviewed local Concept handles;
- 13 documentary Occurrences;
- two `review_only` Concept relation proposals;
- three human-curated Concept paths;
- six Reader/Explain answer contracts;
- explicit non-canonical and no-mutation authority blocks.

The acceptance commit is independently identifiable:

```text
db0841e0  Accept Living Concepts overlay v0.1 editorial baseline
```

### Read-only Adapter

The explicit module:

```bash
python -m nexah.living_concepts answer CFQ-01 --mode reader
python -m nexah.living_concepts answer CFQ-01 --mode explain
```

performs only:

```text
exact pilot question key
        ↓
accepted Overlay binding
        ↓
Reader contract or Explain contract
        ↓
structured response
```

It does not perform fuzzy matching, arbitrary language interpretation,
embeddings, semantic search, inferred graph traversal, autonomous synthesis,
or writing.

The implementation commit is independently identifiable:

```text
0c031fc9  Add read-only Living Concepts answer adapter
```

## Six verified pilot questions

| Key | Question | Authority boundary |
|---|---|---|
| CFQ-01 | What is Transition Geometry? | reviewed editorial synthesis; no universal space |
| CFQ-02 | How is JANUS related to Transition Geometry? | reviewed relation; JANUS identities remain separate |
| CFQ-03 | Where is the Inbetween developed? | curated documentary path; no canonical Inbetween identity |
| CFQ-04 | Show me the path from Boundary to Transition. | curated path; not a deterministic state machine |
| CFQ-05 | Which Works explain Aperture Geometry? | controlled Operator authority plus Work and Research evidence |
| CFQ-06 | What does Balance mean in NEXAH? | `multiple_related_models`; intentionally not unified |

Unknown question keys remain unsupported. The Adapter does not improvise an
answer.

## Evidence and validation

The X2 checkpoint passed:

- YAML validation;
- accepted-answer baseline regression;
- Reader contract tests;
- Explain provenance and uncertainty tests;
- negative authority and mutation tests;
- Living Concepts tests;
- Library tests;
- the complete repository suite.

Dated verification result:

```text
288 tests passed
Canonical Entities:             10
Controlled Operators:           17
New NX-C identities:             0
Canonical Concept edges:         0
Kernel default runtime changes:  0
Are.na writes:                    0
Editorial Writer changes:        0
```

The test count is a dated repository result, not a permanent architecture
constant.

## What the milestone means

The central unit is no longer only a document, Concept node, or relation. X2
introduces a governed explanatory unit:

```text
Question
    ↓
Reviewed answer
    ↓
Evidence and provenance
    ↓
Uncertainty and exclusions
    ↓
Reader or Explain rendition
```

This is an **Editorial Knowledge Contract**. The broader system capability
that stores and presents such contracts is the **Editorial Explanation
Layer**.

Therefore:

```text
Editorial Explanation Layer = system capability
Editorial Knowledge Contract = reviewed explanatory unit
```

## Current boundaries

The following distinctions remain mandatory:

```text
Concept Overlay              ≠ Concept Graph
Concept Answer Adapter       ≠ General Reasoning Engine
Accepted Editorial Baseline  ≠ Canonical Knowledge
Audience rendition           ≠ New truth
```

X2 does not approve:

- permanent Concept identities;
- canonical Concept definitions or graph edges;
- automatic extraction or semantic inference;
- new Operator assignments;
- Registry growth;
- default Kernel loading;
- unrestricted questions;
- Are.na mutation;
- audience-specific renditions.

## Risks at this plateau

1. **Contract inflation** — every question becomes a separately maintained
   answer instead of reusing a stable knowledge core.
2. **Meaning drift** — different renditions slowly change evidence or claim
   boundaries.
3. **Graph laundering** — curated paths are presented as discovered laws.
4. **Authority collapse** — Work statements, Research findings, Operator
   definitions, and editorial synthesis are treated as equivalent.
5. **Runtime expansion** — the six-question Adapter silently becomes a general
   query interface.
6. **False intelligence claim** — contract resolution is described as
   autonomous understanding.

The current validation boundary directly guards against these risks.

## Proposed next bounded phase

The next phase should not add more Concepts or general Kernel behavior. A
conservative X3 pilot should test whether the same accepted contract can have
three consistent editorial renditions:

```text
one accepted knowledge contract
        ├── Curious Beginner
        ├── Advanced Reader
        └── Researcher
```

The audience may change vocabulary, depth, examples, visible technical detail,
and next-step guidance. It may not change identity, evidence, provenance,
claim support, uncertainty, or exclusions.

Suggested phase name:

> **Phase X3 — Editorial Explanation Layer: Audience-Aware Knowledge
> Contracts**

This remains a proposal. X3 begins only after explicit human acceptance of the
X2 Adapter decisions.

## Human checkpoint

The current decision package remains:

- X2-ADP-01 through X2-ADP-07 — recommended `accept`;
- X2-ADP-08, general Kernel integration — recommended `defer`.

**Current conclusion:** READY FOR HUMAN REVIEW OF READ-ONLY CONCEPT ADAPTER.

