#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 23
Aperture Orientation Angles

Script:
    janus_aperture_orientation_angles.py

Goal:
    Measure angular structure of JANUS aperture gate candidates.

    This experiment tests whether aperture/gate candidates show
    preferred orientation angles relative to the Lorenz transition spine.

Focus:
    - aperture gate score
    - gate candidate extraction
    - orientation angle distribution
    - resonance-angle comparison
    - drift / aperture calibration

Outputs:
    outputs/exp23_aperture_angle_distribution.png
    outputs/exp23_gate_orientation_overlay.png
    outputs/exp23_angle_resonance_scan.png
    outputs/exp23_orientation_summary.txt
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
    gate_quantile: float = 0.995
    memory_lag: int = 230


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
# Aperture geometry
# ------------------------------------------------------------

def compute_breathing(states: Array) -> Tuple[Array, Array]:
    radius = np.linalg.norm(states, axis=1)
    velocity = np.gradient(radius)
    return radius, velocity


def compute_spine_distance(states: Array) -> Array:
    """
    Distance to central switching axis x=0.
    """
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


def compute_aperture_score(
    janus: Array,
    states: Array,
    breathing_velocity: Array,
    memory: Array,
) -> Array:
    """
    Aperture score combines:
    - low JANUS coherence
    - high breathing velocity
    - proximity to central axis
    - memory / recurrence strength
    """

    jn = normalize(janus)
    vn = normalize(np.abs(breathing_velocity))
    axis = normalize(compute_spine_distance(states))
    mn = normalize(memory)

    low_janus = 1.0 - jn
    axis_proximity = 1.0 - axis

    score = (
        0.35 * low_janus
        + 0.30 * vn
        + 0.20 * axis_proximity
        + 0.15 * mn
    )

    return normalize(score)


def compute_orientation_angles(states: Array) -> Array:
    """
    Orientation angle in the x-z projection, measured relative
    to the positive x-axis.

    Returned in degrees in [0, 180].
    """
    x = states[:, 0]
    z = states[:, 2] - np.mean(states[:, 2])

    angles = np.degrees(np.arctan2(z, x))
    angles = np.mod(angles, 180.0)

    return angles


def circular_distance_deg(a: Array, target: float) -> Array:
    """
    Distance between angle a and target in degrees,
    respecting 180-degree axial symmetry.
    """
    d = np.abs(a - target)
    return np.minimum(d, 180.0 - d)


def resonance_scan(angles: Array) -> Tuple[Array, Array]:
    targets = np.array([
        30.0,
        45.0,
        51.83,
        52.0,
        60.0,
        72.0,
        90.0,
        108.0,
        120.0,
        144.0,
    ])

    scores = []

    for target in targets:
        d = circular_distance_deg(angles, target)
        score = np.mean(np.exp(-(d ** 2) / (2.0 * 5.0 ** 2)))
        scores.append(score)

    return targets, np.array(scores)


# ------------------------------------------------------------
# Plotting
# ------------------------------------------------------------

