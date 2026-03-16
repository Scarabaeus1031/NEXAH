"""
NEXAH Experiment Tool
Root Family Cycle Scan

Purpose
-------
Compare root-based shell families across multiple scale levels.

We test two experimental families:

    Root-12 family: sqrt(12 * 2^n)
    Root-13 family: sqrt(13 * 3^n)

These are converted into effective shell sizes and then evaluated using:

    • defect density
    • triadic closure density
    • defect-to-triad-boundary distance

Outputs
-------
output/root_family_summary.png
output/root_family_metrics.csv

Usage
-----
cd ENGINE/nexah_kernel/research/experiments/structured_oscillator_networks
python root_family_cycle_scan.py
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


# ------------------------------------------------
# Core dynamics
# ------------------------------------------------
def kuramoto_step(theta, omega, A, K, dt):
    phase_diff = theta[:, None] - theta[None, :]
    coupling = np.sum(A * np.sin(-phase_diff), axis=1)
    dtheta = omega + (K / len(theta)) * coupling
    return theta + dt * dtheta


def build_hub_ring(N):
    G = nx.Graph()
    center = 0

    for i in range(1, N + 1):
        G.add_edge(center, i)

    for i in range(1, N + 1):
        G.add_edge(i, 1 + (i % N))

    return G


def simulate_history(N, steps=1200, dt=0.02, K=1.0, seed=None):
    if seed is not None:
        np.random.seed(seed)

    G = build_hub_ring(N)
    A = nx.to_numpy_array(G)

    nodes = len(A)
    theta = np.random.uniform(0, 2 * np.pi, nodes)
    omega = np.random.normal(0, 0.1, nodes)

    history = []

    for _ in range(steps):
        theta = kuramoto_step(theta, omega, A, K, dt)
        history.append(theta.copy())

    return np.array(history)


# ------------------------------------------------
# Defect analysis
# ------------------------------------------------
def phase_diff_ring(theta_ring):
    diffs = np.roll(theta_ring, -1) - theta_ring
    diffs = (diffs + np.pi) % (2 * np.pi) - np.pi
    return diffs


def detect_vortex_defects(theta_ring, threshold=2.2):
    diffs = phase_diff_ring(theta_ring)
    defects = np.where(np.abs(diffs) > threshold)[0]
    return defects, diffs


def vortex_scan(history, threshold=2.2):
    ring_history = history[:, 1:]
    defect_map = []
    defect_counts = []

    for theta_ring in ring_history:
        defects, _ = detect_vortex_defects(theta_ring, threshold)
        row = np.zeros(len(theta_ring))
        row[defects] = 1
        defect_map.append(row)
        defect_counts.append(len(defects))

    return np.array(defect_map), np.array(defect_counts)


# ------------------------------------------------
# Triadic closure analysis
# ------------------------------------------------
def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def triadic_closure_scores(theta_ring):
    N = len(theta_ring)
    scores = []

    for i in range(N):
        im1 = (i - 1) % N
        ip1 = (i + 1) % N

        d_left = wrap_angle(theta_ring[i] - theta_ring[im1])
        d_right = wrap_angle(theta_ring[ip1] - theta_ring[i])

        mismatch = abs(d_left - d_right)
        mismatch = min(mismatch, 2 * np.pi - mismatch)

        score = 1.0 - mismatch / np.pi
        score = max(0.0, score)
        scores.append(score)

    return np.array(scores)


def detect_triadic_closure(theta_ring, threshold=0.8):
    scores = triadic_closure_scores(theta_ring)
    mask = scores > threshold
    return mask, scores


def compute_closure_history(history, threshold=0.8):
    ring_history = history[:, 1:]
    closure_map = []
    closure_counts = []

    for theta_ring in ring_history:
        mask, _ = detect_triadic_closure(theta_ring, threshold)
        closure_map.append(mask.astype(float))
        closure_counts.append(np.sum(mask))

    return np.array(closure_map), np.array(closure_counts)


# ------------------------------------------------
# Boundary / distance analysis
# ------------------------------------------------
def compute_triad_boundaries(triad_map):
    boundaries = np.zeros_like(triad_map)
    T, N = triad_map.shape

    for t in range(T):
        for i in range(N):
            left = triad_map[t, (i - 1) % N]
            right = triad_map[t, (i + 1) % N]
            if triad_map[t, i] != left or triad_map[t, i] != right:
                boundaries[t, i] = 1

    return boundaries


def compute_defect_distances(defect_map, boundary_map):
    T, N = defect_map.shape
    distances = []

    for t in range(T):
        boundary_indices = np.where(boundary_map[t] == 1)[0]
        defect_indices = np.where(defect_map[t] == 1)[0]

        if len(boundary_indices) == 0 or len(defect_indices) == 0:
            continue

        for d in defect_indices:
            circular_distances = np.minimum(
                np.abs(boundary_indices - d),
                N - np.abs(boundary_indices - d),
            )
            distances.append(np.min(circular_distances))

    return np.array(distances)


# ------------------------------------------------
# Root families
# ------------------------------------------------
def root12_shell(n):
    return int(round(np.sqrt(12 * (2 ** n))))


def root13_shell(n):
    return int(round(np.sqrt(13 * (3 ** n))))


def family_shells():
    root12_ns = list(range(2, 9))
    root13_ns = list(range(1, 6))

    shells = []

    for n in root12_ns:
        N = root12_shell(n)
        if N >= 8:
            shells.append(("root12", n, N, np.sqrt(12 * (2 ** n))))

    for n in root13_ns:
        N = root13_shell(n)
        if N >= 8:
            shells.append(("root13", n, N, np.sqrt(13 * (3 ** n))))

    # remove duplicate N inside same family/n if any weird rounding overlap
    cleaned = []
    seen = set()
    for item in shells:
        key = (item[0], item[2])
        if key not in seen:
            cleaned.append(item)
            seen.add(key)

    return cleaned


# ------------------------------------------------
# Metric computation
# ------------------------------------------------
def evaluate_shell(N, trials=3, steps=1200):
    defect_density_vals = []
    triad_density_vals = []
    defect_boundary_distance_vals = []

    for trial in range(trials):
        history = simulate_history(N=N, steps=steps, seed=1000 + trial)

        defect_map, defect_counts = vortex_scan(history)
        closure_map, closure_counts = compute_closure_history(history)

        boundary_map = compute_triad_boundaries(closure_map)
        distances = compute_defect_distances(defect_map, boundary_map)

        defect_density = defect_map.mean()
        triad_density = closure_map.mean()
        mean_distance = float(np.mean(distances)) if len(distances) > 0 else np.nan

        defect_density_vals.append(defect_density)
        triad_density_vals.append(triad_density)
        defect_boundary_distance_vals.append(mean_distance)

    return {
        "defect_density_mean": float(np.nanmean(defect_density_vals)),
        "triad_density_mean": float(np.nanmean(triad_density_vals)),
        "distance_mean": float(np.nanmean(defect_boundary_distance_vals)),
    }


# ------------------------------------------------
# CSV output
# ------------------------------------------------
def save_metrics_csv(rows, filepath):
    fieldnames = [
        "family",
        "n",
        "root_value",
        "shell_size",
        "defect_density_mean",
        "triad_density_mean",
        "distance_mean",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# ------------------------------------------------
# Plot summary
# ------------------------------------------------
def plot_summary(rows, filepath):
    root12_rows = [r for r in rows if r["family"] == "root12"]
    root13_rows = [r for r in rows if r["family"] == "root13"]

    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=False)

    for subset, label in [(root12_rows, "Root-12"), (root13_rows, "Root-13")]:
        if not subset:
            continue

        x = [r["shell_size"] for r in subset]

        axes[0].plot(x, [r["defect_density_mean"] for r in subset], marker="o", label=label)
        axes[1].plot(x, [r["triad_density_mean"] for r in subset], marker="o", label=label)
        axes[2].plot(x, [r["distance_mean"] for r in subset], marker="o", label=label)

    axes[0].set_title("Root family scan summary")
    axes[0].set_ylabel("Defect density")
    axes[1].set_ylabel("Triadic closure density")
    axes[2].set_ylabel("Mean defect→boundary distance")
    axes[2].set_xlabel("Effective shell size N")

    for ax in axes:
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.show()


# ------------------------------------------------
# Main
# ------------------------------------------------
def main():
    outdir = Path("output")
    outdir.mkdir(exist_ok=True)

    configs = family_shells()
    rows = []

    print("Running root family cycle scan...")
    for family, n, N, root_value in configs:
        print(f"  {family} | n={n} | root≈{root_value:.4f} | N={N}")
        metrics = evaluate_shell(N=N, trials=3, steps=1200)

        rows.append(
            {
                "family": family,
                "n": n,
                "root_value": round(root_value, 6),
                "shell_size": N,
                **metrics,
            }
        )

    save_metrics_csv(rows, outdir / "root_family_metrics.csv")
    plot_summary(rows, outdir / "root_family_summary.png")

    print("Scan completed.")
    print("Saved: output/root_family_metrics.csv")
    print("Saved: output/root_family_summary.png")


if __name__ == "__main__":
    main()
