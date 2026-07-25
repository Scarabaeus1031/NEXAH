# NEXAH Freeze Planning Review 01

## Status

Independent repository planning review.

**Review date:** July 25, 2026  
**Decision:** **conditionally ready for a canonical Framework repository
freeze, but not ready to freeze today**

This review creates no architecture, scientific claim, subsystem, release, or
version. It distinguishes:

- the maintained NEXAH Framework repository;
- independently versioned artifacts such as OLS, the Orientation Kernel,
  ORION, Experience, and the adopted Constitution;
- a canonical source freeze;
- a coordinated public ecosystem launch.

Those distinctions follow the existing
[release policy](../../../RELEASES.md) and are necessary because the repository
already contains a historical `v1.0.0` Kernel-scope tag.

## Executive assessment

The repository is already stable enough in architecture, responsibility
boundaries, OLS release state, validation discipline, and public identity to
serve as the basis of a canonical Version 1 reference.

The remaining pre-freeze work is small. The repository should not be
redesigned, its research should not be broadened, and Architecture and OLS
should remain unchanged. Before a freeze is declared, however, the exact
artifact and release identity must be named, two current-state documents must
be reconciled with adopted governance and the final commit, the reviewed
changes must become one clean candidate, and CI must pass on that candidate.

The proposed Evidence Atlas is the strongest justified completion task before
the freeze, but it is not itself an accuracy blocker. It is a missing
claim-level navigation layer, not missing evidence or architecture.

## What “Version 1” may accurately mean

The phrase **NEXAH Version 1** is currently ambiguous. The repository explicitly
states that NEXAH does not have one shared ecosystem version:

| Scope | Existing version authority |
|---|---|
| Framework repository | Git commit and an approved release identity |
| Orientation Kernel | `pyproject.toml`, currently `0.7.0` |
| OLS | its own canonical release, currently OLS 1.0.0 |
| Constitution | adopted Constitution v1.0 |
| ORION | ORION release records |
| Experience | Experience release records |

A freeze must therefore identify itself as the canonical baseline of the
**Framework repository** and record its exact commit. It must not:

- reuse the historical `v1.0.0` tag;
- imply that Kernel 0.7.0 has become Kernel 1.0;
- re-release OLS 1.0.0;
- synchronize ORION or Experience versions by implication;
- describe the ecosystem as finished.

The final release name and tag remain an owner decision. The decision is a
freeze blocker because freezing under an ambiguous identity would contradict
the maintained release policy.

## 1. Remaining critical work

### A. Repository integrity

1. **Correct the current Governance entry in `REPOSITORY_MAP.md`.**  
   The map still describes the Constitution candidate as non-canonical and
   pending review. The Constitution has since been adopted. The smallest fix is
   to route the current entry to the maintained Governance index and adopted
   Constitution, while retaining `constitution_review_01` as historical review
   material.

2. **Review `ARCHITECTURE/SYSTEM_STATE.md` against the final candidate.**  
   The document calls itself current ground truth but carries a July 17 text
   review. It need not be rewritten. Its implemented facts should be checked,
   any actual mismatch corrected, and its review date and candidate commit
   recorded or the document explicitly retained as a dated snapshot.

3. **Create one clean, immutable candidate.**  
   The four reviews and Identity Alignment Pass are currently uncommitted.
   Freeze only a clean worktree, record the commit SHA, and preserve an artifact
   inventory and checksums as required by the existing release policy.

4. **Run integrity checks on the exact candidate.**  
   This review observed a successful canonical test invocation:
   `python -m pytest -q -p no:cacheprovider` completed with **302 passed**.
   The final candidate still needs that result, Markdown/link validation,
   `git diff --check`, and green public CI on the same commit.

5. **Verify maintained public links.**  
   Root and public entry documents should not freeze links to repositories or
   public surfaces that are absent or private without saying so. Historical
   documents need not be normalized.

### B. Documentation

1. **Implement the minimal Evidence Atlas, preferably before freeze.**  
   Create only the already-designed single page at
   `docs/evidence/README.md`, using the reviewed 28 claim units, and add the
   bounded inbound links approved by Discovery Atlas Review 01. Preserve the
   three blocked evidence chains as blocked.

2. **Record the freeze scope and limits.**  
   Release notes should state what was frozen, the exact commit, validation
   results, independently versioned components, known blocked evidence chains,
   and prohibited implications.

