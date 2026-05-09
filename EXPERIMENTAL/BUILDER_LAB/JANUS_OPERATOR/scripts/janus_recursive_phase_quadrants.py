#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 20
Recursive Phase Quadrants

Script:
    janus_recursive_phase_quadrants.py

Goal:
    Decompose JANUS transport into four recursive phase quadrants:

        Q1 — Expansion
        Q2 — Compression
        Q3 — Memory / Echo
        Q4 — Transition / Gate

    The experiment combines:

    - JANUS coherence
    - radial breathing velocity
    - distance to central axis
    - delayed memory correlation
    - shell crossing density
    - transition quadrant occupation

Outputs:
    outputs/janus_recursive_phase_quadrants.png
    outputs/janus_phase_quadrant_map.png
    outputs/janus_phase_quadrant_timeseries.png
    outputs/janus_phase_quadrant_density.png
    outputs/janus_phase_quadrant_summary.txt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


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
    n_shells: int = 5


# ------------------------------------------------------------
# Lorenz system
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
    t_eval = np.linspace(0.0, n_steps * cfg.dt, n_steps + 1)

    sol = solve_ivp(
        fun=lorenz_rhs,
        t_span=(0.0, float(t_eval[-1])),
        y0=np.array([1.0, 1.0, 1.0], dtype=float),
        t_eval=t_eval,
        method="DOP853",
        rtol=1.0e-10,
        atol=1.0e-12,
    )

    if not sol.success:
        raise RuntimeError(sol.message)

    t = sol.t
    states = sol.y.T

    start = int(len(t) * cfg.transient_fraction)

    return t[start:], states[start:]


# ------------------------------------------------------------
# JANUS computation
# ------------------------------------------------------------

def compute_janus(t: Array, states: Array, eps: float = 1.0e-8) -> Tuple[Array, Array]:
    dt_f = (t[2:] - t[1:-1])[:, None]
    dt_b = (t[1:-1] - t[:-2])[:, None]

    forward = (states[2:] - states[1:-1]) / dt_f
    backward = (states[1:-1] - states[:-2]) / dt_b

    overlap = forward * backward

    numerator = np.linalg.norm(overlap, axis=1)
    denominator = (
        np.linalg.norm(forward, axis=1)
        * np.linalg.norm(backward, axis=1)
        + eps
    )

    janus = numerator / denominator

    return states[1:-1], janus


def normalize(v: Array, eps: float = 1.0e-12) -> Array:
    v_min = np.nanmin(v)
    v_max = np.nanmax(v)

    if not np.isfinite(v_min) or not np.isfinite(v_max):
        return np.zeros_like(v)

    scale = v_max - v_min

    if scale < eps:
        return np.zeros_like(v)

    return (v - v_min) / scale


# ------------------------------------------------------------
# Phase features
# ------------------------------------------------------------

def compute_breathing(states: Array) -> Tuple[Array, Array]:
    radius = np.linalg.norm(states, axis=1)
    velocity = np.gradient(radius)

    return radius, velocity


def compute_axis_distance(states: Array) -> Array:
    return np.abs(states[:, 0])


def compute_memory_signal(janus: Array, lag: int) -> Array:
    memory = np.zeros_like(janus)

    if lag <= 0 or lag >= len(janus):
        return memory

    a = janus[:-lag]
    b = janus[lag:]

    local_memory = 1.0 - np.abs(b - a)
    local_memory = normalize(local_memory)

    memory[lag:] = local_memory

    return memory


def compute_shell_ids(janus: Array, n_shells: int) -> Array:
    edges = np.quantile(janus, np.linspace(0.0, 1.0, n_shells + 1))
    shell_ids = np.digitize(janus, edges[1:-1])

    return shell_ids


def compute_shell_crossings(shell_ids: Array) -> Array:
    crossings = np.zeros_like(shell_ids, dtype=float)
    crossings[1:] = (shell_ids[1:] != shell_ids[:-1]).astype(float)

    return crossings


# ------------------------------------------------------------
# Quadrant classification
# ------------------------------------------------------------

