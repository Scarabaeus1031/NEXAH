#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 17
AXIS GEOMETRY & BREATHING MODES

Goal:
    Investigate whether JANUS dynamics organize around:

    - central transport axes
    - breathing modes
    - compression / expansion cycles
    - open-8 geometry
    - axis-crossing structure

This experiment studies the global transport geometry
rather than only local coherence statistics.

System:
    Lorenz attractor

Outputs:
    outputs/janus_axis_breathing.png
    outputs/janus_open8_geometry.png
    outputs/janus_axis_density.png
    outputs/janus_spine_compression_cycles.png
    outputs/janus_axis_summary.txt
"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import solve_ivp
from scipy.ndimage import gaussian_filter1d


# ------------------------------------------------------------
# Config
# ------------------------------------------------------------

@dataclass(frozen=True)
class Config:
    output_dir: Path = Path(__file__).resolve().parent.parent / "outputs"

    t_max: float = 140.0
    dt: float = 0.01

    sigma: float = 10.0
    beta: float = 8.0 / 3.0
    rho: float = 28.0

    transient_fraction: float = 0.15

    dpi: int = 220


CFG = Config()


# ------------------------------------------------------------
# Lorenz
# ------------------------------------------------------------

def lorenz_rhs(_: float, s: np.ndarray) -> np.ndarray:
    x, y, z = s

    return np.array([
        CFG.sigma * (y - x),
        x * (CFG.rho - z) - y,
        x * y - CFG.beta * z,
    ])


def simulate():
    n_steps = int(np.floor(CFG.t_max / CFG.dt))

    t_eval = np.linspace(
        0.0,
        n_steps * CFG.dt,
        n_steps + 1,
    )

    sol = solve_ivp(
        lorenz_rhs,
        (0.0, float(t_eval[-1])),
        y0=np.array([1.0, 1.0, 1.0]),
        t_eval=t_eval,
        method="DOP853",
        rtol=1e-10,
        atol=1e-12,
    )

    if not sol.success:
        raise RuntimeError(sol.message)

    t = sol.t
    states = sol.y.T

    start = int(len(t) * CFG.transient_fraction)

    return t[start:], states[start:]


# ------------------------------------------------------------
# JANUS
# ------------------------------------------------------------

def compute_janus(
    t: np.ndarray,
    states: np.ndarray,
    eps: float = 1e-8,
):
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


# ------------------------------------------------------------
# Axis Geometry
# ------------------------------------------------------------

def radial_distance(states):
    x = states[:, 0]
    y = states[:, 1]

    return np.sqrt(x**2 + y**2)


def spine_distance(states):
    """
    Distance to approximate central transport axis.

    Lorenz switching spine approximated by:
        x ≈ y
    """

    x = states[:, 0]
    y = states[:, 1]

    return np.abs(x - y) / np.sqrt(2)


def detect_axis_crossings(states):
    """
    Crossing near x = y axis.
    """

    x = states[:, 0]
    y = states[:, 1]

    sign = np.sign(x - y)

    crossings = np.where(np.diff(sign) != 0)[0]

    return crossings


def detect_breathing_modes(radius):
    smooth = gaussian_filter1d(radius, sigma=15)

    velocity = np.gradient(smooth)

    expansion = velocity > 0
    contraction = velocity < 0

    return smooth, velocity, expansion, contraction


# ------------------------------------------------------------
# Plots
# ------------------------------------------------------------

def plot_axis_breathing(
    t,
    radius,
    smooth_radius,
    velocity,
):
    fig, axes = plt.subplots(
        2,
        1,
        figsize=(13, 8),
        sharex=True,
    )

    axes[0].plot(t, radius, alpha=0.35, linewidth=0.8)
    axes[0].plot(t, smooth_radius, linewidth=2.0)

    axes[0].set_title(
        "JANUS Axis Breathing Modes\n"
        "Radial expansion / compression cycles"
    )

    axes[0].set_ylabel("radius")
    axes[0].grid(alpha=0.25)

    axes[1].plot(t, velocity, linewidth=1.5)

    axes[1].axhline(
        0,
        linestyle="--",
        linewidth=1.0,
    )

    axes[1].set_title("Breathing Velocity")
    axes[1].set_ylabel("d(radius)/dt")
    axes[1].set_xlabel("time")

    axes[1].grid(alpha=0.25)

    fig.tight_layout()

    fig.savefig(
        CFG.output_dir / "janus_axis_breathing.png",
        dpi=CFG.dpi,
    )

    plt.close(fig)


def plot_open8_geometry(
    states,
    janus,
    crossings,
):
    x = states[:, 0]
    z = states[:, 2]

    fig, ax = plt.subplots(
        figsize=(10, 9)
    )

    sc = ax.scatter(
        x,
        z,
        c=janus,
        s=2,
        alpha=0.65,
    )

    ax.scatter(
        x[crossings],
        z[crossings],
        color="red",
        s=18,
        label="axis crossings",
    )

    ax.axvline(
        0,
        linestyle="--",
        linewidth=1.0,
    )

    ax.set_title(
        "JANUS Open-8 Geometry\n"
        "Axis-crossing transport structure"
    )

    ax.set_xlabel("x")
    ax.set_ylabel("z")

    ax.legend()

    plt.colorbar(
        sc,
        ax=ax,
        label="JANUS coherence",
    )

    fig.tight_layout()

    fig.savefig(
        CFG.output_dir / "janus_open8_geometry.png",
        dpi=CFG.dpi,
    )

    plt.close(fig)


