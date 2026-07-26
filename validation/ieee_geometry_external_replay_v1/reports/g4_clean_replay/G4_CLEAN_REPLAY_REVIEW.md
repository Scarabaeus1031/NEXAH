# G4 clean-environment replay review

## Classification

**G4: FAILED**

The clean replay completed, but the freshly generated canonical IEEE-14 result
did not reproduce the frozen canonical result. The first runner summary called
the run passed because it checked only six invariant checks and independent
operator equivalence. That classification was too weak and is superseded by
`g4_review_classification.json`. The raw first-run evidence is preserved
unchanged.

No scientific protocol, frozen source, case role, parameter, claim, or test was
changed in response. No second scientific run was performed.

## Entry verification

- Approved G2 protocol SHA-256:
  `bd9d0fa2094b17333b18ec7621f33fd32271c2e759f2b01c9b27f76702ffe5ba`
- G3 classification: `G3_equivalence_passed`
- G3 discrepancies: IEEE-9 `0`; IEEE-14 `0`
- Baseline and replay revision:
  `d3a19138b96aa07dfd623bdebb1003cb02cc60e8`
- Frozen files before replay: `15/15` match
- Clean checkout before replay: yes
- Entry result: all fixed G4 entry checks passed

## Exact environment and route

- CPython 3.12.7
- macOS 26.5.2, Darwin 25.5.0, arm64
- Isolated copied virtual environment: yes
- NEXAH 0.7.0
- NumPy 1.26.4
- pandas 2.3.3
- pandapower 3.4.0
- SciPy 1.13.1
- pytest 7.4.4
- `pip check`: exit 0, no broken requirements
- Replay network state: `PIP_NO_INDEX=1`
- Clean source:
  `/private/tmp/nexah-sr1-g4.tCdR3H/source`
- Disposable output:
  `/private/tmp/nexah-sr1-g4.tCdR3H/g4-review`

The complete package lock and NumPy BLAS/LAPACK configuration are in
`raw/environment_identity.json`.

## Command results

1. **IEEE-9 development replay** — exit `0`, 0.040 s.
   Nineteen campaign positions reproduced with zero discrepancies. The failed
   frames at load scales `2.3` and `2.4` remain explicit, with
   `system_features: null` and zero entity views. No comparator output.

2. **Protocol-hash refusal control** — exit `2`, 0.033 s, expected refusal.
   A byte-altered protocol was rejected with `approved protocol SHA-256
   mismatch`; the record confirms `evaluation_source_loaded: false`. No
   comparator output.

3. **Explicit IEEE-14 evaluation replay** — exit `0`, 55.069 s.
   The approved protocol hash was verified before evaluation load. The
   independent sidecar geometry comparison against the frozen artifact had zero
   discrepancies across 19 positions. No comparator output. However, the
   canonical fresh-source replay set `gate_passed: false`, so this command does
   not satisfy G4.

4. **Frozen V1 tests** — exit `0`, 20.889 s: `2 passed`.

## Discrepancies and negative findings

The fresh canonical report differs from the frozen canonical report:

| Field/check | Frozen reference | Clean replay |
|---|---|---|
| `evaluation-source-replay` | `true` | `false` |
| `evaluation-geometry-replay` | `true` | `false` |
| `evaluation-report-replay` | `true` | `false` |
| `frames_sha256` | `467530…e59219` | `0383a1…ac186` |
| `geometry_sha256` | `ab49aa…f72729` | `d84a1b…cd38` |
| `orientation_sha256` | `2faa1f…ad2b` | `4ab908…5d299` |
| `total_path_length` | `5.55378709510072` | `5.553787095100708` |
| `gate_passed` | `true` | `false` |

Consequently, four claim-audit entries change from
`supported_within_manifest` to `not_supported_by_failed_gate`.

Warnings preserved from stderr:

- Matplotlib used a temporary cache because the default cache path was not
  writable.
- pandapower reported that numba was unavailable and used the slower execution
  route.

These warnings were not repaired or suppressed. IEEE-14 had no failed frames.
IEEE-9 retained its two declared solver boundaries and null payloads.

## Reader-only route

A reader **cannot yet complete this route from the public baseline checkout
alone**, because the G4 sidecar is deliberately uncommitted pending review.
Using the review-candidate sidecar plus the clean baseline checkout, the full
route required no manual data edit, no undocumented command, and no network
during replay. This distinction is preserved rather than treating an
uncommitted candidate as public repository documentation.

## Frozen-source and scope verification

- Frozen files after replay: `15/15` byte-identical.
- Clean checkout after replay: no tracked or untracked changes.
- Original repository frozen files after evidence copy: `15/15` byte-identical.
- Comparator results generated: no.
- Combined score generated: no.
- Post-hoc metric added: no.
- Canonical V1 source changed: no.
- G5 begun: no.
- G6 begun: no.
- Commit created: no.

## Raw artifact hashes

| Artifact under `raw/` | SHA-256 |
|---|---|
| `artifact_hashes.json` | `d333b47cc12e093fd1eb7fb445fc76bfa84a9393d1e99e3757bbc0933871e308` |
| `development/development_replay.json` | `c9a896265c8aa915625aa54eb9417db3e6092a843a81f7786bbb3cd9c64cb01a` |
| `entry_verification.json` | `14926b120c8a742e80a28c2e2965655881cabb83074662f67ce59298fde440c6` |
| `environment_identity.json` | `f4a4b5c7150ce865ea5abc03a4da31ffbf2b5b49a350d7801ea0d90eba7f65ad` |
| `evaluation/canonical_replay.json` | `1622acd09fa6772b6030724db08f9e9bc9a146e2686843f8a32832b1d948db1e` |
| `evaluation/evaluation_replay.json` | `d826dcd6a2d3c71729b31fd7557a214fc0f677e4a9a2dac376718ca8940fa90f` |
| `frozen_hashes_after.json` | `d664b32222c2d8edcfeb9e1763adbcb07da26118cf7aac367024dee25693f555` |
| `frozen_hashes_before.json` | `d664b32222c2d8edcfeb9e1763adbcb07da26118cf7aac367024dee25693f555` |
| `g4_result.json` | `783f6fcd69b7c1300bf6ba8989f8b8760f085e500c7fc821c29b6f397bfeec87` |
| `protocol_hash_refusal_control/g2_protocol_byte_altered.json` | `7796144c16fc9c4fc88d7dfabbb42113cf76e7c0655f7776e5317d4d579e8cbc` |
| `protocol_hash_refusal_control/result/evaluation_replay.json` | `7c4420448ac95e2e4f1f1a976d75d9983b734ff5f469fa842f6e819d4d3ed27a` |

This review package is the G4 stopping point.

