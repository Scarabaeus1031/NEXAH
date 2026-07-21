# OPERATIONS 02 — Launch Execution

**Opened:** 21 July 2026

**Status:** **HOLD — operational execution in progress**

**Authority:** Operations applies the adopted P0 checklist. It does not change
Constitution, Governance, Architecture or semantics.

This is the single living operational source of truth until the first public
launch. Items are checked only after verification. A locally completed item is
not described as publicly complete until its public state is observable.

## Launch Checklist

### Package A — Public Governance

- [x] Constitution v1.0 is committed to the canonical NEXAH repository.
- [x] Governance Index is committed and identifies Constitution v1.0 as the
  highest governance document.
- [x] Constitution Adoption Report is committed.
- [x] Root README and Architecture/Library references point to the adopted
  Constitution.
- [x] Earlier constitutional investigation and review report are explicitly
  historical and non-canonical.
- [x] Public remote `main` contains commit
  `6ac32ec481e8932fd388fef1dd2dc2cfd2529117` with the adopted governance
  baseline.
- [ ] The local Operations documentation series beginning with
  `1de5c4b6a4e2804009b0c599624b0f809cc7997f` is published. Local `main` is
  ahead of `origin/main`; publishing requires explicit GitHub authorization.

**Package result:** complete.

### Package B — Repository Health

- [x] NEXAH README references the Constitution and Governance Index.
- [x] NEXAH README distinguishes the six repository subsystems from
  constitutional Houses.
- [x] ORION README references the Constitution and states its navigation
  boundary.
- [x] Experience README references the Constitution and states its
  presentation boundary.
- [x] Documentation hierarchy is stated consistently as Constitution →
  Governance → Architecture → repository documentation → implementation →
  derived artifacts.
- [x] Framework release/version explanation is linked from the root README.
- [x] ORION publication status and Core mismatch are documented.
- [x] Experience publication status and reproducible build contract are
  documented.
- [x] Reviewable GitHub metadata values are prepared in each active repository.
- [ ] Public GitHub descriptions, homepage fields, topics and profile pins are
  synchronized. **Blocked by GitHub permission.**
- [ ] Public ORION and Experience repository cross-links are added. **Blocked
  until their public repository identities exist.**

**Package result:** locally complete; public metadata remains external.

### Package C — Version Consistency

- [x] Framework implementation version `0.7.0` is identified as the current
  Python/Kernel track, not an ecosystem version.
- [x] Historical tags `v0.5`, `v0.5.0` and `v1.0.0` are preserved and explained
  without rewriting them.
- [x] Constitution v1.0 is separated from Framework, Kernel, ORION and
  Experience versions.
- [x] Existing public “Research Prototype Release” is identified as historical.
- [x] Requirements for the next Framework baseline are documented.
- [ ] Name and version of the next Framework release are approved by the
  release owner. **Owner confirmation required.**

**Package result:** history clarified; future release identity remains an owner
decision.

### Package D — Experience Publication

- [x] README states responsibility, pre-release status and public references.
- [x] Contribution boundary is documented.
- [x] Security reporting policy is documented.
- [x] Build requirements and the external ORION dependency are documented.
- [x] Generated ORION report provenance includes ORION version and source
  digest.
- [x] Local `pnpm verify` gate is defined.
- [x] Experience is consolidated in local publication baseline commit
  `66ea7eb4d0799baffd75392d0d28f3878e72ed50` (executable alpha:
  `28d099c89a109a58385335652c394242ebea278d`).
- [x] Apache 2.0 software and CC BY 4.0 original-content scopes are approved
  and recorded.
- [x] Public repository identity `NEXAH-Experience` is approved.
- [ ] Public GitHub repository and remote are established. **GitHub permission
  required.**
- [ ] Immutable ORION input revision is recorded. **Blocked by ORION baseline.**
- [ ] Public CI is enabled and green. **Blocked by public ORION source and
  GitHub repository identity.**
- [ ] Canonical host and production deployment are verified. **Blocked by
  Domain/TLS/hosting actions.**

