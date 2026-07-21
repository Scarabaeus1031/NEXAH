# NEXAH Catalog Architecture

Status: architecture baseline for a non-canonical descriptive layer  
Version: 0.1  
Scope: six catalog domains and the bounded visual research pass

## Purpose

A NEXAH catalog describes what can be found, where it came from, how it was
reviewed, and how a reader may reach it. Catalog inclusion does not establish
truth, scientific validity, canonical identity, or an accepted definition.

```text
Source publication
        ↓
Descriptive catalog
        ↓
Human review
        ↓
Canonical Registry or accepted knowledge contract
        ↓
Derived Kernel, Reader, and Laboratory views
```

The current Website Catalog is the first implementation of the **Publication
Catalog**. Its existing path and filenames remain unchanged in this sprint: the
architectural name is more durable, while an immediate rename would add risk
without improving the boundary.

## Domain map

| Domain | Central question | Current authority | Canonical authority |
|---|---|---|---|
| Publication | Which published Works exist and what source-supported structure do they have? | Source-keyed catalog records | Human-approved Library Registry, when allocated |
| Concept | Which mentioned, observed, proposed, reviewed, or accepted concepts occur? | Concept overlay and reviewed evidence | Accepted Living Concept/knowledge contract or future explicit authority |
| Operator | Which explicit actions and transformations exist? | Occurrence and candidate descriptions | Existing controlled `NX-OP-*` Registry |
| Laboratory | Which research activities, questions, methods, evidence, and validation records exist? | Research records and bounded studies | The owning research/validation process, never publication status alone |
| Atlas | Which maps, plates, diagrams, and representational systems exist? | Source-keyed representational descriptions | Human-reviewed atlas decision, if one is later defined |
| Navigation | Which curated paths help a person move through NEXAH? | Editorial policies, paths, shelves, and sequences | Human editorial authority |

## Object boundaries

### Publication Catalog

Includes Works, editions, parts, chapters, pages, and source-supported
publication structure. A published Laboratory report is a Publication. The
ongoing Laboratory environment that produced it is not. An atlas may be a
Publication, but individual maps or plates inside it are Atlas objects.

### Concept Catalog

Includes explicit concepts and concept evidence with the states `mentioned`,
`observed`, `proposed`, `reviewed`, `accepted`, and `deprecated`. A repeated
word is not a definition. Titles alone may locate a mention but may not supply
meaning. Existing Living Concepts and accepted Editorial Knowledge Contracts
must be reused rather than duplicated.

### Operator Catalog

Includes controlled Core Operators, proposed operators, occurrences, families,
sequences, and transformation rules. An Operator is an action, not a subject:
Perspective is a Concept; Change Perspective is an Operator candidate. Only
the existing controlled Operator Registry is canonical. Work-level Moves and
visual metaphors remain evidence, not Registry additions.

### Laboratory Catalog

Includes research programs, projects, experiments, hypotheses, methods,
instruments, datasets, cases, observations, open questions, and validation
records. It links activities to publications but does not confuse publication
with validation. Visual recurrence never establishes causation.

### Atlas Catalog

Includes maps, diagrams, plates, coordinate systems, visual models, relational
maps, map families, and representational systems. The title “Atlas” is neither
necessary nor sufficient. A map may visualize a publication statement, but the
Catalog must not convert that statement into a scientific finding.

### Navigation Catalog

Includes entry points, audience paths, thematic paths, shelves, trails,
collections, series navigation, and next-step recommendations. These are
editorial and audience-dependent. Recommendation does not imply conceptual or
scientific dependency.

## Authority boundaries

Each record carries four distinct authorities:

1. `source_authority`: who published or recorded the source;
2. `catalog_authority`: who describes the source in the catalog;
3. `canonical_authority`: who may accept identity or semantics;
4. `review_authority`: who reviewed the extraction or relationship.

Catalog code may propose. It must never allocate `NX-*` or `NX-OP-*` IDs,
promote Proposals, accept Concepts, change Operators, mutate Are.na, or alter
human-reviewed Registry metadata.

## Identity rules

- Publications remain `arena:<channel-id>` until a canonical Library identity
  already exists or is separately approved.
- Pages use `arena-block:<block-id>`. Titles, slugs, and sequence positions are
  mutable attributes, not identity.
- Concepts use local handles until accepted; no `NX-C-*` allocation occurs in
  catalog review.
- Operators use canonical `NX-OP-*` only when resolving an existing controlled
  record. Candidates remain local and explicitly non-canonical.
- Laboratory objects may use stable, repository-owned `lab:<namespace>:<id>`
  identifiers.
- Atlas objects initially remain source-keyed by their source Block.
- Navigation objects use editor-assigned local IDs such as `nav:<path-name>`.

