# NEXAH Library — Kernel Reader Baseline

**Canonical Registry only · Before Proposal Overlay**

This baseline records what the current Orientation Kernel can answer before any
Proposal records, reader journeys, or new identities are loaded.

## Result

| Reader question | State | Observation |
|---|---|---|
| I am new. Which five Works? | partial | The first four are strong, but the Kernel returns seven Works and places THE OPERATOR LIBRARY before THE OPERATOR’S HANDBOOK. |
| I am interested in water. Which three books? | unsupported | Only FIELD ATLAS I is canonical. The Kernel has no confirmed Series query or Proposal overlay for Volumes II–III. |
| I know GEOMETRIA NOVA. What comes next? | partial | Recommendations are explainable, but LIBRARYBOOK ranks first; the reader-oriented learning branch is not prioritized. |
| Show every Work using Transition. | canonical pass | Eight canonical Works are returned through explicit `NX-OP-0005` references. Proposal candidates are correctly absent. |
| I am interested in navigation. Which Series? | unsupported | The current Registry has no Series-level query capable of answering this reader question. |
| I do not know what I am looking for. Surprise me. | unsupported | The Kernel has no curatorial-slot or diversity policy and would reduce discovery to ordinary ranking. |

## Beginner baseline

Current newcomer path:

1. THE VISITOR’S GUIDE
2. GEOMETRIA NOVA
3. THE LANGUAGE BOOK
4. THE LANGUAGE ATLAS
5. THE OPERATOR LIBRARY
6. THE OPERATOR’S HANDBOOK
7. THE ATLAS OF ATLASES

The entrance is directionally correct. The result does not yet satisfy the
reader request for five Works, and its fifth choice is a reference layer rather
than practice.

## After GEOMETRIA NOVA

Current top five recommendations:

1. LIBRARYBOOK — score 17
2. THE OPERATOR’S HANDBOOK — score 15
3. THE LANGUAGE ATLAS — score 14
4. THE CARTOGRAPHY LABORATORY — score 13
5. THE LANGUAGE BOOK — score 12

Every recommendation has reasons, which is a strong foundation. The ranking is
not yet reader-sensitive: shared Operators and builder/research audiences cause
the working LIBRARYBOOK to outrank the learning path.

## Transition

The canonical Operator query returns:

- GEOMETRIA NOVA
- THE OPERATOR’S HANDBOOK
- THE LANGUAGE BOOK
- THE LANGUAGE ATLAS
- FIELD ATLAS I — WATER
- THE CARTOGRAPHY LABORATORY
- THE OPERATOR LIBRARY
- THE ATLAS OF ATLASES

This is a valid canonical answer with explicit provenance. A future Proposal
overlay may add inferred candidates only if they are labeled separately.

## Journey evaluation

- **Beginner:** partially evaluable; ordering and result limit need reader-aware policy.
- **Builder:** not yet evaluable because THE OPERATOR remains a Proposal Work.
- **Research:** not yet evaluable because Field Atlas II–III, Mathematica I, and THE LIVING EQUATION remain Proposals.

## Required next capability

The next Kernel step is not embedding search. It is an explicit Proposal Overlay
that can:

1. distinguish Navigation Entities from Works;
2. read human-confirmed Editorial Sequences;
3. return a requested number of Works;
4. apply audience and journey context to ranking;
5. keep canonical facts separate from Proposal or inferred results;
6. explain every result with provenance.
7. curate deliberate variety for a surprise request rather than maximizing one score.

No Registry growth or ID allocation is authorized by this baseline.
