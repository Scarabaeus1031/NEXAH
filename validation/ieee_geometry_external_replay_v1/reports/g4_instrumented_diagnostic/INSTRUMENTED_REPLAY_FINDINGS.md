# Instrumented replay findings

## Status

Exactly one authorised IEEE-14 diagnostic replay was executed. It completed as
attempt 1 of 1. No retry occurred or is permitted.

The official result remains:

```text
G4_clean_replay_failed
```

Updated root-cause classification:

```text
C — environment-dependent scientific computation
```

Here “environment-dependent” includes the recorded binary/runtime execution
path. The evidence locates the divergence inside numerical solver output, while
the exact BLAS, sparse-solver, or other backend operation responsible remains
unidentified.

## Pre-execution binding

- Source revision:
  `d3a19138b96aa07dfd623bdebb1003cb02cc60e8`
- Protocol SHA-256:
  `b8afa3d79582c0031ec754e542641ef70d7352f1095a82e996249225051ac968`
- Instrument SHA-256:
  `527ee8beaf5475d744b89b27bf1495851c4cfc94372a3745a6a6b51978316d3c`
- Binding SHA-256:
  `e46336489a3045552a297b060308f9986b2aab6d79990ca583901729ab4210a6`
- Observational-only verifier: passed
- Frozen V1 hashes: 15/15 match
- Preserved original G4 evidence: 11/11 match
- Clean source checkout: yes

The instrument calls the canonical fresh IEEE-14 campaign entrypoint exactly
once. It uses the unchanged analysis, probe and brief functions. All evidence
serialization and comparison begins only after the scientific objects have
been computed.

## Environment

- macOS 26.5.2 / Darwin 25.5.0, arm64
- CPython 3.12.7
- Python executable SHA-256:
  `3a816ef2cfd417287d7cdfaaec687c668c1dd21b51acad45f5a8e7d7bff89daa`
- NEXAH 0.7.0
- NumPy 1.26.4
- SciPy 1.13.1
- pandas 2.3.3
- pandapower 3.4.0
- OpenBLAS64 0.3.23.dev, ILP64
- numba unavailable
- all recorded thread-control environment variables unset
- exact solver contract: Newton-Raphson, 30 iterations, tolerance `1e-6` MVA,
  initialization `auto`, independent load points

The complete package lock, wheel metadata, installed `RECORD` hashes, binary
extension hashes, Python build configuration and NumPy/BLAS configuration are
retained in `preflight_environment.json`.

## Exact first divergence

Deterministic traversal order is frames → geometry → Orientation → brief;
mapping keys lexicographic; list indices ascending.

The first unequal leaf is:

| Dimension | Value |
|---|---|
| JSON pointer | `/frames/0/entity_views/0/values/0/2` |
| Processing stage | pandapower result extraction into the bus entity view |
| Frame | `phase-v-ieee-geometry-v1-ieee14:load-000:geometry-frame` |
| Campaign index / load scale | `0` / `0.6` |
| Entity | bus / `bus:0` |
| Field / unit | `p_mw` / MW |
| Canonical | `-119.65391579912867` |
| Fresh | `-119.65391579912881` |
| Canonical binary64 | `c05de9d9c1a6e61a` |
| Fresh binary64 | `c05de9d9c1a6e624` |
| Absolute difference | `1.4210854715202004e-13` |
| Relative difference | `1.1876631550494958e-15` |
| ULP distance | `10` |

This field is extracted directly from `net.res_bus.p_mw`; the divergence
therefore precedes NEXAH frame serialization, system-feature aggregation,
standardization, geometry and Orientation.

## Structure, order, nulls and categories

The recursive comparison found:

- missing keys: 0;
- type differences: 0;
- list-length or shape differences: 0;
- mapping-order differences: 0;
- categorical differences: 0;
- null-placement differences: 0;
- topology-ID differences: 0;
- entity-key or entity-order differences: 0;
- frame-order differences: 0;
- convergence/failure-boundary differences: 0.

All 19 frames converge in the same order. Array dimensions, variable names,
units, case role, topology identity and every non-numeric value are identical.
This excludes D.

## Numeric divergence inventory