## Shared evidence model

Allowed evidence levels are:

- `source_metadata`
- `block_title`
- `visible_page_text`
- `visible_diagram`
- `publication_description`
- `repository_document`
- `accepted_contract`
- `human_editorial_decision`

Extraction status is independent: `not_reviewed`, `machine_observed`,
`visually_reviewed`, `human_confirmed`, `accepted`, or `rejected`. Confidence
may be low, medium, or high, but never substitutes for evidence.

Every assertion preserves the publication key, Are.na Block ID, Block URL,
image URL, review method, reviewer, date, confidence, and notes. A source
fingerprint detects changed or missing pages. Explicit `null`, empty lists, and
`unknown` are preferred to invented values.

## Relationship model

There is no default `related_to` edge. Relationship types are directional and
domain-constrained.

| Type | Direction / inverse | Domains | Evidence | Authority and review |
|---|---|---|---|---|
| `source_contains` | source → publication / `contained_by_source` | source → publication | source metadata | descriptive; review on conflict |
| `publication_contains` | publication → page / `contained_by_publication` | publication → publication-part/page | source order | descriptive; stale check required |
| `publication_mentions` | publication/page → concept / `mentioned_in` | publication → concept | visible text | descriptive; human review for concept status |
| `publication_defines` | publication/page → concept / `defined_in` | publication → concept | explicit visible definition | proposed until human accepted |
| `publication_documents` | publication → laboratory object / `documented_by` | publication → laboratory | source text or repository document | descriptive; does not validate |
| `publication_visualizes` | publication/page → atlas object / `visualized_in` | publication → atlas | visible diagram/map | descriptive; reviewed |
| `concept_related_to` | concept ↔ concept | concept → concept | explicit source or accepted contract | no generic fallback; relation label required |
| `operator_applied_to` | operator → target / `uses_operator` | operator → concept/publication/atlas/lab | explicit action evidence | candidate review unless canonical operator resolved |
| `experiment_tests` | experiment → hypothesis / `tested_by` | laboratory → laboratory | protocol or validation record | research authority review required |
| `observation_supports` | observation → assertion / `supported_by` | laboratory → lab/concept | evidence record | never inferred from publication status |
| `observation_challenges` | observation → assertion / `challenged_by` | laboratory → lab/concept | evidence record | research authority review required |
| `atlas_represents` | atlas object → target / `represented_by` | atlas → concept/lab/publication | labels and source context | descriptive; no causal implication |
| `navigation_recommends` | navigation → publication / `recommended_by` | navigation → publication | human editorial decision | editorial, audience-specific |

## Visual review architecture

The review has two passes:

1. **Triage** reviews every page in a selected Work using a contact sheet or
   thumbnail and assigns a visual role. No semantic extraction is required.
2. **Deep extraction** opens full-resolution source images only for pages with
   explicit definitions, questions, methods, models, diagrams, maps, tables,
   hypotheses, observations, evidence statements, limitations, open questions,
   implementation descriptions, Concepts, or Operators.

The source image remains authoritative. Temporary caches may be used outside
the repository. Thumbnails are sufficient for triage; full resolution is used
only for eligible pages. The repository stores source URLs and deterministic
metadata fingerprints, not a mirror of the image corpus. Derived
transcriptions may be committed when bounded by exact source references and a
review state. Screenshots are retained only when necessary to document a
review discrepancy and subject to publication integrity and copyright review.

## Human review gates

Review states are `extracted`, `queued`, `reviewed`, `accepted`, `revised`, and
`rejected`. Human review is mandatory before accepting a Concept definition,
adding an Operator, saying an experiment supports a claim, defining a series,
establishing dependency between Works, classifying a page as research evidence,
or promoting a relationship to canonical status.

## Prototype placement

Batch A is stored under
`LIBRARY/catalog/review/orientation_foundations/`. This is a review overlay on
four Publications, so it belongs beside the Publication Catalog. It is not an
ongoing Laboratory environment, an Orientation Translation study, a Registry
extension, or a Living Concept overlay.

## Migration considerations

- Keep `LIBRARY/catalog/` paths stable while consumers adopt the architectural
  term Publication Catalog.
- Reuse existing Registry, Living Concept, contract, research, and Reader
  models by reference.
- Promote no Batch A object automatically.
- If the review model stabilizes, separate generation code from reviewed data
  without changing source keys.

## Open decisions

- Whether an accepted Concept Catalog receives its own canonical identity
  namespace.
- Which research authority may accept Laboratory evidence across domains.
- Whether Atlas objects require local IDs beyond their source Block identity.
- How independent human review and transcription correction are recorded.
- Whether the four foundation Works should become a named series; Batch A may
  report only `explicit`, `strongly_implied`, or `editorial_proposal`.

