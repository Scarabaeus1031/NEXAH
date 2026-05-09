#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 16
Transition Orientation Atlas

Cross-system classification of transition geometry using:

    JANUS coherence
    curvature coupling
    low-JANUS / high-curvature overlap
    coherence variance
    transition-orientation angle

Goal:
    Test whether different dynamical systems occupy different
    regions in a JANUS-curvature orientation space.

Outputs:
    outputs/janus_transition_orientation_atlas.png
    outputs/janus_orientation_phase_space.png
    outputs/janus_orientation_vectors.png
    outputs/janus_orientation_summary.txt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Tuple

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.stats import pearsonr


Array = np.ndarray


# ------------------------------------------------------------
# Config
# ------------------------------------------------------------

@dataclass(frozen=True)
class OutputConfig:
    output_dir: Path = Path(__file__).resolve().parent.parent / "outputs"
    dpi: int = 220


@dataclass(frozen=True)
class SystemConfig:
    name: str
    rhs: Callable[[float, Array], Array]
    initial_state: Tuple[float, float, float]
    t_max: float
    dt: float
    transient_fraction: float


# ------------------------------------------------------------
# Dynamical systems
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


def rossler_rhs(_: float, s: Array) -> Array:
    a = 0.2
    b = 0.2
    c = 5.7
    x, y, z = s
    return np.array([
        -y - z,
        x + a * y,
        b + z * (x - c),
    ])


def halvorsen_rhs(_: float, s: Array) -> Array:
    a = 1.4
    x, y, z = s
    return np.array([
        -a * x - 4.0 * y - 4.0 * z - y * y,
        -a * y - 4.0 * z - 4.0 * x - z * z,
        -a * z - 4.0 * x - 4.0 * y - x * x,
    ])


SYSTEMS = [
    SystemConfig(
        name="Lorenz",
        rhs=lorenz_rhs,
        initial_state=(1.0, 1.0, 1.0),
        t_max=90.0,
        dt=0.01,
        transient_fraction=0.15,
    ),
    SystemConfig(
        name="Rossler",
        rhs=rossler_rhs,
        initial_state=(0.2, 0.1, 0.1),
        t_max=160.0,
        dt=0.015,
        transient_fraction=0.15,
    ),
    SystemConfig(
        name="Halvorsen",
        rhs=halvorsen_rhs,
        initial_state=(1.0, 0.0, 0.0),
        t_max=90.0,
        dt=0.01,
        transient_fraction=0.20,
    ),
]


# ------------------------------------------------------------
# Core computation
# ------------------------------------------------------------

def simulate_system(cfg: SystemConfig) -> Tuple[Array, Array]:
    n_steps = int(cfg.t_max / cfg.dt)
    t_eval = np.linspace(0.0, cfg.t_max, n_steps + 1)
    sol = solve_ivp(
        fun=cfg.rhs,
        t_span=(0.0, cfg.t_max),
        y0=np.array(cfg.initial_state, dtype=float),
        t_eval=t_eval,
        method="DOP853",
        rtol=1.0e-10,
        atol=1.0e-12,
    )

    if not sol.success:
        raise RuntimeError(f"{cfg.name} integration failed: {sol.message}")

    t = sol.t
    states = sol.y.T

    start = int(len(t) * cfg.transient_fraction)
    return t[start:], states[start:]


def compute_janus(t: Array, states: Array, eps: float = 1.0e-8) -> Tuple[Array, Array]:
    dt_f = (t[2:] - t[1:-1])[:, None]
    dt_b = (t[1:-1] - t[:-2])[:, None]

    forward = (states[2:] - states[1:-1]) / dt_f
    backward = (states[1:-1] - states[:-2]) / dt_b

    overlap = forward * backward
    numerator = np.linalg.norm(overlap, axis=1)
    denominator = np.linalg.norm(forward, axis=1) * np.linalg.norm(backward, axis=1) + eps

    janus = numerator / denominator
    return states[1:-1], janus


def compute_curvature(states: Array, eps: float = 1.0e-8) -> Array:
    r1 = states[1:-1] - states[:-2]
    r2 = states[2:] - states[1:-1]

    cross = np.cross(r1, r2)
    numerator = np.linalg.norm(cross, axis=1)

    speed = np.linalg.norm(r1, axis=1)
    denominator = speed**3 + eps

    curvature = numerator / denominator
    return curvature


def normalize(v: Array) -> Array:
    v_min = np.nanmin(v)
    v_max = np.nanmax(v)
    scale = v_max - v_min
    if scale <= 0 or not np.isfinite(scale):
        return np.zeros_like(v)
    return (v - v_min) / scale


