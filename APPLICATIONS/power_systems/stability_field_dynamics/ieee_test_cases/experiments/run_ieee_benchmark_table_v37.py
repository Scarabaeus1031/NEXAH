# run_ieee_benchmark_table_v37.py

import numpy as np
import pandas as pd

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import (
    ieee_to_nexah
)


CASES = ["ieee9", "ieee14", "ieee30"]


def compute_metrics(case):

    loads = np.linspace(0.6, 5.0, 80)

    c_struct_list = []
    voltage_min_list = []
    converged_list = []

    for load in loads:
        theta, C, loops, conv = ieee_to_nexah(case, load)

        converged_list.append(conv)

        if not conv:
            c_struct_list.append(np.nan)
            voltage_min_list.append(np.nan)
            continue

        c_struct = np.std(C) * np.mean(loops)
        c_struct_list.append(c_struct)

        V = 1.0 - C
        voltage_min_list.append(np.min(V))

    df = pd.DataFrame({
        "load": loads,
        "c_struct": c_struct_list,
        "min_V": voltage_min_list,
        "converged": converged_list
    })

    # collapse
    collapse_idx = df["converged"] == False
    collapse_load = df.loc[collapse_idx, "load"].min()

    df_valid = df[df["converged"]]

    # derivatives
    df_valid["dc"] = np.gradient(df_valid["c_struct"], df_valid["load"])
    df_valid["d2c"] = np.gradient(df_valid["dc"], df_valid["load"])

    df_valid["dV"] = np.gradient(df_valid["min_V"], df_valid["load"])

    # peaks
    d2c_peak_load = df_valid.loc[df_valid["d2c"].idxmax(), "load"]
    dV_peak_load = df_valid.loc[df_valid["dV"].idxmin(), "load"]

    return {
        "case": case,
        "collapse": collapse_load,
        "d2c_peak": d2c_peak_load,
        "dV_peak": dV_peak_load,
        "lead_d2c": collapse_load - d2c_peak_load,
        "lead_dV": collapse_load - dV_peak_load
    }


def run():

    results = []

    for case in CASES:
        print(f"Running {case}...")
        res = compute_metrics(case)
        results.append(res)

    df = pd.DataFrame(results)

    print("\n--- BENCHMARK TABLE ---")
    print(df)

    df.to_csv(
        "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee_v37_benchmark.csv",
        index=False
    )


if __name__ == "__main__":
    run()
