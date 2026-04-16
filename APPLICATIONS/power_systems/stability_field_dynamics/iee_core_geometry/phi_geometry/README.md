# Phi Geometry – Regime Detection Experiments

This module contains experimental work on early detection of instability
in power system voltage trajectories using geometric and signal-based methods.

## Goal

The original goal was to identify a universal early-warning signal ("Phi-Split")
that predicts voltage collapse significantly earlier than classical methods.

## Current Status (April 2026)

The initial hypothesis of a **universal early warning signal** could not be confirmed.

Instead, the work evolved into a **regime detection framework** based on:

- voltage trajectories
- drift (dv/dt)
- acceleration (d²v/dt²)
- hybrid change score
- adaptive thresholds

---

## Core Idea

System behavior is analyzed as a transition between regimes:

STABLE → DRIFT → PRE-COLLAPSE → COLLAPSE

Rather than detecting a single "magic event", the system identifies:

- changes in signal structure
- rising instability patterns
- regime transitions before collapse

---

## Detection Pipeline

Voltage → Drift → Acceleration → Hybrid Score
↓
Adaptive Threshold (rolling)
↓
Regime Change Detection

---

## Key Findings

### 1. No universal early signal

- Different systems produce different signatures
- No consistent "Phi-Split" timing across cases

---

### 2. Regime detection works

- Stable → unstable transitions can be detected
- Lead times depend on system dynamics
- Typical observed lead times:

| Case              | Lead Time |
|------------------|----------|
| linear decay     | ~30–35   |
| accelerated      | ~20–30   |
| noisy systems    | ~20–25   |
| sharp collapse   | ~0–3     |

---

### 3. Trade-off is fundamental

Early detection depends on:

- sensitivity (early but noisy)
- robustness (late but reliable)

This is a known limitation in dynamical system monitoring.

---

### 4. Critical systems are inherently hard

In near-critical collapse:

- regime change ≈ collapse
- lead time → 0

This is expected behavior in real systems.

---

## Interpretation

The system does **not predict collapse far in advance**.

Instead, it provides:

- structural awareness of system state
- detection of regime transitions
- insight into instability development

This aligns with the NEXAH philosophy:

> Not prediction, but navigation through regimes.

---

## Relation to NEXAH Kernel

This module connects directly to:

ENGINE/kernel/regime/regime_detector.py

It serves as an experimental layer for:

- validating regime detection ideas
- testing signal-based transition detection
- exploring stability landscapes

---

## Limitations

- Synthetic data only (so far)
- No full IEEE simulation integration yet
- No probabilistic confidence model
- No comparison to classical methods (CPF, V-Q, etc.)

---

## Next Steps

- integrate real IEEE test cases
- build regime confidence layer
- compare with classical stability metrics
- connect to navigation engine

---

## Conclusion

This module does not provide a breakthrough predictive signal.

However, it establishes a working foundation for:

- regime-based system analysis
- early instability detection (case-dependent)
- integration into the NEXAH navigation framework

---

## Author

Thomas K. R. Hofmann
