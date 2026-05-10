#!/usr/bin/env python3
"""
JANUS_OPERATOR / EXP-27
Directed Basin Navigation

Goal:
    Test whether JANUS aperture gates can be used as a
    navigable transport system across the Lorenz attractor.

Core idea:
    - detect aperture gate nodes
    - reconstruct transition graph
    - simulate directed basin navigation
    - measure routing stability and transition entropy

Outputs:
    outputs/exp27_navigation_paths.png
    outputs/exp27_navigation_decision_map.png
    outputs/exp27_transition_entropy.png
    outputs/exp27_navigation_summary.txt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import solve_ivp
from scipy.ndimage import gaussian_filter1d
from sklearn.cluster import KMeans


Array = np.ndarray


# ============================================================
# CONFIG
# ============================================================

@dataclass(frozen=True)
class OutputConfig:
    output_dir: Path = Path(__file__).resolve().parent.parent / "outputs"
    dpi: int = 220


@dataclass(frozen=True)
class ExperimentConfig:
    t_max: float = 140.0
    dt: float = 0.01
    transient_fraction: float = 0.15

    smoothing_scale: int = 16
    gate_quantile: float = 0.995

    n_nodes: int = 4
    navigation_steps: int = 18

    seed: int = 42


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
    n_steps = int(np.floor(cfg.t_max / cfg.dt))

    t_eval = np.linspace(
        0.0,
        n_steps * cfg.dt,
        n_steps + 1,
    )

    sol = solve_ivp(
        lorenz_rhs,
        (0.0, float(t_eval[-1])),
        np.array([1.0, 1.0, 1.0], dtype=float),
        t_eval=t_eval,
        rtol=1e-9,
        atol=1e-9,
    )

    transient_cut = int(cfg.transient_fraction * len(sol.t))

    states = sol.y[:, transient_cut:].T
    times = sol.t[transient_cut:]

    return times, states


# ============================================================
# APERTURE SCORE
# ============================================================

def compute_aperture_score(
    states: Array,
    scale: int,
) -> Array:

    x = gaussian_filter1d(states[:, 0], sigma=scale)
    y = gaussian_filter1d(states[:, 1], sigma=scale)
    z = gaussian_filter1d(states[:, 2], sigma=scale)

    dx = np.gradient(x)
    dy = np.gradient(y)
    dz = np.gradient(z)

    velocity = np.sqrt(dx**2 + dy**2 + dz**2)

    curvature = np.sqrt(
        np.gradient(dx)**2
        + np.gradient(dy)**2
        + np.gradient(dz)**2
    )

    aperture = curvature / (velocity + 1e-9)

    aperture -= aperture.min()
    aperture /= aperture.max()

    return aperture


# ============================================================
# GATE EXTRACTION
# ============================================================

def extract_gate_candidates(
    states: Array,
    aperture: Array,
    cfg: ExperimentConfig,
) -> Tuple[Array, Array]:

    threshold = np.quantile(
        aperture,
        cfg.gate_quantile,
    )

    mask = aperture >= threshold

    gate_points = states[mask]
    gate_scores = aperture[mask]

    return gate_points, gate_scores


# ============================================================
# NODE RECONSTRUCTION
# ============================================================

def reconstruct_nodes(
    gate_points: Array,
    cfg: ExperimentConfig,
) -> Tuple[Array, Array]:

    coords = gate_points[:, [0, 2]]

    kmeans = KMeans(
        n_clusters=cfg.n_nodes,
        random_state=cfg.seed,
        n_init=20,
    )

    labels = kmeans.fit_predict(coords)

    centers = kmeans.cluster_centers_

    return labels, centers


# ============================================================
# TRANSITION MATRIX
# ============================================================

def build_transition_matrix(
    labels: Array,
    n_nodes: int,
) -> Array:

    matrix = np.zeros((n_nodes, n_nodes), dtype=int)

    for i in range(len(labels) - 1):
        a = labels[i]
        b = labels[i + 1]

        if a != b:
            matrix[a, b] += 1

    return matrix


# ============================================================
# NAVIGATION
# ============================================================

def normalize_rows(matrix: Array) -> Array:

    prob = matrix.astype(float)

    row_sum = prob.sum(axis=1, keepdims=True)

    row_sum[row_sum == 0] = 1.0

    prob /= row_sum

    return prob


def navigate_graph(
    prob: Array,
    start_node: int,
    n_steps: int,
    rng: np.random.Generator,
) -> List[int]:

    path = [start_node]

    current = start_node

    for _ in range(n_steps):

        p = prob[current]

        if np.sum(p) == 0:
            break

        nxt = rng.choice(
            np.arange(len(p)),
            p=p,
        )

        path.append(int(nxt))
        current = int(nxt)

    return path


# ============================================================
# ENTROPY
# ============================================================

def compute_transition_entropy(
    prob: Array,
) -> Array:

    entropy = np.zeros(prob.shape[0])

    for i in range(prob.shape[0]):

        p = prob[i]

        mask = p > 0

        if np.any(mask):
            entropy[i] = -np.sum(
                p[mask] * np.log2(p[mask])
            )

    return entropy


# ============================================================
# PLOTS
# ============================================================

def plot_navigation_paths(
    states: Array,
    gate_points: Array,
    centers: Array,
    path: List[int],
    output_path: Path,
    cfg: OutputConfig,
) -> None:

    fig, ax = plt.subplots(figsize=(11, 9))

    ax.scatter(
        states[:, 0],
        states[:, 2],
        s=1,
        alpha=0.08,
        color="gray",
    )

    ax.scatter(
        gate_points[:, 0],
        gate_points[:, 2],
        s=16,
        alpha=0.7,
    )

    for i, c in enumerate(centers):

        ax.scatter(
            c[0],
            c[1],
            s=350,
            marker="X",
            edgecolor="black",
            linewidth=2,
            zorder=5,
        )

        ax.text(
            c[0] + 0.3,
            c[1] + 0.3,
            f"N{i}",
            fontsize=12,
            weight="bold",
        )

    for i in range(len(path) - 1):

        a = centers[path[i]]
        b = centers[path[i + 1]]

        ax.plot(
            [a[0], b[0]],
            [a[1], b[1]],
            linewidth=3,
            alpha=0.8,
        )

    ax.axvline(
        0,
        linestyle="--",
        alpha=0.5,
    )

    ax.set_title(
        "EXP-27 — Directed Basin Navigation"
    )

    ax.set_xlabel("x")
    ax.set_ylabel("z")

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=cfg.dpi,
    )

    plt.close(fig)


def plot_decision_map(
    prob: Array,
    output_path: Path,
    cfg: OutputConfig,
) -> None:

    fig, ax = plt.subplots(figsize=(8, 6))

    im = ax.imshow(
        prob,
        cmap="magma",
        origin="upper",
    )

    for i in range(prob.shape[0]):
        for j in range(prob.shape[1]):

            ax.text(
                j,
                i,
                f"{prob[i,j]:.2f}",
                ha="center",
                va="center",
                color="white",
                fontsize=11,
            )

    ax.set_title(
        "EXP-27 — Basin Routing Probability Map"
    )

    ax.set_xlabel("to node")
    ax.set_ylabel("from node")

    fig.colorbar(
        im,
        ax=ax,
        label="transition probability",
    )

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=cfg.dpi,
    )

    plt.close(fig)


def plot_transition_entropy(
    entropy: Array,
    output_path: Path,
    cfg: OutputConfig,
) -> None:

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        np.arange(len(entropy)),
        entropy,
    )

    ax.set_xlabel("node")
    ax.set_ylabel("entropy")

    ax.set_title(
        "EXP-27 — Transition Entropy"
    )

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=cfg.dpi,
    )

    plt.close(fig)


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    cfg = ExperimentConfig()
    out_cfg = OutputConfig()

    out_cfg.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    rng = np.random.default_rng(cfg.seed)

    print("\n==========================================")
    print("EXP-27 — DIRECTED BASIN NAVIGATION")
    print("==========================================")

    times, states = simulate_lorenz(cfg)

    aperture = compute_aperture_score(
        states,
        cfg.smoothing_scale,
    )

    gate_points, gate_scores = extract_gate_candidates(
        states,
        aperture,
        cfg,
    )

    labels, centers = reconstruct_nodes(
        gate_points,
        cfg,
    )

    matrix = build_transition_matrix(
        labels,
        cfg.n_nodes,
    )

    prob = normalize_rows(matrix)

    path = navigate_graph(
        prob,
        start_node=0,
        n_steps=cfg.navigation_steps,
        rng=rng,
    )

    entropy = compute_transition_entropy(prob)

    # ========================================================
    # OUTPUTS
    # ========================================================

    plot_navigation_paths(
        states,
        gate_points,
        centers,
        path,
        out_cfg.output_dir / "exp27_navigation_paths.png",
        out_cfg,
    )

    plot_decision_map(
        prob,
        out_cfg.output_dir / "exp27_navigation_decision_map.png",
        out_cfg,
    )

    plot_transition_entropy(
        entropy,
        out_cfg.output_dir / "exp27_transition_entropy.png",
        out_cfg,
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    summary_path = (
        out_cfg.output_dir
        / "exp27_navigation_summary.txt"
    )

    with open(summary_path, "w") as f:

        f.write(
            "EXP-27 — Directed Basin Navigation\n"
        )

        f.write("=" * 48 + "\n\n")

        f.write(
            f"gate candidates: {len(gate_points)}\n"
        )

        f.write(
            f"graph nodes: {cfg.n_nodes}\n\n"
        )

        f.write("Transition probability matrix:\n\n")

        for row in prob:
            f.write(
                " ".join(
                    f"{v:.3f}" for v in row
                ) + "\n"
            )

        f.write("\n")

        f.write(
            f"navigation path:\n{path}\n\n"
        )

        f.write("Transition entropy:\n")

        for i, e in enumerate(entropy):
            f.write(
                f"node {i}: {e:.6f}\n"
            )

        f.write("\n")

        f.write(
            "Working interpretation:\n"
        )

        f.write(
            "- JANUS gates may support directed basin navigation\n"
        )

        f.write(
            "- low entropy nodes indicate deterministic routing\n"
        )

        f.write(
            "- high entropy nodes indicate unstable routing zones\n"
        )

        f.write(
            "- navigation paths reveal preferred transport corridors\n"
        )

        f.write(
            "- this remains exploratory\n"
        )

    print("\noutputs generated:\n")

    print(
        "outputs/exp27_navigation_paths.png"
    )

    print(
        "outputs/exp27_navigation_decision_map.png"
    )

    print(
        "outputs/exp27_transition_entropy.png"
    )

    print(
        "outputs/exp27_navigation_summary.txt"
    )

    print("\nEXP-27 complete.\n")


if __name__ == "__main__":
    main()
