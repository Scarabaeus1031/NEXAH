#!/usr/bin/env python3
"""
kuramoto_parameter_sweep_v3.py

NEXAH FIELD_LAYER — PARAMETER SWEEP EXPERIMENT

Goal:
Test robustness of FIELD_LAYER transition structure (~8%)
across Kuramoto coupling parameter K.

Sweep:
K in [K_min, ..., K_max]

For each K:
- run field_projection pipeline
- extract:
    Iota %
    event_count
    transition_rate
    drift stats
    return time stats

Output:
- sweep_results.csv
- summary plot
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from field_projection_kuramoto_v3 import run_experiment, KuramotoConfig


def run_sweep(K_values, base_config):
    results = []

    for K in K_values:
        print(f"Running K={K:.3f}")

        config = KuramotoConfig(**{**base_config.__dict__, "coupling_k": K})
        summary = run_experiment(config)

        results.append({
            "K": K,
            "iota_percent": summary["regime_distribution_percent"]["Iota"],
            "iota_event_count": summary["iota_event_count"],
            "transition_rate": summary["transition_rate"],
            "abs_delta_theta_mean": summary["abs_delta_theta_mean"],
            "abs_delta_theta_std": summary["abs_delta_theta_std"],
            "return_time_mean": summary["iota_return_time_mean"],
            "return_time_std": summary["iota_return_time_std"],
            "r_mean": summary["r_mean"],
            "r_std": summary["r_std"]
        })

    return pd.DataFrame(results)


def plot_results(df, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(df["K"], df["iota_percent"], marker="o")
    ax.set_title("Iota % vs Coupling K")
    ax.set_xlabel("K")
    ax.set_ylabel("Iota %")
    fig.tight_layout()
    fig.savefig(output_dir / "iota_vs_K.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(df["K"], df["transition_rate"], marker="o")
    ax.set_title("Transition Rate vs K")
    ax.set_xlabel("K")
    ax.set_ylabel("Transition Rate")
    fig.tight_layout()
    fig.savefig(output_dir / "transition_rate_vs_K.png", dpi=180)
    plt.close(fig)


def main():
    output_dir = Path("outputs/kuramoto_sweep_v3")

    K_values = np.linspace(0.5, 3.0, 12)

    base_config = KuramotoConfig()

    df = run_sweep(K_values, base_config)

    df.to_csv(output_dir / "sweep_results.csv", index=False)
    plot_results(df, output_dir)

    print(df)


if __name__ == "__main__":
    main()
