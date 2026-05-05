#!/usr/bin/env python3
"""
kuramoto_phase_boundary_v8.py

FINAL — Publication-ready phase diagram

Features:
- clean scatter
- smooth phase boundary (spline)
- critical point detection
- high-quality figure
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import time
from scipy.interpolate import UnivariateSpline


# =========================
# CONFIG
# =========================

BASE_INPUT_DIR = Path(__file__).parent / "outputs" / "kuramoto_v6" / "master_runs"


# =========================
# FIND LATEST SWEEP
# =========================

def find_latest_sweep_csv(base_dir: Path):
    runs = sorted([d for d in base_dir.glob("run_*") if d.is_dir()])
    if not runs:
        raise FileNotFoundError("No master_runs found")

    latest = runs[-1]
    sweep_dir = latest / "sweep"

    csv = sweep_dir / "sweep_results.csv"

    if not csv.exists():
        raise FileNotFoundError(f"sweep_results.csv not found in {sweep_dir}")

    print(f"Using sweep file → {csv}")
    return csv


# =========================
# LOAD DATA
# =========================

def load_data():
    csv_path = find_latest_sweep_csv(BASE_INPUT_DIR)
    df = pd.read_csv(csv_path)
    return df


# =========================
# BOUNDARY EXTRACTION
# =========================

def extract_boundary(df, bins=20):

    r = df["r_mean"].values
    drift = df["abs_delta_theta_std"].values

    r_bins = np.linspace(r.min(), r.max(), bins)

    br, bd = [], []

    for i in range(len(r_bins)-1):
        mask = (r >= r_bins[i]) & (r < r_bins[i+1])

        if np.any(mask):
            br.append(r[mask].mean())
            bd.append(drift[mask].max())

    return np.array(br), np.array(bd)


# =========================
# SMOOTH BOUNDARY
# =========================

def smooth_boundary(r, d):

    # sort
    idx = np.argsort(r)
    r = r[idx]
    d = d[idx]

    spline = UnivariateSpline(r, d, s=0.001)
    r_smooth = np.linspace(r.min(), r.max(), 200)
    d_smooth = spline(r_smooth)

    return r_smooth, d_smooth


# =========================
# CRITICAL POINT
# =========================

def find_critical_point(df):

    K = df["K"].values
    drift = df["abs_delta_theta_std"].values

    dK = np.gradient(K)
    dD = np.gradient(drift)

    slope = dD / dK

    idx = np.argmax(slope)

    return {
        "K_c": float(K[idx]),
        "drift": float(drift[idx]),
        "slope": float(slope[idx])
    }


# =========================
# PLOT
# =========================

def plot_final(df, r_s, d_s, critical, out_dir):

    fig, ax = plt.subplots(figsize=(9,7))

    # scatter
    sc = ax.scatter(
        df["r_mean"],
        df["abs_delta_theta_std"],
        c=df["K"],
        cmap="viridis",
        s=80,
        edgecolors="black",
        linewidth=0.5
    )

    # smooth boundary
    ax.plot(r_s, d_s, color="red", linewidth=2.5, label="Phase Boundary")

    # critical point
    ax.scatter(
        df.loc[df["K"] == critical["K_c"], "r_mean"],
        df.loc[df["K"] == critical["K_c"], "abs_delta_theta_std"],
        color="white",
        edgecolors="black",
        s=120,
        zorder=5,
        label=f"Kc ≈ {critical['K_c']:.2f}"
    )

    ax.set_xlabel("Mean Synchronization r")
    ax.set_ylabel("Phase Drift Std σ(Δθ)")
    ax.set_title("Kuramoto Phase Diagram — Final (V8)")

    ax.legend()
    plt.colorbar(sc, ax=ax, label="Coupling K")

    fig.tight_layout()
    fig.savefig(out_dir / "phase_diagram_final.png", dpi=220)
    plt.close(fig)


# =========================
# SAVE
# =========================

def save_outputs(r_s, d_s, critical, out_dir):

    with open(out_dir / "boundary_smooth.json", "w") as f:
        json.dump({
            "r": r_s.tolist(),
            "drift": d_s.tolist()
        }, f, indent=2)

    with open(out_dir / "critical_point.json", "w") as f:
        json.dump(critical, f, indent=2)


# =========================
# MAIN
# =========================

def main():

    base_dir = Path(__file__).parent / "outputs" / "kuramoto_v8"
    run_dir = base_dir / f"final_{int(time.time())}"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"Saving → {run_dir}")

    df = load_data()

    br, bd = extract_boundary(df)
    r_s, d_s = smooth_boundary(br, bd)

    critical = find_critical_point(df)

    plot_final(df, r_s, d_s, critical, run_dir)
    save_outputs(r_s, d_s, critical, run_dir)

    print("\n--- V8 FINAL COMPLETE ---")
    print("Critical point:", critical)


if __name__ == "__main__":
    main()
