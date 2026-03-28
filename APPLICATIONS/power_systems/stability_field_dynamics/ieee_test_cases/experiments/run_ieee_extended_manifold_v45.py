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
# MODELS
# --------------------------------------------------

def base_model(X, a, p, q):
    c, dc = X
    return a * (c ** p) * (dc ** q)

def extended_model(X, a, p, q, b):
    c, dc = X
    return a * (c ** p) * (dc ** q) + b * c * dc

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

def analyze_case(case):

    file_path = BASE_PATH / f"{case}_v43_dataset.csv"

    if not file_path.exists():
        print(f"Missing file: {file_path}")
        return None

    df = pd.read_csv(file_path).dropna()

    load = df["load"].values
    c = df["c"].values

    dc = np.gradient(c, load)
    d2c = np.gradient(dc, load)

    # Normalize
    c_norm = c / np.max(c)
    dc_norm = dc / np.max(dc) if np.max(dc) != 0 else dc
    d2c_norm = d2c / np.max(d2c) if np.max(d2c) != 0 else d2c

    mask = (c_norm > 0) & (dc_norm > 0)
    c_norm = c_norm[mask]
    dc_norm = dc_norm[mask]
    d2c_norm = d2c_norm[mask]

    # --------------------------------------------------
    # BASE FIT (V43)
    # --------------------------------------------------

    popt_base, _ = curve_fit(
        base_model,
        (c_norm, dc_norm),
        d2c_norm,
        maxfev=10000
    )

    pred_base = base_model((c_norm, dc_norm), *popt_base)

    r2_base = r2_score(d2c_norm, pred_base)
    mse_base = mean_squared_error(d2c_norm, pred_base)

    # --------------------------------------------------
    # EXTENDED FIT (V45)
    # --------------------------------------------------

    popt_ext, _ = curve_fit(
        extended_model,
        (c_norm, dc_norm),
        d2c_norm,
        maxfev=20000
    )

    pred_ext = extended_model((c_norm, dc_norm), *popt_ext)

    r2_ext = r2_score(d2c_norm, pred_ext)
    mse_ext = mean_squared_error(d2c_norm, pred_ext)

    # --------------------------------------------------
    # RESIDUALS
    # --------------------------------------------------

    res_base = d2c_norm - pred_base
    res_ext = d2c_norm - pred_ext

    # --------------------------------------------------
    # PLOTS
    # --------------------------------------------------

    # Fit comparison
    plt.figure(figsize=(6,6))
    plt.scatter(d2c_norm, pred_base, label="Base (V43)", alpha=0.6)
    plt.scatter(d2c_norm, pred_ext, label="Extended (V45)", alpha=0.6)
    plt.plot([0,1],[0,1],'k--')
    plt.xlabel("True d²c")
    plt.ylabel("Predicted d²c")
    plt.title(f"{case.upper()} — Fit Comparison (V45)")
    plt.legend()
    plt.grid()
    plt.savefig(BASE_PATH / f"{case}_v45_fit.png", dpi=150)
    plt.close()

    # Residual comparison
    plt.figure(figsize=(10,4))
    plt.plot(res_base, label="Base residual")
    plt.plot(res_ext, label="Extended residual")
    plt.axhline(0, linestyle="--")
    plt.title(f"{case.upper()} — Residual Comparison (V45)")
    plt.legend()
    plt.grid()
    plt.savefig(BASE_PATH / f"{case}_v45_residuals.png", dpi=150)
    plt.close()

    return {
        "case": case,
        "r2_base": r2_base,
        "r2_ext": r2_ext,
        "mse_base": mse_base,
        "mse_ext": mse_ext,
        "b_term": popt_ext[3]
    }

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V45 — EXTENDED MANIFOLD TEST")

    results = []

    for case in CASES:
        print(f"\n--- {case.upper()} ---")
        res = analyze_case(case)
        if res:
            results.append(res)

    df_out = pd.DataFrame(results)

    print("\n--- V45 RESULTS ---")
    print(df_out)

    df_out.to_csv(BASE_PATH / "ieee_v45_extended_fit.csv", index=False)
    print("\nSaved:", BASE_PATH / "ieee_v45_extended_fit.csv")


if __name__ == "__main__":
    main()
