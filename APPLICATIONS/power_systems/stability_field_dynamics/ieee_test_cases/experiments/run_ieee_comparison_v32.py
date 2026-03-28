# run_ieee_comparison_v32.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah,
)

try:
    import pandapower as pp
    import pandapower.networks as pn
except ImportError:
    raise ImportError("pandapower required: pip install pandapower")


print("RUNNING IEEE COMPARISON V32 (HIGH-RES + RANDOM VALIDATION)")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

SYSTEMS = ["ieee9", "ieee14", "ieee30"]

# 🔥 HIGH RESOLUTION GRID
LOADS_DENSE = np.linspace(0.6, 5.0, 200)

# 🔥 RANDOM SAMPLING (KEY TEST)
np.random.seed(42)
LOADS_RANDOM = np.sort(np.random.uniform(0.6, 5.0, 200))

OUTPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def get_min_voltage(case, load):
    if case == "ieee14":
        net = pn.case14()
    elif case == "ieee9":
        net = pn.case9()
    elif case == "ieee30":
        net = pn.case30()
    else:
        raise ValueError(case)

    net.load["p_mw"] *= load
    net.load["q_mvar"] *= load

    try:
        pp.runpp(net, max_iteration=30)
        return net.res_bus["vm_pu"].min(), True
    except:
        return np.nan, False


def compute_c_struct(theta, c, loops):
    return np.std(theta) * np.std(c) * np.mean(loops)


def compute_derivatives(loads, values):
    dc = np.gradient(values, loads)
    d2c = np.gradient(dc, loads)
    return dc, d2c


def run_case(case, loads):

    rows = []

    for load in loads:

        min_v, conv = get_min_voltage(case, load)
        theta, c, loops, conv2 = ieee_to_nexah(case, load)

        if conv and conv2:
            c_struct = compute_c_struct(theta, c, loops)
        else:
            c_struct = np.nan

        rows.append({
            "load": load,
            "min_voltage": min_v,
            "c_struct": c_struct,
            "converged": conv
        })

    df = pd.DataFrame(rows)

    valid = df["c_struct"].notna()

    if valid.sum() > 5:
        dc, d2c = compute_derivatives(
            df.loc[valid, "load"].values,
            df.loc[valid, "c_struct"].values
        )

        df.loc[valid, "dc"] = dc
        df.loc[valid, "d2c"] = d2c

    return df


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

summary = []

for case in SYSTEMS:

    print(f"\n--- {case.upper()} ---")

    # -----------------------------
    # DENSE GRID
    # -----------------------------
    df_dense = run_case(case, LOADS_DENSE)

    collapse_dense = df_dense.loc[df_dense["converged"] == False, "load"]
    collapse_dense = collapse_dense.iloc[0] if len(collapse_dense) else np.nan

    peak_dense = df_dense["d2c"].idxmax()
    peak_load_dense = df_dense.loc[peak_dense, "load"]

    lead_dense = collapse_dense - peak_load_dense

    # -----------------------------
    # RANDOM GRID (CRITICAL TEST)
    # -----------------------------
    df_rand = run_case(case, LOADS_RANDOM)

    collapse_rand = df_rand.loc[df_rand["converged"] == False, "load"]
    collapse_rand = collapse_rand.iloc[0] if len(collapse_rand) else np.nan

    peak_rand = df_rand["d2c"].idxmax()
    peak_load_rand = df_rand.loc[peak_rand, "load"]

    lead_rand = collapse_rand - peak_load_rand

    print(f"DENSE lead time : {lead_dense:.4f}")
    print(f"RANDOM lead time: {lead_rand:.4f}")

    summary.append({
        "case": case,
        "collapse_dense": collapse_dense,
        "peak_dense": peak_load_dense,
        "lead_dense": lead_dense,
        "collapse_random": collapse_rand,
        "peak_random": peak_load_rand,
        "lead_random": lead_rand
    })

    # --------------------------------------------------------
    # PLOT (KEY VALIDATION FIGURE)
    # --------------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(df_dense["load"], df_dense["c_struct"], label="c_struct")
    plt.plot(df_dense["load"], df_dense["d2c"], label="d²c (curvature)")

    if not np.isnan(collapse_dense):
        plt.axvline(collapse_dense, linestyle="--", label="collapse")

    plt.scatter(peak_load_dense, df_dense["d2c"].max(), color="red", label="d²c peak")

    plt.title(f"{case.upper()} — V32 Validation")
    plt.xlabel("Load")
    plt.ylabel("Value")
    plt.legend()
    plt.grid()

    plt.show()


# ------------------------------------------------------------
# SUMMARY TABLE
# ------------------------------------------------------------

summary_df = pd.DataFrame(summary)

print("\n--- VALIDATION SUMMARY ---")
print(summary_df)

summary_df.to_csv(
    os.path.join(OUTPUT_DIR, "ieee_validation_v32.csv"),
    index=False
)
