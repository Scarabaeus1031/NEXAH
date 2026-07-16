# Minimal Concept Overlay v0.1 — Evaluation

**Phase:** X1 · machine-readable pilot  
**Status:** editorial baseline accepted · non-canonical
**Baseline:** Transition Geometry Concept-Family Test  
**Runtime:** not integrated

## Outcome

The Minimal Concept Overlay v0.1 reproduces the structure required by all six
accepted Reader/Explain answers without adding a permanent Concept identity,
canonical graph edge, Registry mutation, Operator mutation, Kernel behavior,
or Are.na write.

The editorial decisions `X1-OVL-01` through `X1-OVL-07` were accepted on
2026-07-16. `X1-OVL-08`, general Kernel integration, remains deferred. This
status transition changes no definition, occurrence, relation, path, or answer
contract.

The overlay contains:

- 7 reviewed handles;
- 13 documentary occurrences;
- 2 typed review-only relations;
- 3 human-curated paths;
- 6 Reader/Explain answer contracts.

## Baseline comparison

| Question | Human baseline | Overlay result | Evidence bundle | Boundary preserved |
|---|---|---|---|---|
| CFQ-01 · Transition Geometry | `pass` | `pass` | definition + Work + Architecture | no universal space |
| CFQ-02 · JANUS relation | `pass` | `pass` | two profiles + review relation | JANUS identities remain separate |
| CFQ-03 · Inbetween | `pass_with_editorial_synthesis` | `pass_with_editorial_synthesis` | occurrences + curated path | path is not a graph edge |
| CFQ-04 · Boundary to Transition | `pass_with_editorial_synthesis` | `pass_with_editorial_synthesis` | Operator profiles + curated path | not a deterministic state machine |
| CFQ-05 · Aperture Geometry | `pass` | `pass` | Operator + Works + Research + path | access is not activation |
| CFQ-06 · Balance | `pass_with_concept_boundary` | `pass_with_concept_boundary` | reviewed models + occurrences | no unified Balance Concept |

## What “reproduces” means here

Version 0.1 does not generate prose through inference. It demonstrates that a
small explicit data contract can resolve every answer into:

```text
focus handle
    + reviewed definition or authority reference
    + documentary occurrences
    + optional review-only relation
    + optional curated path
    + required Explain disclosures
```

The structural test verifies that all references resolve, all six result
states match the human baseline, every answer has Reader and Explain content,
and no forbidden authority is claimed.

This is the correct test before runtime integration: first prove that the
editorial distinctions survive representation; only later test a read-only
adapter.

## Important findings

### 1. Concepts and Operators can coexist without identity collapse

Aperture, Boundary, and Transition are represented as profiles bound to
existing controlled Operator records. No second identity is allocated. JANUS
can reference its existing controlled expression while preserving the broader
principle, planned Bridge, and experimental method as distinct layers.

### 2. Paths need a different status from relations

The Inbetween and Boundary-to-Transition answers depend on useful sequences,
but these sequences are human-curated documentary routes. Modeling them as
`path` with `status: curated` avoids laundering editorial order into graph
truth.

### 3. A negative identity decision remains navigable knowledge

Balance demonstrates that the overlay can answer a question by preserving
heterogeneity. `multiple_related_models` is not a failure state; it is the
evidence-backed result.

### 4. Most knowledge remains in sources

The overlay stores concise Reader summaries, authority references, and claim
boundaries. It does not copy whole Work descriptions or Research arguments.
This preserves the principle that the Library and Research remain the
knowledge-bearing sources.

## Validation gates

| Gate | Result |
|---|---|
| Seven unique pilot handles | pass |
| Existing Operator bindings resolve | pass |
| Occurrence references resolve inside overlay | pass |
| Relation endpoints and evidence resolve | pass |
| Curated path references resolve | pass |
| Six baseline question IDs and result states match | pass |
| Reader answers and Explain disclosures present | pass |
| No `NX-C-...` identity allocated | pass |
| No canonical relation or path declared | pass |
| Registry remains 10 Entities / 17 Operators | pass |
| Kernel and Are.na writer untouched | pass |

## Human decisions required

| Decision | Recommendation | Effect |
|---|---|---|
| X1-OVL-01 · Minimal model | accept | establishes the review-only overlay contract |
| X1-OVL-02 · Seven pilot handles | accept | limits the pilot to reviewed material |
| X1-OVL-03 · Operator profile binding | accept | prevents duplicate Aperture, Boundary, Transition identities |
| X1-OVL-04 · Review-only relations | accept | permits explanation without canonical edges |
| X1-OVL-05 · Curated path object | accept | preserves human sequence as editorial guidance |
| X1-OVL-06 · Balance non-unification | accept | retains `multiple_related_models` |
| X1-OVL-07 · Baseline reproduction | accept | permits design of a read-only adapter |
| X1-OVL-08 · Kernel integration | defer | requires a separate architecture and safety review |

## Recommendation

**Accept Minimal Concept Overlay v0.1 as a review-only machine-readable
contract.** It preserves the human baseline and demonstrates that the Living
Concept layer can be represented without becoming a premature ontology.

If accepted, the next bounded phase is not graph expansion. It is a design
review for a **read-only Concept Overlay adapter** that can answer only the six
pilot questions, always return provenance, and fail closed on unknown or
unreviewed questions.
