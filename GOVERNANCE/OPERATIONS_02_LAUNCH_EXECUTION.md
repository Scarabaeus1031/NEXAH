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
- [ ] Repository-wide license is approved and added. **Owner confirmation
  required; no license is inferred from NEXAH or ORION.**
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
- [ ] Repository-wide license is approved and added. **Owner confirmation
  required.**
- [ ] Public GitHub repository and remote are established. **GitHub permission
  required.**
- [ ] ORION working tree is consolidated into a reviewed immutable baseline.
- [ ] Core compatibility is verified either against the existing detached pin
  or through an explicitly approved new compatibility record.
- [ ] Development Release Gate passes from a clean working tree.

**Core mismatch:** `workspace.yaml` pins
`9f79bb06210402c40c9ef7d9937ca00d86c092b1`. The connected NEXAH checkout is
now at `6ac32ec481e8932fd388fef1dd2dc2cfd2529117`. The newer commit contains
Framework/publication and Governance evolution; it is not automatically an
approved ORION Core baseline. Operations has not changed the pin.

**Package result:** documentation complete; compatibility, license, public
identity and clean baseline remain blocking.

### Package F — Framework Publication

- [x] Adopted Governance baseline is public on `main`.
- [x] Architecture and Library documents reference the adopted Constitution.
- [x] Root README explains Framework, OLS, Kernel, Research and Library
  responsibilities.
- [x] Software and documentation license scopes are explicit.
- [x] Release and version history is clarified without changing tags.
- [x] Local full test suite passes: 302 tests.
- [x] Public smoke jobs for Python 3.10, 3.11 and 3.12 passed on commit
  `829c8684947d8798136b4819afc394cd5a829e54`.
- [ ] Public full CI suite is green on the current launch candidate. The
  previous run failed in the repository test step; a new run for
  `6ac32ec481e8932fd388fef1dd2dc2cfd2529117` is pending verification.
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

## Remaining Owner Actions

The owner must confirm:

1. **License for ORION:** approve a repository-wide code license and any
   separate documentation/content license.
2. **License for Experience:** approve a repository-wide code license and any
   separate editorial/assets license.
3. **Framework release identity:** name and version of the next public
   Framework baseline.
4. **ORION Core compatibility:** keep the original `9f79bb…` pin for the first
   publication or approve verification and a compatibility record for a newer
   NEXAH revision.
5. **Legal facts:** applicable USt-IdNr./W-IdNr., current register data and
   whether a data protection officer exists.
6. **Historical repositories:** approve archive status, historical banners,
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
- update profile pins and historical repository status;
- publish approved tags/releases only after their gates pass.

## Final Launch Status

### HOLD

The public Governance baseline is now present and local publication preparation
has advanced. Launch remains blocked by:

- unconfirmed licenses for ORION and Experience;
- missing public ORION and Experience repository identities;
- unresolved ORION Core compatibility and non-clean ORION baseline;
- public Framework CI not yet green on the current candidate;
- stale public GitHub metadata and historical pins;
- unresolved domain/TLS/hosting state;
- incomplete legal hosting and owner confirmations; and
- absence of a production smoke test.

The next transition is operational, not architectural. Once the owner decisions
and external credentials are available, this same checklist continues; no new
review is required.