def classify_phase_quadrants(
    janus: Array,
    breathing_velocity: Array,
    axis_distance: Array,
    memory: Array,
    shell_crossings: Array,
) -> Array:
    """
    Quadrants:

    0 = Expansion
    1 = Compression
    2 = Memory / Echo
    3 = Transition / Gate
    """

    jn = normalize(janus)
    vn = normalize(np.abs(breathing_velocity))
    an = normalize(axis_distance)
    mn = normalize(memory)

    low_janus = jn < np.quantile(jn, 0.30)
    high_velocity = vn > np
        high_janus = jn > np.quantile(jn, 0.70)
    high_breathing = vn > np.quantile(vn, 0.70)
    low_axis = an < np.quantile(an, 0.35)
    high_memory = mn > np.quantile(mn, 0.70)
    crossing = shell_crossings > 0.0

    quadrants = np.zeros_like(janus, dtype=int)

    # Q1 — Expansion
    quadrants[(breathing_velocity > 0) & high_janus] = 0

    # Q2 — Compression
    quadrants[(breathing_velocity < 0) & high_breathing] = 1

    # Q3 — Memory / Echo
    quadrants[high_memory & ~crossing] = 2

    # Q4 — Transition / Gate
    quadrants[(low_janus | low_axis | crossing) & high_breathing] = 3

    return quadrants


# ------------------------------------------------------------
# Visualization
# ------------------------------------------------------------

