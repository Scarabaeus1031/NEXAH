# IEEE Geometry V1 — Frozen Case Protocol

Status: Phase V work package A / step 5.3 and work package B / step 5.4
implemented

This directory freezes the first NEXAH IEEE Geometry experiment before the new
geometry operators are implemented or evaluated.

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

## Evidence boundary

This is a benchmark protocol, not an operational-grid case:

> **NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE**