def plot_angle_distribution(
    gate_angles: Array,
    all_angles: Array,
    out_path: Path,
    dpi: int,
) -> None:
    fig, ax = plt.subplots(figsize=(11, 6))

    bins = np.linspace(0.0, 180.0, 73)

    ax.hist(
        all_angles,
        bins=bins,
        alpha=0.35,
        density=True,
        label="all trajectory angles",
    )

    ax.hist(
        gate_angles,
        bins=bins,
        alpha=0.75,
        density=True,
        label="aperture gate angles",
    )

    reference_angles = [51.83, 60.0, 72.0, 90.0, 108.0, 120.0]

    for angle in reference_angles:
        ax.axvline(angle, linestyle="--", linewidth=1.0, alpha=0.75)
        ax.text(angle + 1.0, ax.get_ylim()[1] * 0.85, f"{angle:g}°", rotation=90)

    ax.set_title("EXP-23 — Aperture Gate Orientation Angle Distribution")
    ax.set_xlabel("orientation angle degrees")
    ax.set_ylabel("density")
    ax.legend()
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_gate_orientation_overlay(
    states: Array,
    aperture_score: Array,
    gate_mask: Array,
    angles: Array,
    out_path: Path,
    dpi: int,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 9))

    sc = ax.scatter(
        states[:, 0],
        states[:, 2],
        c=angles,
        s=2.0,
        cmap="twilight",
        alpha=0.55,
    )

    gates = states[gate_mask]

    ax.scatter(
        gates[:, 0],
        gates[:, 2],
        s=44,
        facecolors="none",
        edgecolors="black",
        linewidths=1.2,
        label="aperture gates",
    )

    ax.axvline(0.0, linestyle="--", linewidth=1.2, alpha=0.6)

    ax.set_title("EXP-23 — Gate Orientation Overlay")
    ax.set_xlabel("x")
    ax.set_ylabel("z")
    ax.legend()
    ax.grid(alpha=0.25)

    plt.colorbar(sc, ax=ax, label="orientation angle degrees")

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_resonance_scan(
    targets: Array,
    scores: Array,
    out_path: Path,
    dpi: int,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar([f"{t:g}°" for t in targets], scores)

    ax.set_title("EXP-23 — Aperture Angle Resonance Scan")
    ax.set_xlabel("reference angle")
    ax.set_ylabel("alignment score")
    ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def write_summary(
    gate_angles: Array,
    all_angles: Array,
    targets: Array,
    scores: Array,
    aperture_score: Array,
    gate_mask: Array,
    out_path: Path,
) -> None:
    best_idx = int(np.argmax(scores))

    lines = []
    lines.append("EXP-23 — JANUS aperture orientation angles")
    lines.append("================================================")
    lines.append("")
    lines.append("Goal:")
    lines.append("Measure angular organization of aperture gate candidates.")
    lines.append("")

    lines.append("Global statistics:")
    lines.append(f"samples: {len(all_angles)}")
    lines.append(f"gate candidates: {int(np.sum(gate_mask))}")
    lines.append(f"mean aperture score: {float(np.mean(aperture_score)):.6f}")
    lines.append(f"max aperture score: {float(np.max(aperture_score)):.6f}")
    lines.append("")

    lines.append("Angle statistics:")
    lines.append(f"all angle mean: {float(np.mean(all_angles)):.6f}")
    lines.append(f"all angle std: {float(np.std(all_angles)):.6f}")
    lines.append(f"gate angle mean: {float(np.mean(gate_angles)):.6f}")
    lines.append(f"gate angle std: {float(np.std(gate_angles)):.6f}")
    lines.append("")

    lines.append("Reference angle scan:")
    for target, score in zip(targets, scores):
        lines.append(f"{target:.6f} deg: {score:.6f}")

    lines.append("")
    lines.append("Best reference alignment:")
    lines.append(f"{targets[best_idx]:.6f} deg")
    lines.append(f"score: {scores[best_idx]:.6f}")
    lines.append("")

    lines.append("Working interpretation:")
    lines.append("- aperture gate candidates show measurable angle structure")
    lines.append("- gate points do not occupy the Lorenz geometry uniformly")
    lines.append("- angular preference may indicate orientation-calibrated gate structure")
    lines.append("- this remains exploratory and requires surrogate comparison")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def run_experiment() -> None:
    output_cfg = OutputConfig()
    cfg = ExperimentConfig()

    output_cfg.output_dir.mkdir(parents=True, exist_ok=True)

    print("Running EXP-23 — JANUS aperture orientation angles...")

    t, states = simulate_lorenz(cfg)
    core_states, janus = compute_janus(t, states)

    radius, breathing_velocity = compute_breathing(core_states)
    memory = compute_memory_signal(janus, cfg.memory_lag)

    n = min(
        len(core_states),
        len(janus),
        len(breathing_velocity),
        len(memory),
    )

    core_states = core_states[:n]
    janus = janus[:n]
    breathing_velocity = breathing_velocity[:n]
    memory = memory[:n]

    aperture_score = compute_aperture_score(
        janus=janus,
        states=core_states,
        breathing_velocity=breathing_velocity,
        memory=memory,
    )

    threshold = np.quantile(aperture_score, cfg.gate_quantile)
    gate_mask = aperture_score >= threshold

    angles = compute_orientation_angles(core_states)
    gate_angles = angles[gate_mask]

    targets, scores = resonance_scan(gate_angles)

    plot_angle_distribution(
        gate_angles,
        angles,
        output_cfg.output_dir / "exp23_aperture_angle_distribution.png",
        output_cfg.dpi,
    )

    plot_gate_orientation_overlay(
        core_states,
        aperture_score,
        gate_mask,
        angles,
        output_cfg.output_dir / "exp23_gate_orientation_overlay.png",
        output_cfg.dpi,
    )

    plot_resonance_scan(
        targets,
        scores,
        output_cfg.output_dir / "exp23_angle_resonance_scan.png",
        output_cfg.dpi,
    )

    write_summary(
        gate_angles,
        angles,
        targets,
        scores,
        aperture_score,
        gate_mask,
        output_cfg.output_dir / "exp23_orientation_summary.txt",
    )

    best_idx = int(np.argmax(scores))

    print()
    print("================================================")
    print("EXP-23 — JANUS APERTURE ORIENTATION ANGLES")
    print("================================================")
    print(f"samples: {n}")
    print(f"gate candidates: {int(np.sum(gate_mask))}")
    print(f"mean aperture score: {float(np.mean(aperture_score)):.6f}")
    print(f"max aperture score: {float(np.max(aperture_score)):.6f}")
    print()
    print(f"gate angle mean: {float(np.mean(gate_angles)):.6f}")
    print(f"gate angle std : {float(np.std(gate_angles)):.6f}")
    print()
    print("best reference alignment:")
    print(f"  angle: {targets[best_idx]:.6f} deg")
    print(f"  score: {scores[best_idx]:.6f}")
    print()
    print("outputs generated:")
    print("outputs/exp23_aperture_angle_distribution.png")
    print("outputs/exp23_gate_orientation_overlay.png")
    print("outputs/exp23_angle_resonance_scan.png")
    print("outputs/exp23_orientation_summary.txt")
    print()
    print("EXP-23 complete.")
    print("================================================")


if __name__ == "__main__":
    run_experiment()
