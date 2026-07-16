# Read-Only Concept Answer Adapter v0.1 — Evaluation

**Phase:** X2 · accepted-contract resolution
**Status:** human review required
**Overlay:** editorial baseline accepted · non-canonical
**General Kernel integration:** deferred

## Result

The read-only Concept Answer Adapter reproduces all six accepted Transition
Geometry pilot contracts because those answers were editorially reviewed and
encoded in the accepted Overlay—not because software inferred new meaning.

```text
Exact CFQ key
    ↓
Accepted Overlay question binding
    ↓
Reader contract or Explain contract
    ↓
Structured response
```

There is no arbitrary natural-language interpretation, fuzzy matching,
semantic search, embedding, graph traversal, autonomous synthesis, or write
operation.

## Evaluation questions

### Did all six questions reproduce the accepted baseline?

**Yes.** Meaning-bearing Reader and Explain fields match
`concept_overlay_v0_1_expected_answers.yaml` for CFQ-01 through CFQ-06.
Ordering is stable.

### Did Reader Mode remain human-readable?

**Yes.** Reader responses expose the accepted short answer, authority class,
visible non-canonical status, and—where applicable—a human-readable curated
path. They omit source paths, Operator IDs, relation internals, claim-support
records, confidence scores, and implementation details.

### Did Explain Mode preserve provenance and uncertainty?

**Yes.** Explain responses include:

- referenced Concept handles and identity states;
- existing controlled Operator bindings;
- reviewed Occurrences with source, locator, assertion origin, and scoped
  claim support;
- review-only relations;
- curated paths and their non-canonical status;
- the accepted uncertainty disclosures;
- an explicit `non_canonical: true` label.

### Were curated paths kept distinct from graph relations?

**Yes.** Paths remain `status: curated` with `canonical_relation: false`.
Relations remain `status: review_only`. The adapter does not convert either
into graph truth.

### Were Operator authority and broader Concept proposals kept separate?

**Yes.** Aperture, Boundary, Transition, and JANUS expose their existing
Operator bindings without allocating new identities. The broader review
handles retain their original identity states.

### Did Balance remain `multiple_related_models`?

**Yes.** CFQ-06 uses the controlled authority class
`multiple_related_models`, preserves the three model occurrences and their
claim-support boundaries, and states that the models remain intentionally
uncollapsed.

### Did any answer require hidden inference?

**No.** Each response is assembled only from the selected accepted binding and
the records explicitly referenced by its `basis`. Unknown keys return
`state: unsupported`.

### Did the adapter mutate or extend the Overlay?

**No.** A byte-for-byte regression test confirms that loading leaves the
Overlay file unchanged. The adapter has no write method or write CLI option.

### Is the adapter useful without general Kernel integration?

**Yes.** It provides a narrow, inspectable proof that accepted editorial
Concept knowledge can serve human Reader and Explain responses while remaining
separate from the Library Registry and Orientation Kernel runtime.

## Response authority vocabulary

| Authority class | Pilot use |
|---|---|
| `reviewed_editorial_synthesis` | Transition Geometry definition and JANUS relation |
| `curated_path` | Inbetween and Boundary-to-Transition routes |
| `operator_authority` | Aperture route with authoritative Operator binding |
| `multiple_related_models` | Balance non-unification |
| `unsupported` | Any unknown question key or mode |

No confidence score is produced.

## Validation summary

| Gate | Result |
|---|---|
| Six Reader contracts | pass |
| Six Explain contracts | pass |
| Stable accepted-answer ordering | pass |
| Curated paths remain curated | pass |
| Review-only relations remain review-only | pass |
| Required provenance and uncertainty | pass |
| Unsupported question behavior | pass |
| Canonical Overlay rejected | pass |
| Permanent `NX-C-...` identity rejected | pass |
| Unaccepted Overlay rejected | pass |
| Duplicate handles and bindings rejected | pass |
| Unknown Operator rejected | pass |
| Canonical relation rejected | pass |
| Non-curated path rejected | pass |
| Missing disclosures or provenance rejected | pass |
| Mutation permission rejected | pass |
| Claim-support escalation rejected | pass |
| Balance unification rejected | pass |
| Overlay unchanged after load | pass |

## Architecture boundary verification

```text
Canonical Entities              10 · unchanged
Controlled Operators            17 · unchanged
New NX-C identities              0
Canonical Concept edges          0
Kernel default runtime changes   0
Are.na writes                    0
Editorial Writer changes         0
```

The Adapter is available only through explicit use:

```bash
python -m nexah.living_concepts answer CFQ-01 --mode reader
python -m nexah.living_concepts answer CFQ-01 --mode explain
```

It is not registered with the default Library Reader CLI or Kernel loader.

## Smallest justified next step

The smallest next step is **human review of the read-only Adapter**. General
Kernel integration, additional questions, new Concepts, aliases, search, and
graph behavior remain out of scope.

Only after explicit acceptance should a later phase decide whether an equally
strict interface contract between the Adapter and another presentation layer
is justified. No automatic expansion should follow from X2.

## Human decision package

| Decision | Recommendation | Effect |
|---|---|---|
| X2-ADP-01 · Overlay loader | accept | permits explicit loading of the exact accepted pilot or supplied accepted path |
| X2-ADP-02 · Validation boundary | accept | preserves fail-closed authority and provenance checks |
| X2-ADP-03 · Reader reproduction | accept | confirms short human-readable accepted answers |
| X2-ADP-04 · Explain reproduction | accept | confirms provenance, identity, and uncertainty disclosure |
| X2-ADP-05 · Unsupported behavior | accept | prevents arbitrary question interpretation |
| X2-ADP-06 · Baseline regression | accept | freezes meaning-bearing fields for all six questions |
| X2-ADP-07 · Kernel separation | accept | keeps Adapter outside default Kernel runtime |
| X2-ADP-08 · General Kernel integration | defer | requires a separate future human decision |

## Conclusion

**READY FOR HUMAN REVIEW OF READ-ONLY CONCEPT ADAPTER**

