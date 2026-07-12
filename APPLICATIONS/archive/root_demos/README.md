# Legacy Root Demos

This directory preserves standalone demonstration and robustness scripts that
previously lived in the repository root.

They are retained as historical application examples, not as canonical NEXAH
entry points. The supported hands-on entry is documented in the repository
[Quick Start](../../../README.md#-quick-start).

The scripts assume they are launched from the repository root. Some IEEE
examples also depend on historical datasets under `APPLICATIONS/` and may not
represent the current application pipeline.

## Contents

- `run_ieee_demo.py` — synthetic IEEE-style voltage-collapse demonstration
- `run_ieee_noise_robustness.py` — historical IEEE noise experiment
- `run_lorenz_vs_ieee_noise_robustness.py` — cross-system noise comparison
- `run_noise_robustness_demo.py` — single-run robustness visualization
- `run_noise_robustness_multirun.py` — repeated robustness experiment
- `run_noise_robustness_stress_test.py` — multi-level noise stress test
