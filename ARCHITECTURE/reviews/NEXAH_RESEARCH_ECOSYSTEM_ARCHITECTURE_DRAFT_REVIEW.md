# NEXAH Research & Ecosystem Architecture Draft — Authority-Conflict Review

**Review status:** Final revision pass completed for the current draft diff

**Architecture status:** Non-canonical draft

**Adoption decision:** Not made

**Date:** 2026-07-30

## 1. Review Question

Does the proposed
[`NEXAH_RESEARCH_ECOSYSTEM_ARCHITECTURE.md`](../NEXAH_RESEARCH_ECOSYSTEM_ARCHITECTURE.md)
describe the inspected ecosystem without:

- displacing the NEXAH Ecosystem Constitution;
- replacing the Repository Map;
- changing the frozen ORION Version 1 certification;
- transferring authority between repositories or constitutional
  responsibilities;
- presenting Research or a horizon as implemented or certified capability;
- treating placement or indexing as canonical adoption?

## 2. Diff Scope Reviewed

The architecture proposal changes only the central NEXAH repository:

1. adds one non-canonical Architecture Draft;
2. adds one review record for that draft;
3. adds a clearly labeled draft link to `README.md`;
4. adds a clearly labeled draft link to `REPOSITORY_MAP.md`;
5. adds a clearly labeled draft link to `ARCHITECTURE/README.md`.

No Constitution, governance rule, semantic specification, implementation,
test, certified artifact, proof, Runtime, Gateway, public website, or
cross-repository file is changed.

ORION, NEXAHEDRON, and NEXAH Experience were inspected read-only. Their dirty
working trees and exact checked commits are disclosed in the draft's Source
and Status Ledger.

## 3. Diff Reconciliation

The repository state was checked from
`/Users/tho2020/Documents/GitHub/NEXAH`.

```text
$ git status --short
 M ARCHITECTURE/README.md
 M README.md
 M REPOSITORY_MAP.md
?? ARCHITECTURE/NEXAH_RESEARCH_ECOSYSTEM_ARCHITECTURE.md
?? ARCHITECTURE/reviews/NEXAH_RESEARCH_ECOSYSTEM_ARCHITECTURE_DRAFT_REVIEW.md
```

```text
$ git diff --stat
 ARCHITECTURE/README.md | 1 +
 README.md              | 1 +
 REPOSITORY_MAP.md      | 1 +
 3 files changed, 3 insertions(+)
```

```text
$ git diff --name-status
M  ARCHITECTURE/README.md
M  README.md
M  REPOSITORY_MAP.md
```

The two new documents are untracked, so normal `git diff --stat` and
`git diff --name-status` do not list them. They are confirmed by:

```text
$ git ls-files --others --exclude-standard
ARCHITECTURE/NEXAH_RESEARCH_ECOSYSTEM_ARCHITECTURE.md
ARCHITECTURE/reviews/NEXAH_RESEARCH_ECOSYSTEM_ARCHITECTURE_DRAFT_REVIEW.md
```

The current Git worktree therefore contains exactly five affected paths: two
new documents and three one-line index additions. No sixth path, second draft,
temporary root document, or deletion is present. The UI report of six files
and `+987/-38` does not match the current Git worktree and is treated as a
stale or differently scoped UI calculation rather than repository evidence.

## 4. Research-Question Review

The umbrella-question decision was checked against four source families:

| Source | Observed scope | Decision |
|---|---|---|
| `MANIFESTO.md` | Human orientation among heterogeneous bounded representations | primary basis for the umbrella question |
| `GOVERNANCE/ECOSYSTEM_CONSTITUTION.md` | shared Orientation Space with distinct responsibilities and Human authority | constrains both questions |
| `RESEARCH/RESEARCH_VISION.md` | bounded transition-geometry research inside complex dynamical systems | retained as active research and historical lineage, not promoted to the umbrella identity |
| `NEXAHEDRON/docs/rfcs/RFC-0001_OPEN_ORIENTATION_PROTOCOL.md` | cooperation with replaceable external knowledge and intelligence participants | basis for a subordinate Open Systems and Rails question |

**Finding:** “heterogeneous intelligence systems” is too specific to be a
precondition of the umbrella Orientation Research Question. It is justified,
but as a subordinate Open Systems and Rails Research Question. This preserves
the general orientation problem when no AI or external participant is present.

## 5. Diagram Review

The earlier diagram contained:

```text
Research → Framework → OLS → Kernel → ORION
```

Even with a disclaimer, that sequence could be read as a pipeline, maturity
ladder, or authority transfer. It was replaced with a nonlinear responsibility
map organized by Inquiry, Definition, Deterministic Processing, Editorial
Identity, and Human/Public Encounter.

