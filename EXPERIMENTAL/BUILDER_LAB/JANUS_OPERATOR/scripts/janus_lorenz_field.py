#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 01
Janus Lorenz Field

Exploratory directional coherence analysis for the Lorenz system.

Pipeline:
    Lorenz trajectory
    -> forward and backward finite-difference vectors
    -> local Janus overlap
    -> normalized Janus coherence intensity
    -> visual diagnostics

This script is computational and diagnostic. It does not claim a new physical
law or a finalized mathematical theory.

Outputs:
    outputs/janus_lorenz_heatmap.png
    outputs/janus_lorenz_overlay.png
    outputs/janus_lorenz_vectorfield.png
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy.integrate import solve_ivp
from scipy.interpolate import griddata


Array = np.ndarray


@dataclass(frozen=True)
class LorenzConfig:
    """Numerical configuration for the Lorenz experiment."""

    sigma: float = 10.0
    rho: float = 28.0
    beta: float = 8.0 / 3.0
    t_min: float = 0.0
    t_max: float = 80.0
    dt: float = 0.01
    initial_state: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    transient_fraction: float = 0.15
    epsilon: float = 1.0e-8
    random_seed: int = 7


@dataclass(frozen=True)
class OutputConfig:
    """Output paths and plotting configuration."""

    output_dir: Path = Path("outputs")
    dpi: int = 220
    grid_size: int = 360
    vector_stride: int = 40
    max_vector_points: int = 1800


@dataclass(frozen=True)
class JanusResult:
    """Computed trajectory and Janus coherence fields."""

    t: Array
    states: Array
    forward: Array
    backward: Array
    janus_overlap: Array
    janus_intensity: Array


def lorenz_rhs(_: float, state: Array, cfg: LorenzConfig) -> Array:
    """Lorenz system right-hand side."""
    x, y, z = state
    dx = cfg.sigma * (y - x)
    dy = x * (cfg.rho - z) - y
    dz = x * y - cfg.beta * z
    return np.array([dx, dy, dz], dtype=float)


def simulate_lorenz(cfg: LorenzConfig) -> Tuple[Array, Array]:
    """Integrate the Lorenz system and remove an initial transient."""
    np.random.seed(cfg.random_seed)

    t_eval = np.arange(cfg.t_min, cfg.t_max + cfg.dt, cfg.dt)
    solution = solve_ivp(
        fun=lambda t, y: lorenz_rhs(t, y, cfg),
        t_span=(cfg.t_min, cfg.t_max),
        y0=np.array(cfg.initial_state, dtype=float),
        t_eval=t_eval,
        method="DOP853",
        rtol=1.0e-10,
        atol=1.0e-12,
    )

    if not solution.success:
        raise RuntimeError(f"Lorenz integration failed: {solution.message}")

    states = solution.y.T
    t = solution.t

    start = int(len(t) * cfg.transient_fraction)
    return t[start:], states[start:]


def compute_janus_fields(t: Array, states: Array, cfg: LorenzConfig) -> JanusResult:
    """
    Compute forward/backward finite-difference vectors and normalized Janus
    coherence intensity.

    The Janus overlap is implemented as component-wise multiplication:
        J_op(x) = F_forward(x) * F_backward(x)

    The normalized intensity is:
        J(x) = ||J_op(x)|| / (||F_forward|| ||F_backward|| + epsilon)
    """
    if states.ndim != 2 or states.shape[1] != 3:
        raise ValueError("states must have shape (n_samples, 3)")
    if len(t) != len(states):
        raise ValueError("t and states must have the same length")
    if len(states) < 3:
        raise ValueError("at least three trajectory samples are required")

    dt_forward = (t[2:] - t[1:-1])[:, None]
    dt_backward = (t[1:-1] - t[:-2])[:, None]

    centered_t = t[1:-1]
    centered_states = states[1:-1]

    forward = (states[2:] - states[1:-1]) / dt_forward
    backward = (states[1:-1] - states[:-2]) / dt_backward

    janus_overlap = forward * backward
    numerator = np.linalg.norm(janus_overlap, axis=1)
    denominator = (
        np.linalg.norm(forward, axis=1)
        * np.linalg.norm(backward, axis=1)
        + cfg.epsilon
    )
    janus_intensity = numerator / denominator

    return JanusResult(
        t=centered_t,
        states=centered_states,
        forward=forward,
        backward=backward,
        janus_overlap=janus_overlap,
        janus_intensity=janus_intensity,
    )


def normalized(values: Array) -> Array:
    """Normalize values to [0, 1] for plotting."""
    v_min = np.nanmin(values)
    v_max = np.nanmax(values)
    scale = v_max - v_min
    if scale <= 0 or not np.isfinite(scale):
        return np.zeros_like(values)
    return (values - v_min) / scale


def make_colored_line_xy(states: Array, values: Array) -> LineCollection:
    """Build an XY trajectory line colored by scalar values."""
    xy = states[:, :2]
    points = xy.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    line = LineCollection(segments, cmap="viridis", linewidth=0.45, alpha=0.95)
    line.set_array(values[:-1])
    return line


