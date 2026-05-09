#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 17
Parameter Stability Scan

Goal:
    Test whether JANUS transition orientation remains stable
    under parameter variation.

Systems:
    Lorenz rho sweep
    Rossler c sweep
    Halvorsen a sweep

Outputs:
    outputs/janus_parameter_stability_scan.png
    outputs/janus_parameter_orientation_paths.png
    outputs/janus_parameter_summary.txt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Tuple

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
class SweepConfig:
    system: str
    parameter_name: str
    values: List[float]
    initial_state: Tuple[float, float, float]
    t_max: float
    dt: float
    transient_fraction: float


# ------------------------------------------------------------
# System factories
# ------------------------------------------------------------

def make_lorenz_rhs(rho: float) -> Callable[[float, Array], Array]:
    def rhs(_: float, s: Array) -> Array:
        sigma = 10.0
        beta = 8.0 / 3.0
        x, y, z = s
        return np.array([
            sigma * (y - x),
            x * (rho - z) - y,
            x * y - beta * z,
        ])
    return rhs


def make_rossler_rhs(c: float) -> Callable[[float, Array], Array]:
    def rhs(_: float, s: Array) -> Array:
        a = 0.2
        b = 0.2
        x, y, z = s
        return np.array([
            -y - z,
            x + a * y,
            b + z * (x - c),
        ])
    return rhs


def make_halvorsen_rhs(a: float) -> Callable[[float, Array], Array]:
    def rhs(_: float, s: Array) -> Array:
        x, y, z = s
        return np.array([
            -a * x - 4.0 * y - 4.0 * z - y * y,
            -a * y - 4.0 * z - 4.0 * x - z * z,
            -a * z - 4.0 * x - 4.0 * y - x * x,
        ])
    return rhs


SWEEPS = [
    SweepConfig(
        system="Lorenz",
        parameter_name="rho",
        values=[22.0, 24.0, 26.0, 28.0, 30.0, 32.0, 35.0],
        initial_state=(1.0, 1.0, 1.0),
        t_max=90.0,
        dt=0.01,
        transient_fraction=0.15,
    ),
    SweepConfig(
        system="Rossler",
        parameter_name="c",
        values=[4.5, 5.0, 5.7, 6.2, 6.8, 7.5, 8.0],
        initial_state=(0.2, 0.1, 0.1),
        t_max=150.0,
        dt=0.015,
        transient_fraction=0.15,
    ),
    SweepConfig(
        system="Halvorsen",
        parameter_name="a",
        values=[1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70],
        initial_state=(1.0, 0.0, 0.0),
        t_max=90.0,
        dt=0.01,
        transient_fraction=0.20,
    ),
]


# ------------------------------------------------------------
# Numerical core
# ------------------------------------------------------------

def rhs_for(system: str, value: float) -> Callable[[float, Array], Array]:
    if system == "Lorenz":
        return make_lorenz_rhs(value)
    if system == "Rossler":
        return make_rossler_rhs(value)
    if system == "Halvorsen":
        return make_halvorsen_rhs(value)
    raise ValueError(f"Unknown system: {system}")


def simulate_system(cfg: SweepConfig, value: float) -> Tuple[Array, Array]:
    rhs = rhs_for(cfg.system, value)

    # Important:
    # np.arange(0, t_max + dt, dt) can exceed t_span due to floating point.
    # This avoids solve_ivp t_eval errors.
    n_steps = int(np.floor(cfg.t_max / cfg.dt))
    t_eval = np.linspace(0.0, n_steps * cfg.dt, n_steps + 1)

    sol = solve_ivp(
        fun=rhs,
        t_span=(0.0, float(t_eval[-1])),
        y0=np.array(cfg.initial_state, dtype=float),
        t_eval=t_eval,
        method="DOP853",
        rtol=1.0e-10,
        atol=1.0e-12,
    )

    if not sol.success:
    print(
        f"[warning] {cfg.system} parameter={value:g} "
        f"integration unstable: {sol.message}"
    )
    return np.array([]), np.empty((0, 3))

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

    return numerator / denominator


