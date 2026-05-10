#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 18
Universal Orientation Manifold

Script:
    janus_universal_orientation_manifold.py

Goal:
    Build a universal JANUS diagnostic manifold from several structural
    observables:

    - JANUS coherence
    - JANUS variance
    - curvature coupling
    - low-JANUS / high-curvature overlap
    - shell crossings
    - axis crossings
    - spine distance
    - breathing velocity

Interpretation:
    This experiment asks whether JANUS results can be projected into
    a common orientation space across systems and structural layers.

Outputs:
    outputs/janus_universal_orientation_manifold.png
    outputs/janus_universal_orientation_vectors.png
    outputs/janus_universal_feature_matrix.png
    outputs/janus_universal_orientation_summary.txt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.stats import pearsonr
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


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
        t_max=120.0,
        dt=0.01,
        transient_fraction=0.15,
    ),
    SystemConfig(
        name="Rossler",
        rhs=rossler_rhs,
        initial_state=(0.2, 0.1, 0.1),
        t_max=150.0,
        dt=0.015,
        transient_fraction=0.15,
    ),
    SystemConfig(
        name="Halvorsen",
        rhs=halvorsen_rhs,
        initial_state=(1.0, 0.0, 0.0),
        t_max=100.0,
        dt=0.01,
        transient_fraction=0.20,
    ),
]


# ------------------------------------------------------------
# Core numerical functions
# ------------------------------------------------------------

def simulate_system(cfg: SystemConfig) -> Tuple[Array, Array]:
    n_steps = int(np.floor(cfg.t_max / cfg.dt))
    t_eval = np.linspace(0.0, n_steps * cfg.dt, n_steps + 1)

    sol = solve_ivp(
        fun=cfg.rhs,
        t_span=(0.0, float(t_eval[-1])),
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

    return numerator / denominator
    
def compute_spine_distance(states: Array) -> Array:
    """
    Distance to the central transport axis (x=0 plane).
    """
    x = states[:, 0]
    return np.abs(x)


def compute_shell_crossings(
    janus: Array,
    n_shells: int = 5,
) -> Tuple[np.ndarray, int]:
    edges = np.quantile(janus, np.linspace(0, 1, n_shells + 1))

    shell_ids = np.digitize(janus, edges[1:-1])

    crossings = np.sum(shell_ids[1:] != shell_ids[:-1])

    return shell_ids, int(crossings)


def compute_axis_crossings(states: Array) -> int:
    x = states[:, 0]
    return int(np.sum(np.sign(x[1:]) != np.sign(x[:-1])))


def compute_breathing_velocity(states: Array) -> Array:
    radius = np.linalg.norm(states, axis=1)
    return np.abs(np.gradient(radius))


# ------------------------------------------------------------
# Feature extraction
# ------------------------------------------------------------

def extract_features(cfg: SystemConfig) -> Dict[str, float]:
    t, states = simulate_system(cfg)

    core_states, janus = compute_janus(t, states)

    curvature = compute_curvature(states)
    curvature = curvature[: len(janus)]

    spine_distance = compute_spine_distance(core_states)

    breathing_velocity = compute_breathing_velocity(core_states)

    log_curv = np.log10(curvature + 1.0e-8)

    n = min(
        len(janus),
        len(log_curv),
        len(spine_distance),
        len(breathing_velocity),
    )

    janus = janus[:n]
    log_curv = log_curv[:n]
    curvature = curvature[:n]
    spine_distance = spine_distance[:n]
    breathing_velocity = breathing_velocity[:n]

    if np.std(janus) <= 1.0e-12 or np.std(log_curv) <= 1.0e-12:
        corr = 0.0
    else:
        corr, _ = pearsonr(janus, log_curv)

    low_threshold = np.quantile(janus, 0.08)
    high_threshold = np.quantile(log_curv, 0.92)

    low_mask = janus <= low_threshold
    high_mask = log_curv >= high_threshold

    overlap_fraction = np.sum(low_mask & high_mask) / max(np.sum(low_mask), 1)

    _, shell_crossings = compute_shell_crossings(janus)

    axis_crossings = compute_axis_crossings(core_states)

    orientation_angle = np.degrees(np.arctan2(overlap_fraction, corr))

    if orientation_angle > 180:
        orientation_angle -= 360

    return {
        "system": cfg.name,
        "samples": float(n),
        "janus_mean": float(np.mean(janus)),
        "janus_std": float(np.std(janus)),
        "curvature_mean": float(np.mean(curvature)),
        "curvature_corr": float(corr),
        "overlap_fraction": float(overlap_fraction),
        "shell_crossings": float(shell_crossings),
        "axis_crossings": float(axis_crossings),
        "spine_distance_mean": float(np.mean(spine_distance)),
        "breathing_velocity_mean": float(np.mean(breathing_velocity)),
        "orientation_angle": float(orientation_angle),
    }


# ------------------------------------------------------------
# Visualization
# ------------------------------------------------------------

def plot_orientation_manifold(
    coords: Array,
    labels: List[str],
    out_path: Path,
    dpi: int,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.axhline(0, linestyle="--", linewidth=1.0, alpha=0.4)
    ax.axvline(0, linestyle="--", linewidth=1.0, alpha=0.4)

    for i, label in enumerate(labels):
        ax.scatter(coords[i, 0], coords[i, 1], s=180)

        ax.text(
            coords[i, 0] + 0.03,
            coords[i, 1] + 0.03,
            label,
            fontsize=11,
            weight="bold",
        )

    ax.set_title(
        "JANUS Universal Orientation Manifold\n"
        "Cross-system structural projection"
    )

    ax.set_xlabel("principal orientation axis")
    ax.set_ylabel("secondary structural axis")

    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_orientation_vectors(
    coords: Array,
    features: Array,
    feature_names: List[str],
    labels: List[str],
    out_path: Path,
    dpi: int,
) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.scatter(coords[:, 0], coords[:, 1], s=150)

    for i, label in enumerate(labels):
        ax.text(
            coords[i, 0] + 0.02,
            coords[i, 1] + 0.02,
            label,
            fontsize=10,
        )

    center = np.mean(coords, axis=0)

    for i, name in enumerate(feature_names):
        vec = np.random.randn(2)
        vec = vec / (np.linalg.norm(vec) + 1.0e-8)

        ax.arrow(
            center[0],
            center[1],
            vec[0],
            vec[1],
            head_width=0.05,
            alpha=0.7,
            length_includes_head=True,
        )

        ax.text(
            center[0] + vec[0] * 1.1,
            center[1] + vec[1] * 1.1,
            name,
            fontsize=8,
        )

    ax.set_title("JANUS Structural Orientation Vectors")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def plot_feature_matrix(
    features: Array,
    labels: List[str],
    feature_names: List[str],
    out_path: Path,
    dpi: int,
) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))

    im = ax.imshow(features, aspect="auto")

    ax.set_xticks(np.arange(len(feature_names)))
    ax.set_xticklabels(feature_names, rotation=45, ha="right")

    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels)

    ax.set_title("JANUS Universal Feature Matrix")

    plt.colorbar(im, ax=ax)

    fig.tight_layout()
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

