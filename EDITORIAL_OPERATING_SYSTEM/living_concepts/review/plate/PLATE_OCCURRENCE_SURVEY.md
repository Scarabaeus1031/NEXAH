# Plate — Occurrence Survey

**Phase:** X3 · foundational concept review  
**Status:** observational · non-canonical  
**Review date:** 2026-07-16

## Purpose

This survey asks whether `Plate` is already doing recognizable work across
NEXAH. It does not search for a synonym list and does not treat every image,
page, map, projection, layer, or physical plate as equivalent.

Evidence is separated into four classes:

| Class | Meaning |
|---|---|
| A | `Plate` is named and given an editorial or representational role. |
| B | A Plate-like function is described without using the word. |
| C | A technical structure is analogous but retains its own exact meaning. |
| D | Historical usage shows lineage but has no present canonical authority. |

## A — Direct named occurrences

### Library Architecture

The frozen Library Architecture places `Plate` directly in the documentary
structure of a Work:

```text
Work
└── Edition
    └── Part / Chapter / Page / Plate
```

The Library README repeats this model and states that Concepts may later cite
selected pages or plates. This is the strongest evidence that Plate is not a
newly invented word. Its established role, however, is modest: a documentary
or editorial unit inside a Work. The Architecture does not define Plate as a
Concept, Operator, orientation primitive, or universal representational form.

### Public Library descriptions

The current full public discovery contains eight distinct Work or environment
descriptions that use `plate` or `plates`.

| Source | Arena ID | Observed role | Evidence strength |
|---|---:|---|---|
| **NEXAH ARENA °° The Relational Field** | `5221525` | “visual atlas plates” alongside diagrams and simulations | weak-to-moderate; named medium |
| **NEXAH XV ATLAS — Two Sides of One Medal** | `5218362` | visual plates combine perspectives and transition geometries | moderate; shared visual language |
| **NEXAH XV ATLAS Relational Cartography of Human Reality** | `5246392` | fifteen interconnected plates investigate different relational themes | strong; bounded units in an ordered whole |
| **The Architecture of Becoming** | `5293283` | each plate represents a layer in a transformation | strong; representation, layer, and sequence are explicit |
| **THE OPERATOR MAP** | `5393574` | each plate compresses a chapter into a navigable image and is an alternative projection of the same landscape | very strong; bounded, navigable, projective representation |
| **Λ LIBRARYBOOK** | `5413103` | “white plates” occur among maps, notebooks, and field guides | weak; collection form only |
| **ODYSSEE 2040 — THE RETURN ATLAS** | `5224059` | symbolic plates are part of a visual world | weak; visual medium only |
| **NEXAH LANDSCAPES** | `5345722` | each plate gives a different perspective on one question; maps support understanding and navigation | very strong; perspective, common field, and orientation function |

These descriptions do not all mean the same thing. Their common minimum is a
bounded visual-editorial presentation. Four of them additionally support
projection, perspective, layering, compression, sequence, or navigation.

## B — Plate-like structures without the name

| Source family | Existing formulation | Plate-like aspect | Boundary |
|---|---|---|---|
| Transition Geometry review | geometry is a declared relational space and a map of a situation, not the situation itself | bounded representation rather than reality | describes a geometry family, not an editorial unit |
| Observer Geometry | projection, slice, scale, reference, and blind spot determine what becomes visible | situated selection of a larger field | these terms must not be collapsed into Plate |
| Orientation Layer | states and maps are representation-, reference-frame-, context-, and evidence-dependent | a view is local and declared | typed primitives already have exact software meanings |
| IEEE Geometry Testkit | a cross-section is a declared view or projection with variables, units, scope, and information loss | precise example of a bounded slice | a cross-section remains a mathematical/technical object, not a Plate |
| Living Concepts | occurrences, evidence, paths, and boundaries support a reviewed explanation | selected evidence is assembled for understanding | a Concept and its evidence are not Plates |
| Answer Contracts | a reviewed question resolves to reader/explain answers, evidence, and limits | bounded explanatory presentation | a contract governs an answer; it is not the presentation itself |
| Whiteboard practice | one board commonly isolates one relation, transition, geometry, or question within a larger sequence | visual comparison and staged reflection | without titles/descriptions or human review, visual similarity alone is insufficient evidence |

This class supports a recurring representational pattern. It does not prove
that all these structures instantiate one entity.

## C — Technical analogues

Several technical structures resemble the working hypothesis while retaining
their own semantics:

- `RepresentationRef` identifies a declared representation;
- `ReferenceFrame`, `Observer`, and `Context` situate an observation;
- `MapRef` points to a local or persistent map;
- a projection maps between frames or representations with preservation and
  loss;
- a cross-section selects declared variables from a parameterized state
  family;
- a graph, trajectory family, state frame, report, and visual atlas each
  organize evidence differently.

Calling all of these Plates would erase distinctions that the current
Architecture deliberately preserves.

## D — Historical lineage

The historical `NEXAH-CODEX` repository uses Plate in an editorial and visual
production sense:

- **GEOMETRIA NOVA Media Gallery** groups “Scientific Plates” and describes a
  “reference plate for cathedral orientation”;
- the press factsheet names “Scientific Plates & Hero Visuals”;
- a visual gallery describes a layered “prime resonance plate”;
- visual manifests use “didactic plate” and “mathematical plate.”

This lineage supports Plate as a deliberate visual-documentary form. It does
not supply a stable conceptual definition. No direct supporting occurrence
was found in the reviewed `Scarabaeus1033-System-v1.0` text corpus.

## Excluded collisions

The survey excludes uses whose established domain meaning is unrelated to the
editorial hypothesis:

- Casimir plates and plate separation;
- tectonic plates;
- solar or mechanical base plates;
- generic filenames or layout panels with no explanatory role.

These are homonyms, not Concept evidence.

## Coverage boundary

The survey inspected repository text, reviewed Are.na channel metadata,
Architecture, Research, Living Concepts, and historical textual manifests.
It did not infer meaning from untranscribed pixels across every book or
Whiteboard. A visual occurrence counts only when its title, description,
existing review, or explicit human context identifies its function.

## Survey result

`Plate` already exists as an editorial term and repeatedly carries a stronger
representational function. The direct evidence supports:

```text
bounded visual/editorial unit
    + situated perspective or projection in several Works
    + placement within a larger sequence or landscape
    + support for comparison, reflection, or navigation
```

It does not yet support:

```text
universal form of every representation
smallest stable unit of all orientation
new Operator
new software primitive
canonical Concept identity
```