Every numeric difference is recorded with canonical/fresh values, Python repr,
`float.hex`, binary64 bytes, absolute difference, relative difference and ULP
distance in `payloads/recursive_diff.json`.

| Artifact | Numeric differences | Structural/categorical differences |
|---|---:|---:|
| Frames | 1,425 | 0 |
| Geometry | 258 | 0 |
| Orientation | 258 | 0 |
| Brief | 0 | 0 |

Numeric differences occur in every frame and across bus, line and system
features. The largest observed absolute frame difference is
`1.5347723092418164e-12` MW at frame 13, `bus:0`, `p_mw`.

Large ULP counts occur near zero and must not be interpreted as large physical
differences. For example, one geometry delta changes from exact zero to
`-6.217248937900877e-15`. No tolerance or acceptance threshold is inferred from
these observations.

## Propagation and independent divergences

The first global difference is a negative bus active-power value. The system
summary clips negative `p_mw` to zero when calculating total positive bus
consumption. That first leaf therefore affects:

- the complete fresh campaign payload;
- the frames SHA-256;
- the exact `evaluation-source-replay` check.

It does not by itself feed the frozen geometry projection.

Further independent solver-output differences occur in bus voltage, angle,
reactive power, line loading, line active/reactive flow and system summaries.
The first downstream-relevant system-feature difference is:

```text
/frames/0/system_features/values/1
mean_bus_voltage:
1.0565780011669752 → 1.0565780011669754
absolute 2.220446049250313e-16; 1 ULP
```

Together with other system-feature differences, it propagates into:

1. projected frame values;
2. adjacent delta vectors and displacements;
3. cumulative path length;
4. turns and discrete curvature;
5. the embedded analysis inside Orientation.

The first geometry difference is projected frame 0, component 1:

```text
3.0774221717064782 → 3.077422171706486
absolute 7.549516567451064e-15; 17 ULP
```

Final path length remains:

```text
canonical: 5.55378709510072
fresh:     5.553787095100708
absolute:  1.2434497875801753e-14
ULP:       14
```

All 258 Orientation differences are the embedded geometry-analysis
differences. The Orientation report outside that embedded analysis and the
complete Orientation brief remain exactly equal.

## Relation to the original failed G4 run

The diagnostic path length exactly matches the original G4 replay value
`5.553787095100708`, and both runs preserve all aggregate and categorical
results. However, their fresh frames, geometry and Orientation payload hashes
differ from each other despite the same checkout and installed environment.

This is evidence of low-order execution variability within the recorded
environment, not merely a difference between the canonical and diagnostic
machines. It does not identify the responsible backend operation.

## Classification evidence

Supporting C:

- the first divergence is a raw pandapower numerical result;
- only numeric leaves differ;
- all structure, ordering, nulls, topology, categories and case results match;
- the same numerical changes propagate deterministically through geometry;
- the canonical environment contract omits binary build, BLAS/LAPACK, numba,
  sparse-solver and thread-runtime identity;
- the original G4 and diagnostic payload hashes differ even under the same
  recorded environment, demonstrating execution-level low-order variability;
- repository history already records solver-byte portability concerns.

Contradicting or limiting C:

- the exact backend operation causing the variation is not identified;
- all aggregate case outcomes and the brief are identical;
- the final path-length difference is only 14 ULP;
- because no tolerance is authorised, B cannot be formally established even
  though scientific-result equivalence is strongly supported;
- same-environment variability means the cause is not exclusively an
  operating-system or package-version difference.

Why not the alternatives:

- A is excluded because computed binary64 values differ.
- B is not formally selected because exact numbers differ and no justified
  numerical-equivalence rule exists.
- D is excluded by the complete structural/categorical comparison.
- E is superseded because the missing payloads are now retained and the
  divergence is localized to numerical solver output, although the exact
  backend mechanism remains open.

## Boundary confirmation

- Exactly one diagnostic IEEE-14 replay occurred.
- No IEEE-9 solve occurred.
- No retry or environment tuning occurred.
- No tolerance, rounding, comparator output, new scientific metric or combined
  score was introduced.
- No frozen V1, approved protocol or original G4 evidence changed.
- `G4_clean_replay_failed` remains official.
- G5 and G6 remain untouched.
- No external contact or public/scientific claim occurred.
- No commit was created.

