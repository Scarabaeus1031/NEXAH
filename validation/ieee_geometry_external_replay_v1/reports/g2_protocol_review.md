# G2 Protocol Review Record

Status: **candidate ready; G2 not yet passed**

Prepared: 2026-07-26

## Review object

- Protocol ID: `sr1-ieee-geometry-comparator-analysis-v1`
- Version: `1.0.0`
- Candidate:
  `validation/ieee_geometry_external_replay_v1/protocol/g2_protocol_candidate.json`
- Candidate SHA-256:
  `bd9d0fa2094b17333b18ec7621f33fd32271c2e759f2b01c9b27f76702ffe5ba`
- Byte convention: UTF-8, sorted JSON keys, two-space indentation, LF, one
  trailing LF, no non-finite JSON values

This is a candidate digest, not an approval record. No
`g2_protocol_approved.json` or `g2_approval_record.json` exists yet.

## Bounded decisions

1. Tier 0 contains only `v_min_pu`, `v_dev_rms_pu`, `l_max_percent`, and
   `angle_spread_degree`.
2. Bus scope is all stored bus rows. Line scope is all stored line rows and
   excludes transformers and other branch types.
3. Values retain pu, percent, and degree units. No comparator scaling or
   combined score is permitted.
4. Raw solver-reference angles are used without wrapping or unwrapping.
5. Failed or malformed frames yield null levels. Adjacent and centred measures
   never bridge a gap.
6. Numeric artifact checks use absolute tolerance `1e-12` plus relative
   tolerance `1e-10`.
7. Ties use that tolerance, average ranks, and tie-inclusive top-k boundaries.
8. Tier 1 is omitted because a Jacobian comparator would require Pandapower
   internals rather than a stable public high-level interface.
9. Analysis is descriptive, case-separated, null-inclusive, and has no
   performance or operational metric.
10. Future IEEE-9 development and IEEE-14 evaluation must be separate,
    case-restricted commands. Evaluation must verify an approved protocol hash
    before loading any IEEE-14 frame.

## IEEE-9 fixtures

The fixture bundle contains:

- complete raw input vectors and expected Tier 0 levels at campaign indices
  `0`, `4`, and `16`;
- signed adjacent changes from index `3` to `4`;
- the explicit failed-frame/null behavior at index `17`.

The fixtures consume only the committed IEEE-9 development-frame artifact with
SHA-256
`14744e193321398536529cb81c307968ab363510493265ff1e1cf1340f1224d1`.

## Scope verification

- Frozen IEEE Geometry V1 source changed: **no**
- Comparator implementation added: **no**
- New IEEE-14 comparator output generated, loaded, or displayed: **no**
- G3 independent equivalence begun: **no**
- G4 clean replay begun: **no**
- Commit created: **no**

## Approval effect

Approval should cite the candidate SHA-256 above. It would authorise creation of
the immutable approval binding and only the next explicitly approved gate. It
would not itself authorise IEEE-14 evaluation, G3/G4 work, frozen V1 changes,
external contact, publication, grant work, or public Track D.

