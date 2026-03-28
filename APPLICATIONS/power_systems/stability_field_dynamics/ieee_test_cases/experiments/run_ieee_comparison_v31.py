# run_ieee_comparison_v31.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v2 import (
    ieee_to_nexah,
)

try:
    import pandapower as pp
    import pandapower.networks as pn
except ImportError:
    raise ImportError("pandapower required: pip install pandapower")


print("RUNNING IEEE COMPARISON V31 (MULTI-SYSTEM VALIDATION)")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

SYSTEMS = ["ieee9", "ieee14", "ieee30"]
LOADS = np.linspace(0.6, 5.0, 60)

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
    theta_std = np.std(theta)
    c_std = np.std(c)
    loops_mean = np.mean(loops)

    return theta_std * c_std * loops_mean


def compute_derivatives(loads, values):
    dc = np.gradient(values, loads)
    d2c = np.gradient(dc, loads)
    return dc, d2c


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

all_results = {}

for case in SYSTEMS:

    rows = []

    for load in LOADS:

        min_v, conv_phys = get_min_voltage(case, load)

        theta, c, loops, conv_nexah = ieee_to_nexah(case, load)

        if conv_phys and conv_nexah:
            c_struct = compute_c_struct(theta, c, loops)
        else:
            c_struct = np.nan

        rows.append({
            "load": load,
            "min_voltage": min_v,
            "c_struct": c_struct,
            "converged": conv_phys
        })

    df = pd.DataFrame(rows)

    # derivatives only on valid region
    valid = df["c_struct"].notna()

    dc, d2c = compute_derivatives(
        df.loc[valid, "load"].values,
        df.loc[valid, "c_struct"].values
    )

    df.loc[valid, "dc"] = dc
    df.loc[valid, "d2c"] = d2c

    all_results[case] = df

    # save per system
    df.to_csv(
        os.path.join(OUTPUT_DIR, f"{case}_v31.csv"),
        index=False
    )


# ------------------------------------------------------------
# PLOTTING (KEY FIGURE)
# ------------------------------------------------------------

fig, axes = plt.subplots(3, 1, figsize=(10, 14), sharex=True)

for i, case in enumerate(SYSTEMS):

    df = all_results[case]

    # --------------------------------------------------------
    # Plot 1: Voltage
    # --------------------------------------------------------
    ax = axes[i]

    ax.plot(df["load"], df["min_voltage"], label="min(V)", linestyle="--")

    # --------------------------------------------------------
    # Plot 2: c_struct
    # --------------------------------------------------------
    ax.plot(df["load"], df["c_struct"], label="c_struct")

    # --------------------------------------------------------
    # Plot 3: curvature
    # --------------------------------------------------------
    ax.plot(df["load"], df["d2c"], label="d²c (curvature)")

    # collapse marker
    collapse_idx = df["converged"] == False
    if collapse_idx.any():
        collapse_load = df.loc[collapse_idx, "load"].iloc[0]
        ax.axvline(collapse_load, linestyle=":", label="collapse")

    ax.set_title(f"{case.upper()} — Structure vs Physics")
    ax.set_ylabel("Value")
    ax.grid()
    ax.legend()

axes[-1].set_xlabel("Load")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# SUMMARY TABLE
# ------------------------------------------------------------

summary = []

for case, df in all_results.items():

    collapse = df.loc[df["converged"] == False, "load"]
    collapse_load = collapse.iloc[0] if len(collapse) > 0 else np.nan

    valid = df["d2c"].notna()

    d2c_peak = df.loc[valid, "load"][df.loc[valid, "d2c"].idxmax()]

    summary.append({
        "case": case,
        "collapse_load": collapse_load,
        "d2c_peak": d2c_peak,
        "lead_time": collapse_load - d2c_peak
    })

summary_df = pd.DataFrame(summary)

print("\n--- SUMMARY ---")
print(summary_df)

summary_df.to_csv(
    os.path.join(OUTPUT_DIR, "ieee_comparison_v31_summary.csv"),
    index=False
)
