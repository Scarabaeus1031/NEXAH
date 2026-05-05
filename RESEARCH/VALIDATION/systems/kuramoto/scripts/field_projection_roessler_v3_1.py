#!/usr/bin/env python3
"""
field_projection_roessler_v3.py

NEXAH FIELD_LAYER — EXPERIMENTAL BUILD V3
Rössler system field projection experiment.

Pipeline:
1. Simulate Rössler trajectory
2. Align trajectory with PCA basis
3. Compute phase theta = arctan2(gamma, beta)
4. Compute phase drift delta_theta
5. Classify regimes: Theta / Tao / Dao / Iota
6. Detect Iota events via peak detection on |delta_theta|
7. Export comparable CSV, plots, and JSON summary

No symbolic interpretation. Data, structure, and measurable dynamics only.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks
from sklearn.decomposition import PCA


@dataclass(frozen=True)
class RoesslerConfig:
    a: float = 0.2
    b: float = 0.2
    c: float = 5.7
    t_max: float = 500.0
    dt: float = 0.01
    initial_state: Tuple[float, float, float] = (1.0, 0.0, 0.0)
    transient_fraction: float = 0.1
    iota_quantile: float = 0.92
    peak_distance: int = 50
    peak_prominence_quantile: float = 0.75
    output_dir: str = "outputs/roessler_v3"
    random_seed: int = 42


def roessler_rhs(_t: float, state: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
    """Rössler system right-hand side."""
    x, y, z = state
    dx = -y - z
    dy = x + a * y
    dz = b + z * (x - c)
    return np.array([dx, dy, dz], dtype=float)


def simulate_roessler(config: RoesslerConfig) -> Tuple[np.ndarray, np.ndarray]:
    """Simulate the Rössler system and return time array and state matrix."""
    t_eval = np.arange(0.0, config.t_max + config.dt, config.dt)

    sol = solve_ivp(
        roessler_rhs,
        t_span=(0.0, config.t_max),
        y0=np.array(config.initial_state, dtype=float),
        t_eval=t_eval,
        args=(config.a, config.b, config.c),
        method="DOP853",
        rtol=1e-10,
        atol=1e-12,
    )

    if not sol.success:
        raise RuntimeError(f"Rössler integration failed: {sol.message}")

    states = sol.y.T
    return sol.t, states


def remove_transient(
    t: np.ndarray,
    states: np.ndarray,
    transient_fraction: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """Remove initial transient segment from trajectory."""
    if not 0.0 <= transient_fraction < 1.0:
        raise ValueError("transient_fraction must be in [0, 1).")

    start_idx = int(len(t) * transient_fraction)
    return t[start_idx:], states[start_idx:]


def pca_project(states: np.ndarray) -> Tuple[np.ndarray, PCA]:
    """
    Center trajectory and project onto PCA basis.

    Returns projected coordinates columns:
    alpha = PC1, beta = PC2, gamma = PC3
    """
    pca = PCA(n_components=3)
    projected = pca.fit_transform(states)
    return projected, pca


def compute_phase(projected: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute theta and phase drift from PCA projected coordinates."""
    alpha = projected[:, 0]
    beta = projected[:, 1]
    gamma = projected[:, 2]

    theta = np.unwrap(np.arctan2(gamma, beta))
    delta_theta = np.diff(theta, prepend=theta[0])

    return theta, delta_theta, alpha


