#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 10
Janus Attractor Memory

Purpose
-------
Test whether JANUS coherence contains temporal persistence,
delayed self-similarity, recurrence structure, or attractor-memory traces.

Core question:

    Does JANUS only react locally,
    or does it preserve long-range dynamical memory?

Outputs
-------
EXPERIMENTAL/BUILDER_LAB/JANUS_OPERATOR/outputs/
    janus_recurrence_matrix.png
    janus_delayed_correlation.png
    janus_memory_decay.png
    janus_memory_trace.png
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.ndimage import gaussian_filter1d
from scipy.spatial.distance import pdist, squareform


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
    t_max: float = 120.0
    dt: float = 0.01

    transient_fraction: float = 0.15
    epsilon: float = 1.0e-8

    smoothing_sigma: float = 3.0
    recurrence_threshold: float = 0.035
    max_lag: int = 1600

    memory_windows: tuple[int, ...] = (50, 100, 200, 400, 800, 1200)

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
# JANUS coherence
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
# Memory / recurrence analysis
# -----------------------------------------------------------------------------


def build_delay_embedding(signal: Array) -> Array:
    return np.column_stack(
        [
            signal[:-2],
            signal[1:-1],
            signal[2:],
        ]
    )


def compute_recurrence_matrix(signal: Array, cfg: Config) -> Array:
    embedded = build_delay_embedding(signal)

    distances = squareform(
        pdist(
            embedded,
            metric="euclidean",
        )
    )

    recurrence = distances < cfg.recurrence_threshold

    return recurrence.astype(float)


def delayed_self_correlation(signal: Array, cfg: Config) -> tuple[Array, Array]:
    lags = np.arange(1, cfg.max_lag + 1)
    corrs = []

    for lag in lags:
        a = signal[:-lag]
        b = signal[lag:]

        r = np.corrcoef(a, b)[0, 1]
        corrs.append(r)

    return lags, np.array(corrs)


def memory_variance_decay(
    signal: Array,
    cfg: Config,
) -> tuple[Array, Array]:
    windows = np.array(cfg.memory_windows)
    variances = []

    for window in windows:
        kernel = np.ones(window) / window

        rolling = np.convolve(
            signal,
            kernel,
            mode="valid",
        )

        variances.append(np.var(rolling))

    return windows, np.array(variances)


# -----------------------------------------------------------------------------
# Visualizations
# -----------------------------------------------------------------------------


def plot_recurrence_matrix(
    recurrence: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 10))

    image = ax.imshow(
        recurrence,
        origin="lower",
        aspect="auto",
        cmap="magma",
    )

    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label("recurrence")

    ax.set_title("JANUS Recurrence Matrix")
    ax.set_xlabel("time")
    ax.set_ylabel("time")

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_recurrence_matrix.png",
        dpi=cfg.dpi,
    )
    plt.close(fig)


def plot_delayed_correlation(
    lags: Array,
    corrs: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(
        lags,
        corrs,
        linewidth=1.8,
    )

    ax.axhline(
        0,
        linestyle="--",
        alpha=0.55,
    )

    peak_idx = np.argmax(corrs[10:]) + 10
    peak_lag = lags[peak_idx]
    peak_corr = corrs[peak_idx]

    ax.axvline(
        peak_lag,
        linestyle="--",
        alpha=0.75,
    )

    ax.set_title(
        "JANUS Delayed Self-Correlation\n"
        f"peak lag = {peak_lag}, peak corr = {peak_corr:.4f}"
    )
    ax.set_xlabel("lag")
    ax.set_ylabel("correlation")
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_delayed_correlation.png",
        dpi=cfg.dpi,
    )
    plt.close(fig)


def plot_memory_decay(
    windows: Array,
    variances: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        windows,
        variances,
        marker="o",
        linewidth=2.0,
    )

    ax.set_title("JANUS Memory Persistence")
    ax.set_xlabel("window size")
    ax.set_ylabel("rolling-mean variance")
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_memory_decay.png",
        dpi=cfg.dpi,
    )
    plt.close(fig)


def plot_memory_trace(
    t: Array,
    signal: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(16, 5))

    max_points = min(len(signal), 4500)

    ax.plot(
        t[:max_points],
        signal[:max_points],
        linewidth=1.0,
    )

    ax.set_title("JANUS Memory Trace")
    ax.set_xlabel("time")
    ax.set_ylabel("smoothed JANUS coherence")
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_memory_trace.png",
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

    print("Computing JANUS coherence...")
    t_mid, _, janus = compute_janus(t, states, cfg)

    janus_smooth = gaussian_filter1d(
        janus,
        sigma=cfg.smoothing_sigma,
    )

    print("Computing recurrence matrix...")
    recurrence = compute_recurrence_matrix(
        janus_smooth,
        cfg,
    )

    print("Computing delayed self-correlation...")
    lags, corrs = delayed_self_correlation(
        janus_smooth,
        cfg,
    )

    print("Computing memory variance decay...")
    windows, variances = memory_variance_decay(
        janus_smooth,
        cfg,
    )

    print("Generating visualizations...")
    plot_recurrence_matrix(recurrence, cfg)
    plot_delayed_correlation(lags, corrs, cfg)
    plot_memory_decay(windows, variances, cfg)
    plot_memory_trace(t_mid, janus_smooth, cfg)

    peak_idx = np.argmax(corrs[10:]) + 10
    peak_lag = lags[peak_idx]
    peak_corr = corrs[peak_idx]

    print()
    print("JANUS attractor memory experiment complete")
    print(f"samples: {len(janus_smooth)}")
    print(f"peak delayed corr: {peak_corr:.6f}")
    print(f"peak lag: {peak_lag}")
    print()
    print("memory variance decay:")

    for window, variance in zip(windows, variances):
        print(f"window={window:4d} variance={variance:.6f}")

    print()
    print(f"outputs saved to: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
