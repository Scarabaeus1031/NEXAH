# run_ieee_vector_field_v47.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee9", "ieee14", "ieee30"]

GRID_N = 20
EPS = 1e-9

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def normalize_series(x):
    x = np.asarray(x, dtype=float)
    xmin = np.min(x)
    xmax = np.max(x)
    if np.isclose(xmax - xmin, 0.0):
        return np.zeros_like(x)
    return (x - xmin) / (xmax - xmin)


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


def prepare_data(df: pd.DataFrame):
    load = df["load"].values
    c = df["c"].values
    dc = df["dc"].values
    d2c = df["d2c"].values

    c_norm = normalize_series(c)
    dc_norm = normalize_series(dc)
    d2c_norm = normalize_series(d2c)
    tau = normalize_series(load)

    out = pd.DataFrame({
        "load": load,
        "tau": tau,
        "c_norm": c_norm,
        "dc_norm": dc_norm,
        "d2c_norm": d2c_norm,
    })

    return out


def estimate_vector_field(df: pd.DataFrame, grid_n=20):
    """
    State-space:
      x = c_norm
      y = dc_norm

    Flow:
      dx ~ dc_norm
      dy ~ d2c_norm

    We average local vectors onto a grid.
    """
    x = df["c_norm"].values
    y = df["dc_norm"].values

    u = df["dc_norm"].values      # dx/dtau-like proxy
    v = df["d2c_norm"].values     # dy/dtau-like proxy

    x_edges = np.linspace(0.0, 1.0, grid_n + 1)
    y_edges = np.linspace(0.0, 1.0, grid_n + 1)

    x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])

    U = np.full((grid_n, grid_n), np.nan)
    V = np.full((grid_n, grid_n), np.nan)
    N = np.zeros((grid_n, grid_n), dtype=int)

    ix = np.clip(np.digitize(x, x_edges) - 1, 0, grid_n - 1)
    iy = np.clip(np.digitize(y, y_edges) - 1, 0, grid_n - 1)

    for i in range(len(x)):
        gx = ix[i]
        gy = iy[i]

        if np.isnan(U[gy, gx]):
            U[gy, gx] = 0.0
            V[gy, gx] = 0.0

        U[gy, gx] += u[i]
        V[gy, gx] += v[i]
        N[gy, gx] += 1

    valid = N > 0
    U[valid] /= N[valid]
    V[valid] /= N[valid]

    Xg, Yg = np.meshgrid(x_centers, y_centers)

    return Xg, Yg, U, V, N


def detect_infeed_points(df: pd.DataFrame, eps=0.03):
    """
    Approximate 'einfädeln' candidates:
    points where d2c is close to zero.
    """
    sel = np.abs(df["d2c_norm"].values) < eps
    return df.loc[sel].copy()


def branching_measure(df: pd.DataFrame, bins=25):
    """
    For each c-bin, compute variance of d2c.
    Large variance at same c suggests multi-valued behavior / branching.
    """
    c = df["c_norm"].values
    d2c = df["d2c_norm"].values

    edges = np.linspace(0.0, 1.0, bins + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])

    vars_ = []
    counts = []

    for i in range(bins):
        mask = (c >= edges[i]) & (c < edges[i + 1])
        vals = d2c[mask]

        if len(vals) >= 2:
            vars_.append(np.var(vals))
            counts.append(len(vals))
        else:
            vars_.append(np.nan)
            counts.append(len(vals))

    return centers, np.array(vars_), np.array(counts)


# --------------------------------------------------
# PLOTTING
# --------------------------------------------------

def plot_case(case: str, df: pd.DataFrame):
    Xg, Yg, U, V, N = estimate_vector_field(df, grid_n=GRID_N)
    infeed = detect_infeed_points(df, eps=0.03)
    c_var_x, c_var_y, c_var_n = branching_measure(df, bins=25)

    # ------------------------------
    # 1) Vector field + trajectory
    # ------------------------------
    plt.figure(figsize=(8, 7))

    valid = ~np.isnan(U) & ~np.isnan(V)
    plt.quiver(
        Xg[valid], Yg[valid], U[valid], V[valid],
        angles="xy", scale_units="xy", scale=8, alpha=0.7
    )

    plt.scatter(
        df["c_norm"], df["dc_norm"],
        c=df["tau"], cmap="viridis", s=28, label="Trajectory"
    )

    if len(infeed) > 0:
        plt.scatter(
            infeed["c_norm"], infeed["dc_norm"],
            s=55, marker="x", linewidths=2, label="d²c≈0 / infeed candidates"
        )

    plt.xlabel("c (norm)")
    plt.ylabel("dc (norm)")
    plt.title(f"{case.upper()} — Vector Field in Phase Space (V47)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v47_vector_field.png", dpi=150)
    plt.close()

    # ------------------------------
    # 2) Branching measure
    # ------------------------------
    plt.figure(figsize=(8, 4))
    plt.plot(c_var_x, c_var_y, linewidth=2, label="Var[d²c | c-bin]")
    plt.xlabel("c (norm)")
    plt.ylabel("Variance of d²c")
    plt.title(f"{case.upper()} — Branching / Multi-valuedness Measure (V47)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v47_branching.png", dpi=150)
    plt.close()

    # ------------------------------
    # 3) Tau-colored trajectory in (c, d²c)
    # ------------------------------
    plt.figure(figsize=(8, 6))
    plt.scatter(
        df["c_norm"], df["d2c_norm"],
        c=df["tau"], cmap="viridis", s=30
    )
    plt.plot(df["c_norm"], df["d2c_norm"], alpha=0.3)
    if len(infeed) > 0:
        plt.scatter(
            infeed["c_norm"], infeed["d2c_norm"],
            s=60, marker="x", linewidths=2, label="d²c≈0"
        )
        plt.legend()

    plt.xlabel("c (norm)")
    plt.ylabel("d²c (norm)")
    plt.title(f"{case.upper()} — Phase-colored Collapse Path (V47)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v47_phase_path.png", dpi=150)
    plt.close()

    # Summary stats
    max_branch_idx = np.nanargmax(c_var_y) if np.any(np.isfinite(c_var_y)) else None
    max_branch_c = c_var_x[max_branch_idx] if max_branch_idx is not None else np.nan
    max_branch_var = c_var_y[max_branch_idx] if max_branch_idx is not None else np.nan

    return {
        "case": case,
        "num_infeed_points": len(infeed),
        "max_branch_c": max_branch_c,
        "max_branch_var": max_branch_var
    }


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V47 — VECTOR FIELD / FLOW MAP")

    rows = []

    for case in CASES:
        print(f"\n--- {case.upper()} ---")
        raw_df = load_case_dataset(case)
        if raw_df is None:
            continue

        df = prepare_data(raw_df)
        summary = plot_case(case, df)
        rows.append(summary)

    df_out = pd.DataFrame(rows)

    print("\n--- V47 SUMMARY ---")
    print(df_out)

    out_file = BASE_PATH / "ieee_v47_vector_field_summary.csv"
    df_out.to_csv(out_file, index=False)
    print(f"\nSaved: {out_file}")


if __name__ == "__main__":
    main()
