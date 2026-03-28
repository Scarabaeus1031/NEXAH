# run_ieee_geometry_comparison_v54.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")

CASES = ["ieee30", "ieee57", "ieee118"]

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_data(case):
    file_path = BASE_PATH / f"{case}_v52_residual_vs_distance.csv"

    if not file_path.exists():
        print(f"Missing file: {file_path}")
        return None

    df = pd.read_csv(file_path)

    # Clean
    df = df.dropna()

    return df

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("RUNNING V54 — GEOMETRY COMPARISON")

    plt.figure(figsize=(8, 6))

    for case in CASES:
        print(f"\n--- {case.upper()} ---")

        df = load_data(case)

        if df is None:
            continue

        distance = df["distance"].values
        residual = df["residual"].values

        plt.scatter(
            distance,
            residual,
            label=case,
            alpha=0.6
        )

    plt.axhline(0, linestyle="--")

    plt.xlabel("Distance to Rift")
    plt.ylabel("Residual")
    plt.title("V54 — Collapse Geometry Comparison")
    plt.legend()
    plt.grid()

    out_path = BASE_PATH / "ieee_v54_geometry_comparison.png"
    plt.savefig(out_path, dpi=150)
    plt.close()

    print("\nSaved:", out_path)


if __name__ == "__main__":
    main()
