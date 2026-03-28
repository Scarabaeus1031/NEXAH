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
CASES = ["ieee9", "ieee14", "ieee30"]

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
    rr = R[mask]

    if len(xr) == 0:
        return np.array([]), np.array([]), np.array([])

    order = np.argsort(xr)
    return xr[order], yr[order], rr[order]


def signed_residual_strength(residual):
    scale = np.max(np.abs(residual))
    if scale == 0:
        return residual
    return residual / scale


def compute_stability_distance(c, dc, xr, yr):
    """
    Distance from each trajectory point to nearest rift point.
    """
    if len(xr) == 0:
        return np.full_like(c, np.nan, dtype=float)

    tree = cKDTree(np.column_stack([xr, yr]))
    dist, _ = tree.query(np.column_stack([c, dc]), k=1)
    return dist


def estimate_collapse_strength(residual, stability_distance):
    """
    Collapse strength combines:
    - residual magnitude (model mismatch)
    - distance to rift (distance from balance manifold)

    normalized product for interpretability
    """
    r = np.abs(residual)
    d = np.asarray(stability_distance, dtype=float)

    r_norm = r / np.max(r) if np.max(r) > 0 else r
    d_norm = d / np.max(d) if np.max(d) > 0 else d

    strength = r_norm * d_norm
    return strength


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

    # residual grid + rift
    X, Y, R = build_grid(c, dc, residual, GRID_RES)
    xr, yr, rr = extract_rift_points(X, Y, R, eps=EPS)

    # stability distance on actual trajectory
    stability_distance = compute_stability_distance(c, dc, xr, yr)

    # collapse strength
    collapse_strength = estimate_collapse_strength(residual, stability_distance)

    # --------------------------------------------------
    # 1) Stability Distance Map
    # --------------------------------------------------

    plt.figure(figsize=(8, 6))
    sc = plt.scatter(c, dc, c=stability_distance, cmap="magma", s=28)
    plt.colorbar(sc, label="Distance to rift")
    if len(xr) > 0:
        plt.scatter(xr, yr, s=8, c="cyan", alpha=0.6, label="Rift")
    plt.xlabel("c (norm)")
    plt.ylabel("dc (norm)")
    plt.title(f"{case.upper()} — Stability Distance Map (V52)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v52_stability_distance_map.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 2) Collapse Strength Map
    # --------------------------------------------------

    plt.figure(figsize=(8, 6))
    sc = plt.scatter(c, dc, c=collapse_strength, cmap="inferno", s=32)
    plt.colorbar(sc, label="Collapse strength")
    if len(xr) > 0:
        plt.scatter(xr, yr, s=8, c="cyan", alpha=0.6, label="Rift")
    plt.xlabel("c (norm)")
    plt.ylabel("dc (norm)")
    plt.title(f"{case.upper()} — Collapse Strength Map (V52)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v52_collapse_strength_map.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 3) Distance / Strength vs tau
    # --------------------------------------------------

    plt.figure(figsize=(10, 5))
    plt.plot(tau, stability_distance, label="Stability distance")
    plt.plot(tau, collapse_strength, label="Collapse strength")
    plt.xlabel("tau = normalized load")
    plt.ylabel("Normalized measure")
    plt.title(f"{case.upper()} — Stability Distance & Collapse Strength vs tau (V52)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v52_tau_dynamics.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 4) Residual vs distance (phase relation)
    # --------------------------------------------------

    plt.figure(figsize=(8, 5))
    sc = plt.scatter(stability_distance, residual, c=tau, cmap="viridis", s=32)
    plt.colorbar(sc, label="tau")
    plt.axhline(0, linestyle="--", linewidth=1)
    plt.xlabel("Distance to rift")
    plt.ylabel("Residual")
    plt.title(f"{case.upper()} — Residual vs Stability Distance (V52)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v52_residual_vs_distance.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    idx_max_strength = int(np.nanargmax(collapse_strength))
    idx_max_distance = int(np.nanargmax(stability_distance))

    return {
        "case": case,
        "rift_count": int(len(xr)),
        "max_distance": float(np.nanmax(stability_distance)),
        "mean_distance": float(np.nanmean(stability_distance)),
        "max_strength": float(np.nanmax(collapse_strength)),
        "mean_strength": float(np.nanmean(collapse_strength)),
        "tau_max_distance": float(tau[idx_max_distance]),
        "tau_max_strength": float(tau[idx_max_strength]),
        "c_at_max_strength": float(c[idx_max_strength]),
        "dc_at_max_strength": float(dc[idx_max_strength]),
        "residual_at_max_strength": float(residual[idx_max_strength]),
    }


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V52 — STABILITY DISTANCE + COLLAPSE STRENGTH MAP")

    rows = []

    for case in CASES:
        try:
            res = process_case(case)
            if res:
                rows.append(res)
        except Exception as e:
            print(f"[{case}] ERROR: {e}")

    df_out = pd.DataFrame(rows)

    print("\n--- V52 SUMMARY ---")
    print(df_out)

    out_file = BASE_PATH / "ieee_v52_stability_distance_summary.csv"
    df_out.to_csv(out_file, index=False)
    print("\nSaved:", out_file)


if __name__ == "__main__":
    main()
