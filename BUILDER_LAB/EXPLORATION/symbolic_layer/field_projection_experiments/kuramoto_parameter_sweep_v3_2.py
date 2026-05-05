#!/usr/bin/env python3
"""
kuramoto_parameter_sweep_v3.py

NEXAH FIELD_LAYER — PARAMETER SWEEP

Explores system behavior across coupling parameter K.

Outputs:
- sweep_results.csv
- multiple diagnostic plots
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from field_projection_kuramoto_v3 import run_experiment, KuramotoConfig


# =========================
# SWEEP CORE
# =========================

def run_sweep(K_values, base_config):
    results = []

    for K in K_values:
        print(f"\nRunning K = {K:.3f}")

        config = KuramotoConfig(
            **{**base_config.__dict__, "coupling_k": K}
        )

        summary = run_experiment(config)

        results.append({
            "K": K,
            "iota_percent": summary["regime_distribution_percent"].get("Iota", 0),
            "iota_event_count": summary["iota_event_count"],
            "transition_rate": summary["transition_rate"],
            "r_mean": summary["r_mean"],
            "r_std": summary["r_std"],
            "abs_delta_theta_mean": summary["abs_delta_theta_mean"],
            "abs_delta_theta_std": summary["abs_delta_theta_std"],
        })

    return pd.DataFrame(results)


# =========================
# PLOTTING
# =========================

def plot_results(df, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- IOTA %
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df["K"], df["iota_percent"], marker="o")
    ax.set_title("Iota % vs Coupling K")
    ax.set_xlabel("K")
    ax.set_ylabel("Iota %")
    fig.tight_layout()
    fig.savefig(output_dir / "iota_vs_K.png", dpi=180)
    plt.close(fig)

    # --- TRANSITION RATE
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df["K"], df["transition_rate"], marker="o")
    ax.set_title("Transition Rate vs K")
    ax.set_xlabel("K")
    ax.set_ylabel("Transition Rate")
    fig.tight_layout()
    fig.savefig(output_dir / "transition_rate_vs_K.png", dpi=180)
    plt.close(fig)

    # --- r_mean
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df["K"], df["r_mean"], marker="o")
    ax.set_title("Mean Synchronization r vs K")
    ax.set_xlabel("K")
    ax.set_ylabel("r_mean")
    fig.tight_layout()
    fig.savefig(output_dir / "r_mean_vs_K.png", dpi=180)
    plt.close(fig)

    # --- PHASE DIAGRAM (VERY IMPORTANT)
    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(df["r_mean"], df["iota_percent"], c=df["K"], s=60)
    ax.set_xlabel("r_mean (synchronization)")
    ax.set_ylabel("Iota % (transitions)")
    ax.set_title("Phase Diagram: Structure vs Instability")
    plt.colorbar(sc, label="K")
    fig.tight_layout()
    fig.savefig(output_dir / "phase_diagram.png", dpi=180)
    plt.close(fig)


# =========================
# MAIN
# =========================

def main():
    # Sweep range
    K_values = np.linspace(0.5, 3.0, 12)

    base_config = KuramotoConfig()

    # Unique sweep folder
    timestamp = int(time.time())
    output_dir = Path(__file__).parent / "outputs" / "kuramoto_v3" / "sweeps" / f"sweep_{timestamp}"

    df = run_sweep(K_values, base_config)

    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / "sweep_results.csv", index=False)

    plot_results(df, output_dir)

    print("\n--- SWEEP COMPLETE ---")
    print(df)


if __name__ == "__main__":
    main()
