# Orientation MVP Validation

This validation connects the canonical Lorenz transition-structure Demonstrator
to the current Orientation Layer:

```text
deterministic Lorenz trajectory
→ constructed radial-sheet reference
→ V07BackendAdapter
→ OrientationState
→ OrientationReport
→ declared proxy-event comparison
```

## Scientific boundary

The Demonstrator sheet labels are radial bins constructed from the simulated
trajectory. They are a reproducible proxy, not external ground truth. The
validation therefore tests:

- clean end-to-end execution
- repeatability
- source/embedding index alignment
- temporal correspondence between v0.7 label changes and proxy sheet changes
- evidence, uncertainty, and failure-case reporting

It does not establish true regimes, causal intervention, optimal navigation, or
cross-system generality.

## Declared configuration

```text
Demonstrator: steps=8000, dt=0.01, requested sheets=6
v0.7: clusters=6, window=10, random_state=42
event tolerance: ±10 source samples
baseline: predict no transition events
```

These parameters are declared before reading validation scores and are not tuned
against this proxy run.

## Run

From the repository root:

```bash
python -m validation.orientation_mvp.run_validation \
  --recorded-at 2026-07-13T08:00:00+00:00
```

Generated artifacts are written to `outputs/orientation_mvp/` and are ignored by
Git:

```text
orientation_state.json
orientation_report.json
baseline_comparison.json
failure_cases.json
validation_summary.md
```

The committed validation record summarizes a canonical repeated run and its
known limitations.

## Committed evidence

- **[VALIDATION_RECORD.md](VALIDATION_RECORD.md)** — configuration, metrics,
  reproducibility hashes, and interpretation
- **[baseline_comparison.json](baseline_comparison.json)** — machine-readable
  canonical metrics
- **[failure_cases.json](failure_cases.json)** — explicit limitations and
  confirmed boundary behavior
