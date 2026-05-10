#!/usr/bin/env python3
"""
JANUS_OPERATOR / EXP-26
Aperture Basin Graph Reconstruction

Script:
    janus_aperture_basin_graph.py

Goal:
    Reconstruct a graph-like transport structure between
    JANUS aperture gate regions.

Focus:
    - gate-node clustering
    - transition edges
    - directional transport geometry
    - hidden routing corridors
    - basin-network organization

Core Question:
    Do aperture gates behave like isolated events,
    or like connected transport nodes inside
    a structured transition graph?

Outputs:
    outputs/exp26_aperture_graph_overlay.png
    outputs/exp26_transition_adjacency_matrix.png
    outputs/exp26_gate_transition_network.png
    outputs/exp26_transport_flow_map.png
    outputs/exp26_aperture_graph_summary.txt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import solve_ivp
from scipy.spatial.distance import cdist
from scipy.ndimage import gaussian_filter
from sklearn.cluster import DBSCAN


Array = np.ndarray


# ------------------------------------------------------------
# Config
# ------------------------------------------------------------

@dataclass(frozen=True)
class OutputConfig:
    output_dir: Path = Path(__file__).resolve().parent.parent / "outputs"
    dpi: int = 220


@dataclass(frozen=True)
class ExperimentConfig:
    t_max: float = 140.0
    dt: float = 0.01
    transient_fraction: float = 0.15

    memory_lag: int = 230
    gate_quantile: float = 0.995

    dbscan_eps: float = 1.5
    dbscan_min_samples: int = 3


# ------------------------------------------------------------
# Lorenz
# ------------------------------------------------------------

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
        method="DOP853",
        rtol=1.0e-10,
        atol=1.0e-12,
    )

    if not sol.success:
        raise RuntimeError(sol.message)

    t = sol.t
    states = sol.y.T

    cut = int(len(states) * cfg.transient_fraction)

    return t[cut:], states[cut:]


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def normalize(v: Array, eps: float = 1.0e-12) -> Array:
    vmin = np.nanmin(v)
    vmax = np.nanmax(v)

    scale = vmax - vmin

    if scale < eps:
        return np.zeros_like(v)

    return (v - vmin) / scale


def compute_janus(t: Array, states: Array) -> Tuple[Array, Array]:
    dt_f = (t[2:] - t[1:-1])[:, None]
    dt_b = (t[1:-1] - t[:-2])[:, None]

    forward = (states[2:] - states[1:-1]) / dt_f
    backward = (states[1:-1] - states[:-2]) / dt_b

    overlap = forward * backward

    numerator = np.linalg.norm(overlap, axis=1)
    denominator = (
        np.linalg.norm(forward, axis=1)
        * np.linalg.norm(backward, axis=1)
        + 1.0e-8
    )

    janus = numerator / denominator

    return states[1:-1], janus


def compute_memory(janus: Array, lag: int) -> Array:
    memory = np.zeros_like(janus)

    if lag <= 0 or lag >= len(janus):
        return memory

    delayed = 1.0 - np.abs(janus[lag:] - janus[:-lag])

    memory[lag:] = normalize(delayed)

    return memory


def compute_aperture_score(
    states: Array,
    janus: Array,
    memory: Array,
) -> Array:
    velocity = np.gradient(states, axis=0)
    acceleration = np.gradient(velocity, axis=0)

    speed = np.linalg.norm(velocity, axis=1)
    accel = np.linalg.norm(acceleration, axis=1)

    radius = np.linalg.norm(states, axis=1)
    breathing = np.abs(np.gradient(radius))

    low_janus = 1.0 - normalize(janus)
    accel_n = normalize(accel)
    breathing_n = normalize(breathing)
    memory_n = normalize(memory)

    axis_proximity = 1.0 - normalize(np.abs(states[:, 0]))

    score = (
        0.30 * low_janus
        + 0.25 * accel_n
        + 0.20 * breathing_n
        + 0.15 * axis_proximity
        + 0.10 * memory_n
    )

    return normalize(score)


# ------------------------------------------------------------
# Gate graph reconstruction
# ------------------------------------------------------------

def cluster_gate_nodes(
    gate_points: Array,
    cfg: ExperimentConfig,
) -> Tuple[Array, Array]:
    clustering = DBSCAN(
        eps=cfg.dbscan_eps,
        min_samples=cfg.dbscan_min_samples,
    )

    labels = clustering.fit_predict(gate_points[:, [0, 2]])

    valid = labels >= 0

    unique_labels = np.unique(labels[valid])

    centers = []

    for label in unique_labels:
        pts = gate_points[labels == label]

        centers.append(np.mean(pts, axis=0))

    return labels, np.array(centers)


def build_transition_matrix(
    labels: Array,
) -> Array:
    valid = labels >= 0

    unique_labels = np.unique(labels[valid])

    n = len(unique_labels)

    index_map = {lab: i for i, lab in enumerate(unique_labels)}

    M = np.zeros((n, n))

    prev = None

    for lab in labels:
        if lab < 0:
            continue

        idx = index_map[lab]

        if prev is not None and prev != idx:
            M[prev, idx] += 1

        prev = idx

    return M


# ------------------------------------------------------------
# Plots
# ------------------------------------------------------------

def plot_graph_overlay(
    states: Array,
    gate_points: Array,
    labels: Array,
    centers: Array,
    out_path: Path,
    dpi: int,
) -> None:
    fig, ax = plt.subplots(figsize=(11, 9))

    ax.scatter(
        states[:, 0],
        states[:, 2],
        s=1,
        alpha=0.08,
        color="gray",
    )

    unique_labels = np.unique(labels)

    cmap = plt.cm.tab10

    for i, lab in enumerate(unique_labels):
        if lab < 0:
            continue

        pts = gate_points[labels == lab]

        ax.scatter(
            pts[:, 0],
            pts[:, 2],
            s=35,
            alpha=0.85,
            color=cmap(i % 10),
            label=f"node {lab}",
        )

    ax.scatter(
        centers[:, 0],
        centers[:, 2],
        s=250,
        color="black",
        marker="x",
        linewidths=3,
    )

    ax.axvline(0.0, linestyle="--", alpha=0.4)

    ax.set_title(
        "EXP-26 — Aperture Basin Graph Overlay\n"
        "Clustered gate-node reconstruction"
    )

    ax.set_xlabel("x")
    ax.set_ylabel("z")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_transition_matrix(
    M: Array,
    out_path: Path,
    dpi: int,
) -> None:
    fig, ax = plt.subplots(figsize=(8, 7))

    im = ax.imshow(
        M,
        cmap="magma",
        interpolation="nearest",
    )

    ax.set_title(
        "EXP-26 — Transition Adjacency Matrix"
    )

    ax.set_xlabel("to node")
    ax.set_ylabel("from node")

    plt.colorbar(im, ax=ax, label="transition count")

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_gate_network(
    centers: Array,
    M: Array,
    out_path: Path,
    dpi: int,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.scatter(
        centers[:, 0],
        centers[:, 2],
        s=300,
        color="orange",
        edgecolors="black",
        zorder=5,
    )

    n = len(centers)

    for i in range(n):
        ax.text(
            centers[i, 0],
            centers[i, 2],
            str(i),
            ha="center",
            va="center",
            fontsize=10,
            weight="bold",
        )

    max_val = np.max(M) if np.max(M) > 0 else 1.0

    for i in range(n):
        for j in range(n):
            if M[i, j] <= 0:
                continue

            p1 = centers[i]
            p2 = centers[j]

            strength = M[i, j] / max_val

            ax.plot(
                [p1[0], p2[0]],
                [p1[2], p2[2]],
                linewidth=1.0 + 5.0 * strength,
                alpha=0.7,
            )

    ax.axvline(0.0, linestyle="--", alpha=0.4)

    ax.set_title(
        "EXP-26 — Aperture Transition Network"
    )

    ax.set_xlabel("x")
    ax.set_ylabel("z")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_transport_flow_map(
    states: Array,
    gate_points: Array,
    out_path: Path,
    dpi: int,
) -> None:
    H, xe, ze = np.histogram2d(
        gate_points[:, 0],
        gate_points[:, 2],
        bins=260,
    )

    H = gaussian_filter(H.T, sigma=2.0)

    fig, ax = plt.subplots(figsize=(11, 8))

    ax.scatter(
        states[:, 0],
        states[:, 2],
        s=1,
        alpha=0.04,
        color="gray",
    )

    im = ax.imshow(
        H,
        origin="lower",
        extent=[xe[0], xe[-1], ze[0], ze[-1]],
        aspect="auto",
        cmap="inferno",
        alpha=0.95,
    )

    ax.axvline(0.0, linestyle="--", alpha=0.5)

    ax.set_title(
        "EXP-26 — Aperture Transport Flow Map"
    )

    ax.set_xlabel("x")
    ax.set_ylabel("z")

    plt.colorbar(im, ax=ax, label="gate density")

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

def write_summary(
    centers: Array,
    M: Array,
    gate_count: int,
    out_path: Path,
) -> None:
    lines = []

    lines.append("EXP-26 — Aperture Basin Graph Reconstruction")
    lines.append("================================================")
    lines.append("")

    lines.append(f"gate candidates: {gate_count}")
    lines.append(f"graph nodes: {len(centers)}")
    lines.append("")

    lines.append("Transition matrix:")
    lines.append("")

    for row in M:
        lines.append(
            " ".join(f"{int(v):4d}" for v in row)
        )

    lines.append("")
    lines.append("Working interpretation:")
    lines.append("- aperture gates may organize into clustered transport nodes")
    lines.append("- transition edges suggest non-random routing")
    lines.append("- basin transfer may occur through graph-mediated corridors")
    lines.append("- hidden transport geometry may exist beneath continuous flow")
    lines.append("")
    lines.append("Exploratory only.")
    lines.append("")

    out_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def run_experiment() -> None:
    out_cfg = OutputConfig()
    cfg = ExperimentConfig()

    out_cfg.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()
    print("======================================")
    print("EXP-26 — APERTURE BASIN GRAPH")
    print("======================================")
    print()

    t, states = simulate_lorenz(cfg)

    core_states, janus = compute_janus(t, states)

    memory = compute_memory(
        janus,
        cfg.memory_lag,
    )

    n = min(
        len(core_states),
        len(janus),
        len(memory),
    )

    core_states = core_states[:n]
    janus = janus[:n]
    memory = memory[:n]

    aperture = compute_aperture_score(
        core_states,
        janus,
        memory,
    )

    threshold = np.quantile(
        aperture,
        cfg.gate_quantile,
    )

    gate_mask = aperture >= threshold

    gate_points = core_states[gate_mask]

    labels, centers = cluster_gate_nodes(
        gate_points,
        cfg,
    )

    M = build_transition_matrix(labels)

    plot_graph_overlay(
        core_states,
        gate_points,
        labels,
        centers,
        out_cfg.output_dir / "exp26_aperture_graph_overlay.png",
        out_cfg.dpi,
    )

    plot_transition_matrix(
        M,
        out_cfg.output_dir / "exp26_transition_adjacency_matrix.png",
        out_cfg.dpi,
    )

    plot_gate_network(
        centers,
        M,
        out_cfg.output_dir / "exp26_gate_transition_network.png",
        out_cfg.dpi,
    )

    plot_transport_flow_map(
        core_states,
        gate_points,
        out_cfg.output_dir / "exp26_transport_flow_map.png",
        out_cfg.dpi,
    )

    write_summary(
        centers,
        M,
        len(gate_points),
        out_cfg.output_dir / "exp26_aperture_graph_summary.txt",
    )

    print("outputs generated:")
    print()
    print("outputs/exp26_aperture_graph_overlay.png")
    print("outputs/exp26_transition_adjacency_matrix.png")
    print("outputs/exp26_gate_transition_network.png")
    print("outputs/exp26_transport_flow_map.png")
    print("outputs/exp26_aperture_graph_summary.txt")
    print()
    print("EXP-26 complete.")
    print()


if __name__ == "__main__":
    run_experiment()