def classify_regimes(
    delta_theta: np.ndarray,
    iota_quantile: float,
) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Classify phase drift into four regimes using distribution thresholds.

    Theta: near-zero drift
    Tao: positive moderate drift
    Dao: negative moderate drift
    Iota: high absolute drift events
    """
    abs_drift = np.abs(delta_theta)

    theta_threshold = float(np.quantile(abs_drift, 0.35))
    iota_threshold = float(np.quantile(abs_drift, iota_quantile))

    regimes = np.full(delta_theta.shape, "Theta", dtype=object)
    regimes[(abs_drift > theta_threshold) & (delta_theta > 0)] = "Tao"
    regimes[(abs_drift > theta_threshold) & (delta_theta < 0)] = "Dao"
    regimes[abs_drift >= iota_threshold] = "Iota"

    thresholds = {
        "theta_threshold_abs_delta": theta_threshold,
        "iota_threshold_abs_delta": iota_threshold,
        "iota_quantile": iota_quantile,
    }
    return regimes, thresholds


def detect_iota_events(
    delta_theta: np.ndarray,
    iota_threshold: float,
    peak_distance: int,
    peak_prominence_quantile: float,
) -> np.ndarray:
    """Detect Iota events as peaks in absolute phase drift."""
    abs_drift = np.abs(delta_theta)
    prominence = float(np.quantile(abs_drift, peak_prominence_quantile))

    peaks, _properties = find_peaks(
        abs_drift,
        height=iota_threshold,
        distance=peak_distance,
        prominence=prominence,
    )
    return peaks


def build_dataframe(
    t: np.ndarray,
    states: np.ndarray,
    projected: np.ndarray,
    theta: np.ndarray,
    delta_theta: np.ndarray,
    regimes: np.ndarray,
    iota_peaks: np.ndarray,
) -> pd.DataFrame:
    """Build comparable output dataframe."""
    df = pd.DataFrame(
        {
            "t": t,
            "x": states[:, 0],
            "y": states[:, 1],
            "z": states[:, 2],
            "alpha": projected[:, 0],
            "beta": projected[:, 1],
            "gamma": projected[:, 2],
            "theta": theta,
            "delta_theta": delta_theta,
            "abs_delta_theta": np.abs(delta_theta),
            "regime": regimes,
            "is_iota_event": False,
        }
    )

    df.loc[iota_peaks, "is_iota_event"] = True
    return df


def summarize(
    df: pd.DataFrame,
    pca: PCA,
    thresholds: Dict[str, float],
    config: RoesslerConfig,
) -> Dict[str, object]:
    """Compute compact experiment summary."""
    regime_counts = df["regime"].value_counts().to_dict()
    regime_distribution = (df["regime"].value_counts(normalize=True) * 100.0).to_dict()

    iota_event_count = int(df["is_iota_event"].sum())
    transition_rate = float(iota_event_count / len(df))

    summary = {
        "system": "roessler",
        "config": asdict(config),
        "samples": int(len(df)),
        "time_start": float(df["t"].iloc[0]),
        "time_end": float(df["t"].iloc[-1]),
        "pca_explained_variance_ratio": [float(v) for v in pca.explained_variance_ratio_],
        "thresholds": thresholds,
        "regime_counts": {k: int(v) for k, v in regime_counts.items()},
        "regime_distribution_percent": {k: float(v) for k, v in regime_distribution.items()},
        "iota_event_count": iota_event_count,
        "transition_rate": transition_rate,
        "delta_theta_mean": float(df["delta_theta"].mean()),
        "delta_theta_std": float(df["delta_theta"].std()),
        "abs_delta_theta_mean": float(df["abs_delta_theta"].mean()),
        "abs_delta_theta_std": float(df["abs_delta_theta"].std()),
    }
    return summary


def save_plots(df: pd.DataFrame, output_dir: Path) -> None:
    """Save standard plots for comparison across systems."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 3D PCA trajectory
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(df["alpha"], df["beta"], df["gamma"], linewidth=0.4)
    ax.set_title("Rössler V3 — PCA Field Projection")
    ax.set_xlabel("alpha / PC1")
    ax.set_ylabel("beta / PC2")
    ax.set_zlabel("gamma / PC3")
    fig.tight_layout()
    fig.savefig(output_dir / "roessler_v3_pca_projection.png", dpi=180)
    plt.close(fig)

    # Phase drift over time with Iota events
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["t"], df["delta_theta"], linewidth=0.5, label="delta_theta")
    events = df[df["is_iota_event"]]
    ax.scatter(events["t"], events["delta_theta"], s=12, label="Iota events")
    ax.set_title("Rössler V3 — Phase Drift and Iota Events")
    ax.set_xlabel("t")
    ax.set_ylabel("delta_theta")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(output_dir / "roessler_v3_phase_drift_iota.png", dpi=180)
    plt.close(fig)

    # Regime distribution
    fig, ax = plt.subplots(figsize=(7, 5))
    order = ["Theta", "Tao", "Dao", "Iota"]
    counts = df["regime"].value_counts().reindex(order, fill_value=0)
    ax.bar(counts.index, counts.values)
    ax.set_title("Rössler V3 — Regime Distribution")
    ax.set_xlabel("Regime")
    ax.set_ylabel("Samples")
    fig.tight_layout()
    fig.savefig(output_dir / "roessler_v3_regime_distribution.png", dpi=180)
    plt.close(fig)

    # Absolute phase drift histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["abs_delta_theta"], bins=120)
    ax.set_title("Rössler V3 — Absolute Phase Drift Distribution")
    ax.set_xlabel("abs(delta_theta)")
    ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(output_dir / "roessler_v3_abs_phase_drift_histogram.png", dpi=180)
    plt.close(fig)


