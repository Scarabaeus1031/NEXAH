#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 09
Janus Noise Robustness

Purpose
-------
Test whether JANUS coherence structure remains stable under controlled
stochastic perturbations of the Lorenz trajectory.

Core question:

    Is the JANUS signal robust to noise,
    or is it dominated by numerical/sampling artifacts?

This experiment is exploratory and computational.
It does not claim a new physical law.

Outputs
-------
EXPERIMENTAL/BUILDER_LAB/JANUS_OPERATOR/outputs/
    janus_noise_signal_overlay.png
    janus_noise_correlation_decay.png
    janus_noise_distribution_shift.png
    janus_noise_heatmap.png
    janus_noise_summary.txt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.ndimage import gaussian_filter1d


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

    noise_levels: tuple[float, ...] = (
        0.0,
        0.001,
        0.0025,
        0.005,
        0.01,
        0.025,
        0.05,
    )

    smoothing_sigma: float = 3.0
    dpi: int = 220
    seed: int = 7


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# Lorenz system
# -----------------------------------------------------------------------------


def lorenz_rhs(_: float, state: Array, cfg: Config) -> Array:
    x, y, z = state

    dx = cfg.sigma * (y - x)
    dy = x * (cfg.rho - z) - y
    dz = x * y - cfg.beta * z

    return np.array([dx, dy, dz], dtype=float)


# -----------------------------------------------------------------------------
# Simulation and JANUS computation
# -----------------------------------------------------------------------------


def simulate(cfg: Config) -> tuple[Array, Array]:
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



def add_noise(states: Array, noise_level: float, rng: np.random.Generator) -> Array:
    if noise_level == 0.0:
        return states.copy()

    scale = np.std(states, axis=0)
    noise = rng.normal(
        loc=0.0,
        scale=noise_level * scale,
        size=states.shape,
    )

    return states + noise


# -----------------------------------------------------------------------------
# Analysis
# -----------------------------------------------------------------------------


def compute_noise_series(
    t: Array,
    states: Array,
    cfg: Config,
) -> tuple[Array, Array, Array]:
    rng = np.random.default_rng(cfg.seed)

    janus_series = []

    for noise_level in cfg.noise_levels:
        noisy_states = add_noise(states, noise_level, rng)
        _, _, janus = compute_janus(t, noisy_states, cfg)
        janus_smooth = gaussian_filter1d(janus, sigma=cfg.smoothing_sigma)
        janus_series.append(janus_smooth)

    janus_matrix = np.array(janus_series)
    reference = janus_matrix[0]

    correlations = []

    for signal in janus_matrix:
        r = np.corrcoef(reference, signal)[0, 1]
        correlations.append(r)

    return np.array(cfg.noise_levels), janus_matrix, np.array(correlations)


# -----------------------------------------------------------------------------
# Visualizations
# -----------------------------------------------------------------------------


def plot_signal_overlay(
    t_mid: Array,
    noise_levels: Array,
    janus_matrix: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(14, 6))

    step = max(1, len(t_mid) // 6000)

    for i, noise_level in enumerate(noise_levels):
        ax.plot(
            t_mid[::step],
            janus_matrix[i, ::step],
            linewidth=1.0,
            alpha=0.75,
            label=f"noise={noise_level:g}",
        )

    ax.set_title("JANUS Noise Robustness — Signal Overlay")
    ax.set_xlabel("time")
    ax.set_ylabel("smoothed JANUS coherence")
    ax.grid(alpha=0.18)
    ax.legend(ncol=2)

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_noise_signal_overlay.png",
        dpi=cfg.dpi,
    )
    plt.close(fig)



def plot_correlation_decay(
    noise_levels: Array,
    correlations: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        noise_levels,
        correlations,
        marker="o",
        linewidth=2.0,
    )

    ax.set_title("JANUS Robustness — Correlation Decay")
    ax.set_xlabel("relative noise level")
    ax.set_ylabel("correlation with clean JANUS signal")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_noise_correlation_decay.png",
        dpi=cfg.dpi,
    )
    plt.close(fig)



def plot_distribution_shift(
    noise_levels: Array,
    janus_matrix: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, noise_level in enumerate(noise_levels):
        ax.hist(
            janus_matrix[i],
            bins=80,
            density=True,
            alpha=0.30,
            label=f"noise={noise_level:g}",
        )

    ax.set_title("JANUS Noise Robustness — Distribution Shift")
    ax.set_xlabel("JANUS coherence")
    ax.set_ylabel("density")
    ax.grid(alpha=0.18)
    ax.legend(ncol=2)

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_noise_distribution_shift.png",
        dpi=cfg.dpi,
    )
    plt.close(fig)



def plot_noise_heatmap(
    t_mid: Array,
    noise_levels: Array,
    janus_matrix: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(14, 6))

    image = ax.imshow(
        janus_matrix,
        aspect="auto",
        origin="lower",
        extent=(t_mid.min(), t_mid.max(), noise_levels.min(), noise_levels.max()),
        cmap="viridis",
    )

    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label("smoothed JANUS coherence")

    ax.set_title("JANUS Noise Robustness — Scale/Noise Heatmap")
    ax.set_xlabel("time")
    ax.set_ylabel("relative noise level")
    ax.grid(alpha=0.12)

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_noise_heatmap.png",
        dpi=cfg.dpi,
    )
    plt.close(fig)



def write_summary(
    noise_levels: Array,
    janus_matrix: Array,
    correlations: Array,
    cfg: Config,
) -> None:
    lines = []
    lines.append("JANUS noise robustness experiment")
    lines.append("=================================")
    lines.append("")
    lines.append(f"samples per signal: {janus_matrix.shape[1]}")
    lines.append(f"smoothing sigma: {cfg.smoothing_sigma}")
    lines.append("")
    lines.append("noise_level, correlation_to_clean, mean, std")

    for noise_level, signal, corr in zip(noise_levels, janus_matrix, correlations):
        lines.append(
            f"{noise_level:.6f}, {corr:.6f}, "
            f"{np.mean(signal):.6f}, {np.std(signal):.6f}"
        )

    (OUTPUT_DIR / "janus_noise_summary.txt").write_text("\n".join(lines))


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> None:
    cfg = Config()

    print("Running Lorenz simulation...")
    t, states = simulate(cfg)

    print("Computing JANUS noise robustness series...")
    noise_levels, janus_matrix, correlations = compute_noise_series(t, states, cfg)

    t_mid = t[1:-1]

    print("Generating visualizations...")
    plot_signal_overlay(t_mid, noise_levels, janus_matrix, cfg)
    plot_correlation_decay(noise_levels, correlations, cfg)
    plot_distribution_shift(noise_levels, janus_matrix, cfg)
    plot_noise_heatmap(t_mid, noise_levels, janus_matrix, cfg)
    write_summary(noise_levels, janus_matrix, correlations, cfg)

    print()
    print("JANUS noise robustness experiment complete")
    print(f"samples: {janus_matrix.shape[1]}")

    for noise_level, corr in zip(noise_levels, correlations):
        print(f"noise={noise_level:>7g}  corr={corr:.6f}")

    print()
    print(f"outputs saved to: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
