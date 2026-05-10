#!/usr/bin/env python3
"""
JANUS_OPERATOR / EXP-30
Basin Intervention / Controlled Steering

Script:
    scripts_2/janus_basin_intervention_steering.py

Goal:
    Test whether JANUS basin routing can be shifted
    by controlled local aperture intervention.

Core question:
    Can a small directional bias change the predicted basin path?

Outputs:
    outputs/exp30_basin_steering_map.png
    outputs/exp30_intervention_paths.png
    outputs/exp30_control_response.png
    outputs/exp30_transport_shift_matrix.png
    outputs/exp30_intervention_summary.txt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from sklearn.cluster import KMeans


Array = np.ndarray


@dataclass(frozen=True)
class ExperimentConfig:
    t_max: float = 140.0
    dt: float = 0.01
    transient_fraction: float = 0.15
    memory_lag: int = 220
    gate_quantile: float = 0.995
    n_nodes: int = 4
    prediction_horizon: int = 40
    path_length: int = 12
    seed: int = 42

    intervention_strengths: Tuple[float, ...] = (
        -0.30, -0.15, -0.075, 0.0, 0.075, 0.15, 0.30
    )

    intervention_angle_deg: float = 45.0


@dataclass(frozen=True)
class OutputConfig:
    output_dir: Path = Path(__file__).resolve().parent.parent / "outputs"
    dpi: int = 220


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
    n_steps = int(cfg.t_max / cfg.dt)
    t_eval = np.linspace(0.0, cfg.t_max, n_steps)

    sol = solve_ivp(
        lorenz_rhs,
        (0.0, cfg.t_max),
        np.array([1.0, 1.0, 1.0]),
        t_eval=t_eval,
        rtol=1e-9,
        atol=1e-9,
    )

    states = sol.y.T
    cut = int(cfg.transient_fraction * len(states))
    return sol.t[cut:], states[cut:]


def normalize(x: Array) -> Array:
    return (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-12)


def compute_velocity(states: Array) -> Array:
    return np.gradient(states, axis=0)


def compute_curvature(velocity: Array) -> Array:
    accel = np.gradient(velocity, axis=0)
    cross = np.cross(velocity, accel)
    num = np.linalg.norm(cross, axis=1)
    den = np.linalg.norm(velocity, axis=1) ** 3 + 1e-12
    return num / den


def compute_orientation_weight(
    states: Array,
    angle_deg: float,
) -> Array:
    vel = compute_velocity(states)
    xy = vel[:, :2]

    ref = np.array([
        np.cos(np.deg2rad(angle_deg)),
        np.sin(np.deg2rad(angle_deg)),
    ])

    norms = np.linalg.norm(xy, axis=1) + 1e-12
    align = np.abs((xy @ ref) / norms)

    return normalize(align)


def compute_aperture_score(
    states: Array,
    lag: int,
    intervention_strength: float,
    intervention_angle_deg: float,
) -> Array:
    velocity = compute_velocity(states)
    curvature = normalize(compute_curvature(velocity))

    delta = np.linalg.norm(states[lag:] - states[:-lag], axis=1)
    delta = np.pad(delta, (lag, 0), mode="edge")
    delta = normalize(delta)

    orientation = compute_orientation_weight(
        states,
        intervention_angle_deg,
    )

    aperture = 0.55 * curvature + 0.45 * delta

    aperture = aperture + intervention_strength * orientation

    return normalize(aperture)


def detect_gates(aperture: Array, q: float) -> Array:
    return aperture >= np.quantile(aperture, q)


def build_nodes(
    states: Array,
    mask: Array,
    n_nodes: int,
    seed: int,
) -> Tuple[Array, Array, Array]:
    gate_points = states[mask]

    km = KMeans(
        n_clusters=n_nodes,
        random_state=seed,
        n_init=20,
    )

    labels = km.fit_predict(gate_points)
    return gate_points, labels, km.cluster_centers_


def transition_probabilities(labels: Array, horizon: int, n_nodes: int) -> Array:
    mat = np.zeros((n_nodes, n_nodes), dtype=float)

    for i in range(len(labels) - horizon):
        mat[labels[i], labels[i + horizon]] += 1.0

    rows = mat.sum(axis=1)
    probs = np.divide(
        mat,
        rows[:, None],
        out=np.zeros_like(mat),
        where=rows[:, None] != 0,
    )

    return probs


def predicted_path(
    probs: Array,
    start: int = 0,
    length: int = 12,
) -> List[int]:
    path = [start]
    current = start

    for _ in range(length):
        row = probs[current]
        if row.sum() == 0:
            break
        nxt = int(np.argmax(row))
        path.append(nxt)
        current = nxt

    return path


def matrix_shift(a: Array, b: Array) -> float:
    return float(np.linalg.norm(a - b))


def path_similarity(a: List[int], b: List[int]) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(1 for i in range(n) if a[i] == b[i]) / n


def run_single(
    states: Array,
    cfg: ExperimentConfig,
    strength: float,
) -> Dict[str, object]:
    aperture = compute_aperture_score(
        states,
        cfg.memory_lag,
        strength,
        cfg.intervention_angle_deg,
    )

    mask = detect_gates(aperture, cfg.gate_quantile)

    gate_points, labels, centers = build_nodes(
        states,
        mask,
        cfg.n_nodes,
        cfg.seed,
    )

    probs = transition_probabilities(
        labels,
        cfg.prediction_horizon,
        cfg.n_nodes,
    )

    path = predicted_path(
        probs,
        start=0,
        length=cfg.path_length,
    )

    return {
        "aperture": aperture,
        "mask": mask,
        "gate_points": gate_points,
        "labels": labels,
        "centers": centers,
        "probs": probs,
        "path": path,
    }


def plot_steering_map(
    states: Array,
    baseline: Dict[str, object],
    strongest: Dict[str, object],
    outpath: Path,
    dpi: int,
) -> None:
    plt.figure(figsize=(10, 8))

    plt.scatter(
        states[:, 0],
        states[:, 2],
        s=1,
        alpha=0.05,
        color="gray",
    )

    base_points = baseline["gate_points"]
    steer_points = strongest["gate_points"]

    plt.scatter(
        base_points[:, 0],
        base_points[:, 2],
        s=30,
        alpha=0.8,
        label="baseline gates",
    )

    plt.scatter(
        steer_points[:, 0],
        steer_points[:, 2],
        s=30,
        alpha=0.8,
        label="intervened gates",
    )

    plt.axvline(0, linestyle="--", alpha=0.4)

    plt.title("EXP-30 — Basin Steering Map")
    plt.xlabel("x")
    plt.ylabel("z")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=dpi)
    plt.close()


def plot_intervention_paths(
    results: Dict[float, Dict[str, object]],
    outpath: Path,
    dpi: int,
) -> None:
    strengths = list(results.keys())
    paths = [results[s]["path"] for s in strengths]

    max_len = max(len(p) for p in paths)
    mat = np.full((len(paths), max_len), -1.0)

    for i, path in enumerate(paths):
        mat[i, :len(path)] = path

    plt.figure(figsize=(10, 6))
    plt.imshow(mat, aspect="auto")
    plt.colorbar(label="predicted node")
    plt.yticks(range(len(strengths)), [f"{s:+.3f}" for s in strengths])
    plt.xlabel("prediction step")
    plt.ylabel("intervention strength")
    plt.title("EXP-30 — Intervention Path Shift")
    plt.tight_layout()
    plt.savefig(outpath, dpi=dpi)
    plt.close()


def plot_control_response(
    strengths: List[float],
    shifts: List[float],
    similarities: List[float],
    outpath: Path,
    dpi: int,
) -> None:
    plt.figure(figsize=(9, 6))
    plt.plot(strengths, shifts, marker="o", label="matrix shift")
    plt.plot(strengths, similarities, marker="o", label="path similarity")
    plt.axvline(0, linestyle="--", alpha=0.4)
    plt.xlabel("intervention strength")
    plt.ylabel("value")
    plt.title("EXP-30 — Control Response")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=dpi)
    plt.close()


def plot_transport_shift_matrix(
    baseline_probs: Array,
    strongest_probs: Array,
    outpath: Path,
    dpi: int,
) -> None:
    diff = strongest_probs - baseline_probs

    plt.figure(figsize=(8, 6))
    plt.imshow(diff, aspect="auto")
    plt.colorbar(label="probability shift")
    plt.xlabel("to node")
    plt.ylabel("from node")
    plt.title("EXP-30 — Transport Shift Matrix")
    plt.tight_layout()
    plt.savefig(outpath, dpi=dpi)
    plt.close()


def write_summary(
    results: Dict[float, Dict[str, object]],
    shifts: List[float],
    similarities: List[float],
    cfg: ExperimentConfig,
    outpath: Path,
) -> None:
    lines = []

    lines.append("EXP-30 — Basin Intervention / Controlled Steering")
    lines.append("=" * 56)
    lines.append("")
    lines.append("Goal:")
    lines.append("Test whether JANUS aperture routing can be shifted through controlled directional bias.")
    lines.append("")
    lines.append(f"intervention angle: {cfg.intervention_angle_deg:.3f} deg")
    lines.append("")

    baseline_path = results[0.0]["path"]
    lines.append(f"baseline path: {baseline_path}")
    lines.append("")

    for idx, (strength, data) in enumerate(results.items()):
        lines.append(f"intervention strength: {strength:+.3f}")
        lines.append("-" * 36)
        lines.append(f"path: {data['path']}")
        lines.append(f"path similarity to baseline: {similarities[idx]:.6f}")
        lines.append(f"matrix shift from baseline: {shifts[idx]:.6f}")
        lines.append("transition probability matrix:")
        for row in data["probs"]:
            lines.append("  " + " ".join(f"{v:.3f}" for v in row))
        lines.append("")

    lines.append("Working interpretation:")
    lines.append("- if small directional bias changes routing, gates are steerable")
    lines.append("- stable paths indicate rigid transport corridors")
    lines.append("- path flips indicate intervention-sensitive decision zones")
    lines.append("- this is an exploratory control diagnostic, not proof of control theory")
    lines.append("")
    lines.append("Exploratory only.")

    outpath.write_text("\n".join(lines))


def main() -> None:
    cfg = ExperimentConfig()
    outcfg = OutputConfig()
    outcfg.output_dir.mkdir(parents=True, exist_ok=True)

    print()
    print("=" * 56)
    print("EXP-30 — BASIN INTERVENTION / CONTROLLED STEERING")
    print("=" * 56)
    print()

    _, states = simulate_lorenz(cfg)

    results: Dict[float, Dict[str, object]] = {}

    for strength in cfg.intervention_strengths:
        print(f"running intervention strength {strength:+.3f}...")
        results[strength] = run_single(states, cfg, strength)

    baseline = results[0.0]
    baseline_probs = baseline["probs"]
    baseline_path = baseline["path"]

    strengths = list(results.keys())

    shifts = [
        matrix_shift(baseline_probs, results[s]["probs"])
        for s in strengths
    ]

    similarities = [
        path_similarity(baseline_path, results[s]["path"])
        for s in strengths
    ]

    strongest_strength = strengths[int(np.argmax(shifts))]
    strongest = results[strongest_strength]

    plot_steering_map(
        states,
        baseline,
        strongest,
        outcfg.output_dir / "exp30_basin_steering_map.png",
        outcfg.dpi,
    )

    plot_intervention_paths(
        results,
        outcfg.output_dir / "exp30_intervention_paths.png",
        outcfg.dpi,
    )

    plot_control_response(
        strengths,
        shifts,
        similarities,
        outcfg.output_dir / "exp30_control_response.png",
        outcfg.dpi,
    )

    plot_transport_shift_matrix(
        baseline_probs,
        strongest["probs"],
        outcfg.output_dir / "exp30_transport_shift_matrix.png",
        outcfg.dpi,
    )

    write_summary(
        results,
        shifts,
        similarities,
        cfg,
        outcfg.output_dir / "exp30_intervention_summary.txt",
    )

    print()
    print("outputs generated:")
    print("outputs/exp30_basin_steering_map.png")
    print("outputs/exp30_intervention_paths.png")
    print("outputs/exp30_control_response.png")
    print("outputs/exp30_transport_shift_matrix.png")
    print("outputs/exp30_intervention_summary.txt")
    print()
    print("EXP-30 complete.")
    print()


if __name__ == "__main__":
    main()
