#!/usr/bin/env python3
"""
JANUS_OPERATOR / EXP-24
Surrogate Orientation Test

Goal:
    Test whether the aperture gate angle structure survives against
    surrogate controls.

Compares:
    - original Lorenz trajectory
    - time-shuffled surrogate
    - coordinate-shuffled surrogate
    - phase-scrambled surrogate

Outputs:
    outputs/exp24_surrogate_angle_distribution.png
    outputs/exp24_surrogate_resonance_scan.png
    outputs/exp24_surrogate_orientation_summary.txt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


Array = np.ndarray


@dataclass(frozen=True)
class OutputConfig:
    output_dir: Path = Path(__file__).resolve().parent.parent / "outputs"
    dpi: int = 220


@dataclass(frozen=True)
class ExperimentConfig:
    t_max: float = 140.0
    dt: float = 0.01
    transient_fraction: float = 0.15
    gate_quantile: float = 0.995
    memory_lag: int = 230
    seed: int = 42


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

    n_steps = int(np.floor(cfg.t_max / cfg.dt))

    t_eval = np.linspace(
        0.0,
        n_steps * cfg.dt,
        n_steps + 1,
    )

    sol = solve_ivp(
        lorenz_rhs,
        (0.0, float(t_eval[-1])),
        np.array([1.0, 1.0, 1.0], dtype=float),
        t_eval=t_eval,
        rtol=1e-9,
        atol=1e-9,
    )

    states = sol.y.T

    cut = int(len(states) * cfg.transient_fraction)

    return t_eval[cut:], states[cut:]


def normalize(v: Array) -> Array:

    n = np.linalg.norm(v, axis=1, keepdims=True)

    return v / (n + 1e-12)


def janus_signal(states: Array) -> Tuple[Array, Array]:

    fwd = np.gradient(states, axis=0)

    bwd = -fwd

    fwd_n = normalize(fwd)
    bwd_n = normalize(bwd)

    overlap = np.sum(fwd_n * bwd_n, axis=1)

    janus = 1.0 - np.abs(overlap)

    angles = np.degrees(
        np.arctan2(fwd[:, 1], fwd[:, 0])
    )

    angles = (angles + 360.0) % 180.0

    return janus, angles


def aperture_candidates(
    janus: Array,
    angles: Array,
    quantile: float,
) -> Tuple[Array, float]:

    threshold = np.quantile(janus, quantile)

    mask = janus >= threshold

    return angles[mask], threshold


def shuffled_time(states: Array, rng: np.random.Generator) -> Array:

    idx = np.arange(len(states))

    rng.shuffle(idx)

    return states[idx]


def shuffled_coordinates(
    states: Array,
    rng: np.random.Generator,
) -> Array:

    out = states.copy()

    for k in range(out.shape[1]):
        rng.shuffle(out[:, k])

    return out


def phase_scramble(
    signal: Array,
    rng: np.random.Generator,
) -> Array:

    out = np.zeros_like(signal)

    for i in range(signal.shape[1]):

        x = signal[:, i]

        fft = np.fft.rfft(x)

        mag = np.abs(fft)
        phase = np.angle(fft)

        rand_phase = rng.uniform(
            0.0,
            2.0 * np.pi,
            size=len(phase),
        )

        new_fft = mag * np.exp(1j * rand_phase)

        out[:, i] = np.fft.irfft(
            new_fft,
            n=len(x),
        )

    return out


def resonance_scan(
    gate_angles: Array,
    refs: Array,
) -> Dict[float, float]:

    results = {}

    for ref in refs:

        delta = np.abs(gate_angles - ref)

        delta = np.minimum(delta, 180.0 - delta)

        score = np.mean(np.exp(-(delta ** 2) / (2 * 8.0 ** 2)))

        results[ref] = float(score)

    return results


def analyze_dataset(
    name: str,
    states: Array,
    cfg: ExperimentConfig,
):

    janus, angles = janus_signal(states)

    gate_angles, threshold = aperture_candidates(
        janus,
        angles,
        cfg.gate_quantile,
    )

    refs = np.array([
        30,
        45,
        52,
        60,
        72,
        90,
        120,
        144,
    ])

    scan = resonance_scan(gate_angles, refs)

    return {
        "name": name,
        "janus": janus,
        "angles": angles,
        "gate_angles": gate_angles,
        "threshold": threshold,
        "scan": scan,
    }


def main():

    cfg = ExperimentConfig()
    out_cfg = OutputConfig()

    out_cfg.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    rng = np.random.default_rng(cfg.seed)

    print("\n======================================")
    print("EXP-24 — SURROGATE ORIENTATION TEST")
    print("======================================\n")

    _, states = simulate_lorenz(cfg)

    datasets = {
        "original": states,
        "time_shuffle": shuffled_time(states, rng),
        "coord_shuffle": shuffled_coordinates(states, rng),
        "phase_scramble": phase_scramble(states, rng),
    }

    analyses = []

    for name, s in datasets.items():

        analyses.append(
            analyze_dataset(name, s, cfg)
        )

    # ---------------------------------------------------------
    # FIGURE 1
    # ---------------------------------------------------------

    fig, ax = plt.subplots(figsize=(11, 6))

    bins = np.linspace(0, 180, 60)

    for a in analyses:

        ax.hist(
            a["gate_angles"],
            bins=bins,
            density=True,
            alpha=0.45,
            label=a["name"],
        )

    ax.set_title(
        "EXP-24 — Surrogate Aperture Angle Distributions"
    )

    ax.set_xlabel("angle (deg)")
    ax.set_ylabel("density")

    ax.legend()

    fig.tight_layout()

    fig.savefig(
        out_cfg.output_dir /
        "exp24_surrogate_angle_distribution.png",
        dpi=out_cfg.dpi,
    )

    plt.close(fig)

    # ---------------------------------------------------------
    # FIGURE 2
    # ---------------------------------------------------------

    fig, ax = plt.subplots(figsize=(10, 6))

    refs = list(analyses[0]["scan"].keys())

    x = np.arange(len(refs))

    width = 0.18

    for i, a in enumerate(analyses):

        vals = [a["scan"][r] for r in refs]

        ax.bar(
            x + i * width,
            vals,
            width=width,
            label=a["name"],
        )

    ax.set_xticks(
        x + width * 1.5
    )

    ax.set_xticklabels(
        [f"{r:.0f}°" for r in refs]
    )

    ax.set_ylabel("alignment score")

    ax.set_title(
        "EXP-24 — Reference Angle Resonance Scan"
    )

    ax.legend()

    fig.tight_layout()

    fig.savefig(
        out_cfg.output_dir /
        "exp24_surrogate_resonance_scan.png",
        dpi=out_cfg.dpi,
    )

    plt.close(fig)

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    lines = []

    lines.append(
        "EXP-24 — Surrogate Orientation Test"
    )

    lines.append("=" * 48)
    lines.append("")

    for a in analyses:

        lines.append(f"{a['name']}")
        lines.append("-" * 32)

        lines.append(
            f"gate count: {len(a['gate_angles'])}"
        )

        lines.append(
            f"threshold : {a['threshold']:.6f}"
        )

        best_angle = max(
            a["scan"],
            key=a["scan"].get,
        )

        lines.append(
            f"best angle: {best_angle:.3f}"
        )

        lines.append(
            f"best score: "
            f"{a['scan'][best_angle]:.6f}"
        )

        lines.append("")

    lines.append("Working interpretation:")
    lines.append(
        "- compare whether diagonal structure survives surrogate destruction"
    )

    lines.append(
        "- if original geometry differs strongly from surrogates,"
    )

    lines.append(
        "  aperture organization is less likely to be random"
    )

    summary_path = (
        out_cfg.output_dir /
        "exp24_surrogate_orientation_summary.txt"
    )

    summary_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("outputs generated:\n")

    print(
        "outputs/exp24_surrogate_angle_distribution.png"
    )

    print(
        "outputs/exp24_surrogate_resonance_scan.png"
    )

    print(
        "outputs/exp24_surrogate_orientation_summary.txt"
    )

    print("\nEXP-24 complete.\n")


if __name__ == "__main__":
    main()
