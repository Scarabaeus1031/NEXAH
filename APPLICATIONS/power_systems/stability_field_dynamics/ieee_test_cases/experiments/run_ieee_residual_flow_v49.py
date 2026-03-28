import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee9", "ieee14", "ieee30"]

# --------------------------------------------------
# LOAD V43 FIT PARAMETERS
# --------------------------------------------------

fit_df = pd.read_csv(BASE_PATH / "ieee_v43_manifold_fit.csv")

# --------------------------------------------------
# POWER LAW MODEL
# --------------------------------------------------

def power_model(c, dc, a, p, q):
    return a * (c ** p) * (dc ** q)

# --------------------------------------------------
# NORMALIZATION (robust)
# --------------------------------------------------

def normalize_safe(x):
    max_val = np.max(np.abs(x))
    if max_val == 0:
        return x
    return x / max_val

# --------------------------------------------------
# MAIN ANALYSIS
# --------------------------------------------------

def process_case(case):

    print(f"\n--- {case.upper()} ---")

    data_path = BASE_PATH / f"{case}_v43_dataset.csv"

    if not data_path.exists():
        print("Missing dataset:", data_path)
        return None

    df = pd.read_csv(data_path)
    print("Columns:", df.columns.tolist())

    # --------------------------------------------------
    # Extract raw data
    # --------------------------------------------------

    c = df["c"].values
    dc = df["dc"].values
    d2c = df["d2c"].values

    # --------------------------------------------------
    # Normalize
    # --------------------------------------------------

    c_norm = normalize_safe(c)
    dc_norm = normalize_safe(dc)
    d2c_norm = normalize_safe(d2c)

    # --------------------------------------------------
    # Get model params
    # --------------------------------------------------

    params = fit_df[fit_df["case"] == case].iloc[0]
    a, p, q = params["power_a"], params["power_p"], params["power_q"]

    # --------------------------------------------------
    # Compute model + residual
    # --------------------------------------------------

    d2c_model = power_model(c_norm, dc_norm, a, p, q)
    residual = d2c_norm - d2c_model

    # --------------------------------------------------
    # Residual Flow Field
    # --------------------------------------------------

    plt.figure(figsize=(8, 6))

    sc = plt.scatter(c_norm, dc_norm, c=residual, cmap="coolwarm", s=40)
    plt.colorbar(sc, label="Residual (true - model)")

    # residual arrows
    for i in range(1, len(c_norm)):
        plt.arrow(
            c_norm[i-1],
            dc_norm[i-1],
            0,
            residual[i] * 0.2,
            head_width=0.01,
            alpha=0.5,
            color="black"
        )

    plt.xlabel("c (norm)")
    plt.ylabel("dc (norm)")
    plt.title(f"{case.upper()} — Residual Flow Field (V49)")
    plt.grid()

    plt.savefig(BASE_PATH / f"{case}_v49_residual_flow.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # Residual vs c
    # --------------------------------------------------

    plt.figure(figsize=(8, 5))

    sc = plt.scatter(c_norm, residual, c=residual, cmap="coolwarm")
    plt.axhline(0, linestyle="--")

    plt.xlabel("c (norm)")
    plt.ylabel("Residual")
    plt.title(f"{case.upper()} — Residual Structure (V49)")
    plt.grid()

    plt.savefig(BASE_PATH / f"{case}_v49_residual_vs_c.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # Hotspots
    # --------------------------------------------------

    threshold = np.std(residual)
    hotspots = np.abs(residual) > threshold

    return {
        "case": case,
        "mean_residual": float(np.mean(residual)),
        "std_residual": float(np.std(residual)),
        "num_hotspots": int(np.sum(hotspots))
    }

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("RUNNING V49 — RESIDUAL FLOW FIELD")

    results = []

    for case in CASES:
        try:
            res = process_case(case)
            if res:
                results.append(res)
        except Exception as e:
            print(f"[{case}] ERROR:", e)

    df_out = pd.DataFrame(results)

    print("\n--- V49 SUMMARY ---")
    print(df_out)

    df_out.to_csv(BASE_PATH / "ieee_v49_residual_summary.csv", index=False)
    print("\nSaved:", BASE_PATH / "ieee_v49_residual_summary.csv")


if __name__ == "__main__":
    main()
