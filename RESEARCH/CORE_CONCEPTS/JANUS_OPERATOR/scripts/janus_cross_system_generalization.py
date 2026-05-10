#!/usr/bin/env python3
#JANUS_OPERATOR / Experiment 15
#Cross-System Generalization
#
#Test whether JANUS coherence extracts comparable structural signatures
#across different nonlinear dynamical systems:

#    Lorenz      -> switching-dominated
#    Rossler     -> spiral / transport-dominated
#    Halvorsen   -> fragmented / distributed

#Outputs:
 #   outputs/janus_cross_system_overview.png
 #   outputs/janus_cross_system_metrics.png
#    outputs/janus_cross_system_summary.txt


from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Tuple

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.ndimage import gaussian_filter
from scipy.stats import pearsonr


Array = np.ndarray


@dataclass(frozen=True)
class SystemConfig:
    name: str
    rhs: Callable[[float, Array], Array]
    initial_state: Tuple[float, float, float]
    t_max: float
    dt: float
    transient_fraction: float = 0.15


@dataclass(frozen=True)
class OutputConfig:
    output_dir: Path = Path(__file__).resolve().parent.parent / "outputs"
    dpi: int = 220
    bins: int = 260
    smooth_sigma: float = 2.0


def lorenz_rhs(_: float, state: Array) -> Array:
    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0

    x, y, z = state
    return np.array(
        [
            sigma * (y - x),
            x * (rho - z) - y,
            x * y - beta * z,
        ],
        dtype=float,
    )


def rossler_rhs(_: float, state: Array) -> Array:
    a = 0.2
    b = 0.2
    c = 5.7

    x, y, z = state
    return np.array(
        [
            -y - z,
            x + a * y,
            b + z * (x - c),
        ],
        dtype=float,
    )


def halvorsen_rhs(_: float, state: Array) -> Array:
    a = 1.4

    x, y, z = state
    return np.array(
        [
            -a * x - 4.0 * y - 4.0 * z - y * y,
            -a * y - 4.0 * z - 4.0 * x - z * z,
            -a * z - 4.0 * x - 4.0 * y - x * x,
        ],
        dtype=float,
    )


def simulate_system(cfg: SystemConfig) -> Tuple[Array, Array]:
    t_eval = np.arange(0.0, cfg.t_max + cfg.dt, cfg.dt)

    sol = solve_ivp(
        fun=cfg.rhs,
        t_span=(0.0, cfg.t_max),
        y0=np.array(cfg.initial_state, dtype=float),
        t_eval=t_eval,
        method="DOP853",
        rtol=1.0e-9,
        atol=1.0e-11,
    )

    if not sol.success:
        raise RuntimeError(f"{cfg.name} integration failed: {sol.message}")

    t = sol.t
    states = sol.y.T

    start = int(len(t) * cfg.transient_fraction)
    return t[start:], states[start:]


def compute_janus(t: Array, states: Array, epsilon: float = 1.0e-8) -> Array:
    dt_forward = (t[2:] - t[1:-1])[:, None]
    dt_backward = (t[1:-1] - t[:-2])[:, None]

    forward = (states[2:] - states[1:-1]) / dt_forward
    backward = (states[1:-1] - states[:-2]) / dt_backward

    overlap = forward * backward

    numerator = np.linalg.norm(overlap, axis=1)
    denominator = (
        np.linalg.norm(forward, axis=1)
        * np.linalg.norm(backward, axis=1)
        + epsilon
    )

    return numerator / denominator


def compute_curvature(states: Array, epsilon: float = 1.0e-8) -> Array:
    velocity = np.gradient(states, axis=0)
    acceleration = np.gradient(velocity, axis=0)

    cross = np.cross(velocity, acceleration)
    numerator = np.linalg.norm(cross, axis=1)
    denominator = np.linalg.norm(velocity, axis=1) ** 3 + epsilon

    return numerator / denominator


def density_field_xy(states: Array, cfg: OutputConfig) -> Tuple[Array, Array, Array]:
    x = states[:, 0]
    y = states[:, 1]

    hist, xedges, yedges = np.histogram2d(x, y, bins=cfg.bins)
    hist = gaussian_filter(hist.T, sigma=cfg.smooth_sigma)

    return hist, xedges, yedges


def normalized(values: Array) -> Array:
    v_min = np.nanmin(values)
    v_max = np.nanmax(values)
    scale = v_max - v_min
    if scale <= 0 or not np.isfinite(scale):
        return np.zeros_like(values)
    return (values - v_min) / scale


def safe_corr(a: Array, b: Array) -> float:
    n = min(len(a), len(b))
    a = a[:n]
    b = b[:n]

    mask = np.isfinite(a) & np.isfinite(b)
    if np.sum(mask) < 5:
        return float("nan")

    if np.std(a[mask]) == 0 or np.std(b[mask]) == 0:
        return float("nan")

    return float(pearsonr(a[mask], b[mask])[0])


