```python
"""
V35 — Time Dynamics & Structural Transitions
------------------------------------------

Adds temporal structure analysis on top of V34:

- dC (coupling gradient)
- dL (loop gradient)
- state classification
- state transitions
- transition density
- cycle closure error

Output:
- v35_time_dynamics.csv
"""

import numpy as np
import pandas as pd
from tqdm import tqdm

# IMPORT YOUR EXISTING FUNCTIONS HERE
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.run_scan_v34_physical_coupling import (
    run_single_simulation  # <-- adapt if needed
)

# -------------------------
# CONFIG
# -------------------------

LOADS = [1.0, 2.0, 3.0, 4.0]
TIME_STEPS = list(range(24))

# -------------------------
# STATE CLASSIFICATION
# -------------------------

def classify_state(loops):
    if loops == 0:
        return "VOID"
    elif loops <= 3:
        return "WEAK"
    elif loops <= 6:
        return "STABLE"
    else:
        return "OVERDRIVE"

# -------------------------
# MAIN LOOP
# -------------------------

results = []

for load in LOADS:
    print(f"\n=== LOAD {load} ===")

    C_series = []
    L_series = []

    # --- run full cycle ---
    for t in TIME_STEPS:
        C, loops, min_voltage = run_single_simulation(load, t)

        C_series.append(C)
        L_series.append(loops)

    # --- compute dynamics ---
    for i, t in enumerate(TIME_STEPS):

        C = C_series[i]
        L = L_series[i]

        # gradients
        if i == 0:
            dC = 0
            dL = 0
        else:
            dC = C - C_series[i - 1]
            dL = L - L_series[i - 1]

        state = classify_state(L)

        # transition detection
        if i == 0:
            transition = 0
        else:
            prev_state = classify_state(L_series[i - 1])
            transition = int(state != prev_state)

        results.append({
            "load": load,
            "t": t,
            "C": C,
            "loops": L,
            "dC": dC,
            "dL": dL,
            "state": state,
            "transition": transition,
            "min_voltage": min_voltage
        })

    # -------------------------
    # CYCLE ANALYSIS
    # -------------------------

    closure_error = abs(C_series[0] - C_series[-1])
    total_transitions = sum(
        int(classify_state(L_series[i]) != classify_state(L_series[i-1]))
        for i in range(1, len(L_series))
    )

    print(f"Closure error: {closure_error:.6f}")
    print(f"Transitions: {total_transitions}")

# -------------------------
# SAVE RESULTS
# -------------------------

df = pd.DataFrame(results)

df.to_csv("v35_time_dynamics.csv", index=False)

print("\nSaved: v35_time_dynamics.csv")
```
