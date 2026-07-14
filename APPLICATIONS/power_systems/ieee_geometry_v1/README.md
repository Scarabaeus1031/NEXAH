# IEEE Geometry V1 — Frozen Case Protocol

Status: Phase V work packages A–H complete; frozen IEEE-14 gate passed

This directory contains the frozen protocol, physical development frames, and
the first inspectable geometry analysis for the NEXAH IEEE Geometry case.

The canonical [`case_manifest.json`](case_manifest.json) declares:

- IEEE-9 as the manually inspectable method-development case
- IEEE-14 as the prospectively locked Phase V evaluation case
- the shared ordered load-scale campaign
- exact source variables, units, projections, and information loss
- exact geometry formulas and insufficiency policies
- software and solver configuration
- supported claims, prohibited claims, and evaluation rules
- benchmark evidence and `not_observed` outcome status

Both networks were used by earlier NEXAH experiments. IEEE-14 is therefore not
described as historically untouched. Its evaluation role means something more
specific: no Phase V geometry parameter may change after its geometry result is
inspected.

## Validate the manifest

From the repository root:

```bash
nexah validate-ieee-manifest \
  APPLICATIONS/power_systems/ieee_geometry_v1/case_manifest.json
```

The command validates the typed protocol and reports whether the current Python,
NumPy, pandas, Pandapower, and SciPy versions match the frozen environment.

## Build the development frames

```bash
nexah build-ieee-frames \
  APPLICATIONS/power_systems/ieee_geometry_v1/case_manifest.json \
  --case ieee9 \
  --recorded-at 2026-07-14T14:00:00+00:00 \
  --out APPLICATIONS/power_systems/ieee_geometry_v1/development_frames.json
```

The committed artifact contains immutable physical frames, raw system features,
bus and line entity views, declared projection identities, adapter-visible
topology identity, provenance, unknown rather than fabricated uncertainty, and
explicit failed positions. It intentionally contains no normalized geometry,
drift, path length, direction change, or curvature. Those belong to Work Package
C.

Canonical development result:

| Record | Value |
|---|---:|
| Declared frames | 19 |
| Converged physical frames | 17 |
| Explicit failed frames | 2 |
| Failed load scales | 2.3, 2.4 |
| Geometry values computed | 0 |

The artifact is
[`development_frames.json`](development_frames.json). Its topology identifier
describes the adapter-visible bus/line schema under the frozen case and software
version; it is not asserted to be a complete electrical topology model.

## Analyze the development geometry

```bash
nexah analyze-ieee-geometry \
  APPLICATIONS/power_systems/ieee_geometry_v1/case_manifest.json \
  APPLICATIONS/power_systems/ieee_geometry_v1/development_frames.json \
  --out APPLICATIONS/power_systems/ieee_geometry_v1/development_geometry.json
```

The command fits the manifest-declared population standardization on the
IEEE-9 development campaign and applies the six frozen operators:

- adjacent displacement
- normalized local drift along the ordered load-scale parameter
- cumulative path length
- direction change
- local discrete curvature
- sampled distance from a solver failure to the last converged frame

The canonical result is
[`development_geometry.json`](development_geometry.json). It contains 19
projected positions, 18 adjacent relations, 17 centered turn records, and two
explicit solver-boundary records. The contiguous measured path ends at the
last converged position before the first failure; no path is drawn through or
across missing physical states.

These are geometric measurements of a benchmark computation along a declared
parameter campaign. They are not time derivatives, certified voltage-stability
limits, causal effects, or control recommendations. Projection agreement is not
computed yet because the frozen manifest declares projection views but does not
declare a comparison metric between representations. NEXAH leaves that result
absent instead of selecting an undeclared metric after seeing the data.

For the later frozen IEEE-14 gate, the development model must be supplied
unchanged with `--model development_geometry.json`. The evaluation result must
not be used to refit that model.

## Read the Development Orientation Brief

Work Package D applies five read-only perspectives to the same canonical
frames and geometry:

1. physical state and solver-visible variables
2. sampled geometry
3. solver boundary and resolution
4. provenance, uncertainty, and evaluation leakage
5. claim-boundary criticism

Generate the human-readable brief:

```bash
nexah analyze-ieee-geometry \
  APPLICATIONS/power_systems/ieee_geometry_v1/case_manifest.json \
  APPLICATIONS/power_systems/ieee_geometry_v1/development_frames.json \
  --format brief
```

Canonical artifacts:

- [`development_orientation.json`](development_orientation.json) — complete
  report, five probe results, preserved agreement, and limitations
- [`development_orientation_brief.json`](development_orientation_brief.json) —
  compact typed human-facing product
- [`development_orientation_brief.md`](development_orientation_brief.md) —
  Markdown rendering of that same typed brief

The brief locates the last converged sampled position at load scale 2.2,
reports the first solver failure at 2.3, and makes the evidence boundary part of
the result. The probes do not vote, execute, recommend control, or update
episodic memory.

## Run the frozen IEEE-14 evaluation

The evaluation uses the committed IEEE-9 model unchanged:

```bash
nexah build-ieee-frames \
  APPLICATIONS/power_systems/ieee_geometry_v1/case_manifest.json \
  --case ieee14 \
  --recorded-at 2026-07-14T18:00:00+00:00 \
  --out APPLICATIONS/power_systems/ieee_geometry_v1/evaluation_frames.json

nexah analyze-ieee-geometry \
  APPLICATIONS/power_systems/ieee_geometry_v1/case_manifest.json \
  APPLICATIONS/power_systems/ieee_geometry_v1/evaluation_frames.json \
  --model APPLICATIONS/power_systems/ieee_geometry_v1/development_geometry.json \
  --out APPLICATIONS/power_systems/ieee_geometry_v1/evaluation_geometry.json
```

Canonical evaluation artifacts:

- [`evaluation_frames.json`](evaluation_frames.json)
- [`evaluation_geometry.json`](evaluation_geometry.json)
- [`evaluation_orientation.json`](evaluation_orientation.json)
- [`evaluation_orientation_brief.json`](evaluation_orientation_brief.json)
- [`evaluation_orientation_brief.md`](evaluation_orientation_brief.md)

All 19 IEEE-14 positions converge on the frozen grid. The unchanged method
therefore returns 18 adjacent measurements and 17 centered turn measurements,
but no sampled solver-boundary record. It does not infer a physical boundary
from that absence.

The complete WP-F replay, checksums, seven-level validation ladder, and claim
audit are in
[`validation/ieee_geometry_v1/`](../../../validation/ieee_geometry_v1/README.md).

## Enter through the public showcase

The [`showcase/`](showcase/README.md) provides a 90-second map, a ten-minute
runnable case, a full research path, and four reproducible scientific figures.
Every figure is generated from the canonical JSON records above.

The later path from benchmark computation to timestamped external evidence is
specified by the
[`Observed-Evidence Bridge`](../../../testkit/observed_evidence/OBSERVED_EVIDENCE_BRIDGE.md).
Its admission template remains closed until a real source, license, provenance,
measurements, and independently observed outcome are available.

## Evidence boundary

This is a benchmark protocol, not an operational-grid case:

> **NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE**
