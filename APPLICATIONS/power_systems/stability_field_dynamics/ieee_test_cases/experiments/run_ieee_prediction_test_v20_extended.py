import numpy as np
import pandas as pd
from pathlib import Path

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_physical_adapter_v1 import ieee_to_nexah

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")

CASES = ["ieee9", "ieee14", "ieee30", "ieee57", "ieee118"]

LOADS = np.linspace(0.6, 5.0, 60)


# --------------------------------------------------
# STRUCTURE METRIC
# --------------------------------------------------

def compute_c_struct(theta, C, loops):
    """
    Simple structural intensity metric
    (same philosophy as your earlier pipeline)
    """
    return np.std(theta) * np.std(C) * np.std(loops)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def process_case(case):

    print(f"\n--- {case.upper()} ---")

    results = []

    for load in LOADS:

        theta, C, loops, converged = ieee_to_nexah(case, load)

        if not converged:
            # collapse region → stop or mark
            results.append({
                "load": load,
                "c_struct": 0,
                "converged": False
            })
            continue

        c_struct = compute_c_struct(theta, C, loops)

        results.append({
            "load": load,
            "c_struct": c_struct,
            "converged": True
        })

    df = pd.DataFrame(results)

    out_path = BASE_PATH / f"{case}_prediction_test_v20.csv"
    df.to_csv(out_path, index=False)

    print(f"Saved: {out_path}")

    return df


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("RUNNING V20 EXTENDED — REAL DATA")

    for case in CASES:
        process_case(case)


if __name__ == "__main__":
    main()
