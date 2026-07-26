# SR-1 Change Ledger

## 2026-07-26 — G0

- SR-1 implementation plan approved.
- Required G2 protocol SHA-256 control accepted.
- Required IEEE-9 development / IEEE-14 evaluation command separation accepted.

## 2026-07-26 — G1

- Verified clean source worktree at revision
  `d3a19138b96aa07dfd623bdebb1003cb02cc60e8`.
- Ran unchanged V1 canonical gate into `/private/tmp`.
- Ran existing V1 validation test: 2 passed.
- Recorded hashes and reference environment.
- Added only SR-1 sidecar identity, ownership, environment and G1 evidence
  records.
- Added no comparator, analysis protocol, independent operator implementation
  or IEEE-14 comparator output.
- Stopped before G2.

## 2026-07-26 — G2 candidate

- Defined four Tier 0 comparators, source scopes, units, scaling, angle,
  missingness, tolerance, tie and ranking rules.
- Added IEEE-9-only manually checkable fixtures.
- Omitted Tier 1 because it requires solver internals outside the stable public
  Pandapower interface.
- Defined predeclared comparison, null, ambiguity and contradiction handling.
- Defined candidate SHA-256 and future approval-binding mechanism.
- Bound the canonical candidate bytes to SHA-256
  `bd9d0fa2094b17333b18ec7621f33fd32271c2e759f2b01c9b27f76702ffe5ba`
  for review; no approval record exists yet.
- Defined mandatory technical separation of future IEEE-9 development and
  IEEE-14 evaluation commands.
- Did not add comparator implementation or access new IEEE-14 comparator
  output.
- Did not begin G3 or G4.
- Stopped for G2 review without committing.

## 2026-07-26 — G2 approved

- Bound exact candidate bytes unchanged as `g2_protocol_approved.json`.
- Verified approved protocol ID `sr1-ieee-geometry-comparator-analysis-v1`,
  version `1.0.0`, and SHA-256
  `bd9d0fa2094b17333b18ec7621f33fd32271c2e759f2b01c9b27f76702ffe5ba`.
- Added the immutable approval record with Thomas Hofmann / NEXAH as approving
  authority.
- Preserved the explicit prohibition on IEEE-14 Comparator evaluation.

## 2026-07-26 — G3

- Froze the operator-equivalence contract before comparison.
- Implemented all six operators from the manifest formulas and public artifact
  contract without production-operator imports or copied production code.
- Fit IEEE-9 population standardisation once and applied it unchanged to
  IEEE-14.
- Ran IEEE-9 first: 19 positions, 18 steps, 17 turns, two failure boundaries,
  zero discrepancies.
- Loaded and compared the existing frozen IEEE-14 Geometry target only after
  IEEE-9 passed: 19 positions, 18 steps, 17 turns, zero boundaries, zero
  discrepancies.
- Preserved the initial sidecar-test collection path failure, corrected only the
  test repository-root calculation, and passed the final six-test suite.
- Verified all 15 frozen hashes before and after G3.
- Generated no Comparator output, changed no frozen V1 source, began no G4 work,
  and created no commit.
- Classification: `G3_equivalence_passed`.

## 2026-07-26 — G4

- Fixed the G4 entry, command, artifact and stop contract before execution.
- Created a fresh checkout at
  `d3a19138b96aa07dfd623bdebb1003cb02cc60e8`.
- Created an isolated CPython 3.12.7 environment matching the G1 core package
  versions and recorded its full package lock and BLAS/LAPACK identity.
- Verified the approved G2 SHA-256, accepted G3 result, all 15 frozen hashes,
  clean checkout and exact revision before replay.
- Ran IEEE-9 development separately and preserved both failed frames, null
  payloads and solver-boundary records.
- Proved that a byte-altered G2 protocol is rejected before IEEE-14 source load.
- Ran IEEE-14 only through the explicit, hash-gated evaluation command.
- Preserved the clean canonical replay discrepancy: three evaluation replay
  checks failed; three generated artifact hashes changed; total path length
  differed at floating precision; canonical `gate_passed` became false.
- Ran the unchanged frozen V1 test: 2 passed.
- Verified all 15 frozen hashes after replay and a clean source checkout.
- Superseded the initially too-weak runner classification with
  `G4_clean_replay_failed`; tightened the runner to require the complete
  canonical gate and exact canonical report on future use.
- Generated no Comparator output, changed no canonical V1 source, began no G5
  or G6 work, contacted no external party, and created no commit.

## 2026-07-26 — G4 root-cause analysis

- Compared only frozen artifacts, preserved first-run G4 evidence, environment
  records, repository history and existing source.
- Located the earliest observable divergence at the fresh IEEE-14 campaign
  equality check, before geometry and Orientation derivation.
- Inventoried every retained summary difference and calculated the sole
  retained numeric difference as 14 ULP.
- Recorded that the first differing frame, entity and field cannot be recovered
  because the fresh intermediate payloads were not preserved.
- Classified the root cause as `E — unresolved`; environment-dependent
  floating-point computation remains plausible but unproved.
- Performed no IEEE-9 or IEEE-14 replay, created no Comparator result, changed
  no frozen or approved artifact, began no G5/G6 work, and created no commit.
