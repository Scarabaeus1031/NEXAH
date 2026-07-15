# NEXAH Library — Reader Overlay Evaluation

**Canonical-only baseline vs. Canonical + explicit Proposal Overlay**

This evaluation covers only the six human-reviewed Reader questions. The
Overlay allocates no IDs, does not modify the Registry, and never resolves a
Proposal as canonical.

## Results

| Question | Canonical-only | With explicit Overlay | Result |
|---|---|---|---|
| UQ-01 · newcomer, five Works | Partial; seven results | Exactly five canonical Works in the curated beginner order | pass |
| UQ-02 · water, three books | Unsupported | Field Atlas I canonical; II–III visibly Proposal | pass with proposals |
| UQ-03 · after Geometria | Partial; LIBRARYBOOK ranked first | Learning → practice → navigation → documentation → synthesis | pass |
| UQ-04 · Transition | Eight canonical Works | Eight canonical Works plus 24 separately labeled inferred candidates | pass with inference boundary |
| UQ-05 · navigation | Unsupported | Confirmed Orientation Architecture sequence plus two canonical companion maps | pass with proposal Series |
| UQ-06 · surprise me | Unsupported | Visual Work + Field Atlas + Handbook + unexpected connection | pass with curated diversity |

## UQ-01 — Reader Mode

1. THE VISITOR’S GUIDE — canonical
2. THE LANGUAGE BOOK — canonical
3. GEOMETRIA NOVA — canonical
4. THE LANGUAGE ATLAS — canonical
5. THE OPERATOR’S HANDBOOK — canonical

START explains the route but does not consume a Work slot. No score is shown.

## UQ-02 — Water

1. FIELD ATLAS I — WATER — canonical
2. FIELD ATLAS II — THE ARCHITECTURE OF AGENCY — proposal
3. FIELD ATLAS III — MORPHOLOGY — proposal

Explain Mode identifies the confirmed editorial sequence and resolves Proposal
references only as `arena:<channel_id>`.

## UQ-03 — After GEOMETRIA NOVA

The answer is no longer a raw ranking:

1. Learn the language — THE LANGUAGE BOOK
2. Practice the operators — THE OPERATOR’S HANDBOOK
3. Navigate the map — THE LANGUAGE ATLAS
4. See the documented research environment — THE CARTOGRAPHY LABORATORY
5. Enter the working synthesis — LIBRARYBOOK

LIBRARYBOOK remains available but no longer dominates the first recommendation.

## UQ-04 — Transition

- **Canonical:** eight Works with explicit `NX-OP-0005` references.
- **Inferred:** 24 Proposal Works whose public descriptions mention Transition.

Inferred matches are not treated as Operator annotations. Reader Mode labels
their state; Explain Mode reveals the description-match provenance.

## UQ-05 — Navigation

The answer is a thematic starting point, not only a Series lookup:

- Orientation Architecture — confirmed four-volume editorial sequence, Proposal layer
- THE LANGUAGE ATLAS — canonical companion
- THE ATLAS OF ATLASES — canonical companion

## UQ-06 — Surprise me

- Visual Work — THE LIVING EQUATION
- Field Atlas — FIELD ATLAS I — WATER
- Handbook — THE OPERATOR’S HANDBOOK
- Unexpected connection — THE INNER WORLD

The selection uses explicit curatorial slots, not score maximization.

## Mode boundary

### Reader Mode

- short ordered answer;
- no scores;
- no visible Operator IDs or provenance detail;
- canonical, proposal, and inferred state remains visible.

### Explain Mode

- record reference;
- Type, Form, Library Function, and publication status;
- evidence class and source;
- Series sequence where relevant;
- canonical, proposal, or inferred distinction.

## Evaluation conclusion

The Overlay demonstrates that the same Library can orient newcomer, researcher,
builder, thematic explorer, and open-ended browser differently without expanding
the Canonical Registry. It is ready for a second human Reader Review, not for ID
allocation.
