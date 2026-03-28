# run_ieee_scaling_law_v53.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")

CASE_SIZE = {
    "ieee9": 9,
    "ieee14": 14,
    "ieee30": 30,
    "ieee57": 57,
    "ieee118": 118
}

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("RUNNING V53 — SCALING LAW")

    file_path = BASE_PATH / "ieee_v43_manifold_fit.csv"

    if not file_path.exists():
        print("Missing file:", file_path)
        return

    df = pd.read_csv(file_path)

    # add system size
    df["N"] = df["case"].map(CASE_SIZE)

    # sort by size
    df = df.sort_values("N")

    print("\n--- SCALING DATA ---")
    print(df[["case", "N", "power_p", "power_q", "power_r2"]])

    # --------------------------------------------------
    # PLOT p(N), q(N)
    # --------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(df["N"], df["power_p"], marker="o", label="p (state exponent)")
    plt.plot(df["N"], df["power_q"], marker="o", label="q (drift exponent)")

    plt.xlabel("System Size (N buses)")
    plt.ylabel("Exponent Value")
    plt.title("Scaling Law — Exponents vs System Size (V53)")
    plt.legend()
    plt.grid()

    plt.savefig(BASE_PATH / "ieee_v53_scaling_law.png", dpi=150)
    plt.close()

    print("\nSaved:", BASE_PATH / "ieee_v53_scaling_law.png")


if __name__ == "__main__":
    main()
