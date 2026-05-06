# ============================================================
# RUN 030 — NOISE ROBUSTNESS TEST
# ============================================================

import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------
OUT_DIR = Path(__file__).resolve().parent.parent / "outputs/run_030_noise_robustness"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# SCENARIO
# ------------------------------------------------------------
def make_scenario(n=500, noise=0.0, seed=0):
    rng = np.random.default_rng(seed)

    t = np.linspace(0, 100, n)
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
    V += 0.01 * np.sin(0.8 * t) * (t < 25)

    if noise > 0:
        V += rng.normal(0, noise, size=n)

    return t, V


# ------------------------------------------------------------
# EMBEDDING
# ------------------------------------------------------------
def embedding(t, V):
    V_s = gaussian_filter1d(V, sigma=2)
    dV = gaussian_filter1d(np.gradient(V_s, t), sigma=2)
    return V_s, dV


# ------------------------------------------------------------
# DENSITY FIELD
# ------------------------------------------------------------
def density_field(V_s, dV, bins=80):
    H, xedges, yedges = np.histogram2d(V_s, dV, bins=bins)

    if np.max(H) > 0:
        H = H / np.max(H)

    return H, xedges, yedges


# ------------------------------------------------------------
# STRUCTURE METRICS
# ------------------------------------------------------------
def density_metrics(H, threshold=0.15):
    active = H > threshold

    active_cells = int(np.sum(active))
    total_cells = H.size
    sparsity = 1.0 - active_cells / total_cells

    mass = H / (np.sum(H) + 1e-12)
    entropy = -np.sum(mass * np.log(mass + 1e-12))

    # crude concentration: how much mass is in top 10% cells
    flat = H.flatten()
    k = max(1, int(0.1 * len(flat)))
    top_mass = np.sum(np.sort(flat)[-k:]) / (np.sum(flat) + 1e-12)

    return {
        "active_cells": active_cells,
        "sparsity": float(sparsity),
        "entropy": float(entropy),
        "top_10_percent_mass": float(top_mass),
    }


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":
    print("\n=== RUN 030 — NOISE ROBUSTNESS TEST ===\n")

    noise_levels = [0.0, 0.001, 0.003, 0.006, 0.01]
    bins = 80

    results = []

    fig, axs = plt.subplots(1, len(noise_levels), figsize=(18, 4), sharex=False, sharey=False)

    for ax, noise in zip(axs, noise_levels):
        t, V = make_scenario(noise=noise, seed=42)
        V_s, dV = embedding(t, V)

        H, xedges, yedges = density_field(V_s, dV, bins=bins)
        metrics = density_metrics(H)

        metrics["noise"] = noise
        results.append(metrics)

        ax.imshow(
            H.T,
            origin="lower",
            extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
            aspect="auto",
        )

        ax.plot(V_s, dV, color="white", linewidth=0.8, alpha=0.8)

        ax.set_title(f"noise={noise}")
        ax.set_xlabel("V")
        ax.grid(alpha=0.15)

    axs[0].set_ylabel("dV")

    plt.suptitle("Noise Robustness — Density Structure")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_01_noise_density_comparison.png", dpi=150)
    plt.close()

    # --------------------------------------------------------
    # Metrics plot
    # --------------------------------------------------------
    noise = [r["noise"] for r in results]
    entropy = [r["entropy"] for r in results]
    sparsity = [r["sparsity"] for r in results]
    concentration = [r["top_10_percent_mass"] for r in results]

    plt.figure(figsize=(8, 5))
    plt.plot(noise, entropy, marker="o", label="entropy")
    plt.plot(noise, sparsity, marker="o", label="sparsity")
    plt.plot(noise, concentration, marker="o", label="top 10% mass")

    plt.title("Density Structure Robustness Metrics")
    plt.xlabel("noise level")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_02_noise_metrics.png", dpi=150)
    plt.close()

    with open(OUT_DIR / "results.json", "w") as f:
        json.dump(
            {
                "noise_levels": noise_levels,
                "results": results,
                "interpretation": (
                    "This test checks whether the observed density/channel structure "
                    "persists under increasing noise. Stable sparsity and concentration "
                    "suggest real structure; rapid entropy growth suggests sampling/noise sensitivity."
                ),
            },
            f,
            indent=2,
        )

    print("Results:")
    for r in results:
        print(
            f"noise={r['noise']:.3f} | "
            f"active={r['active_cells']} | "
            f"sparsity={r['sparsity']:.3f} | "
            f"entropy={r['entropy']:.3f} | "
            f"top10={r['top_10_percent_mass']:.3f}"
        )

    print(f"\nSaved to: {OUT_DIR}")
