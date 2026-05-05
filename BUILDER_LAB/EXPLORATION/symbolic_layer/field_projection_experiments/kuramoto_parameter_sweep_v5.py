#!/usr/bin/env python3
"""
kuramoto_parameter_sweep_v5.py

Kuramoto V5 Sweep:
- runs field_projection_kuramoto_v5.py logic across K
- collects:
    r_mean
    drift std
    iota_percent
    transition_rate
    lyapunov_estimate
- saves:
    sweep_results.csv
    iota_vs_K.png
    transition_rate_vs_K.png
    r_mean_vs_K.png
    lyapunov_vs_K.png
    event_rate_vs_lyapunov.png
    phase_diagram_r_drift_lyapunov.png
"""

from __future__ import annotations

import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from field_projection_kuramoto_v5 import KuramotoConfig, run_experiment


def run_sweep(K_values: np.ndarray) -> pd.DataFrame:
    results = []

    for K in K_values:
        print(f"\nRunning K={K:.3f}")

        config = KuramotoConfig(coupling_k=float(K))
        summary = run_experiment(config)

        results.append(summary)

    return pd.DataFrame(results)


def save_plot_line(df: pd.DataFrame, x: str, y: str, title: str, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df[x], df[y], marker="o")
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    fig.tight_layout()
    fig.savefig(out, dpi=180)
    plt.close(fig)


def plot_results(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    save_plot_line(df, "K", "iota_percent", "Iota % vs K", output_dir / "iota_vs_K.png")
    save_plot_line(df, "K", "transition_rate", "Transition Rate vs K", output_dir / "transition_rate_vs_K.png")
    save_plot_line(df, "K", "r_mean", "Mean Synchronization r vs K", output_dir / "r_mean_vs_K.png")
    save_plot_line(df, "K", "abs_delta_theta_std", "Phase Drift STD vs K", output_dir / "drift_std_vs_K.png")
    save_plot_line(df, "K", "lyapunov_estimate", "Lyapunov Estimate vs K", output_dir / "lyapunov_vs_K.png")

    # Event rate vs Lyapunov
    fig, ax = plt.subplots(figsize=(7, 5))
    sc = ax.scatter(
        df["lyapunov_estimate"],
        df["transition_rate"],
        c=df["K"],
        s=80,
    )
    ax.axvline(0.0, linewidth=1)
    ax.set_xlabel("lyapunov_estimate")
    ax.set_ylabel("transition_rate")
    ax.set_title("Transition Rate vs Lyapunov")
    plt.colorbar(sc, label="K")
    fig.tight_layout()
    fig.savefig(output_dir / "event_rate_vs_lyapunov.png", dpi=180)
    plt.close(fig)

    # Phase diagram: r_mean vs drift, colored by Lyapunov
    fig, ax = plt.subplots(figsize=(7, 5))
    sc = ax.scatter(
        df["r_mean"],
        df["abs_delta_theta_std"],
        c=df["lyapunov_estimate"],
        s=90,
    )
    ax.set_xlabel("r_mean")
    ax.set_ylabel("abs_delta_theta_std")
    ax.set_title("Phase Diagram: r vs Drift, colored by Lyapunov")
    plt.colorbar(sc, label="lyapunov_estimate")
    fig.tight_layout()
    fig.savefig(output_dir / "phase_diagram_r_drift_lyapunov.png", dpi=180)
    plt.close(fig)

    # Phase diagram: r_mean vs transition_rate, colored by K
    fig, ax = plt.subplots(figsize=(7, 5))
    sc = ax.scatter(
        df["r_mean"],
        df["transition_rate"],
        c=df["K"],
        s=90,
    )
    ax.set_xlabel("r_mean")
    ax.set_ylabel("transition_rate")
    ax.set_title("Phase Diagram: Synchronization vs Events")
    plt.colorbar(sc, label="K")
    fig.tight_layout()
    fig.savefig(output_dir / "phase_diagram_r_events_K.png", dpi=180)
    plt.close(fig)


def main() -> None:
    K_values = np.linspace(0.5, 3.0, 12)

    sweep_id = f"sweep_{int(time.time())}"
    output_dir = (
        Path(__file__).parent
        / "outputs"
        / "kuramoto_v5"
        / "sweeps"
        / sweep_id
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    df = run_sweep(K_values)

    df.to_csv(output_dir / "sweep_results.csv", index=False)
    plot_results(df, output_dir)

    print("\n--- SWEEP V5 COMPLETE ---")
    print(f"Saved to: {output_dir}")
    print(df)


if __name__ == "__main__":
    main()