def analyze_parameter(cfg: SweepConfig, value: float) -> Dict[str, float]:
    t, states = simulate_system(cfg, value)
if len(t) < 10 or len(states) < 10:
    return {
        "parameter": float(value),
        "samples": 0.0,
        "janus_mean": np.nan,
        "janus_std": np.nan,
        "curvature_mean": np.nan,
        "r": np.nan,
        "overlap_fraction": np.nan,
        "orientation_angle": np.nan,
    }
    _, janus = compute_janus(t, states)
    curvature = compute_curvature(states)
    curvature = curvature[: len(janus)]

    log_curv = np.log10(curvature + 1.0e-8)

    n = min(len(janus), len(log_curv))
    janus = janus[:n]
    log_curv = log_curv[:n]
    curvature = curvature[:n]

    if np.std(janus) <= 1.0e-12 or np.std(log_curv) <= 1.0e-12:
        r = 0.0
    else:
        r, _ = pearsonr(janus, log_curv)

    low_threshold = np.quantile(janus, 0.08)
    high_threshold = np.quantile(log_curv, 0.92)

    low_mask = janus <= low_threshold
    high_mask = log_curv >= high_threshold
    overlap_mask = low_mask & high_mask

    overlap_fraction = np.sum(overlap_mask) / max(np.sum(low_mask), 1)

    angle = np.degrees(np.arctan2(overlap_fraction, r))
    if angle > 180:
        angle -= 360

    return {
        "parameter": float(value),
        "samples": float(n),
        "janus_mean": float(np.mean(janus)),
        "janus_std": float(np.std(janus)),
        "curvature_mean": float(np.mean(curvature)),
        "r": float(r),
        "overlap_fraction": float(overlap_fraction),
        "orientation_angle": float(angle),
    }


# ------------------------------------------------------------
# Plotting
# ------------------------------------------------------------

