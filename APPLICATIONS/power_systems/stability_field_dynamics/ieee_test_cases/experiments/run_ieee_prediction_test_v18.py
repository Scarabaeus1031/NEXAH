# run_ieee_prediction_test_v18.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah,
)

print("RUNNING IEEE PREDICTION TEST V18 (EARLY WARNING SYSTEM)")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

LOADS = np.linspace(0.6, 5.0, 40)

OUTPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------

results = []

for load in LOADS:

    theta, c, loops, converged = ieee_to_nexah("ieee14", load_scale=load)

    if converged:
        theta_std = np.std(theta)
        c_std = np.std(c)
        loops_mean = np.mean(loops)

        regime_sep = theta_std * c_std
        c_struct = regime_sep * loops_mean
    else:
        theta_std = c_std = loops_mean = 0.0
        regime_sep = 0.0
        c_struct = 0.0

    results.append({
        "load": load,
        "converged": converged,
        "c_struct": c_struct
    })


df = pd.DataFrame(results)


# ------------------------------------------------------------
# THRESHOLD DETECTION
# ------------------------------------------------------------

df_valid = df[df["converged"] == True]

if len(df_valid) == 0:
    raise ValueError("No converged solutions found!")

max_c = df_valid["c_struct"].max()

# adaptive thresholds
threshold_warning = 0.6 * max_c
threshold_critical = 0.85 * max_c


def classify(val):
    if val >= threshold_critical:
        return "CRITICAL"
    elif val >= threshold_warning:
        return "WARNING"
    else:
        return "SAFE"


df["state"] = df["c_struct"].apply(classify)


# ------------------------------------------------------------
# COLLAPSE DETECTION
# ------------------------------------------------------------

collapse_indices = df[df["converged"] == False].index

if len(collapse_indices) > 0:
    collapse_idx = collapse_indices[0]
    collapse_load = df.loc[collapse_idx, "load"]
else:
    collapse_idx = None
    collapse_load = None


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

csv_path = os.path.join(OUTPUT_DIR, "ieee_prediction_test_v18.csv")
df.to_csv(csv_path, index=False)

print("\n--- RESULTS ---")
print(df)
print(f"\nSaved: {csv_path}")


# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(df["load"], df["c_struct"], label="c_struct", linewidth=2)

# thresholds
plt.axhline(threshold_warning, linestyle="--", label="WARNING threshold")
plt.axhline(threshold_critical, linestyle="--", label="CRITICAL threshold")

# collapse line
if collapse_load is not None:
    plt.axvline(collapse_load, linestyle="--", color="red", label="collapse")

# color-coded points
for i in range(len(df)):
    state = df.loc[i, "state"]
    x = df.loc[i, "load"]
    y = df.loc[i, "c_struct"]

    if state == "CRITICAL":
        plt.scatter(x, y, color="red")
    elif state == "WARNING":
        plt.scatter(x, y, color="orange")
    else:
        plt.scatter(x, y, color="green")

plt.xlabel("Load")
plt.ylabel("c_struct")
plt.title("Early Warning Detection (V18)")
plt.legend()
plt.grid()

plt.show()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print("\n--- EARLY WARNING SUMMARY ---")

print(f"Max c_struct: {max_c:.6f}")
print(f"WARNING threshold: {threshold_warning:.6f}")
print(f"CRITICAL threshold: {threshold_critical:.6f}")

if collapse_load is not None:
    print(f"\nCollapse detected at load ≈ {collapse_load:.3f}")

    # CRITICAL before collapse
    critical_before = df[
        (df["state"] == "CRITICAL") &
        (df["load"] < collapse_load)
    ]

    if len(critical_before) > 0:
        first_critical_load = critical_before.iloc[0]["load"]
        lead_time = collapse_load - first_critical_load

        print(f"First CRITICAL warning at load ≈ {first_critical_load:.3f}")
        print(f"Lead time ≈ {lead_time:.4f}")
    else:
        print("No CRITICAL warning before collapse")

else:
    print("No collapse detected in range")
