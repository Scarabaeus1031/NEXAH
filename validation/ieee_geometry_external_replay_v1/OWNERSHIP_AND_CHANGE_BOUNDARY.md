# SR-1 Ownership and Change Boundary

## Frozen read-only inputs

The following remain owned by IEEE Geometry V1:

- manifest and case roles;
- development and evaluation frames;
- standardisation model and geometry products;
- Orientation reports and briefs;
- six operator definitions and insufficiency policies;
- supported and prohibited claims;
- canonical validation runner and summary;
- V1 tests.

SR-1 reads and verifies these sources. It does not repair, regenerate in place,
retune, reinterpret, or version them.

## SR-1-owned sidecar material

SR-1 may own, after the relevant gate:

- baseline identity and hash records;
- environment capture;
- disposable-output replay orchestration;
- independently written operator-equivalence code;
- predeclared comparator and analysis protocols;
- conventional-indicator sidecar calculations;
- replay, comparison, null, ambiguity and discrepancy reports;
- reviewer-facing instructions.

## Generated-output boundary

All future runners must require a caller-selected output directory outside
frozen V1 paths. No command may default to:

- `APPLICATIONS/power_systems/ieee_geometry_v1/`;
- `validation/ieee_geometry_v1/`;
- any committed canonical artifact path.

## Change classes

| Class | Example | Allowed in SR-1? |
|---|---|---|
| frozen V1 source | manifest, frames, geometry, claims | no |
| frozen V1 validation | canonical runner, summary, tests | no |
| SR-1 source | sidecar runner, independent operators, comparator code | gate-dependent |
| SR-1 protocol | replay/comparator/analysis specification | gate-dependent and hash-bound |
| SR-1 generated evidence | reports, logs, discrepancies, nulls | yes, outside frozen paths |
| new theory/case/outcome | new operator semantics, IEEE case, proxy label | no |

## Gate control

Work stops after every gate. A failed or ambiguous gate is preserved as a
result. It is never resolved by silently changing a frozen source.

At G2:

- approve complete comparator and analysis protocol bytes;
- record their SHA-256 digest;
- preserve approval record, protocol and digest together;
- keep IEEE-9 development and IEEE-14 evaluation as separate commands;
- make IEEE-14 evaluation refuse to run if the protocol hash does not match.

