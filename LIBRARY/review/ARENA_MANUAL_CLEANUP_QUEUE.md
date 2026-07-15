# NEXAH Library — Manual Are.na Cleanup Queue

**Human-executable only · no automatic write authorized**

This queue translates confirmed reader friction into small editorial actions.
It does not authorize the connector, Kernel, or any script to modify Are.na.

## Entry and orientation

| Priority | Affected Channel | Observed problem | Reader impact | Proposed manual action | Evidence source | Automatic write authorized |
|---|---|---|---|---|---|---|
| P0 | [START](https://www.are.na/nexah-scarabaeus1031/01-nexah-start-core-orientation) · `5178452` | START is not privileged on the public Channels landing page. | A newcomer may never find the designed entrance. | Keep START clearly named and place a visible link to it in public profile/library orientation surfaces available to the editor. | `HUMAN_WALKTHROUGH_FINDINGS.md` · HW-01 | no |
| P0 | [Visitor’s Guide](https://www.are.na/nexah-scarabaeus1031/the-visitor-s-guide) · `5404615` | It explains the Library Rooms but contains no onward Channel connections. | The guide describes a route the reader cannot walk. | Add a small orientation group linking Language Book, Geometria Nova, Language Atlas, and Operator’s Handbook; mark Language Book as the beginner continuation. | HW-03 · current public contents | no |

## Beginner continuation

| Priority | Affected Channel | Observed problem | Reader impact | Proposed manual action | Evidence source | Automatic write authorized |
|---|---|---|---|---|---|---|
| P1 | [Language Book](https://www.are.na/nexah-scarabaeus1031/the-language-book) · `5421517` | No direct transition to Geometria Nova. | The confirmed learning sequence breaks after vocabulary. | Add a clearly labeled `Continue → GEOMETRIA NOVA` Channel connection. | `TRAVERSABILITY_AUDIT.md` · RJ-01 | no |
| P1 | [Geometria Nova](https://www.are.na/nexah-scarabaeus1031/geometria-nova) · `5442781` | No direct transition to Language Atlas. | The foundation model does not lead into its visual map. | Add `Continue → THE LANGUAGE ATLAS`. | `TRAVERSABILITY_AUDIT.md` · RJ-01 | no |
| P1 | [Language Atlas](https://www.are.na/nexah-scarabaeus1031/the-language-atlas) · `5426966` | No direct transition to Operator’s Handbook. | The reader cannot move from navigation into practice. | Add `Continue → THE OPERATOR’S HANDBOOK`. | `TRAVERSABILITY_AUDIT.md` · RJ-01 | no |

## Builder path

| Priority | Affected Channel | Observed problem | Reader impact | Proposed manual action | Evidence source | Automatic write authorized |
|---|---|---|---|---|---|---|
| P1 | [START](https://www.are.na/nexah-scarabaeus1031/01-nexah-start-core-orientation) · `5178452` | No Builder-path connection to Operator. | Builders have no visible thematic entrance. | Add a labeled `Builder Path → THE OPERATOR` connection without replacing the beginner entrance. | `TRAVERSABILITY_AUDIT.md` · RJ-02 | no |
| P1 | [Operator](https://www.are.na/nexah-scarabaeus1031/the-operator-xkoop3mjgcs) · `5442721` | No direct transition to Operator Map. | The accessible visual bridge is hidden. | Add `Continue → THE OPERATOR MAP`. | `TRAVERSABILITY_AUDIT.md` · RJ-02 | no |
| P1 | [Operator Map](https://www.are.na/nexah-scarabaeus1031/the-operator-map) · `5393574` | No direct transition to Operator’s Handbook. | The Map behaves like an endpoint instead of a bridge. | Add `Continue → THE OPERATOR’S HANDBOOK`. | HW-05 · RJ-02 | no |
| P1 | [Operator’s Handbook](https://www.are.na/nexah-scarabaeus1031/the-operator-s-handbook) · `5391199` | No main-path transition to Cartography Laboratory. | Practice does not lead into the documented research environment. | Add `Continue → THE CARTOGRAPHY LABORATORY`; keep Operator Library as a separate reference branch. | `TRAVERSABILITY_AUDIT.md` · RJ-02 | no |
| P1 | [Cartography Laboratory](https://www.are.na/nexah-scarabaeus1031/the-cartography-laboratory) · `5386766` | No transition to Librarybook. | The laboratory does not lead into the large synthesis. | Add `Continue → LIBRARYBOOK` with a note that it is a working synthesis. | `TRAVERSABILITY_AUDIT.md` · RJ-02 | no |

## Research path

| Priority | Affected Channel | Observed problem | Reader impact | Proposed manual action | Evidence source | Automatic write authorized |
|---|---|---|---|---|---|---|
| P1 | [Field Atlas I](https://www.are.na/nexah-scarabaeus1031/field-atlas-i-water) · `5415765` | No direct link to Volume II. | The confirmed Series order is not walkable. | Add `Next Volume → FIELD ATLAS II`. | `TRAVERSABILITY_AUDIT.md` · RJ-03 | no |
| P1 | [Field Atlas II](https://www.are.na/nexah-scarabaeus1031/field-atlas-ii-the-architecture-of-agency) · `5404576` | No direct link to Volume III. | The confirmed Series order is not walkable. | Add `Next Volume → FIELD ATLAS III`. | `TRAVERSABILITY_AUDIT.md` · RJ-03 | no |
| P0 | [Field Atlas III](https://www.are.na/nexah-scarabaeus1031/field-atlas-iii-morphology) · `5386781` | The description ends with `Ich finde, das passt inzwischen sehr gut zur gesamten Reihe:`. | Editorial residue interrupts the public Work. | Remove only the stray editorial fragment after confirming the intended final sentence. | HW-07 · public description | no |
| P1 | [Field Atlas III](https://www.are.na/nexah-scarabaeus1031/field-atlas-iii-morphology) · `5386781` | No link to Operational Geometry. | The proposed bridge from morphology into formal geometry is invisible. | Add `Bridge → NEXAH ATLAS — THE OPERATIONAL GEOMETRY OF TRANSITION`. | HW-06 · RJ-03 | no |
| P1 | [Operational Geometry](https://www.are.na/nexah-scarabaeus1031/00-nexah-atlas-the-operational-geometry-of-transition) · `5217666` | No link to Mathematica I. | The bridge Work does not complete the domain transition. | Add `Continue → NEXAH MATHEMATICA I`. | `TRAVERSABILITY_AUDIT.md` · RJ-03 | no |
| P1 | [Mathematica I](https://www.are.na/nexah-scarabaeus1031/nexah-mathematica-i-prime-residue-geometry) · `5203312` | No link to Living Equation. | Formal research does not route toward the synthesis destination. | Add `Continue → THE LIVING EQUATION`. | `TRAVERSABILITY_AUDIT.md` · RJ-03 | no |

## Editorial rule for all actions

Use small Channel connections labeled by reader purpose—`Continue`, `Next
Volume`, `Bridge`, or `Reference`—instead of duplicating descriptions or adding
machine-oriented metadata to the Works. Re-run the read-only audit after the
human editor completes any action.
