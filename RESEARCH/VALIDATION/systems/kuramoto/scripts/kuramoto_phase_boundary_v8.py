#!/usr/bin/env python3
"""
kuramoto_phase_boundary_v8_1.py

FINAL — Clean phase boundary + full interpretation

Adds:
- onset / max drift / max events separation
- multi-panel overview figure
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
    csv = latest / "sweep" / "sweep_results.csv"

    if not csv.exists():
        raise FileNotFoundError(f"sweep_results.csv not found in {latest}")

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
# BOUNDARY
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


def smooth_boundary(r, d):
    idx = np.argsort(r)
    r = r[idx]
    d = d[idx]

    spline = UnivariateSpline(r, d, s=0.001)
    r_s = np.linspace(r.min(), r.max(), 200)
    d_s = spline(r_s)

    return r_s, d_s


# =========================
# CRITICAL STRUCTURE
# =========================

def compute_regime_points(df):

    K = df["K"].values
    drift = df["abs_delta_theta_std"].values
    events = df["transition_rate"].values

    # slope (onset)
    dK = np.gradient(K)
    dD = np.gradient(drift)
    slope = dD / dK

    onset_idx = np.argmax(slope)

    max_drift_idx = np.argmax(drift)
    max_event_idx = np.argmax(events)

    return {
        "onset": {
            "K": float(K[onset_idx]),
            "drift": float(drift[onset_idx]),
            "slope": float(slope[onset_idx])
        },
        "max_drift": {
            "K": float(K[max_drift_idx]),
            "drift": float(drift[max_drift_idx])
        },
        "max_events": {
            "K": float(K[max_event_idx]),
            "rate": float(events[max_event_idx])
        }
    }


# =========================
# PLOTS
# =========================

def plot_phase_diagram(df, r_s, d_s, regimes, out_dir):

    fig, ax = plt.subplots(figsize=(9,7))

    sc = ax.scatter(
        df["r_mean"],
        df["abs_delta_theta_std"],
        c=df["K"],
        cmap="viridis",
        s=80,
        edgecolors="black"
    )

    ax.plot(r_s, d_s, color="red", linewidth=2.5, label="Boundary")

    # markers
    for key, color in zip(["onset", "max_drift", "max_events"], ["white", "red", "blue"]):
        K_val = regimes[key]["K"]
        idx = np.argmin(np.abs(df["K"] - K_val))

        ax.scatter(
            df["r_mean"].iloc[idx],
            df["abs_delta_theta_std"].iloc[idx],
            color=color,
            edgecolors="black",
            s=120,
            label=key
        )

    ax.set_xlabel("r_mean")
    ax.set_ylabel("drift std")
    ax.set_title("Kuramoto Phase Diagram (Final)")

    plt.colorbar(sc, ax=ax, label="K")
    ax.legend()

    fig.tight_layout()
    fig.savefig(out_dir / "phase_diagram_final.png", dpi=220)
    plt.close(fig)


def plot_overview(df, regimes, out_dir):

    fig, axs = plt.subplots(2,2, figsize=(10,8))

    # 1 Drift vs K
    axs[0,0].plot(df["K"], df["abs_delta_theta_std"])
    axs[0,0].set_title("Drift vs K")

    # 2 Events
    axs[0,1].plot(df["K"], df["transition_rate"])
    axs[0,1].set_title("Transition Rate")

    # 3 Iota %
    axs[1,0].plot(df["K"], df["iota_percent"])
    axs[1,0].set_title("Iota %")

    # 4 r_mean
    axs[1,1].plot(df["K"], df["r_mean"])
    axs[1,1].set_title("Synchronization")

    fig.tight_layout()
    fig.savefig(out_dir / "system_overview.png", dpi=200)
    plt.close(fig)


# =========================
# SAVE
# =========================

def save_outputs(r_s, d_s, regimes, out_dir):

    with open(out_dir / "boundary_smooth.json", "w") as f:
        json.dump({
            "r": r_s.tolist(),
            "drift": d_s.tolist()
        }, f, indent=2)

    with open(out_dir / "regime_points.json", "w") as f:
        json.dump(regimes, f, indent=2)


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

    regimes = compute_regime_points(df)

    plot_phase_diagram(df, r_s, d_s, regimes, run_dir)
    plot_overview(df, regimes, run_dir)

    save_outputs(r_s, d_s, regimes, run_dir)

    print("\n--- FINAL COMPLETE ---")
    print(json.dumps(regimes, indent=2))


if __name__ == "__main__":
    main()