def plot_stability_scan(results: Dict[str, List[Dict[str, float]]], out_path: Path, dpi: int) -> None:
    fig, axes = plt.subplots(3, 3, figsize=(16, 13))

    for row, (system, rows) in enumerate(results.items()):
        x = np.array([r["parameter"] for r in rows])
        corr = np.array([r["r"] for r in rows])
        overlap = np.array([r["overlap_fraction"] for r in rows])
        angle = np.array([r["orientation_angle"] for r in rows])

        axes[row, 0].plot(x, corr, marker="o")
        axes[row, 0].axhline(0, linestyle="--", linewidth=1.0)
        axes[row, 0].set_title(f"{system} — JANUS/curvature r")
        axes[row, 0].set_ylabel("Pearson r")
        axes[row, 0].grid(alpha=0.25)

        axes[row, 1].plot(x, overlap, marker="o")
        axes[row, 1].set_title(f"{system} — overlap fraction")
        axes[row, 1].set_ylabel("overlap")
        axes[row, 1].grid(alpha=0.25)

        axes[row, 2].plot(x, angle, marker="o")
        axes[row, 2].set_title(f"{system} — orientation angle")
        axes[row, 2].set_ylabel("degrees")
        axes[row, 2].grid(alpha=0.25)

        for col in range(3):
            axes[row, col].set_xlabel("parameter")

    fig.suptitle(
        "JANUS Parameter Stability Scan\n"
        "Testing whether transition orientation persists under parameter variation",
        fontsize=15,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_orientation_paths(results: Dict[str, List[Dict[str, float]]], out_path: Path, dpi: int) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.axhline(0, linestyle="--", linewidth=1.0)
    ax.axvline(0, linestyle="--", linewidth=1.0)

    for system, rows in results.items():
        corr = np.array([r["r"] for r in rows])
        overlap = np.array([r["overlap_fraction"] for r in rows])
        params = np.array([r["parameter"] for r in rows])

        ax.plot(corr, overlap, marker="o", linewidth=2.0, label=system)

        for i, p in enumerate(params):
            ax.text(corr[i] + 0.006, overlap[i] + 0.004, f"{p:g}", fontsize=8)

    ax.set_title("JANUS Orientation Paths Under Parameter Variation")
    ax.set_xlabel("JANUS vs log-curvature correlation r")
    ax.set_ylabel("low-JANUS / high-curvature overlap fraction")
    ax.legend()
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def write_summary(results: Dict[str, List[Dict[str, float]]], out_path: Path) -> None:
    lines = []
    lines.append("JANUS parameter stability scan")
    lines.append("================================")
    lines.append("")
    lines.append("Goal:")
    lines.append("Test whether JANUS transition orientation remains stable")
    lines.append("under system-parameter variation.")
    lines.append("")

    for system, rows in results.items():
        lines.append(system)
        lines.append("-" * len(system))

        corr = np.array([r["r"] for r in rows])
        overlap = np.array([r["overlap_fraction"] for r in rows])
        angle = np.array([r["orientation_angle"] for r in rows])

        lines.append(f"r mean: {np.mean(corr):.6f}")
        lines.append(f"r std: {np.std(corr):.6f}")
        lines.append(f"overlap mean: {np.mean(overlap):.6f}")
        lines.append(f"overlap std: {np.std(overlap):.6f}")
        lines.append(f"angle mean: {np.mean(angle):.6f}")
        lines.append(f"angle std: {np.std(angle):.6f}")
        lines.append("")

        lines.append("parameter, samples, janus_mean, janus_std, curvature_mean, r, overlap_fraction, orientation_angle")
        for row in rows:
            lines.append(
                f"{row['parameter']:.6f}, "
                f"{int(row['samples'])}, "
                f"{row['janus_mean']:.6f}, "
                f"{row['janus_std']:.6f}, "
                f"{row['curvature_mean']:.6f}, "
                f"{row['r']:.6f}, "
                f"{row['overlap_fraction']:.6f}, "
                f"{row['orientation_angle']:.6f}"
            )
        lines.append("")

    lines.append("Working interpretation:")
    lines.append("- Stable orientation paths indicate system-class persistence.")
    lines.append("- Drifting paths indicate parameter-driven regime changes.")
    lines.append("- Orientation flips indicate a structural transition in JANUS-curvature coupling.")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def run_experiment() -> None:
    output_cfg = OutputConfig()
    output_cfg.output_dir.mkdir(parents=True, exist_ok=True)

    print("Running JANUS parameter stability scan...")

    results: Dict[str, List[Dict[str, float]]] = {}

    for cfg in SWEEPS:
        print(f"Scanning {cfg.system} / {cfg.parameter_name}...")
        rows: List[Dict[str, float]] = []

        for value in cfg.values:
            print(f"  {cfg.parameter_name} = {value:g}")
            rows.append(analyze_parameter(cfg, value))

        results[cfg.system] = rows

    plot_stability_scan(
        results,
        output_cfg.output_dir / "janus_parameter_stability_scan.png",
        output_cfg.dpi,
    )
    plot_orientation_paths(
        results,
        output_cfg.output_dir / "janus_parameter_orientation_paths.png",
        output_cfg.dpi,
    )
    write_summary(
        results,
        output_cfg.output_dir / "janus_parameter_summary.txt",
    )

    print()
    print("================================================")
    print("JANUS PARAMETER STABILITY SCAN")
    print("================================================")

    for system, rows in results.items():
        corr = np.array([r["r"] for r in rows])
        overlap = np.array([r["overlap_fraction"] for r in rows])
        angle = np.array([r["orientation_angle"] for r in rows])

        print(system)
        print(f"  r mean/std       : {np.mean(corr):.6f} / {np.std(corr):.6f}")
        print(f"  overlap mean/std : {np.mean(overlap):.6f} / {np.std(overlap):.6f}")
        print(f"  angle mean/std   : {np.mean(angle):.6f} / {np.std(angle):.6f}")
        print()

    print(f"outputs saved to: {output_cfg.output_dir.resolve()}")
    print("================================================")


if __name__ == "__main__":
    run_experiment()
