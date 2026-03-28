import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score, mean_squared_error

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")

CASES = ["ieee9", "ieee14", "ieee30"]

# --------------------------------------------------
# MODEL DEFINITIONS
# --------------------------------------------------

def power_law_model(X, a, p, q):
    c, dc = X
    return a * (c ** p) * (dc ** q)

def poly_model(X, a, b, c0):
    c, dc = X
    return a * c + b * dc + c0

# --------------------------------------------------
# FIT FUNCTION
# --------------------------------------------------

def fit_models(df, case_name):
    # Filter valid region (avoid collapse artifacts)
    df = df.copy()
    df = df[df["c"] > 0]
    df = df.dropna()

    # Normalize
    c = df["c"].values
    dc = np.gradient(c, df["load"].values)
    d2c = np.gradient(dc, df["load"].values)

    c_norm = c / np.max(c)
    dc_norm = dc / np.max(dc) if np.max(dc) != 0 else dc
    d2c_norm = d2c / np.max(d2c) if np.max(d2c) != 0 else d2c

    # Remove invalid
    mask = (c_norm > 0) & (dc_norm > 0)
    c_norm = c_norm[mask]
    dc_norm = dc_norm[mask]
    d2c_norm = d2c_norm[mask]

    # --------------------------------------------------
    # POWER LAW FIT
    # --------------------------------------------------

    try:
        popt_power, _ = curve_fit(
            power_law_model,
            (c_norm, dc_norm),
            d2c_norm,
            maxfev=10000
        )

        pred_power = power_law_model((c_norm, dc_norm), *popt_power)

        r2_power = r2_score(d2c_norm, pred_power)
        mse_power = mean_squared_error(d2c_norm, pred_power)

    except Exception as e:
        print(f"[{case_name}] Power fit failed:", e)
        popt_power = [np.nan, np.nan, np.nan]
        pred_power = np.zeros_like(d2c_norm)
        r2_power = np.nan
        mse_power = np.nan

    # --------------------------------------------------
    # POLY FIT
    # --------------------------------------------------

    try:
        popt_poly, _ = curve_fit(
            poly_model,
            (c_norm, dc_norm),
            d2c_norm,
            maxfev=10000
        )

        pred_poly = poly_model((c_norm, dc_norm), *popt_poly)

        r2_poly = r2_score(d2c_norm, pred_poly)
        mse_poly = mean_squared_error(d2c_norm, pred_poly)

    except Exception as e:
        print(f"[{case_name}] Poly fit failed:", e)
        popt_poly = [np.nan, np.nan, np.nan]
        pred_poly = np.zeros_like(d2c_norm)
        r2_poly = np.nan
        mse_poly = np.nan

    # --------------------------------------------------
    # PLOTS
    # --------------------------------------------------

    plt.figure(figsize=(10, 5))

    plt.scatter(d2c_norm, pred_power, label="Power-law fit", alpha=0.6)
    plt.scatter(d2c_norm, pred_poly, label="Poly fit", alpha=0.6)

    plt.plot([0, 1], [0, 1], "k--", label="Perfect fit")

    plt.xlabel("True d²c")
    plt.ylabel("Predicted d²c")
    plt.title(f"{case_name.upper()} — Fit Comparison (V43)")
    plt.legend()
    plt.grid()

    plt.savefig(BASE_PATH / f"{case_name}_v43_fit.png", dpi=150)
    plt.close()

    # Residual plot
    plt.figure(figsize=(10, 5))

    plt.scatter(d2c_norm, d2c_norm - pred_power, label="Power residuals", alpha=0.6)
    plt.scatter(d2c_norm, d2c_norm - pred_poly, label="Poly residuals", alpha=0.6)

    plt.axhline(0, linestyle="--")

    plt.xlabel("True d²c")
    plt.ylabel("Residual")
    plt.title(f"{case_name.upper()} — Residuals (V43)")
    plt.legend()
    plt.grid()

    plt.savefig(BASE_PATH / f"{case_name}_v43_residuals.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # RETURN RESULTS
    # --------------------------------------------------

    return {
        "case": case_name,
        "power_a": popt_power[0],
        "power_p": popt_power[1],
        "power_q": popt_power[2],
        "power_r2": r2_power,
        "power_mse": mse_power,
        "poly_a": popt_poly[0],
        "poly_b": popt_poly[1],
        "poly_c": popt_poly[2],
        "poly_r2": r2_poly,
        "poly_mse": mse_poly,
    }

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V43 — MANIFOLD EQUATION FIT")

    results = []

    for case in CASES:
        print(f"\n--- {case.upper()} ---")

        file_path = BASE_PATH / f"{case}_v43_dataset.csv"

        if not file_path.exists():
            print(f"Missing file: {file_path}")
            continue

        df = pd.read_csv(file_path)

        res = fit_models(df, case)
        results.append(res)

    df_out = pd.DataFrame(results)

    print("\n--- V43 RESULTS ---")
    print(df_out)

    df_out.to_csv(BASE_PATH / "ieee_v43_manifold_fit.csv", index=False)
    print("\nSaved:", BASE_PATH / "ieee_v43_manifold_fit.csv")


if __name__ == "__main__":
    main()
