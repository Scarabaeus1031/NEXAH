#!/usr/bin/env python3
"""
JANUS_OPERATOR / EXP-29
Prediction Stability Test

Script:
    scripts_2/janus_prediction_stability_test.py

Goal:
    Test whether EXP-28 predictive routing remains stable under perturbation.

Outputs:
    outputs/exp29_prediction_stability_map.png
    outputs/exp29_forecast_noise_scan.png
    outputs/exp29_path_persistence.png
    outputs/exp29_prediction_robustness_summary.txt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from sklearn.cluster import KMeans


Array = np.ndarray


@dataclass(frozen=True)
class ExperimentConfig:
    t_max: float = 140.0
    dt: float = 0.01
    transient_fraction: float = 0.15
    memory_lag: int = 220
    gate_quantile: float = 0.995
    n_nodes: int = 4
    prediction_horizon: int = 40
    path_length: int = 12
    seed: int = 42
    noise_levels: Tuple[float, ...] = (
        0.0, 0.0005, 0.001, 0.0025, 0.005, 0.01, 0.025
    )


@dataclass(frozen=True)
class OutputConfig:
    output_dir: Path = Path(__file__).resolve().parent.parent / "outputs"
    dpi: int = 220


def lorenz_rhs(_: float, s: Array) -> Array:
    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0
    x, y, z = s
    return np.array([
        sigma * (y - x),
        x * (rho - z) - y,
        x * y - beta * z,
    ])


def simulate_lorenz(cfg: ExperimentConfig) -> Tuple[Array, Array]:
    n_steps = int(cfg.t_max / cfg.dt)
    t_eval = np.linspace(0.0, cfg.t_max, n_steps)

    sol = solve_ivp(
        lorenz_rhs,
        (0.0, cfg.t_max),
        np.array([1.0, 1.0, 1.0]),
        t_eval=t_eval,
        rtol=1e-9,
        atol=1e-9,
    )

    states = sol.y.T
    cut = int(cfg.transient_fraction * len(states))
    return sol.t[cut:], states[cut:]


def compute_velocity(states: Array) -> Array:
    return np.gradient(states, axis=0)


def compute_curvature(velocity: Array) -> Array:
    accel = np.gradient(velocity, axis=0)
    cross = np.cross(velocity, accel)
    num = np.linalg.norm(cross, axis=1)
    den = np.linalg.norm(velocity, axis=1) ** 3 + 1e-12
    return num / den


def normalize(x: Array) -> Array:
    return (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-12)


def compute_aperture_score(states: Array, lag: int) -> Array:
    velocity = compute_velocity(states)
    curvature = normalize(compute_curvature(velocity))

    delta = np.linalg.norm(states[lag:] - states[:-lag], axis=1)
    delta = np.pad(delta, (lag, 0), mode="edge")
    delta = normalize(delta)

    aperture = 0.55 * curvature + 0.45 * delta
    return normalize(aperture)


def detect_gates(aperture: Array, q: float) -> Array:
    return aperture >= np.quantile(aperture, q)


def build_nodes(
    states: Array,
    mask: Array,
    n_nodes: int,
    seed: int,
) -> Tuple[Array, Array, Array]:
    gate_points = states[mask]

    km = KMeans(
        n_clusters=n_nodes,
        random_state=seed,
        n_init=20,
    )

    labels = km.fit_predict(gate_points)
    return gate_points, labels, km.cluster_centers_


def transition_probabilities(labels: Array, horizon: int, n_nodes: int) -> Array:
    mat = np.zeros((n_nodes, n_nodes), dtype=float)

    for i in range(len(labels) - horizon):
        mat[labels[i], labels[i + horizon]] += 1.0

    rows = mat.sum(axis=1)
    probs = np.divide(
        mat,
        rows[:, None],
        out=np.zeros_like(mat),
        where=rows[:, None] != 0,
    )

    return probs


def predicted_path(
    probs: Array,
    start: int = 0,
    length: int = 12,
) -> List[int]:
    path = [start]
    current = start

    for _ in range(length):
        row = probs[current]
        if row.sum() == 0:
            break
        nxt = int(np.argmax(row))
        path.append(nxt)
        current = nxt

    return path


def path_similarity(a: List[int], b: List[int]) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(1 for i in range(n) if a[i] == b[i]) / n


def node_entropy(probs: Array) -> Array:
    out = []
    for row in probs:
        p = row[row > 0]
        if len(p) == 0:
            out.append(0.0)
        else:
            out.append(float(-np.sum(p * np.log2(p))))
    return np.array(out)


def run_single(
    states: Array,
    cfg: ExperimentConfig,
    noise: float,
    rng: np.random.Generator,
) -> Dict[str, object]:
    noisy = states.copy()

    if noise > 0:
        scale = np.std(states, axis=0)
        noisy = noisy + rng.normal(0.0, noise, noisy.shape) * scale

    aperture = compute_aperture_score(noisy, cfg.memory_lag)
    mask = detect_gates(aperture, cfg.gate_quantile)

    _, labels, centers = build_nodes(
        noisy,
        mask,
        cfg.n_nodes,
        cfg.seed,
    )

    probs = transition_probabilities(
        labels,
        cfg.prediction_horizon,
        cfg.n_nodes,
    )

    path = predicted_path(
        probs,
        start=0,
        length=cfg.path_length,
    )

    return {
        "aperture": aperture,
        "mask": mask,
        "labels": labels,
        "centers": centers,
        "probs": probs,
        "path": path,
        "entropy": node_entropy(probs),
    }


def plot_stability_map(
    results: Dict[float, Dict[str, object]],
    outpath: Path,
    dpi: int,
) -> None:
    noise_levels = list(results.keys())
    matrices = [results[n]["probs"] for n in noise_levels]

    fig, axes = plt.subplots(1, len(noise_levels), figsize=(18, 3))

    for ax, noise, mat in zip(axes, noise_levels, matrices):
        ax.imshow(mat, vmin=0, vmax=1)
        ax.set_title(f"noise={noise:g}")
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle("EXP-29 — Prediction Stability Across Noise")
    plt.tight_layout()
    plt.savefig(outpath, dpi=dpi)
    plt.close()


def plot_noise_scan(
    noise_levels: List[float],
    similarities: List[float],
    mean_entropy: List[float],
    outpath: Path,
    dpi: int,
) -> None:
    plt.figure(figsize=(9, 6))
    plt.plot(noise_levels, similarities, marker="o", label="path similarity")
    plt.plot(noise_levels, mean_entropy, marker="o", label="mean entropy")
    plt.xlabel("noise level")
    plt.ylabel("value")
    plt.title("EXP-29 — Forecast Noise Scan")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(outpath, dpi=dpi)
    plt.close()


def plot_path_persistence(
    noise_levels: List[float],
    paths: List[List[int]],
    outpath: Path,
    dpi: int,
) -> None:
    max_len = max(len(p) for p in paths)
    mat = np.full((len(paths), max_len), -1.0)

    for i, path in enumerate(paths):
        mat[i, :len(path)] = path

    plt.figure(figsize=(10, 6))
    plt.imshow(mat, aspect="auto")
    plt.colorbar(label="predicted node")
    plt.yticks(range(len(noise_levels)), [f"{n:g}" for n in noise_levels])
    plt.xlabel("prediction step")
    plt.ylabel("noise level")
    plt.title("EXP-29 — Path Persistence")
    plt.tight_layout()
    plt.savefig(outpath, dpi=dpi)
    plt.close()


def write_summary(
    results: Dict[float, Dict[str, object]],
    similarities: List[float],
    outpath: Path,
) -> None:
    lines = []
    lines.append("EXP-29 — Prediction Stability Test")
    lines.append("=" * 48)
    lines.append("")
    lines.append("Goal:")
    lines.append("Test whether predictive JANUS basin routing remains stable under perturbation.")
    lines.append("")

    base_path = results[0.0]["path"]
    lines.append(f"baseline path: {base_path}")
    lines.append("")

    for idx, (noise, data) in enumerate(results.items()):
        lines.append(f"noise level: {noise:g}")
        lines.append("-" * 32)
        lines.append(f"path: {data['path']}")
        lines.append(f"path similarity to baseline: {similarities[idx]:.6f}")
        lines.append("entropy:")
        for i, h in enumerate(data["entropy"]):
            lines.append(f"  node {i}: {h:.6f}")
        lines.append("transition probability matrix:")
        for row in data["probs"]:
            lines.append("  " + " ".join(f"{v:.3f}" for v in row))
        lines.append("")

    lines.append("Working interpretation:")
    lines.append("- stable predicted paths indicate robust transport routing")
    lines.append("- unstable paths indicate noise-sensitive gate decision structure")
    lines.append("- entropy changes identify fragile routing nodes")
    lines.append("- exploratory only")

    outpath.write_text("\n".join(lines))


def main() -> None:
    cfg = ExperimentConfig()
    outcfg = OutputConfig()
    outcfg.output_dir.mkdir(parents=True, exist_ok=True)

    print()
    print("=" * 52)
    print("EXP-29 — PREDICTION STABILITY TEST")
    print("=" * 52)
    print()

    _, states = simulate_lorenz(cfg)
    rng = np.random.default_rng(cfg.seed)

    results: Dict[float, Dict[str, object]] = {}

    for noise in cfg.noise_levels:
        print(f"running noise level {noise:g}...")
        results[noise] = run_single(states, cfg, noise, rng)

    baseline_path = results[0.0]["path"]
    noise_levels = list(results.keys())
    paths = [results[n]["path"] for n in noise_levels]
    similarities = [path_similarity(baseline_path, p) for p in paths]
    mean_entropy = [float(np.mean(results[n]["entropy"])) for n in noise_levels]

    plot_stability_map(
        results,
        outcfg.output_dir / "exp29_prediction_stability_map.png",
        outcfg.dpi,
    )

    plot_noise_scan(
        noise_levels,
        similarities,
        mean_entropy,
        outcfg.output_dir / "exp29_forecast_noise_scan.png",
        outcfg.dpi,
    )

    plot_path_persistence(
        noise_levels,
        paths,
        outcfg.output_dir / "exp29_path_persistence.png",
        outcfg.dpi,
    )

    write_summary(
        results,
        similarities,
        outcfg.output_dir / "exp29_prediction_robustness_summary.txt",
    )

    print()
    print("outputs generated:")
    print("outputs/exp29_prediction_stability_map.png")
    print("outputs/exp29_forecast_noise_scan.png")
    print("outputs/exp29_path_persistence.png")
    print("outputs/exp29_prediction_robustness_summary.txt")
    print()
    print("EXP-29 complete.")
    print()


if __name__ == "__main__":
    main()
