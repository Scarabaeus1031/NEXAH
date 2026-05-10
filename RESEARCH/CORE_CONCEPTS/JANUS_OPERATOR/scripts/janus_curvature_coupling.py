#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 04
Janus Curvature Coupling

Purpose
-------
Investigate whether local Janus coherence relates to trajectory curvature
inside the Lorenz system.

Core question:

    Do low-Janus regions appear near geometric refolding or curvature
    reorganization zones?

This experiment is exploratory and computational.
It does not claim a new physical law.

Outputs
-------
RESEARCH/CORE_CONCEPTS/JANUS_OPERATOR/outputs/
    janus_curvature_overlay.png
    janus_curvature_scatter.png
    janus_curvature_density.png
    janus_curvature_heatmap.png
    janus_curvature_profile.png
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.interpolate import griddata


Array = np.ndarray


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------


@dataclass(frozen=True)
class Config:
    sigma: float = 10.0
    rho: float = 28.0
    beta: float = 8.0 / 3.0

    t_min: float = 0.0
    t_max: float = 100.0
    dt: float = 0.01

    transient_fraction: float = 0.15

    epsilon: float = 1.0e-8

    smoothing_window: int = 21
    grid_size: int = 320
    dpi: int = 220

    seed: int = 7


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# Lorenz dynamics
# -----------------------------------------------------------------------------


def lorenz_rhs(_: float, state: Array, cfg: Config) -> Array:
    x, y, z = state

    dx = cfg.sigma * (y - x)
    dy = x * (cfg.rho - z) - y
    dz = x * y - cfg.beta * z

    return np.array([dx, dy, dz], dtype=float)


# -----------------------------------------------------------------------------
# Simulation
# -----------------------------------------------------------------------------


def simulate(cfg: Config) -> tuple[Array, Array]:
    np.random.seed(cfg.seed)

    t_eval = np.arange(cfg.t_min, cfg.t_max + cfg.dt, cfg.dt)

    solution = solve_ivp(
        fun=lambda t, y: lorenz_rhs(t, y, cfg),
        t_span=(cfg.t_min, cfg.t_max),
        y0=np.array([1.0, 1.0, 1.0]),
        t_eval=t_eval,
        method="DOP853",
        rtol=1e-10,
        atol=1e-12,
    )

    if not solution.success:
        raise RuntimeError(solution.message)

    states = solution.y.T
    t = solution.t

    start = int(len(t) * cfg.transient_fraction)

    return t[start:], states[start:]


# -----------------------------------------------------------------------------
# Janus coherence
# -----------------------------------------------------------------------------


def compute_janus(t: Array, states: Array, cfg: Config) -> tuple[Array, Array, Array]:
    dt_f = (t[2:] - t[1:-1])[:, None]
    dt_b = (t[1:-1] - t[:-2])[:, None]

    centered_t = t[1:-1]
    centered_states = states[1:-1]

    forward = (states[2:] - states[1:-1]) / dt_f
    backward = (states[1:-1] - states[:-2]) / dt_b

    overlap = forward * backward

    numerator = np.linalg.norm(overlap, axis=1)

    denominator = (
        np.linalg.norm(forward, axis=1)
        * np.linalg.norm(backward, axis=1)
        + cfg.epsilon
    )

    janus = numerator / denominator

    return centered_t, centered_states, janus


# -----------------------------------------------------------------------------
# Curvature
# -----------------------------------------------------------------------------


def compute_curvature(t: Array, states: Array, cfg: Config) -> tuple[Array, Array, Array]:
    """
    Compute trajectory curvature from finite-difference velocity and acceleration.

    kappa(t) = ||v(t) x a(t)|| / (||v(t)||^3 + epsilon)
    """
    dt = np.gradient(t)

    velocity = np.gradient(states, axis=0) / dt[:, None]
    acceleration = np.gradient(velocity, axis=0) / dt[:, None]

    cross = np.cross(velocity, acceleration)
    numerator = np.linalg.norm(cross, axis=1)

    speed = np.linalg.norm(velocity, axis=1)
    denominator = speed**3 + cfg.epsilon

    curvature = numerator / denominator

    return velocity, acceleration, curvature


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------


def normalize(values: Array) -> Array:
    mask = np.isfinite(values)

    if not np.any(mask):
        return np.zeros_like(values)

    v_min = np.min(values[mask])
    v_max = np.max(values[mask])

    return (values - v_min) / (v_max - v_min + 1e-12)



def moving_average(values: Array, window: int) -> Array:
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode="same")


# -----------------------------------------------------------------------------
# Visualizations
# -----------------------------------------------------------------------------


def plot_overlay(
    states: Array,
    janus: Array,
    curvature: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))

    x = states[:, 0]
    y = states[:, 1]

    low_janus = janus < np.quantile(janus, 0.08)
    high_curvature = curvature > np.quantile(curvature, 0.92)
    overlap = low_janus & high_curvature

    ax.plot(x, y, linewidth=0.35, alpha=0.20)

    ax.scatter(
        x[low_janus],
        y[low_janus],
        s=5,
        alpha=0.55,
        label="lowest 8% Janus",
    )

    ax.scatter(
        x[high_curvature],
        y[high_curvature],
        s=5,
        alpha=0.45,
        label="highest 8% curvature",
    )

    ax.scatter(
        x[overlap],
        y[overlap],
        s=16,
        alpha=0.9,
        label="overlap",
    )

    ax.set_title("Janus vs Curvature — Lorenz Overlay")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(alpha=0.18)
    ax.legend()

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_curvature_overlay.png",
        dpi=cfg.dpi,
    )

    plt.close(fig)



