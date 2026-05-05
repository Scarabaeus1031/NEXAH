#!/usr/bin/env python3
"""
field_projection_kuramoto_v3.py

NEXAH FIELD_LAYER — EXPERIMENTAL BUILD V3
Kuramoto oscillator network field projection experiment.

Comparable V3 pipeline:
1. Simulate Kuramoto oscillator phases
2. Compute order parameter r(t) and mean phase psi(t)
3. Build 3D observable state: [r, dr/dt, dpsi/dt]
4. PCA projection: alpha, beta, gamma
5. Phase theta = arctan2(gamma, beta)
6. Phase drift delta_theta
7. Regime classification: Theta / Tao / Dao / Iota
8. Iota peak detection on |delta_theta|
9. Iota event window extraction
10. Export CSV, plots, and JSON summary

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
class KuramotoConfig:
    n_oscillators: int = 128
    coupling_k: float = 1.8
    omega_mean: float = 0.0
    omega_std: float = 1.0
    t_max: float = 500.0
    dt: float = 0.01
    transient_fraction: float = 0.1
    iota_quantile: float = 0.92
    peak_distance: int = 50
    peak_prominence_quantile: float = 0.75
    iota_window: int = 100
    output_dir: str | None = None
    random_seed: int = 42


def kuramoto_rhs(_t: float, phases: np.ndarray, omega: np.ndarray, coupling_k: float) -> np.ndarray:
    """All-to-all Kuramoto model using order-parameter form."""
    z = np.mean(np.exp(1j * phases))
    r = np.abs(z)
    psi = np.angle(z)
    return omega + coupling_k * r * np.sin(psi - phases)


def simulate_kuramoto(config: KuramotoConfig) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Simulate Kuramoto phases and return time, phases, and frequencies."""
    rng = np.random.default_rng(config.random_seed)
    omega = rng.normal(config.omega_mean, config.omega_std, config.n_oscillators)
    omega = omega - omega.mean()
    initial_phases = rng.uniform(-np.pi, np.pi, config.n_oscillators)

    t_eval = np.arange(0.0, config.t_max + config.dt, config.dt)

    sol = solve_ivp(
        kuramoto_rhs,
        t_span=(0.0, config.t_max),
        y0=initial_phases,
        t_eval=t_eval,
        args=(omega, config.coupling_k),
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
    )

    if not sol.success:
        raise RuntimeError(f"Kuramoto integration failed: {sol.message}")

    phases = sol.y.T
    phases = np.mod(phases + np.pi, 2.0 * np.pi) - np.pi
    return sol.t, phases, omega


def remove_transient(
    t: np.ndarray,
    phases: np.ndarray,
    transient_fraction: float,
) -> Tuple[np.ndarray, np.ndarray]:
    """Remove initial transient segment."""
    if not 0.0 <= transient_fraction < 1.0:
        raise ValueError("transient_fraction must be in [0, 1).")
    start_idx = int(len(t) * transient_fraction)
    return t[start_idx:], phases[start_idx:]


