#!/usr/bin/env python3
"""
JANUS_OPERATOR / EXP-28
Predictive Gate Transition Forecast

Goal:
    Test whether JANUS aperture structures contain
    short-horizon predictive transition information.

Core Idea:
    Use current aperture-state geometry
    to estimate upcoming basin transitions.

This experiment does NOT attempt
full trajectory prediction.

Instead it asks:

    "Can gate geometry predict
     near-future transport routing?"

Outputs:
    outputs/exp28_prediction_transition_map.png
    outputs/exp28_prediction_confidence.png
    outputs/exp28_prediction_paths.png
    outputs/exp28_prediction_summary.txt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, List

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans


Array = np.ndarray


# ============================================================
# CONFIG
# ============================================================

@dataclass(frozen=True)
class OutputConfig:
    output_dir: Path = (
        Path(__file__).resolve().parent.parent / "outputs"
    )
    dpi: int = 220


@dataclass(frozen=True)
class ExperimentConfig:
    t_max: float = 140.0
    dt: float = 0.01

    transient_fraction: float = 0.15

    gate_quantile: float = 0.995

    memory_lag: int = 220

    n_nodes: int = 4

    prediction_horizon: int = 40

    random_seed: int = 42


# ============================================================
# LORENZ
# ============================================================

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

    t_eval = np.linspace(
        0.0,
        cfg.t_max,
        n_steps,
    )

    sol = solve_ivp(
        lorenz_rhs,
        (0.0, cfg.t_max),
        np.array([1.0, 1.0, 1.0]),
        t_eval=t_eval,
        rtol=1e-9,
        atol=1e-9,
    )

    states = sol.y.T

    transient_cut = int(
        cfg.transient_fraction * len(states)
    )

    return (
        sol.t[transient_cut:],
        states[transient_cut:],
    )


# ============================================================
# APERTURE SCORE
# ============================================================

def compute_velocity(states: Array) -> Array:
    return np.gradient(states, axis=0)


def compute_curvature(
    velocity: Array,
) -> Array:

    accel = np.gradient(velocity, axis=0)

    cross = np.cross(
        velocity,
        accel,
    )

    num = np.linalg.norm(cross, axis=1)

    den = (
        np.linalg.norm(velocity, axis=1) ** 3
        + 1e-12
    )

    return num / den


def compute_aperture_score(
    states: Array,
    lag: int,
) -> Array:

    vel = compute_velocity(states)

    curvature = compute_curvature(vel)

    delta = np.linalg.norm(
        states[lag:] - states[:-lag],
        axis=1,
    )

    delta = np.pad(
        delta,
        (lag, 0),
        mode="edge",
    )

    curvature = (
        curvature - curvature.min()
    ) / (
        curvature.max() - curvature.min()
        + 1e-12
    )

    delta = (
        delta - delta.min()
    ) / (
        delta.max() - delta.min()
        + 1e-12
    )

    aperture = (
        0.55 * curvature
        + 0.45 * delta
    )

    aperture = (
        aperture - aperture.min()
    ) / (
        aperture.max() - aperture.min()
        + 1e-12
    )

    return aperture


# ============================================================
# GATE DETECTION
# ============================================================

def detect_gate_candidates(
    aperture: Array,
    q: float,
) -> Array:

    threshold = np.quantile(
        aperture,
        q,
    )

    return aperture >= threshold


# ============================================================
# BASIN GRAPH
# ============================================================

def build_basin_nodes(
    states: Array,
    mask: Array,
    n_nodes: int,
    seed: int,
):

    gate_points = states[mask]

    km = KMeans(
        n_clusters=n_nodes,
        random_state=seed,
        n_init=20,
    )

    labels = km.fit_predict(gate_points)

    return (
        gate_points,
        labels,
        km.cluster_centers_,
    )


# ============================================================
# TRANSITION PREDICTION
# ============================================================

def predict_next_nodes(
    labels: Array,
    horizon: int,
    n_nodes: int,
):

    matrix = np.zeros(
        (n_nodes, n_nodes),
        dtype=float,
    )

    for i in range(
        len(labels) - horizon
    ):

        a = labels[i]
        b = labels[i + horizon]

        matrix[a, b] += 1.0

    row_sums = matrix.sum(axis=1)

    probs = np.divide(
        matrix,
        row_sums[:, None],
        out=np.zeros_like(matrix),
        where=row_sums[:, None] != 0,
    )

    return probs


def build_prediction_paths(
    probs: Array,
    start: int = 0,
    length: int = 12,
):

    current = start

    path = [current]

    for _ in range(length):

        row = probs[current]

        if row.sum() == 0:
            break

        nxt = np.argmax(row)

        path.append(int(nxt))

        current = int(nxt)

    return path


# ============================================================
# PLOTS
# ============================================================

def plot_transition_map(
    centers: Array,
    probs: Array,
    outpath: Path,
    dpi: int,
):

    plt.figure(figsize=(9, 8))

    for i in range(len(centers)):

        x1, y1 = centers[i][:2]

        plt.scatter(
            x1,
            y1,
            s=260,
            zorder=5,
        )

        plt.text(
            x1,
            y1,
            f"{i}",
            fontsize=12,
            ha="center",
            va="center",
            color="white",
        )

        for j in range(len(centers)):

            p = probs[i, j]

            if p <= 0:
                continue

            x2, y2 = centers[j][:2]

            plt.plot(
                [x1, x2],
                [y1, y2],
                linewidth=4 * p,
                alpha=0.7,
            )

    plt.title(
        "EXP-28 — Transition Prediction Map"
    )

    plt.xlabel("x")
    plt.ylabel("y")

    plt.tight_layout()

    plt.savefig(outpath, dpi=dpi)

    plt.close()


def plot_prediction_confidence(
    probs: Array,
    outpath: Path,
    dpi: int,
):

    plt.figure(figsize=(8, 6))

    plt.imshow(
        probs,
        aspect="auto",
    )

    plt.colorbar(
        label="transition probability"
    )

    plt.title(
        "EXP-28 — Prediction Confidence Matrix"
    )

    plt.xlabel("future node")
    plt.ylabel("current node")

    plt.tight_layout()

    plt.savefig(outpath, dpi=dpi)

    plt.close()


def plot_navigation_path(
    centers: Array,
    path: List[int],
    outpath: Path,
    dpi: int,
):

    plt.figure(figsize=(9, 8))

    for i in range(len(path) - 1):

        a = centers[path[i]]
        b = centers[path[i + 1]]

        plt.plot(
            [a[0], b[0]],
            [a[1], b[1]],
            linewidth=3,
            alpha=0.8,
        )

    for idx, c in enumerate(centers):

        plt.scatter(
            c[0],
            c[1],
            s=260,
        )

        plt.text(
            c[0],
            c[1],
            f"{idx}",
            fontsize=12,
            ha="center",
            va="center",
            color="white",
        )

    plt.title(
        "EXP-28 — Predicted Basin Navigation"
    )

    plt.xlabel("x")
    plt.ylabel("y")

    plt.tight_layout()

    plt.savefig(outpath, dpi=dpi)

    plt.close()


# ============================================================
# SUMMARY
# ============================================================

def write_summary(
    probs: Array,
    path: List[int],
    outpath: Path,
):

    entropies = []

    for row in probs:

        p = row[row > 0]

        if len(p) == 0:
            entropies.append(0.0)
            continue

        H = -np.sum(p * np.log2(p))

        entropies.append(H)

    lines = []

    lines.append(
        "EXP-28 — Predictive Basin Navigation"
    )

    lines.append("=" * 48)
    lines.append("")

    lines.append(
        "Transition probability matrix:"
    )

    lines.append("")

    for row in probs:

        lines.append(
            " ".join(
                f"{v:.3f}" for v in row
            )
        )

    lines.append("")
    lines.append(
        f"predicted navigation path:"
    )

    lines.append(str(path))

    lines.append("")
    lines.append(
        "Node entropy:"
    )

    for i, H in enumerate(entropies):

        lines.append(
            f"node {i}: {H:.6f}"
        )

    lines.append("")
    lines.append(
        "Working interpretation:"
    )

    lines.append(
        "- JANUS gates may contain predictive transport structure"
    )

    lines.append(
        "- low entropy nodes may act as routing anchors"
    )

    lines.append(
        "- high entropy nodes may act as transition decision zones"
    )

    lines.append(
        "- transport corridors may permit short-horizon forecasting"
    )

    lines.append("")
    lines.append(
        "Exploratory only."
    )

    outpath.write_text(
        "\n".join(lines)
    )


# ============================================================
# MAIN
# ============================================================

def main():

    cfg = ExperimentConfig()

    outcfg = OutputConfig()

    outcfg.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()
    print("=" * 44)
    print(
        "EXP-28 — PREDICTIVE GATE FORECAST"
    )
    print("=" * 44)
    print()

    t, states = simulate_lorenz(cfg)

    aperture = compute_aperture_score(
        states,
        cfg.memory_lag,
    )

    gate_mask = detect_gate_candidates(
        aperture,
        cfg.gate_quantile,
    )

    (
        gate_points,
        labels,
        centers,
    ) = build_basin_nodes(
        states,
        gate_mask,
        cfg.n_nodes,
        cfg.random_seed,
    )

    probs = predict_next_nodes(
        labels,
        cfg.prediction_horizon,
        cfg.n_nodes,
    )

    path = build_prediction_paths(
        probs,
        start=0,
        length=12,
    )

    plot_transition_map(
        centers,
        probs,
        outcfg.output_dir
        / "exp28_prediction_transition_map.png",
        outcfg.dpi,
    )

    plot_prediction_confidence(
        probs,
        outcfg.output_dir
        / "exp28_prediction_confidence.png",
        outcfg.dpi,
    )

    plot_navigation_path(
        centers,
        path,
        outcfg.output_dir
        / "exp28_prediction_paths.png",
        outcfg.dpi,
    )

    write_summary(
        probs,
        path,
        outcfg.output_dir
        / "exp28_prediction_summary.txt",
    )

    print("outputs generated:")
    print()

    print(
        "outputs/exp28_prediction_transition_map.png"
    )

    print(
        "outputs/exp28_prediction_confidence.png"
    )

    print(
        "outputs/exp28_prediction_paths.png"
    )

    print(
        "outputs/exp28_prediction_summary.txt"
    )

    print()
    print("EXP-28 complete.")
    print()


if __name__ == "__main__":
    main()