def plot_janus_heatmap(result: JanusResult, out_path: Path, cfg: OutputConfig) -> None:
    """Save an interpolated XY heatmap of Janus coherence intensity."""
    x = result.states[:, 0]
    y = result.states[:, 1]
    j = result.janus_intensity

    xi = np.linspace(np.percentile(x, 1), np.percentile(x, 99), cfg.grid_size)
    yi = np.linspace(np.percentile(y, 1), np.percentile(y, 99), cfg.grid_size)
    grid_x, grid_y = np.meshgrid(xi, yi)

    grid_j = griddata(
        points=np.column_stack([x, y]),
        values=j,
        xi=(grid_x, grid_y),
        method="linear",
    )

    fig, ax = plt.subplots(figsize=(9.5, 7.5))
    image = ax.imshow(
        grid_j,
        extent=(xi.min(), xi.max(), yi.min(), yi.max()),
        origin="lower",
        aspect="auto",
        cmap="viridis",
    )
    ax.scatter(x[::15], y[::15], c=j[::15], s=0.2, cmap="viridis", alpha=0.35)

    cbar = fig.colorbar(image, ax=ax, fraction=0.045, pad=0.04)
    cbar.set_label("Normalized Janus coherence J(x)")

    ax.set_title("Janus Lorenz Field — XY Coherence Heatmap")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(out_path, dpi=cfg.dpi)
    plt.close(fig)


def plot_janus_overlay(result: JanusResult, out_path: Path, cfg: OutputConfig) -> None:
    """Save XY trajectory colored by Janus intensity."""
    fig, ax = plt.subplots(figsize=(9.5, 7.5))

    line = make_colored_line_xy(result.states, result.janus_intensity)
    ax.add_collection(line)
    ax.autoscale()

    low_threshold = np.quantile(result.janus_intensity, 0.08)
    low_mask = result.janus_intensity <= low_threshold
    ax.scatter(
        result.states[low_mask, 0],
        result.states[low_mask, 1],
        s=2.5,
        c="black",
        alpha=0.45,
        label="lowest 8% J(x)",
    )

    cbar = fig.colorbar(line, ax=ax, fraction=0.045, pad=0.04)
    cbar.set_label("Normalized Janus coherence J(x)")

    ax.set_title("Janus Lorenz Field — Trajectory Overlay")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper right", frameon=True)
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(out_path, dpi=cfg.dpi)
    plt.close(fig)


def plot_janus_vectorfield(result: JanusResult, out_path: Path, cfg: OutputConfig) -> None:
    """Save a sparse XY vector-field view with Janus coloring."""
    n = len(result.states)
    stride = max(cfg.vector_stride, n // cfg.max_vector_points)
    idx = np.arange(0, n, stride)

    x = result.states[idx, 0]
    y = result.states[idx, 1]
    u = result.forward[idx, 0]
    v = result.forward[idx, 1]
    j = result.janus_intensity[idx]

    speed = np.sqrt(u**2 + v**2)
    speed = np.where(speed == 0, 1.0, speed)
    u_norm = u / speed
    v_norm = v / speed

    fig, ax = plt.subplots(figsize=(9.5, 7.5))
    q = ax.quiver(
        x,
        y,
        u_norm,
        v_norm,
        j,
        cmap="viridis",
        angles="xy",
        scale_units="xy",
        scale=0.55,
        width=0.0022,
        alpha=0.85,
    )

    ax.scatter(
        result.states[::20, 0],
        result.states[::20, 1],
        s=0.15,
        c=normalized(result.janus_intensity[::20]),
        cmap="viridis",
        alpha=0.25,
    )

    cbar = fig.colorbar(q, ax=ax, fraction=0.045, pad=0.04)
    cbar.set_label("Normalized Janus coherence J(x)")

    ax.set_title("Janus Lorenz Field — Forward Direction Vectors")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(alpha=0.18)

    fig.tight_layout()
    fig.savefig(out_path, dpi=cfg.dpi)
    plt.close(fig)


def print_summary(result: JanusResult) -> None:
    """Print concise numerical diagnostics."""
    j = result.janus_intensity
    print("JANUS Lorenz experiment complete")
    print(f"samples: {len(j)}")
    print(f"J min:   {np.min(j):.6f}")
    print(f"J mean:  {np.mean(j):.6f}")
    print(f"J max:   {np.max(j):.6f}")
    print(f"J q05:   {np.quantile(j, 0.05):.6f}")
    print(f"J q50:   {np.quantile(j, 0.50):.6f}")
    print(f"J q95:   {np.quantile(j, 0.95):.6f}")


def run_experiment() -> None:
    """Run the full Janus Lorenz experiment and save all outputs."""
    lorenz_cfg = LorenzConfig()
    output_cfg = OutputConfig()
    output_cfg.output_dir.mkdir(parents=True, exist_ok=True)

    t, states = simulate_lorenz(lorenz_cfg)
    result = compute_janus_fields(t, states, lorenz_cfg)

    plot_janus_heatmap(
        result,
        output_cfg.output_dir / "janus_lorenz_heatmap.png",
        output_cfg,
    )
    plot_janus_overlay(
        result,
        output_cfg.output_dir / "janus_lorenz_overlay.png",
        output_cfg,
    )
    plot_janus_vectorfield(
        result,
        output_cfg.output_dir / "janus_lorenz_vectorfield.png",
        output_cfg,
    )

    print_summary(result)
    print(f"outputs saved to: {output_cfg.output_dir.resolve()}")


if __name__ == "__main__":
    run_experiment()
