# run_ieee_prediction_test_v30.py

import os
import numpy as np
import pandas as pd

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah,
)

try:
    import pandapower as pp
    import pandapower.networks as pn
except:
    raise ImportError("pip install pandapower")


print("RUNNING IEEE30 BENCHMARK (NEXAH vs CLASSICAL)")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

LOADS = np.linspace(0.6, 5.0, 60)

OUTPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# CLASSICAL BASELINE
# ------------------------------------------------------------

def get_min_voltage(case, load):

    if case == "ieee30":
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


# ------------------------------------------------------------
# NEXAH METRICS
# ------------------------------------------------------------

def compute_metrics(theta, c, loops):

    theta_std = np.std(theta)
    c_std = np.std(c)
    loops_mean = np.mean(loops)
    loops_std = np.std(loops)

    regime_sep = theta_std * c_std
    c_struct = regime_sep * loops_mean

    fragmentation = theta_std * loops_std

    return c_struct, fragmentation


# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------

rows = []

for load in LOADS:

    # Classical
    min_v, converged = get_min_voltage("ieee30", load)

    # NEXAH
    theta, c, loops, conv2 = ieee_to_nexah("ieee30", load)

    if converged:
        c_struct, fragmentation = compute_metrics(theta, c, loops)
    else:
        c_struct = np.nan
        fragmentation = np.nan

    rows.append({
        "load": load,
        "converged": converged,
        "min_voltage": min_v,
        "c_struct": c_struct,
        "fragmentation": fragmentation,
    })


df = pd.DataFrame(rows)

# Derivatives
df["dc"] = np.gradient(df["c_struct"])
df["d2c"] = np.gradient(df["dc"])


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

csv_path = os.path.join(OUTPUT_DIR, "ieee30_benchmark.csv")
df.to_csv(csv_path, index=False)

print("\n--- RESULTS ---")
print(df)
print(f"\nSaved: {csv_path}")


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

collapse = df[df["converged"] == False]

if len(collapse) > 0:
    collapse_load = collapse.iloc[0]["load"]
else:
    collapse_load = np.nan

print("\n--- SUMMARY ---")
print("Collapse load:", collapse_load)

print("\nMax c_struct:", df["c_struct"].max())
print("Max d2c:", df["d2c"].max())
