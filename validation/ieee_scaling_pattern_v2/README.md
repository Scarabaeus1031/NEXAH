# IEEE Scaling Pattern Validation V2

Status: canonical H–K validation completed and frozen

Artifacts:

- **[VALIDATION_RECORD.md](VALIDATION_RECORD.md)** — design, results, limits,
  and interpretation
- **[canonical_result.json](canonical_result.json)** — complete branch,
  boundary, and pattern evidence
- **[canonical_summary.md](canonical_summary.md)** — compact aggregate result
- **[run_validation.py](run_validation.py)** — executable frozen method

## Question

Does the historical `c_struct` curvature contain a stable interior feature that
is independent of derivative-edge selection and persists at larger network
scale?

## Frozen H–K design

- H: start each case at its native `lambda = 1.0` operating point and scan
  upward and downward separately
- I: bisect every bracketed upward convergence boundary to width `<= 0.005`
- J: use a seven-point local cubic second derivative, relative prominence,
  four-step boundary distance, every-second-point resolution check, and a
  quadratic monotone null
- K: keep PEGASE-9241 outside method development and apply the unchanged method
- solve every point independently from the standard pandapower case
- preserve non-convergence without fabricated physical arrays
- make no continuation-power-flow, causal, prediction, or control claim

## Canonical conclusion

All seven development cases and held-out PEGASE-9241 converge at the native
baseline. Upward convergence boundaries are bracketed and refined for every
case. None of the six development cases with enough samples passes the frozen
edge-independent precursor criteria; IEEE-300 is too close to its upper
boundary for the declared seven-point method. PEGASE-9241 is likewise too close
to its boundary for J and closes the held-out gate as an explicit **boundary of
validity**, not cross-scale support.

## Reproduce

```bash
python -m validation.ieee_scaling_pattern_v2.run_validation \
  --recorded-at 2026-07-13T21:00:00+00:00 \
  --output-dir outputs/ieee_scaling_pattern_v2
```

Canonical JSON floats are serialized to 12 significant digits to remove
platform-level solver/BLAS noise below the reported precision. This does not
change calculations or classifications.
