# IEEE Geometry V1 — Frozen Case Protocol

Status: Phase V work package A / step 5.3 implemented

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

## Evidence boundary

This is a benchmark protocol, not an operational-grid case:

> **NO OBSERVED OUTCOME → NO EPISODIC MEMORY UPDATE**