**Package result:** local publication candidate prepared; not publicly
releasable.

### Package E — ORION Publication

- [x] README states architecture status, scope and non-capabilities.
- [x] Constitution and repository ownership references are present.
- [x] Security reporting policy is documented.
- [x] Publication baseline and exact Release Gate conditions are documented.
- [x] Core mismatch is explained without weakening the Release Gate.
- [x] ORION remains `0.3.0-dev.0`; no stable release is claimed.
- [x] Apache 2.0 software and CC BY 4.0 original-content scopes are approved
  and recorded.
- [x] Public repository identity `NEXAH-ORION` is approved.
- [ ] Public GitHub repository and remote are established. **GitHub permission
  required.**
- [x] ORION working tree is consolidated into local publication baseline commit
  `b86b641aee2e284da12427e4f77c822a3abd0a27` (executable baseline:
  `0a9c031e3d71b75abd007e12b493acc93d8e4cc8`).
- [x] Core compatibility is verified against the existing unchanged detached
  pin.
- [x] Development Release Gate passes in an isolated clean workspace containing
  ORION `b86b641…` and Core `9f79bb…`.

**Core mismatch:** `workspace.yaml` pins
`9f79bb06210402c40c9ef7d9937ca00d86c092b1`. The connected clean NEXAH
checkout is on the newer local Operations series. It therefore differs from
the approved ORION Core baseline. The newer commits contain publication and
Governance work; Operations has not changed the pin.

**Package result:** local baseline, licensing, repository identity and
configured-pin compatibility complete; public remote and owner adoption remain
blocking.

### Package F — Framework Publication

- [x] Adopted Governance baseline is public on `main`.
- [x] Architecture and Library documents reference the adopted Constitution.
- [x] Root README explains Framework, OLS, Kernel, Research and Library
  responsibilities.
- [x] Software and documentation license scopes are explicit.
- [x] Release and version history is clarified without changing tags.
- [x] Unnamed release notes, compatibility summary, reproducibility evidence
  and artifact inventory are prepared.
- [x] Local full test suite passes: 302 tests.
- [x] Public smoke jobs for Python 3.10, 3.11 and 3.12 passed on public commit
  `6ac32ec481e8932fd388fef1dd2dc2cfd2529117`.
- [ ] Public full CI suite is green on the current launch candidate. The
  repository test job for public commit `6ac32ec…` failed after 49 minutes 26
  seconds in `Run repository tests`; anonymous access does not expose the
  failing test log. Local launch commits have not been authorized for push.
- [ ] GitHub homepage field is corrected; its current target is stale.
  **GitHub permission required.**
- [ ] GitHub description and topics reflect the current Framework role.
  **GitHub permission required.**
- [ ] Next Framework release identity is approved. **Owner confirmation
  required.**

**Package result:** source and governance locally ready; public CI and metadata
remain blocking.

### Package G — Historical Repositories

Canonical classification:

| Repository | Classification | Public launch treatment |
|---|---|---|
| `Scarabaeus1031/NEXAH` | **Current** | Canonical public Framework/Governance entry after P0 closure |
| `Scarabaeus1033/NEXAH-CODEX` | **Historical research** | Preserve; add historical banner and remove from canonical launch pins |
| `Scarabaeus1031/Scarabaeus1033-Archive` | **Archive** | Preserve; mark GitHub repository archived after owner confirmation |
| `Scarabaeus1033/Scarabaeus1033-System-v1.0` | **Archive** | Preserve existing archived state; do not present as current architecture |

- [x] Current, Historical and Archive classifications are recorded
  canonically here.
- [x] No history, repository or artifact was deleted or rewritten.
- [ ] Historical banner is added to `NEXAH-CODEX`. **GitHub/repository
  permission required.**
- [ ] `Scarabaeus1033-Archive` is marked archived. **Owner confirmation and
  GitHub permission required.**
- [ ] Personal profile pins show only canonical current repositories.
  **GitHub permission required.**
- [ ] License/provenance of historical public repositories is confirmed.
  **Owner confirmation required.**

