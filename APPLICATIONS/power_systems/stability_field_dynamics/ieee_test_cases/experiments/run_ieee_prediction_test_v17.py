# run_ieee_prediction_test_v17.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah,
)

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    detect_gh_corridor,
)

try:
    import pandapower as pp
    import pandapower.networks as pn
except ImportError:
    raise ImportError("pandapower required: pip install pandapower")


print("RUNNING IEEE PREDICTION TEST V17 (STRUCTURE vs PHYSICS)")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

LOADS = np.linspace(0.6, 5.0, 25)

OUTPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def get_min_voltage(case: str, load_scale: float):
    if case == "ieee14":
        net = pn.case14()
    elif case == "ieee9":
        net = pn.case9()
    else:
        raise ValueError(case)

    net.load["p_mw"] *= load_scale
    net.load["q_mvar"] *= load_scale

    try:
        pp.runpp(net, max_iteration=30, tolerance_mva=1e-6)
        return net.res_bus["vm_pu"].min(), True
    except:
        return np.nan, False


def compute_metrics(theta, c, loops):
    theta_std = np.std(theta)
    c_std = np.std(c)
    loops_mean = np.mean(loops)

    regime_separation = theta_std * c_std
    c_struct = regime_separation * loops_mean

    return theta_std, c_std, loops_mean, regime_separation, c_struct


# ------------------------------------------------------------
# MAIN ANALYSIS
# ------------------------------------------------------------

def run_case(case_name):

    results = []

    for load in LOADS:

        # --- PHYSICAL BASELINE ---
        min_v, converged_pf = get_min_voltage(case_name, load)

        # --- NEXAH ---
        theta, c, loops, converged_nexah = ieee_to_nexah(case_name, load_scale=load)

        if converged_nexah:
            theta_std, c_std, loops_mean, regime_sep, c_struct = compute_metrics(theta, c, loops)

            gh = detect_gh_corridor(theta, c, loops)
            gh_points = len(gh["theta_corridor"])
        else:
            theta_std = c_std = loops_mean = 0.0
            regime_sep = 0.0
            c_struct = 0.0
            gh_points = 0

        results.append({
            "load": load,
            "converged_pf": converged_pf,
            "converged_nexah": converged_nexah,
            "min_voltage": min_v,
            "theta_std": theta_std,
            "c_std": c_std,
            "loops_mean": loops_mean,
            "regime_separation": regime_sep,
            "c_struct": c_struct,
            "gh_points": gh_points,
        })

    return pd.DataFrame(results)


# ------------------------------------------------------------
# RUN BOTH SYSTEMS
# ------------------------------------------------------------

df14 = run_case("ieee14")
df9 = run_case("ieee9")

# Save
df14.to_csv(os.path.join(OUTPUT_DIR, "ieee14_v17.csv"), index=False)
df9.to_csv(os.path.join(OUTPUT_DIR, "ieee9_v17.csv"), index=False)


# ------------------------------------------------------------
# PLOTTING
# ------------------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(12, 10))


# IEEE14 — c_struct
axes[0, 0].plot(df14["load"], df14["c_struct"])
axes[0, 0].set_title("IEEE14 — c_struct")
axes[0, 0].grid()


# IEEE14 — Voltage
axes[0, 1].plot(df14["load"], df14["min_voltage"], color="orange")
axes[0, 1].axhline(0.7, linestyle="--")
axes[0, 1].set_title("IEEE14 — min(V)")
axes[0, 1].grid()


# IEEE9 — c_struct
axes[1, 0].plot(df9["load"], df9["c_struct"])
axes[1, 0].set_title("IEEE9 — c_struct")
axes[1, 0].grid()


# IEEE9 — Voltage
axes[1, 1].plot(df9["load"], df9["min_voltage"], color="orange")
axes[1, 1].axhline(0.7, linestyle="--")
axes[1, 1].set_title("IEEE9 — min(V)")
axes[1, 1].grid()


plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print("\n--- SUMMARY IEEE14 ---")
print(df14[["load", "c_struct", "min_voltage"]])

print("\n--- SUMMARY IEEE9 ---")
print(df9[["load", "c_struct", "min_voltage"]])