3. **Do not perform another identity rewrite.**  
   The maintained Research and Library entrances have already received the
   minimal status and reading boundaries identified by Repository Identity
   Review 01.

### C. Research

No research result must be completed to permit the Framework repository
freeze. Research should retain its local status:

- exact constructions remain exact;
- bounded empirical findings remain bounded;
- hypotheses remain hypotheses;
- missing POA, NTO, and DERIS/HYDRA source chains remain blocked where the
  Evidence Register says they are blocked;
- exploratory and historical material remains visibly non-canonical.

Independent replication, broader samples, reader-effect studies, and
cross-domain mechanism validation are scientifically valuable, but they are
new evidence work rather than corrections to the current repository.

### D. Library

The Library release check passes with editorial warnings:

- Registry coverage and proposal isolation pass;
- the fixed reader regression set passes;
- the initial series structure is confirmed;
- direct traversability and twelve manual cleanup actions remain incomplete.

Because the Library already presents itself as a pilot with local status, these
editorial warnings do not make the repository inaccurate. Preserve them in the
freeze record and continue the cleanup after the freeze.

### E. Public communication

Repository identity is sufficiently aligned for a source freeze:

- NEXAH is presented as evidence-bound orientation work;
- subsystem responsibilities remain separate;
- Human interpretation remains final authority;
- stronger universal and causal readings are rejected;
- NEXAH and NEXAHEDRON retain distinct public roles.

The supplied **Orienting NEXAH** overview is consistent with this identity, but
it is not yet repository evidence and should be treated as a publication
candidate. Before public use:

1. do not link to an Evidence Atlas until that page exists;
2. label maturity ratings with date, method, and source, or present them as an
   informative editorial synthesis rather than an unexplained score;
3. frame “better questions” as a mission or commitment, not as a demonstrated
   reader outcome;
4. make clear that a Version 1 freeze is a stable baseline, not a finished
   system.

### F. Infrastructure

For a **repository freeze**, the required infrastructure is limited to a
reproducible candidate and green CI on its exact commit.

DNS, TLS, hosting, legal checks, public smoke tests, and publication of
independent ORION or Experience repositories are blockers for a coordinated
public launch, not for freezing the NEXAH source repository. The two events
must not be reported as the same event.

Any compatibility statement involving ORION must cite the exact approved Core
revision. A connected-Core revision difference is not an architecture defect,
but an unqualified compatibility claim would be inaccurate.

## 2. True freeze blockers

A blocker here means that freezing first would create an inaccurate,
unidentified, or unreproducible canonical repository.

| Blocker | Why it is a blocker | Smallest resolution |
|---|---|---|
| Ambiguous “NEXAH Version 1” identity | The repository rejects one ecosystem-wide version and already has a historical `v1.0.0` tag | Approve a new, unambiguous Framework release name/tag and state its scope |
| Outdated Governance status in `REPOSITORY_MAP.md` | A maintained current-state map contradicts the adopted Constitution | Replace only the current Governance status and preserve the review as historical |
| Unverified current System State | A document labelled current ground truth predates the final candidate | Recheck facts and stamp the final review date/commit or mark it as a dated snapshot |
| No immutable final candidate | The reviewed state is still a dirty worktree | Commit the intended files, record the SHA, and freeze only that clean tree |
| No green CI on the exact freeze commit | Existing release policy requires it; a local pass is not the public release record | Run the canonical suite and required checks on the final commit until CI is green |
| Unverified canonical outbound links | A canonical entry point must not direct readers to missing resources without qualification | Check maintained front-door links and correct or qualify only actual failures |

No scientific hypothesis, new experiment, new architecture document, or
Library cleanup item belongs in this blocker list.

## 3. Prioritization