def analyze_system(cfg: SystemConfig, out_cfg: OutputConfig) -> Dict[str, object]:
    t, states = simulate_system(cfg)

    janus = compute_janus(t, states)
    centered_states = states[1:-1]
    centered_t = t[1:-1]

    curvature = compute_curvature(centered_states)
    log_curvature = np.log10(curvature + 1.0e-8)

    hist, xedges, yedges = density_field_xy(centered_states, out_cfg)

    j_norm = normalized(janus)
    c_norm = normalized(log_curvature)

    low_janus_threshold = np.quantile(janus, 0.08)
    high_curvature_threshold = np.quantile(log_curvature, 0.92)

    low_janus_mask = janus <= low_janus_threshold
    high_curvature_mask = log_curvature >= high_curvature_threshold
    overlap_mask = low_janus_mask & high_curvature_mask

    return {
        "name": cfg.name,
        "t": centered_t,
        "states": centered_states,
        "janus": janus,
        "curvature": curvature,
        "log_curvature": log_curvature,
        "density": hist,
        "xedges": xedges,
        "yedges": yedges,
        "janus_mean": float(np.mean(janus)),
        "janus_std": float(np.std(janus)),
        "janus_min": float(np.min(janus)),
        "janus_max": float(np.max(janus)),
        "curvature_mean": float(np.mean(curvature)),
        "corr_janus_curvature": safe_corr(janus, log_curvature),
        "low_janus_count": int(np.sum(low_janus_mask)),
        "high_curvature_count": int(np.sum(high_curvature_mask)),
        "overlap_count": int(np.sum(overlap_mask)),
        "overlap_fraction": float(np.sum(overlap_mask) / max(np.sum(low_janus_mask), 1)),
        "low_janus_mask": low_janus_mask,
        "high_curvature_mask": high_curvature_mask,
        "overlap_mask": overlap_mask,
        "j_norm": j_norm,
        "c_norm": c_norm,
    }


def plot_cross_system_overview(results: Dict[str, Dict[str, object]], out_path: Path, cfg: OutputConfig) -> None:
    fig, axes = plt.subplots(
        nrows=len(results),
        ncols=4,
        figsize=(18, 4.8 * len(results)),
    )

    if len(results) == 1:
        axes = np.array([axes])

    for row, (_, result) in enumerate(results.items()):
        states = result["states"]
        janus = result["janus"]
        density = result["density"]
        xedges = result["xedges"]
        yedges = result["yedges"]
        low_mask = result["low_janus_mask"]
        high_mask = result["high_curvature_mask"]
        overlap_mask = result["overlap_mask"]

        x = states[:, 0]
        y = states[:, 1]

        ax = axes[row, 0]
        ax.plot(x, y, linewidth=0.35, alpha=0.55)
        ax.set_title(f"{result['name']} — raw dynamics")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(alpha=0.15)

        ax = axes[row, 1]
        extent = (xedges[0], xedges[-1], yedges[0], yedges[-1])
        ax.imshow(
            density,
            extent=extent,
            origin="lower",
            aspect="auto",
            cmap="viridis",
        )
        ax.set_title("Density field")
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        ax = axes[row, 2]
        sc = ax.scatter(x, y, c=janus, s=1.5, cmap="viridis", alpha=0.7)
        ax.set_title("JANUS coherence field")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        fig.colorbar(sc, ax=ax, fraction=0.045, pad=0.04)

        ax = axes[row, 3]
        ax.scatter(x, y, s=0.5, alpha=0.12, label="trajectory")
        ax.scatter(
            x[low_mask],
            y[low_mask],
            s=4,
            alpha=0.7,
            label="low JANUS",
        )
        ax.scatter(
            x[high_mask],
            y[high_mask],
            s=4,
            alpha=0.7,
            label="high curvature",
        )
        ax.scatter(
            x[overlap_mask],
            y[overlap_mask],
            s=18,
            alpha=0.9,
            label="overlap",
        )
        ax.set_title("Transition-candidate overlap")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend(loc="best", fontsize=8)
        ax.grid(alpha=0.15)

    fig.suptitle(
        "JANUS Cross-System Generalization\n"
        "Dynamics → Density → Coherence → Transition-Candidate Geometry",
        fontsize=16,
        y=0.995,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=cfg.dpi)
    plt.close(fig)


