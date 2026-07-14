# IEEE Geometry V1 — 10-Minute Runnable Case

## Prerequisites

Use the repository environment documented in `case_manifest.json`. From the
repository root, confirm that NEXAH and its test dependencies are installed.

## Reproduce the complete frozen gate

```bash
python validation/ieee_geometry_v1/run_validation.py \
  --out /tmp/nexah-ieee-geometry-v1.json
```

This one command:

1. validates the locked environment and adapter protocol;
2. reproduces the IEEE-9 development model;
3. reconstructs IEEE-14 from Pandapower;
4. applies the unchanged IEEE-9 model and six frozen operators;
5. regenerates all five probes and the Orientation Brief;
6. checks every product against its canonical artifact;
7. audits supported and prohibited claims.

## Inspect the result

```bash
python -m json.tool /tmp/nexah-ieee-geometry-v1.json | less
```

The expected top-level result is:

```text
gate_passed: true
development: 17 converged, 2 failed
evaluation:  19 converged, 0 failed
parameter_retuning: false
evaluation solver boundaries: 0
```

The zero is meaningful: no boundary was observed on the frozen IEEE-14 grid.
It is not a claim that no physical boundary exists elsewhere.

## Read the human result

- [IEEE-14 Orientation Brief](../evaluation_orientation_brief.md)
- [Canonical validation summary](../../../../validation/ieee_geometry_v1/canonical_summary.md)
- [Physical campaign figure](figures/01-physical-campaign.png)
- [Path geometry figure](figures/02-path-geometry.png)
- [Turning geometry figure](figures/03-turning-geometry.png)
- [Evidence-boundary figure](figures/04-evidence-boundary.png)

## Verify the test gate

```bash
python -m pytest tests/validation/test_ieee_geometry_v1.py -q
```

The test executes the validation twice and requires byte-identical results.
For contracts, formulas, provenance, and limitations, continue with the
**[Research path](RESEARCH_PATH.md)**.