| Priority | Task | Reason | Freeze blocker? |
|---|---|---|---|
| P0 | Define the Framework freeze scope, name, tag, and exact independently versioned exclusions | Prevents a false ecosystem-wide Version 1 claim | Yes |
| P0 | Correct the Governance status in `REPOSITORY_MAP.md` | Removes a direct contradiction in current navigation | Yes |
| P0 | Verify and stamp `SYSTEM_STATE.md` against the final candidate | Makes “current ground truth” accurate at freeze | Yes |
| P0 | Commit one clean candidate and record its SHA | Makes the freeze identifiable and reproducible | Yes |
| P0 | Pass tests, Markdown/link checks, diff checks, and public CI on that SHA | Satisfies maintained release discipline | Yes |
| P0 | Verify canonical front-door outbound links | Prevents broken canonical navigation | Yes |
| P1 | Implement the single-page Evidence Atlas | Completes the strongest review-supported navigation gap | No, if explicitly deferred and not linked as existing |
| P1 | Write bounded release notes and known-limit record | Prevents the freeze from overstating scope | Part of the release decision |
| P1 | Review the supplied overview before publication | Keeps public identity aligned with evidence and maturity | No for source freeze; yes for publishing that visual |
| P2 | Complete Library traversability and manual editorial cleanup | Improves reader experience without changing current claims | No |
| P2 | Restore or repository-address missing POA, NTO, and DERIS/HYDRA evidence where appropriate | Unblocks particular evidence chains | No |
| P2 | Complete public hosting, legal, domain, and smoke checks | Enables coordinated public launch | No for source freeze |
| P3 | Run new replications, reader studies, and cross-domain validation | Extends evidence beyond the frozen baseline | No; after Version 1 |

## 4. Audit of the four previous reviews

### Discovery Atlas Review 01

| Recommendation | Status | Freeze treatment |
|---|---|---|
| Use a structured, non-authoritative Evidence Atlas | Still missing | Prefer before freeze |
| Use one Markdown page at `docs/evidence/README.md` | Designed, not implemented | Implement without expansion |
| Preserve 28 bounded claim units and their limits | Implemented in the reviewed register | Use as the source |
| Keep unavailable POA, NTO, and DERIS/HYDRA evidence visibly blocked | Implemented in review; not yet propagated to an Atlas | Preserve, do not infer |
| Add only bounded inbound navigation | Still missing | Add with the Atlas |

### Repository Synthesis Review 01

| Recommendation or conclusion | Status | Freeze treatment |
|---|---|---|
| Treat NEXAH as a coherent federated research program | Implemented in maintained identity | Preserve |
| Do not claim one unified scientific theory | Implemented in boundaries and status notices | Preserve |
| Recognize methodological and architectural coherence as stronger than universal mechanism claims | Implemented in the review and Identity Alignment Pass | Preserve |
| Keep uneven maturity, limitations, and blocked chains visible | Partially implemented; claim-level visibility remains distributed | Evidence Atlas improves this |
| Seek broader replication and global replay | Intentionally future work | After Version 1 |

### Methodology Review 01

| Recommendation or conclusion | Status | Freeze treatment |
|---|---|---|
| Describe Orientation Methodology only as an informative emerging synthesis | Implemented | Preserve |
| Do not create a subsystem, OLS extension, or new authority | Implemented | No architecture change |
| Preserve orientation/recommendation/authorization/execution boundaries | Implemented | Preserve |
| Treat Evidence Atlas as navigation, not validation | Implemented in design | Preserve in implementation |
| Validate general method effectiveness separately | Intentionally postponed | After Version 1 |

### Repository Identity Review 01

| Recommendation | Status | Freeze treatment |
|---|---|---|
| Add local Research status context | Implemented by Identity Alignment Pass 01 | Complete |
| Qualify stronger legacy mechanism language without erasing it | Implemented | Complete |
| Add a visual-reading boundary to the Library entrance | Implemented | Complete |
| Leave the already aligned root and Architecture identity unchanged | Implemented | Preserve |
| Keep NEXAH and NEXAHEDRON roles distinct | Supported publicly and in maintained documentation | Verify links; do not redesign |
| Avoid a new methodology marketing layer | Implemented | Preserve |

The Identity Alignment Pass itself reports no change to Architecture, OLS,
research ownership, scientific findings, or Human authority. Its recommended
document edits are complete but must still be included in the final candidate.

## 5. Evidence Atlas decision

**Recommendation: implement before freeze, but do not classify it as a strict
accuracy blocker.**

Reasons to implement it before freeze:

- it is the one concrete, repository-wide navigation task directly recommended
  by the completed review sequence;
- Version 1 is intended to stabilize evidence visibility and navigation rather
  than extend theory;
- the work is bounded to one Markdown page and a few links;
- it makes negative results, limitations, and blocked evidence as discoverable
  as positive findings;
- the supplied public overview already anticipates it.

Reasons it is not a strict blocker:

- the authoritative evidence already exists in its owning locations;
- Architecture, OLS, validation, and Research do not depend on the Atlas;
- the repository remains accurate without it if no current link claims that it
  exists;
- the review explicitly defines it as a map, not an authority.