def plot_cross_system_metrics(results: Dict[str, Dict[str, object]], out_path: Path, cfg: OutputConfig) -> None:
    names = list(results.keys())

    janus_means = [results[name]["janus_mean"] for name in names]
    janus_stds = [results[name]["janus_std"] for name in names]
    corr = [results[name]["corr_janus_curvature"] for name in names]
    overlap = [results[name]["overlap_fraction"] for name in names]

    x = np.arange(len(names))

    fig, axes = plt.subplots(2, 2, figsize=(13, 8))

    axes[0, 0].bar(x, janus_means)
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(names)
    axes[0, 0].set_title("Mean JANUS coherence")
    axes[0, 0].set_ylabel("mean")

    axes[0, 1].bar(x, janus_stds)
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(names)
    axes[0, 1].set_title("JANUS coherence variance proxy")
    axes[0, 1].set_ylabel("std")

    axes[1, 0].bar(x, corr)
    axes[1, 0].axhline(0.0, linestyle="--", linewidth=1)
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(names)
    axes[1, 0].set_title("JANUS vs log-curvature correlation")
    axes[1, 0].set_ylabel("Pearson r")

    axes[1, 1].bar(x, overlap)
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(names)
    axes[1, 1].set_title("Low-JANUS / high-curvature overlap fraction")
    axes[1, 1].set_ylabel("fraction")

    for ax in axes.ravel():
        ax.grid(alpha=0.2)

    fig.suptitle("JANUS Cross-System Metrics", fontsize=16)
    fig.tight_layout()
    fig.savefig(out_path, dpi=cfg.dpi)
    plt.close(fig)


def write_summary(results: Dict[str, Dict[str, object]], out_path: Path) -> None:
    lines = []
    lines.append("JANUS cross-system generalization experiment")
    lines.append("===========================================")
    lines.append("")
    lines.append("Systems:")
    lines.append("- Lorenz: switching-dominated reference")
    lines.append("- Rossler: spiral / transport-dominated")
    lines.append("- Halvorsen: fragmented / distributed stress test")
    lines.append("")
    lines.append("")

    for name, result in results.items():
        lines.append(f"{name}")
        lines.append("-" * len(name))
        lines.append(f"samples: {len(result['janus'])}")
        lines.append(f"JANUS mean: {result['janus_mean']:.6f}")
        lines.append(f"JANUS std: {result['janus_std']:.6f}")
        lines.append(f"JANUS min: {result['janus_min']:.6f}")
        lines.append(f"JANUS max: {result['janus_max']:.6f}")
        lines.append(f"curvature mean: {result['curvature_mean']:.6f}")
        lines.append(f"JANUS vs log-curvature r: {result['corr_janus_curvature']:.6f}")
        lines.append(f"low-JANUS count: {result['low_janus_count']}")
        lines.append(f"high-curvature count: {result['high_curvature_count']}")
        lines.append(f"overlap count: {result['overlap_count']}")
        lines.append(f"overlap fraction: {result['overlap_fraction']:.6f}")
        lines.append("")

    lines.append("Interpretation:")
    lines.append("JANUS is tested here as a cross-system coherence observable.")
    lines.append("The goal is not identical visual geometry across systems.")
    lines.append("The goal is persistence of extractable transition structure.")
    lines.append("")
    lines.append("Working reading:")
    lines.append("- Lorenz should show concentrated switching corridors.")
    lines.append("- Rossler should show spiral / transport coherence.")
    lines.append("- Halvorsen should show fragmented distributed transition regions.")
    lines.append("")
    lines.append("If all three show non-random JANUS organization,")
    lines.append("JANUS is not only a Lorenz-specific observable.")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def run_experiment() -> None:
    out_cfg = OutputConfig()
    out_cfg.output_dir.mkdir(parents=True, exist_ok=True)

    systems = [
        SystemConfig(
            name="Lorenz",
            rhs=lorenz_rhs,
            initial_state=(1.0, 1.0, 1.0),
            t_max=90.0,
            dt=0.01,
        ),
        SystemConfig(
            name="Rossler",
            rhs=rossler_rhs,
            initial_state=(1.0, 0.0, 0.0),
            t_max=250.0,
            dt=0.02,
        ),
        SystemConfig(
            name="Halvorsen",
            rhs=halvorsen_rhs,
            initial_state=(1.0, 0.0, 0.0),
            t_max=80.0,
            dt=0.01,
        ),
    ]

    print("Running JANUS cross-system generalization experiment...")

    results: Dict[str, Dict[str, object]] = {}

    for system in systems:
        print(f"Analyzing {system.name}...")
        results[system.name] = analyze_system(system, out_cfg)

    plot_cross_system_overview(
        results,
        out_cfg.output_dir / "janus_cross_system_overview.png",
        out_cfg,
    )

    plot_cross_system_metrics(
        results,
        out_cfg.output_dir / "janus_cross_system_metrics.png",
        out_cfg,
    )

    write_summary(
        results,
        out_cfg.output_dir / "janus_cross_system_summary.txt",
    )

    print("")
    print("================================================")
    print("JANUS CROSS-SYSTEM GENERALIZATION")
    print("================================================")

    for name, result in results.items():
        print(f"{name}:")
        print(f"  samples: {len(result['janus'])}")
        print(f"  JANUS mean: {result['janus_mean']:.6f}")
        print(f"  JANUS std : {result['janus_std']:.6f}")
        print(f"  JANUS-curvature r: {result['corr_janus_curvature']:.6f}")
        print(f"  overlap fraction: {result['overlap_fraction']:.6f}")
        print("")

    print(f"outputs saved to: {out_cfg.output_dir.resolve()}")
    print("================================================")


if __name__ == "__main__":
    run_experiment()
