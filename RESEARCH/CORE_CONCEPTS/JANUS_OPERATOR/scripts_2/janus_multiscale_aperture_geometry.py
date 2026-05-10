#!/usr/bin/env python3
"""
JANUS_OPERATOR / EXP-25
Multi-Scale Aperture Geometry

Script:
    janus_multiscale_aperture_geometry.py

Goal:
    Test whether JANUS aperture gate structure persists across
    multiple temporal smoothing scales.

Focus:
    - aperture score stability
    - gate persistence across scales
    - multi-scale aperture ridges
    - recursive / basin-like gate organization

Outputs:
    outputs/exp25_multiscale_aperture_map.png
    outputs/exp25_aperture_scale_variance.png
    outputs/exp25_persistent_gate_overlay.png
    outputs/exp25_multiscale_gate_density.png
    outputs/exp25_multiscale_aperture_summary.txt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.ndimage import gaussian_filter1d, gaussian_filter


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
    scales: Tuple[int, ...] = (1, 2, 4, 8, 16, 32, 64)


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
# Core helpers
# ------------------------------------------------------------

def normalize_1d(v: Array, eps: float = 1.0e-12) -> Array:
    v_min = np.nanmin(v)
    v_max = np.nanmax(v)
    scale = v_max - v_min

    if not np.isfinite(scale) or scale < eps:
        return np.zeros_like(v)

    return (v - v_min) / scale


def normalize_vectors(v: Array, eps: float = 1.0e-12) -> Array:
    n = np.linalg.norm(v, axis=1, keepdims=True)
    return v / (n + eps)


def smooth_states(states: Array, scale: int) -> Array:
    if scale <= 1:
        return states.copy()

    return gaussian_filter1d(
        states,
        sigma=float(scale),
        axis=0,
        mode="nearest",
    )


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


def compute_memory_signal(janus: Array, lag: int) -> Array:
    memory = np.zeros_like(janus)

    if lag <= 0 or lag >= len(janus):
        return memory

    a = janus[:-lag]
    b = janus[lag:]

    local_memory = 1.0 - np.abs(b - a)

    memory[lag:] = normalize_1d(local_memory)

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

    axis_proximity = 1.0 - normalize_1d(np.abs(states[:, 0]))
    low_janus = 1.0 - normalize_1d(janus)
    accel_n = normalize_1d(accel)
    breathing_n = normalize_1d(breathing)
    memory_n = normalize_1d(memory)

    score = (
        0.30 * low_janus
        + 0.25 * accel_n
        + 0.20 * breathing_n
        + 0.15 * axis_proximity
        + 0.10 * memory_n
    )

    return normalize_1d(score)


def analyze_scale(
    t: Array,
    states: Array,
    scale: int,
    cfg: ExperimentConfig,
) -> Dict[str, Array | float | int]:
    smoothed = smooth_states(states, scale)

    core_states, janus = compute_janus(t, smoothed)
    memory = compute_memory_signal(janus, cfg.memory_lag)

    n = min(len(core_states), len(janus), len(memory))

    core_states = core_states[:n]
    janus = janus[:n]
    memory = memory[:n]

    aperture = compute_aperture_score(
        core_states,
        janus,
        memory,
    )

    threshold = np.quantile(aperture, cfg.gate_quantile)
    gate_mask = aperture >= threshold

    return {
        "scale": scale,
        "states": core_states,
        "janus": janus,
        "memory": memory,
        "aperture": aperture,
        "threshold": float(threshold),
        "gate_mask": gate_mask,
        "gate_count": int(np.sum(gate_mask)),
        "variance": float(np.var(aperture)),
        "mean": float(np.mean(aperture)),
        "max": float(np.max(aperture)),
    }


# ------------------------------------------------------------
# Visualizations
# ------------------------------------------------------------

def plot_multiscale_aperture_map(
    results: List[Dict[str, Array | float | int]],
    out_path: Path,
    dpi: int,
) -> None:
    min_len = min(len(r["aperture"]) for r in results)

    matrix = np.array([
        r["aperture"][:min_len]
        for r in results
    ])

    fig, ax = plt.subplots(figsize=(16, 6))

    im = ax.imshow(
        matrix,
        aspect="auto",
        interpolation="nearest",
        cmap="magma",
    )

    ax.set_title(
        "EXP-25 — Multi-Scale JANUS Aperture Map\n"
        "Aperture score across smoothing scales"
    )
    ax.set_xlabel("time index")
    ax.set_ylabel("scale")

    ax.set_yticks(np.arange(len(results)))
    ax.set_yticklabels([str(r["scale"]) for r in results])

    plt.colorbar(im, ax=ax, label="aperture score")

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_aperture_scale_variance(
    results: List[Dict[str, Array | float | int]],
    out_path: Path,
    dpi: int,
) -> None:
    scales = np.array([r["scale"] for r in results], dtype=float)
    variances = np.array([r["variance"] for r in results], dtype=float)
    means = np.array([r["mean"] for r in results], dtype=float)
    maxima = np.array([r["max"] for r in results], dtype=float)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(scales, variances, marker="o", label="variance")
    ax.plot(scales, means, marker="o", label="mean")
    ax.plot(scales, maxima, marker="o", label="max")

    ax.set_xscale("log", base=2)

    ax.set_title("EXP-25 — Aperture Statistics Across Scales")
    ax.set_xlabel("smoothing scale")
    ax.set_ylabel("value")
    ax.grid(alpha=0.25)
    ax.legend()

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_persistent_gate_overlay(
    results: List[Dict[str, Array | float | int]],
    out_path: Path,
    dpi: int,
) -> None:
    base = results[0]
    states = base["states"]
    n = len(states)

    persistence = np.zeros(n)

    for r in results:
        mask = r["gate_mask"]
        m = min(n, len(mask))
        persistence[:m] += mask[:m].astype(float)

    persistence = persistence / len(results)

    fig, ax = plt.subplots(figsize=(10, 9))

    sc = ax.scatter(
        states[:, 0],
        states[:, 2],
        c=persistence,
        s=3,
        cmap="plasma",
        alpha=0.85,
    )

    ax.axvline(0.0, linestyle="--", linewidth=1.0, alpha=0.5)

    ax.set_title(
        "EXP-25 — Persistent Aperture Gate Overlay\n"
        "Gate persistence across smoothing scales"
    )
    ax.set_xlabel("x")
    ax.set_ylabel("z")
    ax.grid(alpha=0.25)

    plt.colorbar(sc, ax=ax, label="gate persistence")

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_multiscale_gate_density(
    results: List[Dict[str, Array | float | int]],
    out_path: Path,
    dpi: int,
) -> None:
    xs = []
    zs = []

    for r in results:
        states = r["states"]
        mask = r["gate_mask"]

        m = min(len(states), len(mask))

        xs.append(states[:m, 0][mask[:m]])
        zs.append(states[:m, 2][mask[:m]])

    x_all = np.concatenate(xs)
    z_all = np.concatenate(zs)

    H, xe, ze = np.histogram2d(
        x_all,
        z_all,
        bins=260,
    )

    H = gaussian_filter(H.T, sigma=2.0)

    fig, ax = plt.subplots(figsize=(10, 8))

    im = ax.imshow(
        H,
        origin="lower",
        extent=[xe[0], xe[-1], ze[0], ze[-1]],
        aspect="auto",
        cmap="inferno",
    )

    ax.axvline(0.0, linestyle="--", linewidth=1.0, alpha=0.5)

    ax.set_title(
        "EXP-25 — Multi-Scale Aperture Gate Density\n"
        "Accumulated gate density over all scales"
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
    results: List[Dict[str, Array | float | int]],
    out_path: Path,
) -> None:
    lines = []

    lines.append("EXP-25 — JANUS multi-scale aperture geometry")
    lines.append("================================================")
    lines.append("")

    lines.append("Goal:")
    lines.append("Test whether aperture gate structure persists across smoothing scales.")
    lines.append("")

    lines.append("Scale statistics:")
    lines.append("")

    for r in results:
        lines.append(f"scale: {r['scale']}")
        lines.append(f"  gate candidates: {r['gate_count']}")
        lines.append(f"  threshold: {r['threshold']:.6f}")
        lines.append(f"  mean aperture: {r['mean']:.6f}")
        lines.append(f"  max aperture: {r['max']:.6f}")
        lines.append(f"  aperture variance: {r['variance']:.6f}")
        lines.append("")

    lines.append("Working interpretation:")
    lines.append("- persistent gate locations across scale indicate robust aperture geometry")
    lines.append("- scale collapse would indicate noise-level gate artifacts")
    lines.append("- multi-scale density highlights recurring transition corridors")
    lines.append("- this remains exploratory and should be compared with surrogate controls")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def run_experiment() -> None:
    output_cfg = OutputConfig()
    cfg = ExperimentConfig()

    output_cfg.output_dir.mkdir(parents=True, exist_ok=True)

    print()
    print("==========================================")
    print("EXP-25 — MULTI-SCALE APERTURE GEOMETRY")
    print("==========================================")
    print()

    t, states = simulate_lorenz(cfg)

    results = []

    for scale in cfg.scales:
        print(f"Analyzing scale {scale}...")
        results.append(
            analyze_scale(
                t=t,
                states=states,
                scale=scale,
                cfg=cfg,
            )
        )

    plot_multiscale_aperture_map(
        results,
        output_cfg.output_dir / "exp25_multiscale_aperture_map.png",
        output_cfg.dpi,
    )

    plot_aperture_scale_variance(
        results,
        output_cfg.output_dir / "exp25_aperture_scale_variance.png",
        output_cfg.dpi,
    )

    plot_persistent_gate_overlay(
        results,
        output_cfg.output_dir / "exp25_persistent_gate_overlay.png",
        output_cfg.dpi,
    )

    plot_multiscale_gate_density(
        results,
        output_cfg.output_dir / "exp25_multiscale_gate_density.png",
        output_cfg.dpi,
    )

    write_summary(
        results,
        output_cfg.output_dir / "exp25_multiscale_aperture_summary.txt",
    )

    print()
    print("outputs generated:")
    print("outputs/exp25_multiscale_aperture_map.png")
    print("outputs/exp25_aperture_scale_variance.png")
    print("outputs/exp25_persistent_gate_overlay.png")
    print("outputs/exp25_multiscale_gate_density.png")
    print("outputs/exp25_multiscale_aperture_summary.txt")
    print()
    print("EXP-25 complete.")
    print()


if __name__ == "__main__":
    run_experiment()
