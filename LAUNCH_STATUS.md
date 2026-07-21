# NEXAH Launch Status

**Control:** Launch Control 01

**Date:** 21 July 2026

**Status:** **HOLD — local execution complete; external authority required**

This is the concise operational handoff for the first public launch. It applies
the adopted Constitution and Governance without changing them. Detailed
history remains in `GOVERNANCE/OPERATIONS_01_PUBLIC_LAUNCH_PREPARATION.md` and
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
  `18d8a454842c8f25301ca4d3118f7ad903de55a2`; executable work entered at
  `0a9c031e3d71b75abd007e12b493acc93d8e4cc8` and was not changed afterwards.
- ORION tests pass: 75 tests, one optional Ollama integration test skipped.
- ORION `18d8a45…` plus unchanged Core pin
  `9f79bb06210402c40c9ef7d9937ca00d86c092b1` passes the complete Development
  Release Gate in an isolated clean workspace.
- Experience is consolidated locally at publication baseline commit
  `a1e031cb51978ca1207851cc7f292a4a5c37b115`; its executable alpha entered at
  `28d099c89a109a58385335652c394242ebea278d` and was not changed afterwards.
- Experience verification passes: Astro reports no diagnostics, 53 tests pass,
  195 pages build, and the internal-link check finds no broken links.
- Experience deployment inputs, artifact boundary and production smoke test
  are prepared in `docs/DEPLOYMENT_READINESS.md`.
- Security, contribution, conduct, publication baseline, pull-request guidance
  and reviewable repository metadata are prepared wherever locally possible.
- No architecture, Governance, semantic contract, runtime authority or Core
  pin was changed.

## Waiting for Owner

1. Approve the repository-wide ORION license and any separate documentation
   license.
2. Approve the Experience code license and the license scope for original
   editorial content and assets.
3. Assign the next Framework release name and tag. Existing tags remain
   historical and must not be reused.
4. Approve publication of ORION with the already verified Core pin `9f79bb…`,
   or explicitly request a separate qualification of a newer Framework commit.
5. Confirm whether Haptikdesign GmbH has a publishable USt-IdNr. or W-IdNr. and
   whether a Datenschutzbeauftragter is appointed.
6. Confirm historical-repository archive status, licensing, banners and removal
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
2. Create or confirm the public ORION and Experience repositories, visibility
   and remotes.
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

- owner decisions above are recorded and legal placeholders are resolved;
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

**Owner: approve the ORION and Experience licensing scopes.**

This is the first action because public repository creation, contribution and
deployment must not proceed with an intentionally unresolved license.
