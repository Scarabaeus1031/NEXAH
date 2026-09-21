# IEEE Projection Fidelity V1 — Canonical Validation

Status: `GATE PASSED`

This package validates the separately frozen projection-comparison sidecar over
the committed IEEE Geometry V1 frames. It does not rerun pandapower and does not
alter the original Geometry V1 result.

## Reproduce

```bash
python -m validation.ieee_projection_fidelity_v1.run_validation \
  --out /tmp/ieee_projection_fidelity_v1.json
```

## Canonical decision

`IEEE_PROJECTION_FIDELITY_CONFIRMED`

- raw-source reproduction maximum error: `0.0`;
- quotient-plus-residual raw reconstruction maximum error: `5.68e-14`;
- quotient-plus-residual pair-distance maximum error: `1.33e-15`;
- quotient-only kernel-counterfactual maximum distance: `2.22e-16`;
- quotient-plus-residual kernel detection: `1.0`;
- IEEE-14 evaluation refit: `false`.

See [`canonical_summary.md`](canonical_summary.md),
[`canonical_result.json`](canonical_result.json), and
[`VALIDATION_RECORD.md`](VALIDATION_RECORD.md).

## Boundary

This is a representation-fidelity result. It does not establish operational
utility, stability prediction, early warning, risk, causality, control,
universal compression superiority, or a physical AXIS08 identity.
