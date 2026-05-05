#!/usr/bin/env python3
"""
kuramoto_phase_boundary_v7.py

FINAL LAYER — Phase Boundary Extraction

Input:
- sweep_results.csv (from v6)

Output:
- clean phase diagram
- extracted boundary curve
- boundary JSON
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import time


# =========================
# CONFIG
# =========================

BASE_INPUT_DIR = Path(__file__).parent / "outputs" / "kuramoto_v6" / "master_runs"


# =========================
# LOAD DATA (AUTO-DETECT)
# =========================

def find_latest_sweep_csv(base_dir: Path):
    runs = sorted(base_dir.glob("run_*"), key=lambda p: p.stat().st_mtime)

    if not runs:
        raise FileNotFoundError("No run_* directories found in master_runs")

    latest_run = runs[-1]
    csv_path = latest_run / "sweep_results.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"sweep_results.csv not found in {latest_run}")

    print(f"Using sweep file → {csv_path}")
    return csv_path


def load_data():
    csv_path = find_latest_sweep_csv(BASE_INPUT_DIR)
    df = pd.read_csv(csv_path)
    return df


# =========================
# MAIN
# =========================

def main():
    base_dir = Path(__file__).parent / "outputs" / "kuramoto_v7"
    run_dir = base_dir / f"boundary_run_{int(time.time())}"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"Saving → {run_dir}")

    df = load_data()

    boundary_r, boundary_d = extract_boundary(df)

    plot_phase_diagram(df, boundary_r, boundary_d, run_dir)
    save_boundary(boundary_r, boundary_d, run_dir)

    print("\n--- PHASE BOUNDARY V7 COMPLETE ---")
    print(f"Boundary points: {len(boundary_r)}")

# =========================
# BOUNDARY EXTRACTION
# =========================

def extract_boundary(df, bins=20):
    """
    Extract upper envelope of drift_std vs r_mean
    """

    r = df["r_mean"].values
    drift = df["abs_delta_theta_std"].values

    r_bins = np.linspace(r.min(), r.max(), bins)

    boundary_r = []
    boundary_d = []

    for i in range(len(r_bins) - 1):
        mask = (r >= r_bins[i]) & (r < r_bins[i + 1])

        if np.any(mask):
            max_drift = drift[mask].max()
            mean_r = r[mask].mean()

            boundary_r.append(mean_r)
            boundary_d.append(max_drift)

    return np.array(boundary_r), np.array(boundary_d)


# =========================
# PLOTS
# =========================

def plot_phase_diagram(df, boundary_r, boundary_d, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)

    # scatter
    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(
        df["r_mean"],
        df["abs_delta_theta_std"],
        c=df["K"],
        s=60
    )

    # boundary
    ax.plot(boundary_r, boundary_d, color="red", linewidth=2, label="phase boundary")

    ax.set_xlabel("r_mean (synchronization)")
    ax.set_ylabel("abs_delta_theta_std (drift)")
    ax.set_title("Kuramoto Phase Diagram (V7)")
    ax.legend()

    plt.colorbar(sc, ax=ax, label="K")

    fig.tight_layout()
    fig.savefig(out_dir / "phase_diagram_with_boundary.png", dpi=180)
    plt.close(fig)


# =========================
# SAVE BOUNDARY
# =========================

def save_boundary(boundary_r, boundary_d, out_dir):
    data = {
        "r_mean": boundary_r.tolist(),
        "drift_std": boundary_d.tolist()
    }

    with open(out_dir / "phase_boundary.json", "w") as f:
        json.dump(data, f, indent=2)


# =========================
# MAIN
# =========================

def main():
    base_dir = Path(__file__).parent / "outputs" / "kuramoto_v7"
    run_dir = base_dir / f"boundary_run_{int(time.time())}"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"Saving → {run_dir}")

    df = load_data(INPUT_CSV)

    boundary_r, boundary_d = extract_boundary(df)

    plot_phase_diagram(df, boundary_r, boundary_d, run_dir)
    save_boundary(boundary_r, boundary_d, run_dir)

    print("\n--- PHASE BOUNDARY V7 COMPLETE ---")
    print(f"Boundary points: {len(boundary_r)}")


if __name__ == "__main__":
    main()
