# G4 root-cause analysis

## Scope and conclusion

This is a bounded forensic analysis of the frozen canonical artifacts and the
preserved first G4 run. No IEEE-9 or IEEE-14 computation was rerun.

**Classification: E — unresolved.**

The evidence proves that the first divergence occurs in the freshly solved
IEEE-14 source campaign, before geometry and Orientation are derived. It also
proves that the divergence includes at least one changed binary64 value and is
therefore not serialization-only. But the first G4 runner retained only hashes
and summary values—not the fresh frames, geometry, or Orientation payloads.
Consequently, the first differing field, frame, entity, and solver value cannot
be recovered from the evidence now available.

Classifying the result as B or C would overstate the evidence:

- B requires a complete numerical comparison showing equivalence; that
  comparison is impossible without the fresh payload.
- C is plausible and has strong circumstantial support, but the reference
  BLAS/LAPACK, numba state, package-build identity, and transitive lock were not
  recorded, so environment dependence cannot be isolated as the exclusive
  cause.

## Exact first-divergence location

The earliest observable divergence is:

```text
validation/ieee_geometry_v1/run_validation.py:159-160
evaluation_campaign.to_dict() == committed_evaluation_frames
result: false
```

All earlier gate checks pass:

- environment lock;
- adapter protocol;
- IEEE-9 development freeze;
- no IEEE-14 refit.

The fresh campaign is created at `run_validation.py:55-79`; its nineteen
independent pandapower solves begin through `nexah/sources/ieee.py:224-244`.
The adapter then extracts bus values at lines 256-269, line values at lines
271-287, and system summaries at lines 297-311.

The precise field/frame/entity location is **not retained**. The runner stored
only:

- the fresh campaign SHA-256;
- the fresh geometry SHA-256;
- the fresh Orientation SHA-256;
- aggregate counts;
- total path length;
- boolean gate outcomes.

It did not store the fresh payloads or a recursive diff. Recovering a more
specific location would require a second IEEE-14 execution, which was expressly
not authorised.

## Complete retained summary diff

There is exactly one differing numeric value retained on both sides:

| Path | Frozen | Replay | Absolute | Relative | ULP distance |
|---|---:|---:|---:|---:|---:|
| `evaluation_result.total_path_length` | 5.55378709510072 | 5.553787095100708 | 1.2434497875801753e-14 | 2.238922317848817e-15 | 14 |

The ULP size at both values is `8.881784197001252e-16`.

All remaining summary differences are non-numeric consequences or hashes:

- `evaluation-source-replay`: true → false;
- `evaluation-geometry-replay`: true → false;
- `evaluation-report-replay`: true → false;
- frames, geometry, and Orientation SHA-256 values differ;
- `gate_passed`: true → false;
- four claim-audit statuses change from `supported_within_manifest` to
  `not_supported_by_failed_gate`.

The machine-readable inventory contains every differing retained summary field
and the field-level ULP calculation. It cannot inventory unretained underlying
numeric differences, and explicitly marks them unavailable rather than
inventing values.

## Structural and categorical comparison

The following aggregate structure is exactly equal:

- 19 declared frames;
- 19 converged frames;
- 0 failed frames;
- 18 available steps;
- 17 available turns;
- 0 insufficient steps or turns;
- 0 solver boundaries;
- identical empty failed-load-scale list;
- identical freeze object;
- identical limitations;
- identical brief SHA-256.

The frozen payload has, at every frame, two entity views: 14 buses × 4 variables
and 15 lines × 3 variables. It has no null system-feature payloads. Its geometry
contains 19 projected frames, 18 steps, 17 turns, and no solver boundary.

For the fresh payload, only the aggregate counts above survive. Exact fresh
array shapes, mapping keys, frame/entity ordering, topology ID, null placement,
entity IDs, categorical values, and per-frame convergence flags were not
retained. Therefore:

- no structural divergence is demonstrated;
- structural equivalence is not proved;
- mapping insertion order alone is excluded as a hash cause because
  `_payload_sha256` serializes with `sort_keys=True`;
- list, frame, or entity ordering cannot be excluded.

## Propagation

1. Pandapower solves the nineteen IEEE-14 load points and the adapter extracts
   bus/line arrays and seven summary features.
2. The generated campaign fails exact equality against the frozen frames; its
   canonical payload hash changes.
3. The fixed IEEE-9 standardization is applied to the changed system features.
   Projection, displacement, drift, curvature, and cumulative path values are
   derived. The geometry hash changes, and the final path length moves by 14
   ULP.
4. The five probes embed the analysis into the Orientation context. Its hash
   changes and exact report replay fails.
5. The Orientation brief remains byte-equivalent. This is consistent with its
   selected categorical content and formatted values being insensitive to the
   observed low-order change; it does not prove full numerical equivalence.
6. `gate_passed = all(check["passed"] for check in checks)` becomes false.
7. Claim text remains unchanged, but four audit statuses change solely because
   their status is conditional on `gate_passed`.

