# run_ieee_stability_distance_v52.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import griddata
from scipy.spatial import cKDTree

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee9", "ieee14", "ieee30", "ieee57", "ieee118"]

GRID_RES = 140
EPS = 0.03  # residual≈0 tolerance for rift extraction

# --------------------------------------------------
# LOAD FIT PARAMETERS
# --------------------------------------------------

fit_df = pd.read_csv(BASE_PATH / "ieee_v43_manifold_fit.csv")

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def normalize_safe(x):
    x = np.asarray(x, dtype=float)
    m = np.max(np.abs(x))
    if m == 0:
        return x
    return x / m


def power_model(c, dc, a, p, q):
    return a * (np.abs(c) ** p) * (np.abs(dc) ** q)


def load_case_dataset(case):
    file_path = BASE_PATH / f"{case}_v43_dataset.csv"
    if not file_path.exists():
        print(f"Missing file: {file_path}")
        return None
    return pd.read_csv(file_path).dropna()


def prepare_data(df):
    c = normalize_safe(df["c"].values)
    dc = normalize_safe(df["dc"].values)
    d2c = normalize_safe(df["d2c"].values)
    load = df["load"].values
    tau = (load - np.min(load)) / (np.max(load) - np.min(load)) if np.max(load) > np.min(load) else np.zeros_like(load)
    return c, dc, d2c, tau


def build_grid(c, dc, z, grid_res=140):
    xi = np.linspace(0, 1, grid_res)
    yi = np.linspace(0, 1, grid_res)
    X, Y = np.meshgrid(xi, yi)

    Z = griddata(
        (c, dc),
        z,
        (X, Y),
        method="linear",
        fill_value=np.nan
    )

    return X, Y, Z


def extract_rift_points(X, Y, R, eps=0.03):
    valid = np.isfinite(R)
    mask = valid & (np.abs(R) < eps)

    xr = X[mask]
    yr = Y[mask]

    if len(xr) == 0:
        return np.array([]), np.array([])

    order = np.argsort(xr)
    return xr[order], yr[order]


def compute_stability_distance(c, dc, xr, yr):
    if len(xr) == 0:
        return np.full_like(c, np.nan, dtype=float)

    tree = cKDTree(np.column_stack([xr, yr]))
    dist, _ = tree.query(np.column_stack([c, dc]), k=1)
    return dist


def estimate_collapse_strength(residual, stability_distance):
    r = np.abs(residual)
    d = np.asarray(stability_distance, dtype=float)

    r_norm = r / np.max(r) if np.max(r) > 0 else r
    d_norm = d / np.max(d) if np.max(d) > 0 else d

    return r_norm * d_norm


# --------------------------------------------------
# CASE PROCESSING
# --------------------------------------------------

def process_case(case):
    print(f"\n--- {case.upper()} ---")

    df = load_case_dataset(case)
    if df is None:
        return None

    c, dc, d2c, tau = prepare_data(df)

    params = fit_df[fit_df["case"] == case].iloc[0]
    a, p, q = params["power_a"], params["power_p"], params["power_q"]

    d2c_model = power_model(c, dc, a, p, q)
    residual = d2c - d2c_model

    # GRID + RIFT
    X, Y, R = build_grid(c, dc, residual, GRID_RES)
    xr, yr = extract_rift_points(X, Y, R, eps=EPS)

    stability_distance = compute_stability_distance(c, dc, xr, yr)
    collapse_strength = estimate_collapse_strength(residual, stability_distance)

    # --------------------------------------------------
    # PLOTS
    # --------------------------------------------------

    plt.figure(figsize=(8, 6))
    sc = plt.scatter(c, dc, c=stability_distance, cmap="magma", s=28)
    plt.colorbar(sc, label="Distance to rift")
    if len(xr) > 0:
        plt.scatter(xr, yr, s=8, c="cyan", alpha=0.6)
    plt.title(f"{case.upper()} — Stability Distance")
    plt.savefig(BASE_PATH / f"{case}_v52_stability_distance_map.png")
    plt.close()

    plt.figure(figsize=(8, 6))
    sc = plt.scatter(c, dc, c=collapse_strength, cmap="inferno", s=28)
    plt.colorbar(sc, label="Collapse strength")
    if len(xr) > 0:
        plt.scatter(xr, yr, s=8, c="cyan", alpha=0.6)
    plt.title(f"{case.upper()} — Collapse Strength")
    plt.savefig(BASE_PATH / f"{case}_v52_collapse_strength_map.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    sc = plt.scatter(stability_distance, residual, c=tau, cmap="viridis", s=32)
    plt.colorbar(sc, label="tau")
    plt.axhline(0, linestyle="--")
    plt.title(f"{case.upper()} — Residual vs Distance")
    plt.savefig(BASE_PATH / f"{case}_v52_residual_vs_distance.png")
    plt.close()

    # --------------------------------------------------
    # 🔥 WICHTIG: EXPORT FÜR V54
    # --------------------------------------------------

    df_geom = pd.DataFrame({
        "c": c,
        "dc": dc,
        "residual": residual,
        "distance": stability_distance,
        "tau": tau
    })

    out_geom = BASE_PATH / f"{case}_v52_residual_vs_distance.csv"
    df_geom.to_csv(out_geom, index=False)

    print(f"Saved geometry data: {out_geom}")

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    return {
        "case": case,
        "max_distance": float(np.nanmax(stability_distance)),
        "max_strength": float(np.nanmax(collapse_strength)),
    }


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V52 — STABILITY DISTANCE + COLLAPSE STRENGTH MAP")

    rows = []

    for case in CASES:
        res = process_case(case)
        if res:
            rows.append(res)

    df_out = pd.DataFrame(rows)
    df_out.to_csv(BASE_PATH / "ieee_v52_stability_distance_summary.csv", index=False)

    print("\nSaved summary")


if __name__ == "__main__":
    main()