def extract_iota_event_windows(df: pd.DataFrame, window: int = 100) -> pd.DataFrame:
    """Extract local windows around each Iota peak for fine-structure analysis."""
    events = df[df["is_iota_event"]].copy()
    records = []

    for idx in events.index:
        start = max(0, idx - window)
        end = min(len(df) - 1, idx + window)

        segment = df.iloc[start:end+1]

        record = {
            "event_index": int(idx),
            "t_peak": float(df.loc[idx, "t"]),
            "delta_theta_peak": float(df.loc[idx, "delta_theta"]),
            "abs_delta_theta_peak": float(df.loc[idx, "abs_delta_theta"]),
            "pre_window_mean": float(df.iloc[start:idx]["abs_delta_theta"].mean() if idx > start else 0.0),
            "post_window_mean": float(df.iloc[idx:end]["abs_delta_theta"].mean() if idx < end else 0.0),
            "local_density": float(segment["abs_delta_theta"].mean()),
            "cluster_width": int(end - start),
            "return_time_to_next_event": None
        }

        records.append(record)

    # compute return times
    for i in range(len(records) - 1):
        records[i]["return_time_to_next_event"] = records[i+1]["t_peak"] - records[i]["t_peak"]

    return pd.DataFrame(records)


def run_experiment(config: RoesslerConfig) -> Dict[str, object]:
    """Run full Rössler FIELD_LAYER V3 experiment."""
    np.random.seed(config.random_seed)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    t_raw, states_raw = simulate_roessler(config)
    t, states = remove_transient(t_raw, states_raw, config.transient_fraction)

    projected, pca = pca_project(states)
    theta, delta_theta, _alpha = compute_phase(projected)
    regimes, thresholds = classify_regimes(delta_theta, config.iota_quantile)
    iota_peaks = detect_iota_events(
        delta_theta=delta_theta,
        iota_threshold=thresholds["iota_threshold_abs_delta"],
        peak_distance=config.peak_distance,
        peak_prominence_quantile=config.peak_prominence_quantile,
    )

    df = build_dataframe(t, states, projected, theta, delta_theta, regimes, iota_peaks)
    summary = summarize(df, pca, thresholds, config)

    df.to_csv(output_dir / "roessler_v3_field_projection.csv", index=False)

    # Iota event windows (fine structure)
    iota_windows_df = extract_iota_event_windows(df)
    iota_windows_df.to_csv(output_dir / "roessler_v3_iota_event_windows.csv", index=False)
    with open(output_dir / "roessler_v3_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    save_plots(df, output_dir)

    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rössler FIELD_LAYER V3 experiment")
    parser.add_argument("--a", type=float, default=0.2)
    parser.add_argument("--b", type=float, default=0.2)
    parser.add_argument("--c", type=float, default=5.7)
    parser.add_argument("--t-max", type=float, default=500.0)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--x0", type=float, default=1.0)
    parser.add_argument("--y0", type=float, default=0.0)
    parser.add_argument("--z0", type=float, default=0.0)
    parser.add_argument("--transient-fraction", type=float, default=0.1)
    parser.add_argument("--iota-quantile", type=float, default=0.92)
    parser.add_argument("--peak-distance", type=int, default=50)
    parser.add_argument("--peak-prominence-quantile", type=float, default=0.75)
    parser.add_argument("--output-dir", type=str, default="outputs/roessler_v3")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = RoesslerConfig(
        a=args.a,
        b=args.b,
        c=args.c,
        t_max=args.t_max,
        dt=args.dt,
        initial_state=(args.x0, args.y0, args.z0),
        transient_fraction=args.transient_fraction,
        iota_quantile=args.iota_quantile,
        peak_distance=args.peak_distance,
        peak_prominence_quantile=args.peak_prominence_quantile,
        output_dir=args.output_dir,
    )

    summary = run_experiment(config)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
