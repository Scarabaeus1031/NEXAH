#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 03
Janus Switching Prediction

Purpose
-------
Investigate whether local Janus coherence changes
before Lorenz lobe switching events.

Core question:

    Does directional coherence weaken
    prior to lobe transitions?

This experiment is exploratory and computational.
It does not claim a new physical law.

Outputs
-------
EXPERIMENTAL/BUILDER_LAB/JANUS_OPERATOR/outputs/
    janus_switching_timeseries.png
    janus_switching_events.png
    janus_switching_phase_overlay.png
    janus_switching_distribution.png
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


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

    transient_fraction: float = 0.12

    epsilon: float = 1.0e-8

    switch_window: int = 180
    smoothing_window: int = 35

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
# Switching analysis
# -----------------------------------------------------------------------------



def detect_switches(states: Array) -> Array:
    """
    Detect lobe switching via sign changes in x.
    """
    x = states[:, 0]

    signs = np.sign(x)

    switch_idx = np.where(signs[:-1] != signs[1:])[0]

    return switch_idx



def moving_average(values: Array, window: int) -> Array:
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode="same")



def extract_switch_windows(
    janus: Array,
    switch_idx: Array,
    cfg: Config,
) -> Array:
    segments = []

    for idx in switch_idx:
        start = idx - cfg.switch_window
        end = idx + cfg.switch_window

        if start < 0 or end >= len(janus):
            continue

        segment = janus[start:end]
        segments.append(segment)

    return np.array(segments)


# -----------------------------------------------------------------------------
# Visualizations
# -----------------------------------------------------------------------------



def plot_timeseries(
    t: Array,
    janus: Array,
    switch_idx: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(14, 5))

    smoothed = moving_average(janus, cfg.smoothing_window)

    ax.plot(t, janus, linewidth=0.5, alpha=0.25, label="raw Janus")
    ax.plot(t, smoothed, linewidth=1.5, label="smoothed Janus")

    for idx in switch_idx:
        ax.axvline(t[idx], alpha=0.18)

    ax.set_title("Janus Coherence Across Lorenz Switching Events")
    ax.set_xlabel("time")
    ax.set_ylabel("Janus coherence")
    ax.grid(alpha=0.18)
    ax.legend()

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_switching_timeseries.png",
        dpi=cfg.dpi,
    )

    plt.close(fig)



def plot_switch_events(
    segments: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))

    center = cfg.switch_window

    for segment in segments:
        ax.plot(segment, alpha=0.08, linewidth=0.7)

    mean_segment = np.mean(segments, axis=0)

    ax.plot(
        mean_segment,
        linewidth=3,
        label="mean switching profile",
    )

    ax.axvline(center, linestyle="--", alpha=0.6, label="switch event")

    ax.set_title("Average Janus Profile Around Switching")
    ax.set_xlabel("relative time index")
    ax.set_ylabel("Janus coherence")
    ax.grid(alpha=0.18)
    ax.legend()

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_switching_events.png",
        dpi=cfg.dpi,
    )

    plt.close(fig)



def plot_phase_overlay(
    states: Array,
    janus: Array,
    switch_idx: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 7))

    x = states[:, 0]
    y = states[:, 1]

    ax.plot(x, y, linewidth=0.35, alpha=0.18)

    low_mask = janus < np.quantile(janus, 0.08)

    ax.scatter(
        x[low_mask],
        y[low_mask],
        s=3,
        alpha=0.45,
        label="lowest 8% Janus",
    )

    ax.scatter(
        x[switch_idx],
        y[switch_idx],
        s=18,
        alpha=0.8,
        label="switch events",
    )

    ax.set_title("Switch Events vs Low-Janus Regions")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(alpha=0.18)
    ax.legend()

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_switching_phase_overlay.png",
        dpi=cfg.dpi,
    )

    plt.close(fig)



def plot_distribution(
    janus: Array,
    switch_idx: Array,
    cfg: Config,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 6))

    switch_values = janus[switch_idx]

    ax.hist(
        janus,
        bins=120,
        alpha=0.45,
        density=True,
        label="global Janus",
    )

    ax.hist(
        switch_values,
        bins=60,
        alpha=0.65,
        density=True,
        label="switch-event Janus",
    )

    ax.set_title("Janus Distribution at Switching Events")
    ax.set_xlabel("Janus coherence")
    ax.set_ylabel("density")
    ax.grid(alpha=0.18)
    ax.legend()

    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "janus_switching_distribution.png",
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

    print("Detecting switching events...")
    switch_idx = detect_switches(states_mid)

    print("Extracting switching windows...")
    segments = extract_switch_windows(janus, switch_idx, cfg)

    print("Generating visualizations...")

    plot_timeseries(t_mid, janus, switch_idx, cfg)
    plot_switch_events(segments, cfg)
    plot_phase_overlay(states_mid, janus, switch_idx, cfg)
    plot_distribution(janus, switch_idx, cfg)

    switch_values = janus[switch_idx]

    print()
    print("JANUS switching experiment complete")
    print(f"samples: {len(janus)}")
    print(f"switch events: {len(switch_idx)}")
    print(f"global mean: {np.mean(janus):.6f}")
    print(f"switch mean: {np.mean(switch_values):.6f}")
    print(f"global q05: {np.quantile(janus, 0.05):.6f}")
    print(f"switch q05: {np.quantile(switch_values, 0.05):.6f}")
    print()
    print(f"outputs saved to: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