def compute_order_parameter(phases: np.ndarray, dt: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Compute r(t), psi(t), dr/dt, and dpsi/dt."""
    z = np.mean(np.exp(1j * phases), axis=1)
    r = np.abs(z)
    psi = np.unwrap(np.angle(z))
    dr_dt = np.gradient(r, dt)
    dpsi_dt = np.gradient(psi, dt)
    return r, psi, dr_dt, dpsi_dt


def build_observable_state(r: np.ndarray, dr_dt: np.ndarray, dpsi_dt: np.ndarray) -> np.ndarray:
    """Build 3D observable state for PCA projection."""
    return np.column_stack([r, dr_dt, dpsi_dt])


def pca_project(states: np.ndarray) -> Tuple[np.ndarray, PCA]:
    """Center observable state and project onto PCA basis."""
    pca = PCA(n_components=3)
    projected = pca.fit_transform(states)
    return projected, pca


def compute_phase(projected: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Compute theta and phase drift from PCA projected coordinates."""
    beta = projected[:, 1]
    gamma = projected[:, 2]
    theta = np.unwrap(np.arctan2(gamma, beta))
    delta_theta = np.diff(theta, prepend=theta[0])
    return theta, delta_theta


def classify_regimes(
    delta_theta: np.ndarray,
    iota_quantile: float,
) -> Tuple[np.ndarray, Dict[str, float]]:
    """Classify phase drift into Theta / Tao / Dao / Iota regimes."""
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
    r: np.ndarray,
    psi: np.ndarray,
    dr_dt: np.ndarray,
    dpsi_dt: np.ndarray,
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
            "r": r,
            "psi": psi,
            "dr_dt": dr_dt,
            "dpsi_dt": dpsi_dt,
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


def extract_iota_event_windows(df: pd.DataFrame, window: int = 100) -> pd.DataFrame:
    """Extract local windows around each Iota peak for fine-structure analysis."""
    events = df[df["is_iota_event"]].copy()
    records = []

    for idx in events.index:
        start = max(0, idx - window)
        end = min(len(df) - 1, idx + window)
        segment = df.iloc[start:end + 1]

        record = {
            "event_index": int(idx),
            "t_peak": float(df.loc[idx, "t"]),
            "r_peak": float(df.loc[idx, "r"]),
            "dr_dt_peak": float(df.loc[idx, "dr_dt"]),
            "dpsi_dt_peak": float(df.loc[idx, "dpsi_dt"]),
            "delta_theta_peak": float(df.loc[idx, "delta_theta"]),
            "abs_delta_theta_peak": float(df.loc[idx, "abs_delta_theta"]),
            "pre_window_mean": float(df.iloc[start:idx]["abs_delta_theta"].mean() if idx > start else 0.0),
            "post_window_mean": float(df.iloc[idx:end]["abs_delta_theta"].mean() if idx < end else 0.0),
            "local_density": float(segment["abs_delta_theta"].mean()),
            "cluster_width": int(end - start),
            "return_time_to_next_event": None,
        }
        records.append(record)

    for i in range(len(records) - 1):
        records[i]["return_time_to_next_event"] = records[i + 1]["t_peak"] - records[i]["t_peak"]

    return pd.DataFrame(records)


def summarize(
    df: pd.DataFrame,
    iota_windows_df: pd.DataFrame,
    pca: PCA,
    omega: np.ndarray,
    thresholds: Dict[str, float],
    config: KuramotoConfig,
) -> Dict[str, object]:
    """Compute compact experiment summary."""
    regime_counts = df["regime"].value_counts().to_dict()
    regime_distribution = (df["regime"].value_counts(normalize=True) * 100.0).to_dict()
    iota_event_count = int(df["is_iota_event"].sum())
    transition_rate = float(iota_event_count / len(df))

    return {
        "system": "kuramoto",
        "config": asdict(config),
        "samples": int(len(df)),
        "time_start": float(df["t"].iloc[0]),
        "time_end": float(df["t"].iloc[-1]),
        "omega_mean_actual": float(omega.mean()),
        "omega_std_actual": float(omega.std()),
        "r_mean": float(df["r"].mean()),
        "r_std": float(df["r"].std()),
        "r_min": float(df["r"].min()),
        "r_max": float(df["r"].max()),
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
        "iota_window_local_density_mean": float(iota_windows_df["local_density"].mean()) if len(iota_windows_df) else 0.0,
        "iota_return_time_mean": float(iota_windows_df["return_time_to_next_event"].dropna().mean()) if len(iota_windows_df) > 1 else 0.0,
        "iota_return_time_std": float(iota_windows_df["return_time_to_next_event"].dropna().std()) if len(iota_windows_df) > 2 else 0.0,
    }


def save_plots(df: pd.DataFrame, output_dir: Path) -> None:
    """Save standard plots for comparison across systems."""
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df["t"], df["r"], linewidth=0.7)
    ax.set_title("Kuramoto V3 — Synchronization Signal r(t)")
    ax.set_xlabel("t")
    ax.set_ylabel("r")
    fig.tight_layout()
    fig.savefig(output_dir / "kuramoto_v3_order_parameter.png", dpi=180)
    plt.close(fig)

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(df["alpha"], df["beta"], df["gamma"], linewidth=0.35)
    ax.set_title("Kuramoto V3 — PCA Field Projection")
    ax.set_xlabel("alpha / PC1")
    ax.set_ylabel("beta / PC2")
    ax.set_zlabel("gamma / PC3")
    fig.tight_layout()
    fig.savefig(output_dir / "kuramoto_v3_pca_projection.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["t"], df["delta_theta"], linewidth=0.5, label="delta_theta")
    events = df[df["is_iota_event"]]
    ax.scatter(events["t"], events["delta_theta"], s=12, label="Iota events")
    ax.set_title("Kuramoto V3 — Phase Drift and Iota Events")
    ax.set_xlabel("t")
    ax.set_ylabel("delta_theta")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(output_dir / "kuramoto_v3_phase_drift_iota.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    order = ["Theta", "Tao", "Dao", "Iota"]
    counts = df["regime"].value_counts().reindex(order, fill_value=0)
    ax.bar(counts.index, counts.values)
    ax.set_title("Kuramoto V3 — Regime Distribution")
    ax.set_xlabel("Regime")
    ax.set_ylabel("Samples")
    fig.tight_layout()
    fig.savefig(output_dir / "kuramoto_v3_regime_distribution.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["abs_delta_theta"], bins=120)
    ax.set_title("Kuramoto V3 — Absolute Phase Drift Distribution")
    ax.set_xlabel("abs(delta_theta)")
    ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(output_dir / "kuramoto_v3_abs_phase_drift_histogram.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(df["r"], df["dr_dt"], s=2, alpha=0.35)
    ax.set_title("Kuramoto V3 — Slice Projection: r vs dr/dt")
    ax.set_xlabel("r")
    ax.set_ylabel("dr/dt")
    fig.tight_layout()
    fig.savefig(output_dir / "kuramoto_v3_slice_r_dr_dt.png", dpi=180)
    plt.close(fig)


def run_experiment(config: KuramotoConfig) -> Dict[str, object]:
    """Run full Kuramoto FIELD_LAYER V3 experiment."""
    base_dir = Path(__file__).parent / "outputs" / "kuramoto_v3"

    # unique run folder
    run_id = f"K_{config.coupling_k:.3f}".replace(".", "_")

    output_dir = base_dir / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    
    t_raw, phases_raw, omega = simulate_kuramoto(config)
    t, phases = remove_transient(t_raw, phases_raw, config.transient_fraction)

    r, psi, dr_dt, dpsi_dt = compute_order_parameter(phases, config.dt)
    states = build_observable_state(r, dr_dt, dpsi_dt)

    projected, pca = pca_project(states)
    theta, delta_theta = compute_phase(projected)
    regimes, thresholds = classify_regimes(delta_theta, config.iota_quantile)
    iota_peaks = detect_iota_events(
        delta_theta=delta_theta,
        iota_threshold=thresholds["iota_threshold_abs_delta"],
        peak_distance=config.peak_distance,
        peak_prominence_quantile=config.peak_prominence_quantile,
    )

    df = build_dataframe(t, r, psi, dr_dt, dpsi_dt, projected, theta, delta_theta, regimes, iota_peaks)
    iota_windows_df = extract_iota_event_windows(df, window=config.iota_window)
    summary = summarize(df, iota_windows_df, pca, omega, thresholds, config)

    df.to_csv(output_dir / "kuramoto_v3_field_projection.csv", index=False)
    iota_windows_df.to_csv(output_dir / "kuramoto_v3_iota_event_windows.csv", index=False)
    with open(output_dir / "kuramoto_v3_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    save_plots(df, output_dir)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Kuramoto FIELD_LAYER V3 experiment")
    parser.add_argument("--n-oscillators", type=int, default=128)
    parser.add_argument("--coupling-k", type=float, default=1.8)
    parser.add_argument("--omega-mean", type=float, default=0.0)
    parser.add_argument("--omega-std", type=float, default=1.0)
    parser.add_argument("--t-max", type=float, default=500.0)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--transient-fraction", type=float, default=0.1)
    parser.add_argument("--iota-quantile", type=float, default=0.92)
    parser.add_argument("--peak-distance", type=int, default=50)
    parser.add_argument("--peak-prominence-quantile", type=float, default=0.75)
    parser.add_argument("--iota-window", type=int, default=100)
    parser.add_argument("--output-dir", type=str, default="outputs/kuramoto_v3")
    parser.add_argument("--random-seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = KuramotoConfig(
        n_oscillators=args.n_oscillators,
        coupling_k=args.coupling_k,
        omega_mean=args.omega_mean,
        omega_std=args.omega_std,
        t_max=args.t_max,
        dt=args.dt,
        transient_fraction=args.transient_fraction,
        iota_quantile=args.iota_quantile,
        peak_distance=args.peak_distance,
        peak_prominence_quantile=args.peak_prominence_quantile,
        iota_window=args.iota_window,
        output_dir=args.output_dir,
        random_seed=args.random_seed,
    )

    summary = run_experiment(config)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
