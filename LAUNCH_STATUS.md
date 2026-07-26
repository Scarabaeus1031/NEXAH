# NEXAH Launch Status

**Current-status review:** 26 July 2026

**Current classification:** **PUBLIC RESEARCH SURFACES LIVE — bounded
external-resonance test ready; integrated ORION service not claimed**

This section is the current operational handoff. The dated Launch Control 02
record below is preserved as historical execution evidence and no longer
describes the present public state.

## Current verified state

- **Framework:** NEXAH Framework 1.0 is frozen at annotated tag
  `framework-v1.0.0`, commit
  `87f438d05a8841166ea32719b9fda807acf5cb6b`. Later documentation does not move
  or alter that baseline.
- **Public repositories:** `NEXAH`, `NEXAH-ORION`, `NEXAH-Experience` and
  `NEXAHEDRON` exist publicly. Their versions and authority boundaries remain
  independent.
- **Public sites:** `https://nexah.de` and `https://nexahedron.com` are live.
  `nexah.de` is the public entry and Visitor Guide; NEXAHEDRON is the
  Human-facing reference implementation and a bounded development preview.
- **Experience:** the static public home is deployed. The exact source revision
  of the current `nexah.de` deployment has not been attested in the repository
  and remains explicitly unknown.
- **ORION Version 1:** the certified frozen Core is public at tag `v1.0.0`,
  commit `d34fbb2f99334534f4db89465a29f8bdb16d14d3`. Its certified responsibility
  runs from confirmed structural Representation through UNDERSTAND, Relations,
  Navigation, Orientation Map and Expression. Runtime, Gateway, applications,
  Human Reports, presentation, interpretation and decision-making are excluded
  from that certified baseline.
- **NEXAHEDRON Version 1 source:** the public source release is tagged
  `v1.0.0` at commit
  `cf21e8f03e6adde02245fbe077a827a367644c40`. Its repository contains a
  NEXAHEDRON-owned, fail-closed Consumer Seam to a separately governed
  Gateway path. That local seam is not a certified ORION Version 1
  responsibility.
- **Public ORION connection:** the currently deployed NEXAHEDRON preview has
  no configured `ORION_GATEWAY_URL`. It therefore offers a Human-owned
  Workspace and Orientation Record, not a public ORION-backed execution route.
- **Product boundary:** NEXAHEDRON is a reference implementation, not a
  production-complete product. Framework 1.0 is a bounded research baseline,
  not an ecosystem-wide product release.
- **Outreach:** Track A is prepared for a bounded Visitor Guide comprehension
  and resonance test. Preparation is not completed outreach: no participant
  selection, invitation or external contact is recorded by this status.

## Current unresolved operational facts

1. The deployed NEXAHEDRON site derives from precursor commit `f273ae5…`, not
   the tagged Version 1 source commit `cf21e8f…`; aligning them requires a
   separately authorised deployment.
2. NEXAHEDRON apex and `www` canonical-host behavior is not yet attested as one
   permanent redirect.
3. The exact deployed `nexah.de` source revision is not recorded.
4. A production ORION transport is not configured and is not required for the
   current Track A Visitor Guide test.

## Current entry route

```text
https://nexah.de
→ https://nexah.de/visitor-guide/
→ optional Library or one pinned GitHub object
```

This route tests whether the public problem and authority boundaries are
understood. It does not test product value, scientific validity or an
ORION-backed NEXAHEDRON workflow.

---

## Preserved historical handoff — Launch Control 02

**Control:** Launch Control 02

**Date:** 22 July 2026

**Status:** **HOLD — local execution complete; external authority required**

This was the concise operational handoff for the first public launch at the
date above. It applies the adopted Constitution and Governance without changing
them. It is preserved for history and is superseded for current-state purposes
by the verified section above. Detailed history remains in
`GOVERNANCE/OPERATIONS_01_PUBLIC_LAUNCH_PREPARATION.md` and
`GOVERNANCE/OPERATIONS_02_LAUNCH_EXECUTION.md`.

## Completed

- Constitution v1.0, Governance Index and Adoption Report are public in the
  canonical NEXAH repository at public commit `6ac32ec…`.
- README, Governance references, repository boundaries and version history are
  consistent across Framework, ORION and Experience.
- The unnamed Framework candidate contains release scope, compatibility,
  verification, reproducibility and artifact inventory in
  `FRAMEWORK_RELEASE_CANDIDATE.md`.
- Framework local verification passes: 302 tests.
- Framework wheel preflight passes from a Git archive:
  `nexah-0.7.0-py3-none-any.whl`, 157918 bytes,
  SHA-256 `41128146de0c84ba20fa81761afd0b09abfc079f9bf00444bd64838663ba76e7`.
- ORION is consolidated locally. Its complete publication baseline is commit
  `b86b641aee2e284da12427e4f77c822a3abd0a27`; executable work entered at
  `0a9c031e3d71b75abd007e12b493acc93d8e4cc8` and was not changed afterwards.