def plot_scatter(janus: Array, curvature: Array, cfg: Config) -> None:
    mask = np.isfinite(janus) & np.isfinite(curvature)

    log_curvature = np.log10(curvature[mask] + cfg.epsilon)
    correlation = np.corrcoef(janus[mask], log_curvature)[0, 1]

    fig, ax = plt.subplots(figsize=(8, 7))

    ax.scatter(
        janus[mask],
        log_curvature,
        s=4,
        alpha=0.30,
    )

    ax.set_title(
        f"Janus vs Curvature\nPearson r = {correlation:.4f}"
    )

    ax.set_xlabel("Janus coherence")
    ax.set_ylabel("log10 curvature")
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_curvature_scatter.png",
        dpi=cfg.dpi,
    )

    plt.close(fig)



def plot_density(janus: Array, curvature: Array, cfg: Config) -> None:
    mask = np.isfinite(janus) & np.isfinite(curvature)

    fig, ax = plt.subplots(figsize=(8, 7))

    hist = ax.hist2d(
        janus[mask],
        np.log10(curvature[mask] + cfg.epsilon),
        bins=120,
        cmap="viridis",
    )

    cbar = fig.colorbar(hist[3], ax=ax)
    cbar.set_label("density")

    ax.set_title("Janus–Curvature Joint Density")
    ax.set_xlabel("Janus coherence")
    ax.set_ylabel("log10 curvature")
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_curvature_density.png",
        dpi=cfg.dpi,
    )

    plt.close(fig)



def plot_heatmap(
    states: Array,
    janus: Array,
    curvature: Array,
    cfg: Config,
) -> None:
    x = states[:, 0]
    y = states[:, 1]

    combined = normalize(curvature) * (1.0 - normalize(janus))

    xi = np.linspace(np.percentile(x, 1), np.percentile(x, 99), cfg.grid_size)
    yi = np.linspace(np.percentile(y, 1), np.percentile(y, 99), cfg.grid_size)

    grid_x, grid_y = np.meshgrid(xi, yi)

    grid = griddata(
        points=np.column_stack([x, y]),
        values=combined,
        xi=(grid_x, grid_y),
        method="linear",
    )

    fig, ax = plt.subplots(figsize=(10, 8))

    image = ax.imshow(
        grid,
        extent=(xi.min(), xi.max(), yi.min(), yi.max()),
        origin="lower",
        aspect="auto",
        cmap="magma",
    )

    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label("high curvature × low Janus")

    ax.set_title("Joint Curvature-Reconfiguration Field")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_curvature_heatmap.png",
        dpi=cfg.dpi,
    )

    plt.close(fig)



def plot_profile(
    t: Array,
    janus: Array,
    curvature: Array,
    cfg: Config,
) -> None:
    fig, ax1 = plt.subplots(figsize=(14, 5))

    janus_smoothed = moving_average(janus, cfg.smoothing_window)
    curvature_smoothed = moving_average(
        normalize(np.log10(curvature + cfg.epsilon)),
        cfg.smoothing_window,
    )

    ax1.plot(
        t,
        janus_smoothed,
        linewidth=1.2,
        label="Janus coherence",
    )

    ax1.plot(
        t,
        curvature_smoothed,
        linewidth=1.0,
        alpha=0.85,
        label="normalized log curvature",
    )

    ax1.set_title("Temporal Coupling: Janus Coherence and Curvature")
    ax1.set_xlabel("time")
    ax1.set_ylabel("normalized value")
    ax1.grid(alpha=0.18)
    ax1.legend()

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_curvature_profile.png",
        dpi=cfg.dpi,
    )

    plt.close(fig)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> None:
    cfg = Config()

    print("Running Lorenz simulation...")
    t, states = simulate(cfg)

    print("Computing Janus coherence...")
    t_mid, states_mid, janus = compute_janus(t, states, cfg)

    print("Computing curvature...")
    _, _, curvature_full = compute_curvature(t, states, cfg)

    curvature = curvature_full[1:-1]

    print("Generating visualizations...")

    plot_overlay(states_mid, janus, curvature, cfg)
    plot_scatter(janus, curvature, cfg)
    plot_density(janus, curvature, cfg)
    plot_heatmap(states_mid, janus, curvature, cfg)
    plot_profile(t_mid, janus, curvature, cfg)

    mask = np.isfinite(janus) & np.isfinite(curvature)
    log_curvature = np.log10(curvature[mask] + cfg.epsilon)
    correlation = np.corrcoef(janus[mask], log_curvature)[0, 1]

    low_janus = janus < np.quantile(janus, 0.08)
    high_curvature = curvature > np.quantile(curvature, 0.92)
    overlap = low_janus & high_curvature

    print()
    print("JANUS curvature experiment complete")
    print(f"samples: {np.sum(mask)}")
    print(f"correlation Janus vs log curvature: {correlation:.6f}")
    print(f"janus mean: {np.mean(janus):.6f}")
    print(f"curvature mean: {np.mean(curvature):.6f}")
    print(f"low-Janus count: {np.sum(low_janus)}")
    print(f"high-curvature count: {np.sum(high_curvature)}")
    print(f"overlap count: {np.sum(overlap)}")
    print()
    print(f"outputs saved to: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
