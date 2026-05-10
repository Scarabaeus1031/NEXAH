#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 02
Janus vs FTLE Comparison

Purpose
-------
Compare local Janus directional coherence against a finite-time
Lyapunov-style separation estimate inside the Lorenz system.

This experiment investigates whether:

    low Janus coherence regions
    correlate with
    locally unstable transport structure.

The script remains exploratory and computational.
It does not claim new physics or a finalized theory.

Outputs
-------
outputs/
    janus_ftle_overlay.png
    janus_ftle_scatter.png
    janus_ftle_heatmap.png
    janus_ftle_joint_density.png
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.interpolate import griddata


Array = np.ndarray


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

    perturbation: float = 1.0e-7
    ftle_horizon_steps: int = 12

    grid_size: int = 300
    dpi: int = 220

    seed: int = 7


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# Dynamical system
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
# Janus field
# -----------------------------------------------------------------------------


def compute_janus(t: Array, states: Array, cfg: Config) -> Array:
    dt_f = (t[2:] - t[1:-1])[:, None]
    dt_b = (t[1:-1] - t[:-2])[:, None]

    fwd = (states[2:] - states[1:-1]) / dt_f
    bwd = (states[1:-1] - states[:-2]) / dt_b

    overlap = fwd * bwd

    numerator = np.linalg.norm(overlap, axis=1)

    denominator = (
        np.linalg.norm(fwd, axis=1)
        * np.linalg.norm(bwd, axis=1)
        + cfg.epsilon
    )

    return numerator / denominator


# -----------------------------------------------------------------------------
# FTLE-style local divergence estimate
# -----------------------------------------------------------------------------


def compute_ftle(states: Array, cfg: Config) -> Array:
    n = len(states)

    ftle = np.full(n, np.nan)

    for i in range(n - cfg.ftle_horizon_steps):
        x0 = states[i]

        random_direction = np.random.normal(size=3)
        random_direction /= np.linalg.norm(random_direction)

        x1 = x0 + cfg.perturbation * random_direction

        ref_final = states[i + cfg.ftle_horizon_steps]

        t_local = np.arange(
            0,
            cfg.ftle_horizon_steps * cfg.dt + cfg.dt,
            cfg.dt,
        )

        pert_solution = solve_ivp(
            fun=lambda t, y: lorenz_rhs(t, y, cfg),
            t_span=(0, cfg.ftle_horizon_steps * cfg.dt),
            y0=x1,
            t_eval=t_local,
            method="DOP853",
            rtol=1e-9,
            atol=1e-11,
        )

        if not pert_solution.success:
            continue

        pert_final = pert_solution.y[:, -1]

        delta_0 = cfg.perturbation
        delta_t = np.linalg.norm(pert_final - ref_final)

        ftle[i] = (
            np.log((delta_t + cfg.epsilon) / delta_0)
            / (cfg.ftle_horizon_steps * cfg.dt)
        )

    return ftle


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------


def normalize(values: Array) -> Array:
    mask = np.isfinite(values)

    v_min = np.min(values[mask])
    v_max = np.max(values[mask])

    return (values - v_min) / (v_max - v_min + 1e-12)


# -----------------------------------------------------------------------------
# Plots
# -----------------------------------------------------------------------------


def plot_overlay(states: Array, janus: Array, ftle: Array, cfg: Config) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))

    x = states[:, 0]
    y = states[:, 1]

    janus_low = janus < np.quantile(janus, 0.08)

    ftle_high = ftle > np.nanquantile(ftle, 0.92)

    ax.plot(x, y, linewidth=0.35, alpha=0.28, color="steelblue")

    ax.scatter(
        x[janus_low],
        y[janus_low],
        s=6,
        alpha=0.6,
        label="low Janus",
    )

    ax.scatter(
        x[ftle_high],
        y[ftle_high],
        s=6,
        alpha=0.6,
        label="high FTLE",
    )

    overlap = janus_low & ftle_high

    ax.scatter(
        x[overlap],
        y[overlap],
        s=10,
        alpha=0.9,
        label="overlap",
    )

    ax.set_title("Janus vs FTLE — Lorenz Overlay")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(alpha=0.18)
    ax.legend()

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "janus_ftle_overlay.png", dpi=cfg.dpi)
    plt.close(fig)



def plot_scatter(janus: Array, ftle: Array, cfg: Config) -> None:
    mask = np.isfinite(ftle)

    fig, ax = plt.subplots(figsize=(8, 7))

    ax.scatter(
        janus[mask],
        ftle[mask],
        s=4,
        alpha=0.3,
    )

    correlation = np.corrcoef(janus[mask], ftle[mask])[0, 1]

    ax.set_title(
        f"Janus vs FTLE Correlation\nPearson r = {correlation:.4f}"
    )

    ax.set_xlabel("Janus coherence")
    ax.set_ylabel("FTLE estimate")
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "janus_ftle_scatter.png", dpi=cfg.dpi)
    plt.close(fig)



def plot_joint_heatmap(states: Array, janus: Array, ftle: Array, cfg: Config) -> None:
    mask = np.isfinite(ftle)

    x = states[mask, 0]
    y = states[mask, 1]

    combined = normalize(ftle[mask]) * (1.0 - normalize(janus[mask]))

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
    cbar.set_label("high FTLE × low Janus")

    ax.set_title("Joint Transition Sensitivity Field")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "janus_ftle_heatmap.png", dpi=cfg.dpi)
    plt.close(fig)



def plot_density(janus: Array, ftle: Array, cfg: Config) -> None:
    mask = np.isfinite(ftle)

    fig, ax = plt.subplots(figsize=(8, 7))

    hist = ax.hist2d(
        janus[mask],
        ftle[mask],
        bins=120,
        cmap="viridis",
    )

    cbar = fig.colorbar(hist[3], ax=ax)
    cbar.set_label("density")

    ax.set_title("Janus–FTLE Joint Density")
    ax.set_xlabel("Janus coherence")
    ax.set_ylabel("FTLE estimate")
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "janus_ftle_joint_density.png", dpi=cfg.dpi)
    plt.close(fig)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> None:
    cfg = Config()

    print("Running Lorenz simulation...")
    t, states = simulate(cfg)

    print("Computing Janus coherence...")
    janus = compute_janus(t, states, cfg)

    states_mid = states[1:-1]

    print("Computing FTLE estimates...")
    ftle = compute_ftle(states_mid, cfg)

    print("Generating visualizations...")

    plot_overlay(states_mid, janus, ftle, cfg)
    plot_scatter(janus, ftle, cfg)
    plot_joint_heatmap(states_mid, janus, ftle, cfg)
    plot_density(janus, ftle, cfg)

    mask = np.isfinite(ftle)

    correlation = np.corrcoef(janus[mask], ftle[mask])[0, 1]

    print()
    print("JANUS vs FTLE experiment complete")
    print(f"samples: {np.sum(mask)}")
    print(f"correlation: {correlation:.6f}")
    print(f"janus mean: {np.mean(janus):.6f}")
    print(f"ftle mean: {np.nanmean(ftle):.6f}")
    print()
    print(f"outputs saved to: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