- ORION tests pass: 75 tests, one optional Ollama integration test skipped.
- ORION `b86b641…` plus unchanged Core pin
  `9f79bb06210402c40c9ef7d9937ca00d86c092b1` passes the complete Development
  Release Gate in an isolated clean workspace.
- Experience is consolidated locally at publication baseline commit
  `66ea7eb4d0799baffd75392d0d28f3878e72ed50`; its executable alpha entered at
  `28d099c89a109a58385335652c394242ebea278d` and was not changed afterwards.
- Experience verification passes: Astro reports no diagnostics, 53 tests pass,
  195 pages build, and the internal-link check finds no broken links.
- Experience deployment inputs, artifact boundary and production smoke test
  are prepared in `docs/DEPLOYMENT_READINESS.md`.
- Security, contribution, conduct, publication baseline, pull-request guidance
  and reviewable repository metadata are prepared wherever locally possible.
- Software licensing is fixed as Apache 2.0 for Framework, ORION and
  Experience. Original documentation, specifications, research, books and
  visual material remain under CC BY 4.0 where applicable.
- Public repository identities are approved as `NEXAH`, `NEXAH-ORION` and
  `NEXAH-Experience`; no repository was renamed or created locally.
- No architecture, Governance, semantic contract, runtime authority or Core
  pin was changed.

## Waiting for Owner

1. Assign the next Framework release name and tag. Existing tags remain
   historical and must not be reused.
2. Approve publication of ORION with the already verified Core pin `9f79bb…`,
   or explicitly request a separate qualification of a newer Framework commit.
3. Confirm whether Haptikdesign GmbH has a publishable USt-IdNr. or W-IdNr. and
   whether a Datenschutzbeauftragter is appointed.
4. Confirm historical-repository archive status, licensing, banners and removal
   from canonical profile pins.

No other owner decision is currently known.

## Waiting for Infrastructure

1. Confirm `nexah.de` as the canonical host currently configured in Astro, or
   choose `www.nexah.de` before the final build.
2. Provide the hosting target and its required apex and WWW DNS records.
3. Configure DNS for both names without inventing A, AAAA or CNAME values.
4. Issue a certificate valid for both `nexah.de` and `www.nexah.de`.
5. Configure one permanent `301` or `308` redirect from the non-canonical host
   to the canonical HTTPS host.
6. Confirm hosting provider, server location, server-log recipients and exact
   retention period; publish those facts in Privacy.
7. Deploy `dist/` generated from the approved Experience and ORION commits and
   retain the prior immutable deployment as rollback target.
8. Run the prepared production smoke test covering HTTPS, redirect, primary
   rooms, legal pages, metadata, sitemap, contact delivery and absence of
   browser-to-ORION/provider traffic.

No DNS record, hosting endpoint or retention value has been guessed.

## Waiting for GitHub

1. Authorize a normal push of local NEXAH `main`; no force-push is required.
2. Create public repositories `NEXAH-ORION` and `NEXAH-Experience`, then
   configure their remotes without renaming either local repository.
3. Apply the prepared repository descriptions, topics, homepage fields and
   canonical profile pins from each `.github/REPOSITORY_METADATA.md`.
4. Add public CI after ORION's public immutable URL exists; Experience CI must
   consume that exact revision rather than a moving branch.
5. Provide authorized access to the failed NEXAH test-suite log, or supply its
   exact failing test output. Anonymous GitHub access exposes only exit code 1.
6. Add historical banners, archive the approved historical repository and
   remove historical repositories from canonical profile pins.
7. After the owner assigns a Framework release identity, push the final
   candidate, require green CI, create the approved tag and publish artifacts
   with SHA-256 checksums.

The public NEXAH CI run for commit `6ac32ec…` has successful Python 3.10, 3.11
and 3.12 smoke jobs. Its full test job failed after 49 minutes 26 seconds in
`Run repository tests`. Local execution passes 302 tests. No CI-specific change
will be guessed without the authorized failure log. A corrected result still
does not replace the required green run on the final candidate.

## GO Criteria

GO requires exactly these conditions:

- remaining owner decisions above are recorded and legal placeholders are
  resolved;
- local NEXAH commits and the approved ORION and Experience baselines are
  public under their confirmed repository identities and licenses;
- the owner-approved Framework release candidate has green public CI and an
  unambiguous release identity;
- repository metadata, historical banners and canonical pins are applied;
- one canonical HTTPS host works, the alternate host redirects permanently and
  the certificate covers both;
- verified Experience `dist/` is deployed with recorded immutable inputs; and
- the complete production smoke test passes.

Documentation, repository organization, Governance, Architecture and local
verification are no longer launch blockers.

## Immediate Next Action

**GitHub owner: create the public `NEXAH-ORION` and `NEXAH-Experience`
repositories.**

This is the first action because licensing and repository identities are now
settled, while remotes, public CI and immutable cross-links depend on those two
repositories existing.
