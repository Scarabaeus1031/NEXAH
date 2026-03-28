# run_ieee_phase_regime_manifold_v46.py

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

# Split between early/stable and late/pre-collapse regime
REGIME_THRESHOLD = 0.60

# --------------------------------------------------
# MODELS
# --------------------------------------------------

def regime_model(X, a, p, q, b, s):
    """
    d2c = a * c^p * dc^q + b * c * dc + s * tau
    """
    c, dc, tau = X
    return a * (c ** p) * (dc ** q) + b * c * dc + s * tau


def safe_clip_positive(x, eps=1e-9):
    return np.clip(x, eps, None)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def load_case_dataset(case: str):
    file_path = BASE_PATH / f"{case}_v43_dataset.csv"

    if not file_path.exists():
        print(f"Missing file: {file_path}")
        return None

    df = pd.read_csv(file_path).dropna().copy()

    required = {"load", "c", "dc", "d2c"}
    if not required.issubset(df.columns):
        print(f"{case}: dataset missing required columns {required}")
        return None

    return df


def normalize_series(x):
    x = np.asarray(x, dtype=float)
    xmin = np.min(x)
    xmax = np.max(x)
    if np.isclose(xmax - xmin, 0.0):
        return np.zeros_like(x)
    return (x - xmin) / (xmax - xmin)


def prepare_data(df: pd.DataFrame):
    load = df["load"].values
    c = df["c"].values
    dc = df["dc"].values
    d2c = df["d2c"].values

    # normalize
    c_norm = normalize_series(c)
    dc_norm = normalize_series(dc)
    d2c_norm = normalize_series(d2c)

    # phase coordinate
    tau = normalize_series(load)

    # keep positive region for power-law part
    c_pos = safe_clip_positive(c_norm)
    dc_pos = safe_clip_positive(dc_norm)

    out = pd.DataFrame({
        "load": load,
        "tau": tau,
        "c_norm": c_norm,
        "dc_norm": dc_norm,
        "d2c_norm": d2c_norm,
        "c_pos": c_pos,
        "dc_pos": dc_pos,
    })

    return out


def fit_single_regime(df_regime: pd.DataFrame, regime_name: str, case: str):
    c = df_regime["c_pos"].values
    dc = df_regime["dc_pos"].values
    tau = df_regime["tau"].values
    y = df_regime["d2c_norm"].values

    if len(y) < 6:
        return None

    try:
        popt, _ = curve_fit(
            regime_model,
            (c, dc, tau),
            y,
            maxfev=50000,
            p0=[1.0, 0.5, 1.0, 0.5, 0.1]
        )

        pred = regime_model((c, dc, tau), *popt)
        r2 = r2_score(y, pred)
        mse = mean_squared_error(y, pred)
        residuals = y - pred

        return {
            "case": case,
            "regime": regime_name,
            "a": popt[0],
            "p": popt[1],
            "q": popt[2],
            "b": popt[3],
            "s": popt[4],
            "r2": r2,
            "mse": mse,
            "pred": pred,
            "true": y,
            "residuals": residuals,
            "tau": tau,
            "c_norm": df_regime["c_norm"].values
        }

    except Exception as e:
        print(f"[{case} | {regime_name}] fit failed: {e}")
        return None


def plot_case(case: str, full_df: pd.DataFrame, safe_fit: dict, critical_fit: dict):
    plt.figure(figsize=(7, 7))

    # raw
    plt.scatter(
        full_df["c_norm"],
        full_df["d2c_norm"],
        s=25,
        alpha=0.5,
        label="True trajectory"
    )

    if safe_fit is not None:
        plt.scatter(
            safe_fit["c_norm"],
            safe_fit["pred"],
            s=20,
            alpha=0.8,
            label="SAFE/WARNING fit"
        )

    if critical_fit is not None:
        plt.scatter(
            critical_fit["c_norm"],
            critical_fit["pred"],
            s=20,
            alpha=0.8,
            label="CRITICAL fit"
        )

    plt.axvline(REGIME_THRESHOLD, linestyle="--", linewidth=1, label="Regime split")
    plt.xlabel("c (norm)")
    plt.ylabel("d²c (norm)")
    plt.title(f"{case.upper()} — Phase + Regime Model (V46)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v46_fit.png", dpi=150)
    plt.close()

    # residual trace
    plt.figure(figsize=(10, 4))

    if safe_fit is not None:
        plt.plot(
            safe_fit["residuals"],
            label="SAFE/WARNING residuals"
        )

    if critical_fit is not None:
        offset = len(safe_fit["residuals"]) if safe_fit is not None else 0
        x = np.arange(offset, offset + len(critical_fit["residuals"]))
        plt.plot(
            x,
            critical_fit["residuals"],
            label="CRITICAL residuals"
        )

    plt.axhline(0, linestyle="--", linewidth=1)
    plt.title(f"{case.upper()} — Residuals (V46)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v46_residuals.png", dpi=150)
    plt.close()


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V46 — PHASE + REGIME AWARE EQUATION")

    rows = []

    for case in CASES:
        print(f"\n--- {case.upper()} ---")

        raw_df = load_case_dataset(case)
        if raw_df is None:
            continue

        df = prepare_data(raw_df)

        df_safe = df[df["c_norm"] < REGIME_THRESHOLD].copy()
        df_critical = df[df["c_norm"] >= REGIME_THRESHOLD].copy()

        safe_fit = fit_single_regime(df_safe, "SAFE_WARNING", case)
        critical_fit = fit_single_regime(df_critical, "CRITICAL", case)

        plot_case(case, df, safe_fit, critical_fit)

        if safe_fit is not None:
            rows.append({
                "case": case,
                "regime": "SAFE_WARNING",
                "a": safe_fit["a"],
                "p": safe_fit["p"],
                "q": safe_fit["q"],
                "b": safe_fit["b"],
                "s_tau": safe_fit["s"],
                "r2": safe_fit["r2"],
                "mse": safe_fit["mse"],
            })

        if critical_fit is not None:
            rows.append({
                "case": case,
                "regime": "CRITICAL",
                "a": critical_fit["a"],
                "p": critical_fit["p"],
                "q": critical_fit["q"],
                "b": critical_fit["b"],
                "s_tau": critical_fit["s"],
                "r2": critical_fit["r2"],
                "mse": critical_fit["mse"],
            })

    df_out = pd.DataFrame(rows)

    print("\n--- V46 RESULTS ---")
    print(df_out)

    out_file = BASE_PATH / "ieee_v46_phase_regime_fit.csv"
    df_out.to_csv(out_file, index=False)
    print(f"\nSaved: {out_file}")


if __name__ == "__main__":
    main()