def analyze_system(cfg: SystemConfig) -> Dict[str, object]:
    t, states = simulate_system(cfg)
    centered_states, janus = compute_janus(t, states)

    curvature_raw = compute_curvature(states)
    curvature_raw = curvature_raw[: len(janus)]

    log_curv = np.log10(curvature_raw + 1.0e-8)

    n = min(len(janus), len(log_curv), len(centered_states))
    janus = janus[:n]
    log_curv = log_curv[:n]
    centered_states = centered_states[:n]

    r, _ = pearsonr(janus, log_curv)

    low_threshold = np.quantile(janus, 0.08)
    high_threshold = np.quantile(log_curv, 0.92)

    low_mask = janus <= low_threshold
    high_mask = log_curv >= high_threshold
    overlap_mask = low_mask & high_mask

    overlap_fraction = np.sum(overlap_mask) / max(np.sum(low_mask), 1)

    # Orientation angle in JANUS-curvature space.
    # r < 0 => negative coupling, r > 0 => positive coupling.
    # overlap acts as vertical strength / transition specificity.
    angle = np.degrees(np.arctan2(overlap_fraction, r))

    # Keep angle readable around [-180, 180]
    if angle > 180:
        angle -= 360

    return {
        "name": cfg.name,
        "states": centered_states,
        "janus": janus,
        "log_curvature": log_curv,
        "janus_mean": float(np.mean(janus)),
        "janus_std": float(np.std(janus)),
        "curvature_mean": float(np.mean(curvature_raw[:n])),
        "r": float(r),
        "low_count": int(np.sum(low_mask)),
        "high_count": int(np.sum(high_mask)),
        "overlap_count": int(np.sum(overlap_mask)),
        "overlap_fraction": float(overlap_fraction),
        "orientation_angle": float(angle),
    }


# ------------------------------------------------------------
# Plotting
# ------------------------------------------------------------

