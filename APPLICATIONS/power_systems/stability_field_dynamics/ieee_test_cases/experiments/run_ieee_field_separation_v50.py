# run_ieee_field_separation_v50.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import griddata

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee9", "ieee14", "ieee30"]
GRID_RES = 60

# --------------------------------------------------
# LOAD FIT PARAMETERS
# --------------------------------------------------

fit_df = pd.read_csv(BASE_PATH / "ieee_v43_manifold_fit.csv")

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def normalize_safe(x):
    x = np.asarray(x, dtype=float)
    max_val = np.max(np.abs(x))
    if max_val == 0:
        return x
    return x / max_val

def power_model(c, dc, a, p, q):
    # magnitude-based version to avoid NaNs for fractional q
    return a * (np.abs(c) ** p) * (np.abs(dc) ** q)

def load_case_dataset(case):
    file_path = BASE_PATH / f"{case}_v43_dataset.csv"
    if not file_path.exists():
        print(f"Missing file: {file_path}")
        return None
    df = pd.read_csv(file_path).dropna()
    return df

def prepare_data(df):
    c = df["c"].values
    dc = df["dc"].values
    d2c = df["d2c"].values

    c_norm = normalize_safe(c)
    dc_norm = normalize_safe(dc)
    d2c_norm = normalize_safe(d2c)

    return c_norm, dc_norm, d2c_norm

def build_grid_field(c, dc, values, grid_res=60, method="linear"):
    xi = np.linspace(0, 1, grid_res)
    yi = np.linspace(0, 1, grid_res)
    X, Y = np.meshgrid(xi, yi)

    Z = griddata(
        (c, dc),
        values,
        (X, Y),
        method=method,
        fill_value=np.nan
    )

    return X, Y, Z

def compute_curl(U, V):
    dVdx = np.gradient(V, axis=1)
    dUdy = np.gradient(U, axis=0)
    return dVdx - dUdy

# --------------------------------------------------
# MAIN ANALYSIS
# --------------------------------------------------

def process_case(case):

    print(f"\n--- {case.upper()} ---")

    df = load_case_dataset(case)
    if df is None:
        return None

    c_norm, dc_norm, d2c_norm = prepare_data(df)

    # Load power-law params
    params = fit_df[fit_df["case"] == case].iloc[0]
    a, p, q = params["power_a"], params["power_p"], params["power_q"]

    # --------------------------------------------------
    # Decompose field
    # --------------------------------------------------

    d2c_model = power_model(c_norm, dc_norm, a, p, q)
    d2c_resid = d2c_norm - d2c_model
    d2c_total = d2c_norm

    # --------------------------------------------------
    # Build grid fields
    # --------------------------------------------------

    X, Y, V_model = build_grid_field(c_norm, dc_norm, d2c_model, GRID_RES)
    _, _, V_resid = build_grid_field(c_norm, dc_norm, d2c_resid, GRID_RES)
    _, _, V_total = build_grid_field(c_norm, dc_norm, d2c_total, GRID_RES)

    # U field is common "horizontal drift"
    _, _, U_field = build_grid_field(c_norm, dc_norm, dc_norm, GRID_RES)

    # Replace NaNs for plotting / curl
    U_plot = np.nan_to_num(U_field, nan=0.0)
    V_model_plot = np.nan_to_num(V_model, nan=0.0)
    V_resid_plot = np.nan_to_num(V_resid, nan=0.0)
    V_total_plot = np.nan_to_num(V_total, nan=0.0)

    # --------------------------------------------------
    # 1) Three-field quiver comparison
    # --------------------------------------------------

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    fields = [
        ("Model Field", V_model_plot),
        ("Residual Field", V_resid_plot),
        ("Total Field", V_total_plot),
    ]

    for ax, (title, Vfield) in zip(axes, fields):
        step = 4
        ax.quiver(
            X[::step, ::step],
            Y[::step, ::step],
            U_plot[::step, ::step],
            Vfield[::step, ::step],
            angles="xy",
            scale_units="xy",
            scale=8,
            alpha=0.8
        )
        ax.scatter(c_norm, dc_norm, c=np.linspace(0, 1, len(c_norm)), cmap="viridis", s=18)
        ax.set_title(f"{case.upper()} — {title} (V50)")
        ax.set_xlabel("c (norm)")
        ax.set_ylabel("dc (norm)")
        ax.grid(True)

    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v50_field_separation.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 2) Heatmaps of vertical component
    # --------------------------------------------------

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    heatmaps = [
        ("Model d²c", V_model_plot),
        ("Residual d²c", V_resid_plot),
        ("Total d²c", V_total_plot),
    ]

    for ax, (title, Z) in zip(axes, heatmaps):
        im = ax.imshow(
            Z,
            extent=[0, 1, 0, 1],
            origin="lower",
            aspect="auto"
        )
        ax.set_title(f"{case.upper()} — {title} (V50)")
        ax.set_xlabel("c")
        ax.set_ylabel("dc")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v50_heatmaps.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 3) Curl comparison
    # --------------------------------------------------

    curl_model = compute_curl(U_plot, V_model_plot)
    curl_resid = compute_curl(U_plot, V_resid_plot)
    curl_total = compute_curl(U_plot, V_total_plot)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    curls = [
        ("Model Curl", curl_model),
        ("Residual Curl", curl_resid),
        ("Total Curl", curl_total),
    ]

    curl_means = {}
    curl_max = {}

    for ax, (title, C) in zip(axes, curls):
        im = ax.imshow(
            C,
            extent=[0, 1, 0, 1],
            origin="lower",
            aspect="auto"
        )
        ax.set_title(f"{case.upper()} — {title} (V50)")
        ax.set_xlabel("c")
        ax.set_ylabel("dc")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

        curl_means[title] = float(np.nanmean(np.abs(C)))
        curl_max[title] = float(np.nanmax(np.abs(C)))

    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v50_curl_separation.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # Summary metrics
    # --------------------------------------------------

    residual_std = float(np.nanstd(d2c_resid))
    residual_max = float(np.nanmax(np.abs(d2c_resid)))

    return {
        "case": case,
        "residual_std": residual_std,
        "residual_max": residual_max,
        "model_curl_mean": curl_means["Model Curl"],
        "resid_curl_mean": curl_means["Residual Curl"],
        "total_curl_mean": curl_means["Total Curl"],
        "model_curl_max": curl_max["Model Curl"],
        "resid_curl_max": curl_max["Residual Curl"],
        "total_curl_max": curl_max["Total Curl"],
    }

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V50 — FIELD SEPARATION")

    results = []

    for case in CASES:
        try:
            res = process_case(case)
            if res:
                results.append(res)
        except Exception as e:
            print(f"[{case}] ERROR: {e}")

    df_out = pd.DataFrame(results)

    print("\n--- V50 SUMMARY ---")
    print(df_out)

    out_file = BASE_PATH / "ieee_v50_field_separation_summary.csv"
    df_out.to_csv(out_file, index=False)
    print("\nSaved:", out_file)

if __name__ == "__main__":
    main()
