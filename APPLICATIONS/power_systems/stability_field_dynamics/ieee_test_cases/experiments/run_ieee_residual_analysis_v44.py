import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit
from scipy.fft import fft
from sklearn.metrics import r2_score

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee9", "ieee14", "ieee30"]

# --------------------------------------------------
# MODEL
# --------------------------------------------------

def power_law_model(X, a, p, q):
    c, dc = X
    return a * (c ** p) * (dc ** q)

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

    # normalize
    c_norm = c / np.max(c)
    dc_norm = dc / np.max(dc) if np.max(dc) != 0 else dc
    d2c_norm = d2c / np.max(d2c) if np.max(d2c) != 0 else d2c

    mask = (c_norm > 0) & (dc_norm > 0)
    c_norm = c_norm[mask]
    dc_norm = dc_norm[mask]
    d2c_norm = d2c_norm[mask]

    # --------------------------------------------------
    # FIT
    # --------------------------------------------------

    popt, _ = curve_fit(
        power_law_model,
        (c_norm, dc_norm),
        d2c_norm,
        maxfev=10000
    )

    pred = power_law_model((c_norm, dc_norm), *popt)

    residuals = d2c_norm - pred

    # --------------------------------------------------
    # METRICS
    # --------------------------------------------------

    r2 = r2_score(d2c_norm, pred)
    residual_std = np.std(residuals)

    # --------------------------------------------------
    # PLOTS
    # --------------------------------------------------

    # 1. Residual vs Load
    plt.figure(figsize=(10, 4))
    plt.plot(residuals, label="Residual")
    plt.axhline(0, linestyle="--")
    plt.title(f"{case.upper()} — Residual over trajectory")
    plt.grid()
    plt.legend()
    plt.savefig(BASE_PATH / f"{case}_v44_residual_trace.png", dpi=150)
    plt.close()

    # 2. Residual vs c
    plt.figure(figsize=(6, 6))
    plt.scatter(c_norm, residuals, alpha=0.6)
    plt.axhline(0, linestyle="--")
    plt.xlabel("c (norm)")
    plt.ylabel("Residual")
    plt.title(f"{case.upper()} — Residual vs c")
    plt.grid()
    plt.savefig(BASE_PATH / f"{case}_v44_residual_vs_c.png", dpi=150)
    plt.close()

    # 3. Residual histogram
    plt.figure(figsize=(6, 4))
    plt.hist(residuals, bins=30)
    plt.title(f"{case.upper()} — Residual distribution")
    plt.grid()
    plt.savefig(BASE_PATH / f"{case}_v44_residual_hist.png", dpi=150)
    plt.close()

    # 4. Fourier (structure detection)
    fft_vals = np.abs(fft(residuals))
    plt.figure(figsize=(10, 4))
    plt.plot(fft_vals)
    plt.title(f"{case.upper()} — Residual Fourier Spectrum")
    plt.grid()
    plt.savefig(BASE_PATH / f"{case}_v44_residual_fft.png", dpi=150)
    plt.close()

    return {
        "case": case,
        "r2": r2,
        "residual_std": residual_std,
        "a": popt[0],
        "p": popt[1],
        "q": popt[2]
    }

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V44 — RESIDUAL STRUCTURE ANALYSIS")

    results = []

    for case in CASES:
        print(f"\n--- {case.upper()} ---")
        res = analyze_case(case)
        if res:
            results.append(res)

    df_out = pd.DataFrame(results)

    print("\n--- V44 SUMMARY ---")
    print(df_out)

    df_out.to_csv(BASE_PATH / "ieee_v44_residual_analysis.csv", index=False)
    print("\nSaved:", BASE_PATH / "ieee_v44_residual_analysis.csv")


if __name__ == "__main__":
    main()
