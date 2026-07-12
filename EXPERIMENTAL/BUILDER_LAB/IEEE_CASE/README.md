# IEEE Case — Historical Synthetic Gate Prototype

> **Status: historical synthetic signal experiment.** Despite the directory and
> filename, `scripts/ieee_gate_detection_v1.py` does not load, simulate, or
> analyze an IEEE power-system test case.

## What the Script Does

The script generates a hand-constructed scalar signal with three phases:

```text
small periodic signal
→ growing oscillation
→ noisy larger oscillation
```

It computes a rolling lag-one autocorrelation proxy, smooths it, and marks
samples where its absolute value is below a fixed threshold. Those marked
samples are candidate low-autocorrelation points for this synthetic signal.

They are not:

- IEEE bus or branch observations
- power-flow or dynamic-simulation results
- the current NEXAH Gate Operator
- validated transition events
- evidence of coherence loss in an electrical grid

## Current Power-System Work

Use **[APPLICATIONS/power_systems/](../../../APPLICATIONS/power_systems/)** for
the current power-system application and benchmark studies. In particular, the
stability-field and field-navigation modules contain the actual IEEE benchmark
lineages.

The script is retained here because it documents an early conceptual step from
scalar signal statistics toward transition-region analysis. It should not be
promoted into the current application.

---

**Reviewed:** July 12, 2026