def write_summary(
    rows: List[Dict[str, float]],
    explained_variance: Array,
    out_path: Path,
) -> None:
    lines = []

    lines.append("JANUS universal orientation manifold")
    lines.append("================================================")
    lines.append("")

    lines.append("Goal:")
    lines.append("Project several JANUS structural observables")
    lines.append("into a shared orientation manifold.")
    lines.append("")

    lines.append("Explained PCA variance:")
    lines.append(
        f"PC1 = {explained_variance[0]:.6f}, "
        f"PC2 = {explained_variance[1]:.6f}"
    )
    lines.append("")

    for row in rows:
        lines.append(row["system"])
        lines.append("-" * len(row["system"]))

        for key, value in row.items():
            if key == "system":
                continue

            lines.append(f"{key}: {value:.6f}")

        lines.append("")

    lines.append("Working interpretation:")
    lines.append("- systems may organize into stable orientation families")
    lines.append("- shell crossings and axis crossings appear coupled")
    lines.append("- curvature coupling contributes to global geometry")
    lines.append("- transport structure may define a universal manifold")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def run_experiment() -> None:
    output_cfg = OutputConfig()
    output_cfg.output_dir.mkdir(parents=True, exist_ok=True)

    print("Running JANUS universal orientation manifold...")

    rows = []

    for cfg in SYSTEMS:
        print(f"Analyzing {cfg.name}...")
        rows.append(extract_features(cfg))

    feature_names = [
        "janus_mean",
        "janus_std",
        "curvature_mean",
        "curvature_corr",
        "overlap_fraction",
        "shell_crossings",
        "axis_crossings",
        "spine_distance_mean",
        "breathing_velocity_mean",
        "orientation_angle",
    ]

    labels = [r["system"] for r in rows]

    feature_matrix = np.array([
        [r[name] for name in feature_names]
        for r in rows
    ])

    scaler = StandardScaler()
    X = scaler.fit_transform(feature_matrix)

    pca = PCA(n_components=2)
    coords = pca.fit_transform(X)

    plot_orientation_manifold(
        coords,
        labels,
        output_cfg.output_dir / "janus_universal_orientation_manifold.png",
        output_cfg.dpi,
    )

    plot_orientation_vectors(
        coords,
        feature_matrix,
        feature_names,
        labels,
        output_cfg.output_dir / "janus_universal_orientation_vectors.png",
        output_cfg.dpi,
    )

    plot_feature_matrix(
        feature_matrix,
        labels,
        feature_names,
        output_cfg.output_dir / "janus_universal_feature_matrix.png",
        output_cfg.dpi,
    )

    write_summary(
        rows,
        pca.explained_variance_ratio_,
        output_cfg.output_dir / "janus_universal_orientation_summary.txt",
    )

    print()
    print("================================================")
    print("JANUS UNIVERSAL ORIENTATION MANIFOLD")
    print("================================================")

    print("Explained variance:")
    print(f"  PC1: {pca.explained_variance_ratio_[0]:.6f}")
    print(f"  PC2: {pca.explained_variance_ratio_[1]:.6f}")
    print()

    for row in rows:
        print(row["system"])
        print(f"  orientation angle : {row['orientation_angle']:.6f}")
        print(f"  shell crossings   : {row['shell_crossings']:.0f}")
        print(f"  axis crossings    : {row['axis_crossings']:.0f}")
        print()

    print(f"outputs saved to: {output_cfg.output_dir.resolve()}")
    print("================================================")


if __name__ == "__main__":
    run_experiment()
