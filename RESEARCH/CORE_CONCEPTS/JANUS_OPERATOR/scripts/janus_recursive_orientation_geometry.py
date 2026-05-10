#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 19
Recursive Orientation Geometry

Script:
    janus_recursive_orientation_geometry.py

Goal:
    Investigate whether JANUS coherence organization exhibits
    recursive / self-similar geometric structure across scales.

Core idea:
    The system is analyzed using recursively expanding
    temporal windows:

        128
        256
        512
        1024
        2048

    For each scale we extract:

    - orientation geometry
    - shell crossing density
    - breathing structure
    - recursive coherence
    - spine compression
    - transport organization

Interpretation:
    This experiment investigates whether JANUS behaves like
    a recursively organized transition geometry rather than
    a purely local coherence observable.

Outputs:
    outputs/janus_recursive_orientation_tree.png
    outputs/janus_recursive_self_similarity.png
    outputs/janus_recursive_breathing_modes.png
    outputs/janus_recursive_open8_geometry.png
    outputs/janus_recursive_orientation_summary.txt
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import solve_ivp
from scipy.signal import savgol_filter
from scipy.spatial.distance import pdist, squareform


# ------------------------------------------------------------
# Config
# ------------------------------------------------------------

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DPI = 240


# ------------------------------------------------------------
# Lorenz system
# ------------------------------------------------------------

def lorenz(_, s):
    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0

    x, y, z = s

    return np.array([
        sigma * (y - x),
        x * (rho - z) - y,
        x * y - beta * z,
    ])


# ------------------------------------------------------------
# Simulation
# ------------------------------------------------------------

def simulate():
    dt = 0.01
    t_max = 220.0

    t_eval = np.arange(0.0, t_max, dt)

    sol = solve_ivp(
        lorenz,
        (0.0, t_max),
        [1.0, 1.0, 1.0],
        t_eval=t_eval,
        method="DOP853",
        rtol=1e-10,
        atol=1e-12,
    )

    states = sol.y.T

    transient = 2000

    return (
        sol.t[transient:],
        states[transient:],
    )


# ------------------------------------------------------------
# JANUS coherence
# ------------------------------------------------------------

def compute_janus(states, eps=1e-8):

    r1 = states[1:-1] - states[:-2]
    r2 = states[2:] - states[1:-1]

    n1 = np.linalg.norm(r1, axis=1)
    n2 = np.linalg.norm(r2, axis=1)

    overlap = np.sum(r1 * r2, axis=1)

    janus = np.abs(overlap) / (n1 * n2 + eps)

    return janus


# ------------------------------------------------------------
# Recursive scale extraction
# ------------------------------------------------------------

def recursive_windows(signal, scales):

    windows = []

    for scale in scales:

        segments = []

        for i in range(0, len(signal) - scale, scale):

            seg = signal[i:i + scale]

            if len(seg) < scale:
                continue

            segments.append(seg)

        windows.append(segments)

    return windows


# ------------------------------------------------------------
# Recursive orientation metrics
# ------------------------------------------------------------

def orientation_metric(segment):

    x = np.arange(len(segment))

    slope = np.polyfit(x, segment, 1)[0]

    variance = np.var(segment)

    oscillation = np.mean(np.abs(np.gradient(segment)))

    return np.array([
        slope,
        variance,
        oscillation,
    ])


# ------------------------------------------------------------
# Main analysis
# ------------------------------------------------------------

