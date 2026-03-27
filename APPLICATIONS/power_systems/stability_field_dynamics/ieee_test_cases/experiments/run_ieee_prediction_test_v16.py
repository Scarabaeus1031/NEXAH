# run_ieee_prediction_test_v16.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah,
)


print("RUNNING IEEE PREDICTION TEST V16 (C_STRUCT vs COLLAPSE)")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

LOADS = np.linspace(0.6, 5.0, 30)

OUTPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

results = []


# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------

for load in LOADS:

    theta, c, loops, converged = ieee_to_nexah("ieee14", load_scale=load)

    theta_std = np.std(theta)
    c_std = np.std(c)
    loops_mean = np.mean(loops)

    # structural metrics
    regime_separation = theta_std * c_std
    c_struct = regime_separation * loops_mean

    row = {
        "load": load,
        "converged": int(converged),
        "theta_std": theta_std,
        "c_std": c_std,
        "loops_mean": loops_mean,
        "regime_separation": regime_separation,
        "c_struct": c_struct,
    }

    results.append(row)


# ------------------------------------------------------------
# DATAFRAME
# ------------------------------------------------------------

df = pd.DataFrame(results)

csv_path = os.path.join(
    OUTPUT_DIR,
    "ieee_prediction_test_v16.csv"
)

df.to_csv(csv_path, index=False)

print("\n--- RESULTS ---")
print(df)
print(f"\nSaved: {csv_path}")


# ------------------------------------------------------------
# COLLAPSE DETECTION
# ------------------------------------------------------------

collapse_indices = df[df["converged"] == 0].index

if len(collapse_indices) > 0:
    collapse_idx = collapse_indices[0]
    collapse_load = df.loc[collapse_idx, "load"]
else:
    collapse_idx = None
    collapse_load = None


# ------------------------------------------------------------
# PRE-COLLAPSE ANALYSIS
# ------------------------------------------------------------

if collapse_idx is not None and collapse_idx > 0:

    pre_df = df.iloc[:collapse_idx]

    max_c_struct = pre_df["c_struct"].max()
    max_idx = pre_df["c_struct"].idxmax()
    max_load = df.loc[max_idx, "load"]

    print("\n--- PRE-COLLAPSE ANALYSIS ---")
    print(f"Collapse load: {collapse_load:.3f}")
    print(f"Max c_struct before collapse: {max_c_struct:.6f} at load {max_load:.3f}")

    distance = collapse_load - max_load

    print(f"Distance (load units): {distance:.4f}")

else:
    print("\n[!] No collapse detected in range.")


# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(df["load"], df["c_struct"], marker="o", label="c_struct")

if collapse_load is not None:
    plt.axvline(collapse_load, linestyle="--", color="red", label="collapse")

plt.xlabel("Load")
plt.ylabel("c_struct")
plt.title("c_struct vs Load (IEEE14)")
plt.legend()
plt.grid(True)

plt.show()


# ------------------------------------------------------------
# SIMPLE THRESHOLD TEST
# ------------------------------------------------------------

threshold = 0.8 * df["c_struct"].max()

df["predicted_risk"] = df["c_struct"] > threshold

print("\n--- THRESHOLD TEST ---")
print(df[["load", "c_struct", "converged", "predicted_risk"]])
