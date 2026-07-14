# IEEE Geometry V1 Validation

Status: Phase V Work Package F canonical gate

This validation applies the standardization fitted on the IEEE-9 development
campaign to the prospectively locked IEEE-14 evaluation campaign without
refitting or case-specific branches.

Run from the repository root:

```bash
python validation/ieee_geometry_v1/run_validation.py \
  --out validation/ieee_geometry_v1/canonical_summary.json
```

The runner rebuilds IEEE-14 from the frozen manifest and compares the fresh
frames, geometry, five-probe Orientation Report, JSON brief, and Markdown brief
with their committed canonical artifacts. It also reproduces the IEEE-9 model,
checks the environment and adapter protocol, audits every allowed and prohibited
claim, and preserves the outcome boundary.

The gate validates reproducible software behavior within the declared benchmark
protocol. It does not validate operational-grid behavior, prediction, physical
stability, causal control, or real-world generalization.