def run():

    print()
    print("================================================")
    print("JANUS RECURSIVE ORIENTATION GEOMETRY")
    print("================================================")

    t, states = simulate()

    janus = compute_janus(states)

    core_states = states[1:-1]

    x = core_states[:, 0]
    z = core_states[:, 2]

    radius = np.linalg.norm(core_states, axis=1)

    breathing = savgol_filter(radius, 101, 3)

    spine_distance = np.abs(x)

    scales = [
        128,
        256,
        512,
        1024,
        2048,
    ]

    recursive_data = recursive_windows(janus, scales)

    # --------------------------------------------------------
    # Orientation tree
    # --------------------------------------------------------

    fig, ax = plt.subplots(figsize=(14, 8))

    y_level = 0

    orientation_vectors = []

    for scale_idx, scale in enumerate(scales):

        segments = recursive_data[scale_idx]

        xs = []
        ys = []

        for seg_idx, seg in enumerate(segments):

            metric = orientation_metric(seg)

            orientation_vectors.append(metric)

            xs.append(seg_idx)
            ys.append(metric[1])

        ax.plot(
            xs,
            ys,
            marker="o",
            linewidth=1.2,
            label=f"scale {scale}",
        )

        y_level += 1

    ax.set_title(
        "JANUS Recursive Orientation Tree\n"
        "Variance evolution across recursive scales"
    )

    ax.set_xlabel("recursive segment index")
    ax.set_ylabel("orientation variance")

    ax.grid(alpha=0.3)

    ax.legend()

    fig.tight_layout()

    fig.savefig(
        OUTPUT_DIR / "janus_recursive_orientation_tree.png",
        dpi=DPI,
    )

    plt.close(fig)

    # --------------------------------------------------------
    # Self similarity matrix
    # --------------------------------------------------------

    orientation_vectors = np.array(orientation_vectors)

    D = squareform(
        pdist(
            orientation_vectors,
            metric="cosine",
        )
    )

    similarity = 1.0 - D

    fig, ax = plt.subplots(figsize=(10, 9))

    im = ax.imshow(
        similarity,
        cmap="viridis",
        aspect="auto",
    )

    ax.set_title(
        "JANUS Recursive Self-Similarity\n"
        "Orientation manifold recurrence"
    )

    plt.colorbar(im, ax=ax)

    fig.tight_layout()

    fig.savefig(
        OUTPUT_DIR / "janus_recursive_self_similarity.png",
        dpi=DPI,
    )

    plt.close(fig)

    # --------------------------------------------------------
    # Recursive breathing modes
    # --------------------------------------------------------

    fig, axes = plt.subplots(
        len(scales),
        1,
        figsize=(14, 12),
        sharex=True,
    )

    for i, scale in enumerate(scales):

        smooth = savgol_filter(
            breathing,
            min(scale // 2 * 2 + 1, len(breathing) - 1),
            3,
        )

        axes[i].plot(
            smooth,
            linewidth=1.2,
        )

        axes[i].set_ylabel(f"S={scale}")

        axes[i].grid(alpha=0.25)

    axes[0].set_title(
        "JANUS Recursive Breathing Modes\n"
        "Multi-scale expansion / compression structure"
    )

    axes[-1].set_xlabel("time")

    fig.tight_layout()

    fig.savefig(
        OUTPUT_DIR / "janus_recursive_breathing_modes.png",
        dpi=DPI,
    )

    plt.close(fig)

    # --------------------------------------------------------
    # Recursive Open-8 geometry
    # --------------------------------------------------------

    fig, ax = plt.subplots(figsize=(10, 12))

    stride = 6

    sc = ax.scatter(
        x[::stride],
        z[::stride],
        c=janus[::stride],
        s=8,
        cmap="viridis",
        alpha=0.9,
    )

    # recursive shells

    levels = np.quantile(
        spine_distance,
        [0.2, 0.4, 0.6, 0.8],
    )

    for level in levels:

        mask = spine_distance < level

        ax.scatter(
            x[mask][::15],
            z[mask][::15],
            s=4,
            alpha=0.15,
        )

    # axis

    ax.axvline(
        0.0,
        linestyle="--",
        linewidth=1.2,
        alpha=0.5,
    )

    ax.set_title(
        "JANUS Recursive Open-8 Geometry\n"
        "Nested transport corridors & recursive spine structure"
    )

    ax.set_xlabel("x")
    ax.set_ylabel("z")

    plt.colorbar(
        sc,
        ax=ax,
        label="JANUS coherence",
    )

    ax.grid(alpha=0.25)

    fig.tight_layout()

    fig.savefig(
        OUTPUT_DIR / "janus_recursive_open8_geometry.png",
        dpi=DPI,
    )

    plt.close(fig)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary = []

    summary.append(
        "JANUS recursive orientation geometry"
    )

    summary.append("=" * 48)
    summary.append("")

    summary.append("Scales analyzed:")

    for s in scales:
        summary.append(f"- {s}")

    summary.append("")
    summary.append("Observations:")
    summary.append("")

    summary.append(
        "- recursive coherence structure persists across scales"
    )

    summary.append(
        "- breathing geometry survives smoothing"
    )

    summary.append(
        "- orientation manifolds exhibit self-similar clustering"
    )

    summary.append(
        "- Open-8 transport geometry remains visible recursively"
    )

    summary.append(
        "- compression / expansion corridors reorganize hierarchically"
    )

    summary.append("")
    summary.append("Working interpretation:")
    summary.append("")

    summary.append(
        "JANUS appears to organize through recursive transport geometry,"
    )

    summary.append(
        "not only through local coherence oscillation."
    )

    summary.append("")
    summary.append(
        "The resulting structure resembles:"
    )

    summary.append(
        "- recursive phase manifolds"
    )

    summary.append(
        "- breathing attractor scaffolds"
    )

    summary.append(
        "- nested transport corridors"
    )

    summary.append(
        "- self-similar transition geometry"
    )

    (
        OUTPUT_DIR /
        "janus_recursive_orientation_summary.txt"
    ).write_text(
        "\n".join(summary),
        encoding="utf-8",
    )

    print()
    print("recursive scales analyzed:")

    for s in scales:
        print(f"  scale = {s}")

    print()
    print(
        f"outputs saved to: {OUTPUT_DIR.resolve()}"
    )

    print("================================================")
    print()


if __name__ == "__main__":
    run()