Only `OLS → Kernel → ORION` remains directional, and only as a labeled,
bounded contract dependency. Research informs Framework and OLS only through
explicit adoption. No edge transfers authority.

## 6. Authority Review

| Review area | Result | Basis |
|---|---|---|
| Constitution remains highest authority | PASS | Draft header, Purpose, status vocabulary, Source Ledger, and Promotion Gate all subordinate the proposal to `GOVERNANCE/ECOSYSTEM_CONSTITUTION.md` |
| Repository Map is supplemented, not replaced | PASS | One labeled draft entry is added; the existing map and all existing routes remain intact |
| Governance is not created by documentation placement | PASS | Draft is marked non-canonical; indexing, merging, committing, or publishing is explicitly insufficient for adoption |
| Human authority remains Human | PASS | Human retains intention, interpretation, acceptance, Reflection, Rest, decision, and effect authority |
| Framework authority remains distinct | PASS | Shared Orientation Space and responsibility boundaries remain Framework responsibilities; execution and Human meaning are excluded |
| OLS 1.0 and Kernel remain distinct | PASS | OLS 1.0 owns released semantics as a published specification; Kernel maturity and execution do not replace that authority |
| Library Registry and Living Atlas remain distinct | PASS | Registry identity and Living Atlas editorial relations do not become semantics, validation, certification, or interpretation |
| ORION Version 1 scope remains frozen | PASS | Certified capabilities are enumerated from the frozen baseline; terminal STOP remains `at_slice_iv_certified`; Runtime, Gateway, LYRA, SIRIUS, reasoning, applications, and Human Reports remain outside |
| Wider ORION direction is not presented as certification | PASS | Replaceable participants and orchestration are labeled open research horizon and tied to accepted ADRs rather than the Version 1 certificate |
| NEXAHEDRON does not acquire ORION or evidence authority | PASS | It is described as a bounded Human-facing experiment and faithful presentation layer |
| NEXAH Experience does not acquire Research or Core authority | PASS | It remains the public and intellectual entrance and routing surface |
| Repository responsibilities are not silently reassigned | PASS WITH OWNER REVIEW | The mapping restates inspected front doors and governing documents; repository-owner confirmation is still required before adoption |
| Historical lineage is not current authority | PASS | Transition geometry, JANUS, RL, and application research are labeled historical lineage and/or active research |
| Research horizon is not a product promise | PASS | Non-claims exclude a universal theory, general AI assistant, global runtime, autonomous authority, and NEXAHEDRON production promise |
| Maturity and authority remain independent | PASS | Every principal component now records maturity/evidence separately from authority class; implementation is explicitly denied authority-generating force |

## 7. Ambiguities Corrected During Review

The following formulations were rejected or narrowed before this review was
closed:

- “cross-repository architecture baseline” became “Architecture Draft —
  non-canonical”;
- “canonical home” became “appropriate location for this draft”;
- “canonical outputs” became “owned outputs”;
- every index link now says “Draft (non-canonical)”;
- ORION's certified Version 1 capabilities were separated from its wider
  research horizon;
- Kernel “decision” language was replaced with deterministic execution;
- exact repository commits, dirty states, and source paths were added;
- maturity/evidence status was separated from authority class;
- OLS 1.0, Kernel, ORION V1, Library Registry, NEXAHEDRON, Experience, and
  Human were classified on both axes;
- the umbrella Research Question was separated from the subordinate Open
  Systems and Rails Research Question;
- the linear-looking architecture diagram was replaced by a nonlinear
  responsibility map;
- the five-path Git diff was reconciled against the inconsistent UI count.

## 8. Remaining Adoption Questions

These questions do not invalidate the draft, but they require explicit Human
and repository-owner review before canonical adoption:

1. Do the owning maintainers accept the descriptive cross-repository
   responsibility rows?
2. Does NEXAH governance want one cross-repository research architecture to
   become canonical, or should it remain an informative research map?
3. Should the public interface mapping be adopted as architecture, or remain
   an editorial consequence of the governing responsibilities?
4. Do the maintainers accept the two-question structure: a general umbrella
   Orientation Research Question and a subordinate Open Systems and Rails
   Research Question?

## 9. Review Verdict

**No direct authority conflict was found in the reviewed draft.**

The proposal preserves the Constitution, supplements the Repository Map,
leaves ORION Version 1 unchanged, and does not modify another repository.

This verdict means the document is suitable for Human and owner review. It
does **not** make the document canonical. Canonical adoption remains a separate
governance action after review of the complete diff.