Recommended banner text for historical repositories:

> **Historical NEXAH material.** This repository preserves an earlier research
> state. It is not the current NEXAH Framework, ORION architecture or Ecosystem
> Constitution. Begin with the canonical NEXAH repository.

**Package result:** classification complete; public repository presentation
remains external.

### Package H — Launch Gate

- [x] One living operational checklist exists.
- [x] Constitution published.
- [x] Governance synchronized in the current NEXAH repository.
- [x] Framework version history clarified.
- [x] Experience local publication boundary documented.
- [x] ORION local publication boundary documented.
- [x] Historical repository classification recorded.
- [ ] Framework current CI green.
- [ ] Framework public metadata verified.
- [ ] ORION public baseline ready.
- [ ] Experience public baseline ready.
- [ ] Domain verified.
- [ ] TLS verified.
- [ ] Legal information confirmed.
- [ ] Hosting facts confirmed.
- [ ] Public cross-links verified.
- [ ] Production smoke test completed.
- [ ] **GO**.

## Completed Work

1. Adopted Governance is committed and observable on public NEXAH `main`.
2. Historical constitutional reviews remain preserved and clearly subordinate.
3. Framework release signals are explained in `RELEASES.md` without tag or
   history mutation.
4. Experience now contains a contribution boundary, security policy,
   publication baseline and explicit license status.
5. ORION now contains a security policy and a publication baseline describing
   its exact Core mismatch and valid resolution paths.
6. Current, Historical and Archive repository classes are recorded.
7. No architecture, contract, runtime behavior, evidence or semantics changed.
8. Local Framework verification passed with 302 tests; Experience verification
   passed with 53 tests and 195 generated pages; ORION tests passed and its
   workspace check now reports only the exact Core revision mismatch.
9. ORION and Experience are consolidated into local immutable commits.
10. ORION's unchanged configured Core pin passes the complete Development
    Release Gate in an isolated clean workspace.
11. GitHub metadata values, Framework release material and Experience
    deployment handoff are prepared for immediate external execution.

## Remaining Owner Actions

The owner must confirm:

1. **Framework release identity:** name and version of the next public
   Framework baseline.
2. **ORION Core adoption:** approve the successfully verified original
   `9f79bb…` pin for the first publication, or explicitly request qualification
   of a newer NEXAH revision.
3. **Legal facts:** applicable USt-IdNr./W-IdNr., current register data and
   whether a data protection officer exists.
4. **Historical repositories:** approve archive status, historical banners,
   license treatment and removal from profile pins.

## Remaining External Actions

### DNS, TLS and hosting

- choose `nexah.de` or `www.nexah.de` as canonical host;
- issue a valid certificate covering the required hosts;
- redirect the non-canonical host permanently;
- provide hosting company, server location, recipient categories and exact
  server-log retention period;
- deploy the immutable Experience baseline;
- run the production metadata, legal-navigation and link smoke test.

### GitHub permissions

- create or confirm public ORION and Experience repositories;
- configure remotes and public metadata;
- correct NEXAH homepage, description and topics;
- configure public CI and required checks;
- provide authorized access to the failed public test log or supply its exact
  failing test output before any CI-specific change is attempted;
- authorize publication of the local Operations commit series (no force-push
  is required; local `main` is directly ahead of public `main`);
- update profile pins and historical repository status;
- publish approved tags/releases only after their gates pass.

## Final Launch Status

### HOLD

The public Governance baseline is now present and local publication preparation
has advanced. Launch remains blocked by:

- missing public repositories and remotes for the approved identities
  `NEXAH-ORION` and `NEXAH-Experience`;
- owner adoption of the verified ORION/Core pair;
- public Framework CI not yet green on the current candidate;
- stale public GitHub metadata and historical pins;
- unresolved domain/TLS/hosting state;
- incomplete legal hosting and owner confirmations; and
- absence of a production smoke test.

The next transition is operational, not architectural. Once the owner decisions
and external credentials are available, this same checklist continues; no new
review is required.