If implementation is postponed, the freeze notes should say so explicitly and
the supplied overview must not publish an active Evidence Atlas route.

## 6. Public ecosystem assessment

| Surface | Version 1 role | Assessment |
|---|---|---|
| Repository / GitHub | canonical revisions, evidence, code, responsibility boundaries | Aligned in identity; final commit, CI, links, and release identity remain |
| `nexah.de` | public and intellectual entrance, Library and orientation | Previously reviewed as aligned; final public link/smoke verification belongs to launch |
| NEXAHEDRON | bounded Human-facing laboratory/workspace | Distinct role is supported; do not merge it with repository authority |
| Library | curated Human interpretation and visual navigation | Aligned after the reading-boundary edit; editorial cleanup remains |
| Are.na | live visual source and publication surface | Source/publication authority remains separate from repository evidence |

This is sufficient for a **source repository freeze** after the P0 items. It is
not evidence that every public surface is deployment-ready. Public launch
readiness must continue to use the existing operational launch gates.

## 7. Research status recommendation

### Freeze

- OLS 1.0.0 as its already released semantic artifact;
- adopted Constitution v1.0 as governance baseline;
- completed POA records only where they are repository-addressable;
- completed validation bundles and negative results at their current bounded
  claims;
- the four reviews and Identity Alignment Pass as dated review artifacts.

“Freeze” here means preserve the exact released or reviewed artifact. It does
not transfer its authority to the Framework release.

### Mark or retain as exploratory

- transition-geometry mechanism hypotheses;
- theoretical extensions;
- unreplicated cross-domain correspondences;
- visuals whose source methods or evidence chains are absent;
- DERIS/HYDRA, NTO, and POA materials that the Evidence Register currently
  cannot trace inside the repository.

### Leave active

- bounded research programs with clear local ownership;
- Library editorial work;
- application studies;
- empirical replication and Human studies.

No research program needs to be declared complete merely to freeze the
repository that preserves it.

## 8. Architecture recommendation

**Leave Architecture unchanged.**

The Architecture README already:

- assigns separate responsibilities;
- subordinates cross-system coordination to the adopted Constitution;
- keeps OLS semantic authority separate from implementations;
- keeps Human interpretation outside autonomous execution;
- treats diagrams and pipelines as informative rather than mandatory;
- rejects one universal runtime.

The required `SYSTEM_STATE.md` verification is state maintenance, not an
architecture correction. The Governance entry in `REPOSITORY_MAP.md` is a
navigation correction, not a new responsibility.

## 9. Optional improvements after Version 1

- finish Library direct traversability and the twelve open editorial actions;
- add independent replication and broader statistical validation;
- validate whether the method improves Human questions or decisions;
- restore missing primary evidence chains where authoritative materials exist;
- add automation to the Evidence Atlas only if the single-page version proves
  difficult to maintain;
- complete coordinated public launch work;
- explore new applications without changing frozen semantic and governance
  artifacts.

None of these should delay the source freeze once the P0 items are complete.

## Final answers

### What absolutely must happen before Freeze?

Define the Framework-specific release identity; correct the outdated Governance
status; verify and stamp System State; produce one clean candidate commit;
verify canonical links; and obtain green tests, documentation checks, and
public CI on that exact commit.

### What should happen soon after Freeze?

If it was not included, publish the minimal Evidence Atlas first. Then complete
Library navigation cleanup and coordinated public launch checks without
changing the frozen baseline.

### What should wait for Version 2?

New architecture, new OLS semantics, generalized methodology claims, new
cross-domain mechanisms, broader applications, automation around the Evidence
Atlas, and scientific claims requiring new replication or Human studies.

### Is the repository already stable enough to serve as the canonical Version 1 reference?

**Yes in substance, but not yet as an identified release artifact.** Its
architecture, identity, semantic authority, and evidence discipline are stable
enough. The remaining blockers concern consistency and release integrity, not
research expansion.

### Would this review approve the freeze today?

**No.** Approval should follow only after these smallest blockers are closed:

1. unambiguous Framework freeze identity;
2. corrected Governance status in the current repository map;
3. verified System State for the candidate;
4. clean committed candidate with recorded SHA;
5. verified maintained links;
6. green required checks and public CI on that SHA.

After those items, this review recommends approval. The Evidence Atlas should
preferably be included for a complete Version 1 navigation layer, but its
absence alone does not make the frozen repository false.