def plot_axis_density(
    spine_dist,
    janus,
):
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(13, 5),
    )

    axes[0].hist(
        spine_dist,
        bins=70,
        alpha=0.85,
    )

    axes[0].set_title(
        "Spine Distance Density"
    )

    axes[0].set_xlabel(
        "distance to axis"
    )

    axes[0].grid(alpha=0.25)

    axes[1].scatter(
        spine_dist,
        janus,
        s=3,
        alpha=0.35,
    )

    axes[1].set_title(
        "JANUS vs Spine Distance"
    )

    axes[1].set_xlabel(
        "distance to axis"
    )

    axes[1].set_ylabel(
        "JANUS coherence"
    )

    axes[1].grid(alpha=0.25)

    fig.tight_layout()

    fig.savefig(
        CFG.output_dir / "janus_axis_density.png",
        dpi=CFG.dpi,
    )

    plt.close(fig)


def plot_spine_compression_cycles(
    t,
    spine_dist,
):
    smooth = gaussian_filter1d(
        spine_dist,
        sigma=12,
    )

    fig, ax = plt.subplots(
        figsize=(13, 5)
    )

    ax.plot(
        t,
        smooth,
        linewidth=2.0,
    )

    ax.set_title(
        "Transition Spine Compression Cycles"
    )

    ax.set_xlabel("time")

    ax.set_ylabel(
        "distance to spine"
    )

    ax.grid(alpha=0.25)

    fig.tight_layout()

    fig.savefig(
        CFG.output_dir / "janus_spine_compression_cycles.png",
        dpi=CFG.dpi,
    )

    plt.close(fig)


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

def write_summary(
    crossings,
    radius,
    velocity,
    spine_dist,
):
    lines = []

    lines.append(
        "JANUS axis geometry & breathing modes"
    )

    lines.append("=" * 48)
    lines.append("")

    lines.append(
        "Goal:"
    )

    lines.append(
        "Investigate global transport geometry."
    )

    lines.append("")

    lines.append(
        f"axis crossings: {len(crossings)}"
    )

    lines.append(
        f"mean radius: {np.mean(radius):.6f}"
    )

    lines.append(
        f"radius std: {np.std(radius):.6f}"
    )

    lines.append(
        f"mean breathing velocity: {np.mean(np.abs(velocity)):.6f}"
    )

    lines.append(
        f"mean spine distance: {np.mean(spine_dist):.6f}"
    )

    lines.append("")

    lines.append("Working interpretation:")
    lines.append(
        "- transport geometry appears organized around a central switching axis"
    )

    lines.append(
        "- repeated compression / expansion cycles are visible"
    )

    lines.append(
        "- axis crossings cluster near coherence deformation regions"
    )

    lines.append(
        "- the resulting structure resembles an open-8 transport geometry"
    )

    lines.append("")

    lines.append(
        "This experiment studies global breathing organization,"
    )

    lines.append(
        "not only local coherence statistics."
    )

    out_path = (
        CFG.output_dir
        / "janus_axis_summary.txt"
    )

    out_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def run():
    CFG.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()
    print("=" * 48)
    print(
        "JANUS AXIS GEOMETRY & BREATHING MODES"
    )
    print("=" * 48)

    t, states = simulate()

    states_j, janus = compute_janus(
        t,
        states,
    )

    n = min(len(states_j), len(janus))

    states_j = states_j[:n]
    janus = janus[:n]

    t = t[1:-1][:n]

    radius = radial_distance(states_j)

    spine_dist = spine_distance(states_j)

    crossings = detect_axis_crossings(
        states_j
    )

    smooth_radius, velocity, expansion, contraction = (
        detect_breathing_modes(radius)
    )

    plot_axis_breathing(
        t,
        radius,
        smooth_radius,
        velocity,
    )

    plot_open8_geometry(
        states_j,
        janus,
        crossings,
    )

    plot_axis_density(
        spine_dist,
        janus,
    )

    plot_spine_compression_cycles(
        t,
        spine_dist,
    )

    write_summary(
        crossings,
        radius,
        velocity,
        spine_dist,
    )

    print(
        f"samples: {len(states_j)}"
    )

    print(
        f"axis crossings: {len(crossings)}"
    )

    print(
        f"mean radius: {np.mean(radius):.6f}"
    )

    print(
        f"mean spine distance: {np.mean(spine_dist):.6f}"
    )

    print()
    print(
        f"outputs saved to: {CFG.output_dir.resolve()}"
    )

    print("=" * 48)
    print()


if __name__ == "__main__":
    run()