def plot_recursive_phase_quadrants(
    states: Array,
    janus: Array,
    quadrants: Array,
    out_path: Path,
    dpi: int,
) -> None:
    labels = [
        "Q1 Expansion",
        "Q2 Compression",
        "Q3 Memory / Echo",
        "Q4 Transition / Gate",
    ]

    fig, ax = plt.subplots(figsize=(10, 9))

    sc = ax.scatter(
        states[:, 0],
        states[:, 2],
        c=quadrants,
        s=2.0,
        cmap="tab10",
        alpha=0.75,
    )

    ax.axvline(0.0, linestyle="--", linewidth=1.2, alpha=0.6)

    ax.set_title(
        "JANUS Recursive Phase Quadrants\n"
        "Expansion / Compression / Echo / Gate"
    )
    ax.set_xlabel("x")
    ax.set_ylabel("z")
    ax.grid(alpha=0.25)

    cbar = plt.colorbar(sc, ax=ax, ticks=[0, 1, 2, 3])
    cbar.ax.set_yticklabels(labels)

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_phase_quadrant_map(
    janus: Array,
    breathing_velocity: Array,
    quadrants: Array,
    out_path: Path,
    dpi: int,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 8))

    sc = ax.scatter(
        janus,
        breathing_velocity,
        c=quadrants,
        s=3,
        cmap="tab10",
        alpha=0.7,
    )

    ax.axhline(0.0, linestyle="--", linewidth=1.0, alpha=0.6)

    ax.set_title("JANUS Phase Quadrant Map")
    ax.set_xlabel("JANUS coherence")
    ax.set_ylabel("breathing velocity")
    ax.grid(alpha=0.25)

    cbar = plt.colorbar(sc, ax=ax, ticks=[0, 1, 2, 3])
    cbar.ax.set_yticklabels([
        "Expansion",
        "Compression",
        "Memory / Echo",
        "Transition / Gate",
    ])

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_phase_quadrant_timeseries(
    t: Array,
    janus: Array,
    quadrants: Array,
    out_path: Path,
    dpi: int,
) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(15, 7), sharex=True)

    axes[0].plot(t, janus, linewidth=1.0)
    axes[0].set_ylabel("JANUS coherence")
    axes[0].set_title("JANUS Recursive Phase Quadrant Timeseries")
    axes[0].grid(alpha=0.25)

    axes[1].plot(t, quadrants, linewidth=1.0)
    axes[1].set_yticks([0, 1, 2, 3])
    axes[1].set_yticklabels([
        "Expansion",
        "Compression",
        "Memory",
        "Gate",
    ])
    axes[1].set_xlabel("time")
    axes[1].set_ylabel("phase quadrant")
    axes[1].grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_phase_quadrant_density(
    quadrants: Array,
    shell_ids: Array,
    out_path: Path,
    dpi: int,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 6))

    matrix = np.zeros((4, int(np.max(shell_ids)) + 1))

    for q, s in zip(quadrants, shell_ids):
        matrix[int(q), int(s)] += 1

    matrix = matrix / np.maximum(matrix.sum(axis=1, keepdims=True), 1)

    im = ax.imshow(matrix, aspect="auto", cmap="viridis")

    ax.set_title("JANUS Phase Quadrant / Shell Occupation Density")
    ax.set_xlabel("JANUS shell id")
    ax.set_ylabel("phase quadrant")
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels([
        "Expansion",
        "Compression",
        "Memory / Echo",
        "Transition / Gate",
    ])

    plt.colorbar(im, ax=ax, label="normalized occupation")

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def write_summary(
    quadrants: Array,
    shell_crossings: Array,
    memory: Array,
    breathing_velocity: Array,
    out_path: Path,
) -> None:
    names = [
        "Expansion",
        "Compression",
        "Memory / Echo",
        "Transition / Gate",
    ]

    lines = []
    lines.append("JANUS recursive phase quadrants")
    lines.append("================================================")
    lines.append("")
    lines.append("Goal:")
    lines.append("Decompose JANUS transport into four recursive phase regimes.")
    lines.append("")

    total = len(quadrants)

    for idx, name in enumerate(names):
        count = int(np.sum(quadrants == idx))
        frac = count / max(total, 1)

        lines.append(f"Q{idx + 1} — {name}")
        lines.append("-" * (6 + len(name)))
        lines.append(f"count: {count}")
        lines.append(f"fraction: {frac:.6f}")
        lines.append("")

    lines.append("Global statistics:")
    lines.append(f"samples: {total}")
    lines.append(f"shell crossings: {int(np.sum(shell_crossings))}")
    lines.append(f"mean memory signal: {float(np.mean(memory)):.6f}")
    lines.append(f"mean abs breathing velocity: {float(np.mean(np.abs(breathing_velocity))):.6f}")
    lines.append("")

    lines.append("Working interpretation:")
    lines.append("- expansion and compression form breathing transport phases")
    lines.append("- memory / echo captures delayed recurrence structure")
    lines.append("- transition / gate identifies low-coherence axis-linked crossings")
    lines.append("- the four regimes form a recursive phase decomposition of JANUS flow")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def run_experiment() -> None:
    output_cfg = OutputConfig()
    cfg = ExperimentConfig()

    output_cfg.output_dir.mkdir(parents=True, exist_ok=True)

    print("Running JANUS recursive phase quadrants...")

    t, states = simulate_lorenz(cfg)
    core_states, janus = compute_janus(t, states)

    radius, breathing_velocity = compute_breathing(core_states)
    axis_distance = compute_axis_distance(core_states)
    memory = compute_memory_signal(janus, cfg.memory_lag)

    shell_ids = compute_shell_ids(janus, cfg.n_shells)
    shell_crossings = compute_shell_crossings(shell_ids)

    n = min(
        len(core_states),
        len(janus),
        len(breathing_velocity),
        len(axis_distance),
        len(memory),
        len(shell_ids),
        len(shell_crossings),
    )

    core_states = core_states[:n]
    janus = janus[:n]
    breathing_velocity = breathing_velocity[:n]
    axis_distance = axis_distance[:n]
    memory = memory[:n]
    shell_ids = shell_ids[:n]
    shell_crossings = shell_crossings[:n]
    t_core = t[1:-1][:n]

    quadrants = classify_phase_quadrants(
        janus=janus,
        breathing_velocity=breathing_velocity,
        axis_distance=axis_distance,
        memory=memory,
        shell_crossings=shell_crossings,
    )

    plot_recursive_phase_quadrants(
        core_states,
        janus,
        quadrants,
        output_cfg.output_dir / "janus_recursive_phase_quadrants.png",
        output_cfg.dpi,
    )

    plot_phase_quadrant_map(
        janus,
        breathing_velocity,
        quadrants,
        output_cfg.output_dir / "janus_phase_quadrant_map.png",
        output_cfg.dpi,
    )

    plot_phase_quadrant_timeseries(
        t_core,
        janus,
        quadrants,
        output_cfg.output_dir / "janus_phase_quadrant_timeseries.png",
        output_cfg.dpi,
    )

    plot_phase_quadrant_density(
        quadrants,
        shell_ids,
        output_cfg.output_dir / "janus_phase_quadrant_density.png",
        output_cfg.dpi,
    )

    write_summary(
        quadrants,
        shell_crossings,
        memory,
        breathing_velocity,
        output_cfg.output_dir / "janus_phase_quadrant_summary.txt",
    )

    print()
    print("================================================")
    print("JANUS RECURSIVE PHASE QUADRANTS")
    print("================================================")
    print(f"samples: {n}")
    print(f"shell crossings: {int(np.sum(shell_crossings))}")
    print(f"mean memory signal: {float(np.mean(memory)):.6f}")
    print(f"mean abs breathing velocity: {float(np.mean(np.abs(breathing_velocity))):.6f}")

    for idx, name in enumerate([
        "Expansion",
        "Compression",
        "Memory / Echo",
        "Transition / Gate",
    ]):
        count = int(np.sum(quadrants == idx))
        frac = count / max(n, 1)
        print(f"Q{idx + 1} {name}: {count} ({frac:.6f})")

    print()
    print(f"outputs saved to: {output_cfg.output_dir.resolve()}")
    print("================================================")


if __name__ == "__main__":
    run_experiment()