The claim-status change is therefore a gate consequence, not evidence of a new
physical outcome or altered claim.

## Environment and implementation analysis

The declared environment lock passes because it covers CPython and selected
top-level package versions. Both records identify Python 3.12.7, arm64, macOS
26.5.2, NumPy 1.26.4, pandas 2.3.3, pandapower 3.4.0, and SciPy 1.13.1.

The G4 environment additionally records:

- a pip NumPy arm64 wheel;
- OpenBLAS64 0.3.23.dev with ILP64;
- no available numba path;
- nineteen pandapower warnings that numba acceleration was disabled;
- the complete G4 transitive package lock.

The reference environment did **not** record:

- BLAS/LAPACK implementation or build flags;
- NumPy/SciPy wheel or conda build identity;
- numba availability and version;
- thread settings;
- complete transitive dependencies.

The repository history is material evidence. Commit
`c6104446549657f7c82e02cb69902faaf9f49498` changed the validation test with the
explicit explanation that solver and renderer byte streams may vary across
operating systems even under the frozen package set. It retained protocol and
aggregate checks while removing mandatory equality with the canonical bytes.
Thus environment-sensitive low-order solver output was already recognized as a
portability concern.

This supports an environment-dependent floating-point explanation, but does
not prove which component caused it:

- BLAS/LAPACK and reduction order are plausible;
- numba-enabled versus disabled pandapower paths are plausible;
- different binary builds under identical package versions are plausible;
- solver-level floating-point path is plausible;
- serialization-only is contradicted by the changed binary64 path length;
- nondeterministic mapping order is contradicted by sorted-key hashing;
- list/entity ordering and structural differences remain untested because the
  fresh payload is absent.

## Four reproducibility meanings

| Meaning | Result |
|---|---|
| Byte reproducibility | Failed: three payload hashes and the summary differ. |
| Numerical reproducibility | Unresolved: the one retained aggregate differs by 14 ULP; underlying values are absent. |
| Structural equivalence | Unresolved: aggregate structure matches, exact fresh structures are absent. |
| Scientific-result equivalence | Unresolved: no convergence/boundary/count change is observed and the brief is identical, but a complete field-level comparison is unavailable and no tolerance is authorised. |

No tolerance is proposed. The 14-ULP aggregate observation alone cannot justify
a field-wide or scientifically meaningful tolerance.

## Evidence supporting and contradicting classification E

Supporting:

- fresh source, geometry, and Orientation payloads were not retained;
- their differing hashes cannot be inverted into field values;
- exact first field/frame/entity and full ULP distribution are unknowable;
- reference BLAS/LAPACK, numba state, and binary build identity are absent;
- exact fresh structure and ordering are absent.

Potentially contradicting:

- all aggregate structural results match;
- the brief SHA-256 remains identical;
- the sole retained numerical difference is small: 14 ULP;
- repository history explicitly anticipates cross-environment solver-byte
  variation.

These points make C plausible and B possible, but they do not meet the evidence
threshold for either classification.

## Remediation options

| Option | Implementation | Environment contract | Serialization contract | Gate semantics | Scientific claims |
|---|---|---|---|---|---|
| Preserve G4 failure and take no action | no | no | no | no | no |
| Under separate approval, perform one instrumented replay that writes fresh frames, geometry, Orientation, and a recursive field/ULP diff before deletion | diagnostic sidecar only | no | no | no | no |
| Reconstruct and lock binary distribution identity: wheel/conda hashes, BLAS/LAPACK, numba state, threads, architecture and transitive lock | setup/tooling | **yes** | no | no | no |
| Package an exact container or environment image corresponding to the canonical generation environment | deployment tooling | **yes** | no | no | no |
| Add a canonical float encoding or normalized serialization layer | **yes** | no | **yes** | possibly | no, unless it changes retained precision |
| Replace byte equality with a numerical gate | diagnostic/gate code | possibly | no | **yes** | potentially; requires prior field-level evidence and scientific justification |
| Regenerate canonical artifacts in the G4 environment | **yes** | **yes** | possibly | yes | potentially; not a diagnostic remedy |

The last three options are not justified by the current evidence. In
particular, no tolerance should be selected from the single 14-ULP aggregate.

## Recommended next decision

Keep G4 failed and approve, only if further resolution is required, a single
**instrumented evidence-retention replay** under a new explicit authorisation.
It should execute the unchanged frozen runner once, preserve each fresh
intermediate payload, and produce an exact recursive comparison before any
discussion of tolerance, environment relaxation, or gate changes.

That decision would not itself authorise a tolerance, canonical regeneration,
protocol modification, G5, or G6.

## Boundary confirmation

- No second IEEE-9 or IEEE-14 scientific run occurred.
- No comparator result or combined score was produced.
- No new performance metric was introduced.
- Frozen V1 artifacts, operators, parameters, claims, and case roles were not
  changed.
- The approved G2 protocol and preserved G4 evidence were not changed.
- G5 and G6 remain untouched.
- No commit was created.

