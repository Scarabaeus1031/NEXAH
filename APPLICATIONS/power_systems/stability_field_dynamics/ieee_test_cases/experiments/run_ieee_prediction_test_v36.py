# run_ieee_prediction_test_v36.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah
)


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

SYSTEMS = ["ieee9", "ieee14", "ieee30"]

LOAD_MIN = 0.6
LOAD_MAX = 5.0
N_STEPS = 120  # high resolution

ALPHA = 0.6  # curvature weight
BETA = 0.4   # fragmentation weight


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def normalize(x):
    x = np.array(x)
    if np.nanmax(x) - np.nanmin(x) == 0:
        return np.zeros_like(x)
    return (x - np.nanmin(x)) / (np.nanmax(x) - np.nanmin(x))


def compute_fragmentation(theta):
    return np.std(theta)


def compute_c_struct(C, loops):
    return np.std(C) * (1 + np.mean(loops))


# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------

results = []

for case in SYSTEMS:

    loads = np.linspace(LOAD_MIN, LOAD_MAX, N_STEPS)

    c_struct_list = []
    frag_list = []
    converged_list = []

    for load in loads:
        theta, C, loops, converged = ieee_to_nexah(case, load)

        if not converged:
            c_struct_list.append(np.nan)
            frag_list.append(np.nan)
            converged_list.append(False)
            continue

        c_struct = compute_c_struct(C, loops)
        frag = compute_fragmentation(theta)

        c_struct_list.append(c_struct)
        frag_list.append(frag)
        converged_list.append(True)

    df = pd.DataFrame({
        "load": loads,
        "c_struct": c_struct_list,
        "fragmentation": frag_list,
        "converged": converged_list
    })

    # --------------------------------------------------------
    # DERIVATIVES
    # --------------------------------------------------------

    df["dc"] = np.gradient(df["c_struct"], df["load"])
    df["d2c"] = np.gradient(df["dc"], df["load"])

    # --------------------------------------------------------
    # NORMALIZATION
    # --------------------------------------------------------

    df["d2c_norm"] = normalize(df["d2c"])
    df["frag_norm"] = normalize(df["fragmentation"])

    # --------------------------------------------------------
    # UNIFIED PREDICTOR
    # --------------------------------------------------------

    df["prediction_score"] = (
        ALPHA * df["d2c_norm"] +
        BETA * df["frag_norm"]
    )

    # --------------------------------------------------------
    # COLLAPSE DETECTION
    # --------------------------------------------------------

    collapse_idx = df[~df["converged"]].index.min()

    if pd.isna(collapse_idx):
        continue

    collapse_load = df.loc[collapse_idx, "load"]

    # Peak before collapse
    valid = df[df["load"] < collapse_load]
    peak_idx = valid["prediction_score"].idxmax()
    peak_load = df.loc[peak_idx, "load"]

    lead_time = collapse_load - peak_load

    results.append({
        "case": case,
        "collapse_load": collapse_load,
        "peak_load": peak_load,
        "lead_time": lead_time
    })

    # --------------------------------------------------------
    # PLOT (PAPER READY)
    # --------------------------------------------------------

    plt.figure(figsize=(10, 5))

    plt.plot(df["load"], normalize(df["prediction_score"]),
             label="Unified Predictor", linewidth=2)

    plt.axvline(collapse_load, linestyle="--", label="Collapse")

    plt.scatter(
        peak_load,
        normalize(df.loc[peak_idx, "prediction_score"]),
        color="red",
        zorder=5,
        label="Prediction Peak"
    )

    plt.title(f"{case.upper()} — Unified Collapse Predictor (V36)")
    plt.xlabel("Load")
    plt.ylabel("Normalized Score")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.savefig(
        f"APPLICATIONS/power_systems/stability_field_dynamics/"
        f"ieee_test_cases/outputs/v36_{case}.png"
    )
    plt.close()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

summary = pd.DataFrame(results)

print("\n--- V36 SUMMARY ---")
print(summary)

summary.to_csv(
    "APPLICATIONS/power_systems/stability_field_dynamics/"
    "ieee_test_cases/outputs/ieee_prediction_v36_summary.csv",
    index=False
)
