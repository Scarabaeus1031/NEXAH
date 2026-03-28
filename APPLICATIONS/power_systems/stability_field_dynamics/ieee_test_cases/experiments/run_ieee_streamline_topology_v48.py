# run_ieee_streamline_topology_v48.py

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
# HELPERS
# --------------------------------------------------

def normalize(x):
    x = np.asarray(x, dtype=float)
    xmin, xmax = np.min(x), np.max(x)
    if np.isclose(xmax - xmin, 0):
        return np.zeros_like(x)
    return (x - xmin) / (xmax - xmin)

def load_dataset(case):
    file_path = BASE_PATH / f"{case}_v43_dataset.csv"
    if not file_path.exists():
        print(f"Missing: {file_path}")
        return None
    df = pd.read_csv(file_path).dropna()
    return df

def prepare(df):
    c = normalize(df["c"].values)
    dc = normalize(df["dc"].values)
    d2c = normalize(df["d2c"].values)
    return c, dc, d2c

# --------------------------------------------------
# VECTOR FIELD INTERPOLATION
# --------------------------------------------------

def build_field(c, dc, d2c):
    # grid
    xi = np.linspace(0, 1, GRID_RES)
    yi = np.linspace(0, 1, GRID_RES)
    X, Y = np.meshgrid(xi, yi)

    # vectors
    U = dc
    V = d2c

    # interpolate scattered → grid
    Ug = griddata((c, dc), U, (X, Y), method="linear", fill_value=0)
    Vg = griddata((c, dc), V, (X, Y), method="linear", fill_value=0)

    return X, Y, Ug, Vg

# --------------------------------------------------
# STREAMLINE PLOT
# --------------------------------------------------

def plot_stream(case, c, dc, d2c):
    X, Y, U, V = build_field(c, dc, d2c)

    plt.figure(figsize=(8, 7))

    # streamlines (FLOW!)
    plt.streamplot(
        X, Y, U, V,
        density=1.2,
        linewidth=1,
        arrowsize=1.2
    )

    # trajectory overlay
    plt.scatter(c, dc, c=np.linspace(0,1,len(c)), cmap="viridis", s=20)

    # highlight low-acceleration (infeed)
    mask = np.abs(d2c) < 0.03
    plt.scatter(c[mask], dc[mask], marker="x", s=60, label="d²c≈0")

    plt.xlabel("c (norm)")
    plt.ylabel("dc (norm)")
    plt.title(f"{case.upper()} — Streamline Topology (V48)")
    plt.grid(True)
    plt.legend()

    plt.savefig(BASE_PATH / f"{case}_v48_streamlines.png", dpi=150)
    plt.close()

# --------------------------------------------------
# CURL / ROTATION ANALYSIS
# --------------------------------------------------

def compute_curl(U, V):
    # numerical curl approximation
    dVdx = np.gradient(V, axis=1)
    dUdy = np.gradient(U, axis=0)
    return dVdx - dUdy

def plot_curl(case, c, dc, d2c):
    X, Y, U, V = build_field(c, dc, d2c)
    curl = compute_curl(U, V)

    plt.figure(figsize=(8, 6))
    plt.imshow(curl, extent=[0,1,0,1], origin="lower", aspect="auto")
    plt.colorbar(label="Curl (rotation strength)")
    plt.title(f"{case.upper()} — Flow Rotation / Curl (V48)")
    plt.xlabel("c")
    plt.ylabel("dc")

    plt.savefig(BASE_PATH / f"{case}_v48_curl.png", dpi=150)
    plt.close()

    return np.nanmean(np.abs(curl)), np.nanmax(np.abs(curl))

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V48 — FLOW TOPOLOGY / STREAMLINES")

    results = []

    for case in CASES:
        print(f"\n--- {case.upper()} ---")
        df = load_dataset(case)
        if df is None:
            continue

        c, dc, d2c = prepare(df)

        plot_stream(case, c, dc, d2c)
        mean_curl, max_curl = plot_curl(case, c, dc, d2c)

        results.append({
            "case": case,
            "mean_curl": mean_curl,
            "max_curl": max_curl
        })

    df_out = pd.DataFrame(results)

    print("\n--- V48 SUMMARY ---")
    print(df_out)

    df_out.to_csv(BASE_PATH / "ieee_v48_flow_topology.csv", index=False)
    print("\nSaved:", BASE_PATH / "ieee_v48_flow_topology.csv")


if __name__ == "__main__":
    main()
