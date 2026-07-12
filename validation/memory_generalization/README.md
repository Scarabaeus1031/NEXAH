# Memory Generalization Validation

Status: preregistered synthetic benchmark

This benchmark evaluates whether the initial episodic similarity heuristic
retrieves the correct stored system family across identical, noisy, and
parameter-shifted trajectories.

## Declared design

- families: Lorenz, Rössler, Kuramoto
- one stored reference episode per family
- shared context domain: `synthetic-dynamical-system`
- v0.7: six clusters, window 10, seed 42
- queries per family:
  - identical clean trajectory
  - relative Gaussian noise 0.01
  - relative Gaussian noise 0.05
  - parameter shift
- primary metric: Top-1 family accuracy
- separation metric: expected-family similarity minus best alternative
- chance baseline: 1/3
- no parameter tuning after reading results

All systems share one context-domain value so family identity cannot leak
through the domain-match component of the similarity function.

System equations and parameters follow existing NEXAH Demonstrator examples.
They are implemented as deterministic validation fixtures rather than imported
from plot-generating historical scripts.

## Run

```bash
python -m validation.memory_generalization.run_validation \
  --recorded-at 2026-07-13T10:00:00+00:00
```

Generated outputs are written to `outputs/memory_generalization/`. The compact
canonical result and failure cases are committed after the repeated run.

## Committed evidence

- **[VALIDATION_RECORD.md](VALIDATION_RECORD.md)** — design, metrics,
  reproducibility, and interpretation
- **[canonical_result.json](canonical_result.json)** — all canonical rankings
  and aggregate results
- **[failure_cases.json](failure_cases.json)** — boundaries and observed
  retrieval failures

## Boundary

This benchmark tests discrimination among three deterministic synthetic
families. It does not establish semantic memory, meaningful outcome transfer,
calibrated similarity, or real-world generality.
