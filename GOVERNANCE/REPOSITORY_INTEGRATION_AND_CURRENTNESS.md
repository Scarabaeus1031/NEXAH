# Desk 03 — Repository Integration and Currentness

**Role:** `03 Framework & Library Steward · 10 NEXAH Core`

**Owner-confirmed responsibility:** 2026-08-20

**Repository-history status:** `REVIEW_REQUIRED` until this bounded documentation change is explicitly accepted into NEXAH history

**Primary repository:** `Scarabaeus1031/NEXAH`

**Operational return:** `02 Mission Control Director`

## Purpose

This is the single NEXAH entry point for completed, repository-relevant results
from ecosystem desks. It connects those results to the existing Evidence Atlas,
Library Registry, architecture continuity ledger, update queue and drift check.
It creates no second ledger, queue, registry, Constitution or lifecycle.

The Framework & Library Steward checks repository routing, currentness,
provenance and the accuracy of the public NEXAH projection. Source repositories
retain their scientific, semantic, product, release, presentation and
publication authority. Thomas retains Adoption, meaning, priority, decision,
consent and STOP.

## Existing mechanism

| Responsibility | Existing controlling source |
|---|---|
| Authority, canonical homes and derived projections | [Ecosystem Constitution](ECOSYSTEM_CONSTITUTION.md) |
| Cross-repository roles and change control | [Adopted Research & Ecosystem Architecture](../ARCHITECTURE/NEXAH_RESEARCH_ECOSYSTEM_ARCHITECTURE.md) and its [Adoption Decision](../ARCHITECTURE/NEXAH_RESEARCH_ECOSYSTEM_ARCHITECTURE_ADOPTION_DECISION.md) |
| Public claim navigation | [Evidence Atlas](../docs/evidence/README.md) |
| Evidence candidates awaiting source/owner review | [Evidence Atlas Update Queue](../docs/evidence/EVIDENCE_ATLAS_UPDATE_QUEUE.md) |
| Library identity and provenance | [Library Architecture and Registry](../LIBRARY/README.md) |
| Architecture synchronization status and its one update queue | Science Lab [`01_ECOSYSTEM_ARCHITECTURE_STATUS_LEDGER.md`](https://github.com/Scarabaeus1031/NEXAH-Science-Lab/blob/a561aad160bb1e6e85e95d349ed9d843246ebc2c/NEXAH_ORION_ECOSYSTEM_ARCHITECTURE_CONTINUITY_AND_DRIFT_CONTROL/01_ECOSYSTEM_ARCHITECTURE_STATUS_LEDGER.md) at immutable revision `a561aad160bb1e6e85e95d349ed9d843246ebc2c` |
| Update triggers and target selection | Science Lab [`00_ARCHITECTURE_CONTINUITY_INVARIANT.md`](https://github.com/Scarabaeus1031/NEXAH-Science-Lab/blob/a561aad160bb1e6e85e95d349ed9d843246ebc2c/NEXAH_ORION_ECOSYSTEM_ARCHITECTURE_CONTINUITY_AND_DRIFT_CONTROL/00_ARCHITECTURE_CONTINUITY_INVARIANT.md) and [`03_REPOSITORY_UPDATE_MATRIX.md`](https://github.com/Scarabaeus1031/NEXAH-Science-Lab/blob/a561aad160bb1e6e85e95d349ed9d843246ebc2c/NEXAH_ORION_ECOSYSTEM_ARCHITECTURE_CONTINUITY_AND_DRIFT_CONTROL/03_REPOSITORY_UPDATE_MATRIX.md) at the same immutable revision |
| Read-only drift verification | Science Lab [`02_ARCHITECTURE_DRIFT_CHECK.md`](https://github.com/Scarabaeus1031/NEXAH-Science-Lab/blob/a561aad160bb1e6e85e95d349ed9d843246ebc2c/NEXAH_ORION_ECOSYSTEM_ARCHITECTURE_CONTINUITY_AND_DRIFT_CONTROL/02_ARCHITECTURE_DRIFT_CHECK.md) at the same immutable revision |
| Portfolio, WIP and operational return | Mission Control lifecycle, decisions, tickets and handoffs |

The architecture ledger owns synchronization status and maintenance queueing
only. It has no semantic, scientific or product authority. The Evidence Atlas
is a non-authoritative navigation layer. The Library Registry owns editorial
identity only within its declared contract.

## When a desk must hand off

A completed or adopted result enters this route when it affects at least one
of the following:

- the public NEXAH README, Repository Map or central navigation;
- Framework or OLS status, normativity, release identity or conformance claims;
- Evidence Atlas or Library Registry entries;
- architecture status, public architecture explanation or the Master Visual;
- cross-repository links, versions, commit identities or release references;
- a provenance or reproducibility chain;
- a public capability, Research or Application statement;
- a Source Repository status represented by NEXAH; or
- an existing public statement made stale by the result.

No handoff is needed for unfinished exploration, local notes, internal
intermediate work, tests without a closed finding, historical material without
current status effect, or a result explicitly classified
`NO_PUBLIC_OR_REPOSITORY_IMPACT`.

## Required intake

Use one bounded handoff with at least these fields:

```yaml
source_desk:
source_repository:
source_authority:
result_id:
result_status:
immutable_source:
source_revision_or_hash:
bounded_claim:
explicit_limits:
adoption_state:
affected_public_surfaces:
proposed_treatment:
owner_review_required:
```

`immutable_source` must be a repository-addressable path, release, tag, commit,
manifest or stable external citation. A local filename without repository
identity is not sufficient for a public update.

Use existing treatment vocabulary:

`NO_UPDATE_REQUIRED` · `CURRENTNESS_SYNC` · `EVIDENCE_ATLAS_CANDIDATE` ·
`ARCHITECTURE_CANDIDATE` · `PUBLICATION_REVIEW_REQUIRED` ·
`PROVENANCE_UPDATE` · `NEGATIVE_EVIDENCE` · `NOT_ADOPTED` ·
`HISTORICAL_ONLY` · `OWNER_REVIEW_REQUIRED`

The proposed treatment is an intake signal, not a disposition or authority
grant.

## Steward processing contract

For each accepted handoff, Desk 03:

1. verifies Source Authority and immutable source identity;
2. preserves the source's bounded claim, limits and adoption state;
3. identifies exact public or canonical targets;
4. checks Constitution, Framework, OLS and repository authority boundaries;
5. routes the result to the existing architecture update queue, Evidence Atlas
   Update Queue, Library review/Registry path, publication owner, or
   `NO_UPDATE_REQUIRED`;
6. assigns exactly one primary disposition;
7. escalates only a genuine meaning, identity, authority or Adoption decision;
8. performs only separately authorized, bounded repository changes;
9. verifies links, hashes, versions, status wording and drift; and
10. returns `CURRENT`, `NO_UPDATE_REQUIRED` or one exact residual finding to
    Mission Control.

Desk 03 does not reassess scientific validity, certify ORION, decide product or
portfolio state, authorize publication, or promote Research into Architecture.

## Queue routing

| Finding | Existing destination |
|---|---|
| Architecture, authority or cross-repository currentness | Existing EASL row and single UQ queue in the Architecture Status Ledger |
| Bounded evidence candidate | [Evidence Atlas Update Queue](../docs/evidence/EVIDENCE_ATLAS_UPDATE_QUEUE.md) |
| Library Work, Edition, metadata or curated relation | Existing Library Registry/review path |
| Public release or deployment claim | Owning release/publication surface; Desk 03 records only the repository projection need |
| No public or repository effect | `NO_UPDATE_REQUIRED`; no queue entry |
| Meaning, identity, Adoption or unresolved authority conflict | `OWNER_REVIEW_REQUIRED` and return through Mission Control |

One result may require several target checks, but it receives one coherent
changeset and one primary disposition. A green state in one repository cannot
mark another repository current.

## Batch and cadence rule

Normal handoffs collect in the existing queue and are processed in bounded
maintenance batches. There is no immediate-response requirement and no new
Power Session per result.

- Process at most one coherent changeset per queue entry.
- Run a batch when a coherent target set is ready, before a relevant release or
  public architecture publication, or when a public statement requires repair.
- Treat an active authority contradiction, false public capability claim or
  broken immutable release identity as an immediate fail-closed finding.
- Retain the existing quarterly lightweight architecture-drift hygiene check.
- A completed batch does not activate the next batch or downstream work.

## Repo-sync done condition

A repository sync is complete only when:

1. Source Authority, immutable source and revision/hash are verified;
2. bounded claim, explicit limits and Adoption state are preserved;
3. every affected target has one recorded treatment;
4. any required Owner decision and repository authorization are recorded;
5. the authorized diff contains no claim expansion or authority transfer;
6. links, versions, hashes and status wording pass verification;
7. the existing ledger/queue is updated, or `NO_UPDATE_REQUIRED` is recorded;
8. remaining uncertainty is one exact owned finding with a return trigger; and
9. Mission Control receives the result without an automatic ticket or project
   activation.

## Current queue reconciliation — 2026-08-20

| Item | Classification | Current finding | Treatment |
|---|---|---|---|
| `UQ-004 / EASL-011` | `EXISTING_NEEDS_CURRENTNESS_SYNC` | The two-file NEXAH status transcription exists on review branch commit `6da37e76…`, is absent from current `main`, and predates D-021–D-025. | Keep `REVIEW_REQUIRED`. Rebuild the bounded status sync from current `main`; do not merge the old transcription without re-review. |
| `UQ-005 / EASL-009` | `EXISTING_AND_CURRENT` | Master Visual V1 and its manifest are versioned. Only the abbreviated historical ledger reference remains non-reconstructible. | Preserve `REVIEW_REQUIRED` as a bounded historical traceability finding. No currentness update unless a reconstructible immutable reference and separate authorization exist. |
| `UQ-006 / EASL-006, EASL-013` | `EXISTING_NEEDS_CURRENTNESS_SYNC` | The continuity package is now tracked and remote-durable through the Science Lab maintenance branch; the Phase 4B package remains untracked. The queue wording still groups both as uncommitted. | Science Lab ledger owner must prospectively split the resolved durability fact from the remaining Phase 4B finding. No NEXAH content change follows. |
| `EAQ-003` | `EXISTING_NEEDS_CURRENTNESS_SYNC` | D-021 retains the IEEE work as an unnumbered, non-activated Candidate; it is not Application 01. | Correct the queue projection prospectively; preserve all IEEE evidence and keep Atlas admission subject to source and owner review. |
| `D-022` | `NO_UPDATE_REQUIRED` | ORION Research Session remains a Candidate without Application ID and is not represented as an active NEXAH product in current public NEXAH pages. | Recheck only if a public surface claims activation or an Application ID. |
| `D-023` | `CURRENTNESS_SYNC` | Runtime 1.1 is `HOLD_UNTIL · NOT_ADOPTED · NOT_RELEASE_READY · NOT_PUBLICLY_CLAIMABLE`. Current NEXAH already excludes Runtime from Certified Core but lacks the later controlling hold in its compact status projection. | Include a bounded pointer in the next UQ-004 reader-baseline sync; do not alter ORION authority. |
| `D-024` | `NO_UPDATE_REQUIRED` | The certified ORION pin remains `d34fbb2…`; no NEXAH or frozen dependency change is required. | Preserve exact pin and fail-closed behavior. |
| `D-025 / APP-01-H1` | `NO_UPDATE_REQUIRED` for capability/public claims | H1 is `READY` for Desk acceptance, not active implementation and not a public capability. | A later completed H1 result must use this intake if it affects Applications, Evidence Atlas, Framework/OLS or public navigation. |
| `P1 / MC-001` | `NO_UPDATE_REQUIRED` | Closed under `REPORTED_EVENTS_ONLY`; no public scientific, capability or product claim follows. | Mission Control retains the operational record. |

Historical source reports remain unchanged. Corrections are prospective status
projections and pointers only.

## Return record

Return the result to Mission Control with:

```yaml
result_id:
primary_disposition:
targets_checked:
repository_change:
verification:
remaining_finding:
finding_owner:
return_trigger:
mission_control_action:
```

`mission_control_action` may request pointer/status synchronization. It does not
create or activate a ticket unless Mission Control already has that authority.