def plot_orientation_atlas(results: Dict[str, Dict[str, object]], out_path: Path, dpi: int) -> None:
    names = list(results.keys())
    r_values = np.array([results[n]["r"] for n in names])
    overlap_values = np.array([results[n]["overlap_fraction"] for n in names])
    mean_values = np.array([results[n]["janus_mean"] for n in names])
    angles = np.array([results[n]["orientation_angle"] for n in names])

    fig, axes = plt.subplots(2, 2, figsize=(13, 10))

    ax = axes[0, 0]
    ax.axvline(0, linestyle="--", linewidth=1.2)
    ax.scatter(r_values, overlap_values, s=180)
    for i, name in enumerate(names):
        ax.text(r_values[i] + 0.01, overlap_values[i] + 0.005, name)
    ax.set_title("JANUS Transition Orientation Space")
    ax.set_xlabel("JANUS vs log-curvature correlation r")
    ax.set_ylabel("low-JANUS / high-curvature overlap fraction")
    ax.grid(alpha=0.25)

    ax = axes[0, 1]
    ax.bar(names, angles)
    ax.axhline(0, linestyle="--", linewidth=1.2)
    ax.set_title("Transition Orientation Angle")
    ax.set_ylabel("angle degrees")
    ax.grid(alpha=0.25)

    ax = axes[1, 0]
    ax.bar(names, mean_values)
    ax.set_title("Mean JANUS Coherence")
    ax.set_ylabel("mean")
    ax.grid(alpha=0.25)

    ax = axes[1, 1]
    ax.bar(names, [results[n]["janus_std"] for n in names])
    ax.set_title("JANUS Coherence Variance Proxy")
    ax.set_ylabel("std")
    ax.grid(alpha=0.25)

    fig.suptitle(
        "JANUS Transition Orientation Atlas\n"
        "System class as orientation in coherence-curvature space",
        fontsize=15,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_phase_space(results: Dict[str, Dict[str, object]], out_path: Path, dpi: int) -> None:
    fig, axes = plt.subplots(1, len(results), figsize=(17, 5))

    for ax, (name, result) in zip(axes, results.items()):
        j = result["janus"]
        c = normalize(result["log_curvature"])

        ax.scatter(j[:-1], j[1:], c=c[:-1], s=1.4, cmap="viridis", alpha=0.65)
        ax.set_title(f"{name}\nJ(t) → J(t+1)")
        ax.set_xlabel("J(t)")
        ax.set_ylabel("J(t+1)")
        ax.grid(alpha=0.2)

    fig.suptitle("JANUS Orientation Phase Space", fontsize=15)
    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_orientation_vectors(results: Dict[str, Dict[str, object]], out_path: Path, dpi: int) -> None:
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.axhline(0, linestyle="--", linewidth=1.2)
    ax.axvline(0, linestyle="--", linewidth=1.2)

    for name, result in results.items():
        r = result["r"]
        o = result["overlap_fraction"]
        angle = result["orientation_angle"]

        ax.arrow(
            0,
            0,
            r,
            o,
            head_width=0.012,
            length_includes_head=True,
            alpha=0.85,
        )
        ax.scatter([r], [o], s=120)
        ax.text(r + 0.01, o + 0.01, f"{name}\n{angle:.1f}°")

    ax.set_title("JANUS Transition Orientation Vectors")
    ax.set_xlabel("correlation axis: JANUS ↔ curvature")
    ax.set_ylabel("transition-overlap axis")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def write_summary(results: Dict[str, Dict[str, object]], out_path: Path) -> None:
    lines = []
    lines.append("JANUS transition orientation atlas")
    lines.append("==================================")
    lines.append("")
    lines.append("Interpretation:")
    lines.append("Orientation is defined in a 2D diagnostic space:")
    lines.append("x = JANUS vs log-curvature correlation")
    lines.append("y = low-JANUS / high-curvature overlap fraction")
    lines.append("")
    lines.append("Negative x indicates anti-coupling.")
    lines.append("Positive x indicates co-coupling.")
    lines.append("High y indicates localized transition-candidate overlap.")
    lines.append("")

    for name, result in results.items():
        lines.append(f"{name}")
        lines.append("-" * len(name))
        lines.append(f"samples: {len(result['janus'])}")
        lines.append(f"JANUS mean: {result['janus_mean']:.6f}")
        lines.append(f"JANUS std: {result['janus_std']:.6f}")
        lines.append(f"curvature mean: {result['curvature_mean']:.6f}")
        lines.append(f"JANUS vs log-curvature r: {result['r']:.6f}")
        lines.append(f"low-JANUS count: {result['low_count']}")
        lines.append(f"high-curvature count: {result['high_count']}")
        lines.append(f"overlap count: {result['overlap_count']}")
        lines.append(f"overlap fraction: {result['overlap_fraction']:.6f}")
        lines.append(f"transition orientation angle: {result['orientation_angle']:.6f} degrees")
        lines.append("")

    lines.append("Working reading:")
    lines.append("- Lorenz should occupy a negative-coupling switching region.")
    lines.append("- Rossler should occupy a near-tangential transport region.")
    lines.append("- Halvorsen may occupy an inverted fragmented-coupling region.")
    lines.append("")
    lines.append("If these orientations remain stable under parameter variation,")
    lines.append("JANUS can be treated as a system-class diagnostic,")
    lines.append("not only a Lorenz-specific coherence observable.")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def run_experiment() -> None:
    output_cfg = OutputConfig()
    output_cfg.output_dir.mkdir(parents=True, exist_ok=True)

    print("Running JANUS transition orientation atlas...")

    results: Dict[str, Dict[str, object]] = {}
    for system_cfg in SYSTEMS:
        print(f"Analyzing {system_cfg.name}...")
        results[system_cfg.name] = analyze_system(system_cfg)

    plot_orientation_atlas(
        results,
        output_cfg.output_dir / "janus_transition_orientation_atlas.png",
        output_cfg.dpi,
    )
    plot_phase_space(
        results,
        output_cfg.output_dir / "janus_orientation_phase_space.png",
        output_cfg.dpi,
    )
    plot_orientation_vectors(
        results,
        output_cfg.output_dir / "janus_orientation_vectors.png",
        output_cfg.dpi,
    )
    write_summary(
        results,
        output_cfg.output_dir / "janus_orientation_summary.txt",
    )

    print()
    print("================================================")
    print("JANUS TRANSITION ORIENTATION ATLAS")
    print("================================================")
    for name, result in results.items():
        print(f"{name}:")
        print(f"  samples: {len(result['janus'])}")
        print(f"  JANUS mean: {result['janus_mean']:.6f}")
        print(f"  JANUS std : {result['janus_std']:.6f}")
        print(f"  r(JANUS, log curvature): {result['r']:.6f}")
        print(f"  overlap fraction: {result['overlap_fraction']:.6f}")
        print(f"  orientation angle: {result['orientation_angle']:.3f}°")
        print()

    print(f"outputs saved to: {output_cfg.output_dir.resolve()}")
    print("================================================")


if __name__ == "__main__":
    run_experiment()
