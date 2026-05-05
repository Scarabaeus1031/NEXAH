#!/usr/bin/env python3
"""
kuramoto_master_v6.py

NEXAH FIELD_LAYER — Kuramoto Master Experiment V6

Includes:
- Kuramoto simulation
- PCA field projection
- phase drift
- adaptive Iota detection
- finite-time Lyapunov estimate with renormalized perturbation
- K sweep
- phase boundary extraction
- plots
- optional GIF

Outputs are written to a unique run folder:
outputs/kuramoto_v6/master_runs/run_<timestamp>/
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path

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
    random_seed: int = 42
    iota_sigma: float = 2.5
    theta_sigma: float = 0.5
    peak_distance: int = 50
    lyapunov_eps: float = 1e-7
    lyapunov_segment_time: float = 1.0


def kuramoto_rhs(_t, phases, omega, k):
    z = np.mean(np.exp(1j * phases))
    r = np.abs(z)
    psi = np.angle(z)
    return omega + k * r * np.sin(psi - phases)


def circular_difference(a, b):
    return np.angle(np.exp(1j * (a - b)))


def simulate(config: KuramotoConfig):
    rng = np.random.default_rng(config.random_seed)

    omega = rng.normal(config.omega_mean, config.omega_std, config.n_oscillators)
    omega -= omega.mean()

    phases0 = rng.uniform(-np.pi, np.pi, config.n_oscillators)

    t_eval = np.arange(0.0, config.t_max + config.dt, config.dt)

    sol = solve_ivp(
        kuramoto_rhs,
        (0.0, config.t_max),
        phases0,
        t_eval=t_eval,
        args=(omega, config.coupling_k),
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
    )

    if not sol.success:
        raise RuntimeError(sol.message)

    phases = np.mod(sol.y.T + np.pi, 2.0 * np.pi) - np.pi

    return sol.t, phases, omega


def estimate_lyapunov(config: KuramotoConfig):
    rng = np.random.default_rng(config.random_seed)

    omega = rng.normal(config.omega_mean, config.omega_std, config.n_oscillators)
    omega -= omega.mean()

    x = rng.uniform(-np.pi, np.pi, config.n_oscillators)
    perturb = rng.normal(size=config.n_oscillators)
    perturb /= np.linalg.norm(perturb)

    y = x + config.lyapunov_eps * perturb

    t = 0.0
    log_growth = []
    times = []

    n_segments = int(config.t_max / config.lyapunov_segment_time)

    for _ in range(n_segments):
        t_next = t + config.lyapunov_segment_time

        sol_x = solve_ivp(
            kuramoto_rhs,
            (t, t_next),
            x,
            args=(omega, config.coupling_k),
            method="DOP853",
            rtol=1e-9,
            atol=1e-11,
        )

        sol_y = solve_ivp(
            kuramoto_rhs,
            (t, t_next),
            y,
            args=(omega, config.coupling_k),
            method="DOP853",
            rtol=1e-9,
            atol=1e-11,
        )

        x = sol_x.y[:, -1]
        y = sol_y.y[:, -1]

        delta = circular_difference(y, x)
        dist = np.linalg.norm(delta)
        dist = max(dist, 1e-15)

        growth = np.log(dist / config.lyapunov_eps)
        log_growth.append(growth)

        delta = delta / dist * config.lyapunov_eps
        y = x + delta

        t = t_next
        times.append(t)

    lyap = float(np.sum(log_growth) / config.t_max)

    return lyap, np.array(times), np.cumsum(log_growth) / np.array(times)


def run_single(config: KuramotoConfig, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    t, phases, omega = simulate(config)

    cut = int(len(t) * config.transient_fraction)
    t = t[cut:]
    phases = phases[cut:]

    z = np.mean(np.exp(1j * phases), axis=1)
    r = np.abs(z)
    psi = np.unwrap(np.angle(z))

    dr_dt = np.gradient(r, config.dt)
    dpsi_dt = np.gradient(psi, config.dt)

    state = np.column_stack([r, dr_dt, dpsi_dt])

    pca = PCA(n_components=3)
    projected = pca.fit_transform(state)

    alpha = projected[:, 0]
    beta = projected[:, 1]
    gamma = projected[:, 2]

    theta = np.unwrap(np.arctan2(gamma, beta))
    delta_theta = np.diff(theta, prepend=theta[0])
    abs_delta_theta = np.abs(delta_theta)

    mean_abs = float(abs_delta_theta.mean())
    std_abs = float(abs_delta_theta.std())

    theta_threshold = mean_abs + config.theta_sigma * std_abs
    iota_threshold = mean_abs + config.iota_sigma * std_abs

    regimes = np.full(len(abs_delta_theta), "Theta", dtype=object)
    regimes[(abs_delta_theta > theta_threshold) & (delta_theta > 0)] = "Tao"
    regimes[(abs_delta_theta > theta_threshold) & (delta_theta < 0)] = "Dao"
    regimes[abs_delta_theta >= iota_threshold] = "Iota"

    peaks, _ = find_peaks(
        abs_delta_theta,
        height=iota_threshold,
        distance=config.peak_distance,
    )

    lyapunov, lyap_t, lyap_curve = estimate_lyapunov(config)

    df = pd.DataFrame({
        "t": t,
        "r": r,
        "psi": psi,
        "dr_dt": dr_dt,
        "dpsi_dt": dpsi_dt,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "theta": theta,
        "delta_theta": delta_theta,
        "abs_delta_theta": abs_delta_theta,
        "regime": regimes,
        "is_iota_event": False,
    })
    df.loc[peaks, "is_iota_event"] = True
    df.to_csv(output_dir / "data.csv", index=False)

    lyap_df = pd.DataFrame({
        "t": lyap_t,
        "lyapunov_running_estimate": lyap_curve,
    })
    lyap_df.to_csv(output_dir / "lyapunov_curve.csv", index=False)

    summary = {
        "config": asdict(config),
        "K": config.coupling_k,
        "samples": int(len(df)),
        "r_mean": float(r.mean()),
        "r_std": float(r.std()),
        "r_min": float(r.min()),
        "r_max": float(r.max()),
        "abs_delta_theta_mean": mean_abs,
        "abs_delta_theta_std": std_abs,
        "theta_threshold": float(theta_threshold),
        "iota_threshold": float(iota_threshold),
        "iota_percent": float((regimes == "Iota").mean() * 100.0),
        "n_events": int(len(peaks)),
        "transition_rate": float(len(peaks) / len(df)),
        "lyapunov_estimate": float(lyapunov),
        "pca_explained_variance_ratio": [
            float(v) for v in pca.explained_variance_ratio_
        ],
    }

    with open(output_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    save_single_plots(df, peaks, lyap_df, summary, output_dir)

    return summary


def save_single_plots(df, peaks, lyap_df, summary, output_dir):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["t"], df["r"])
    ax.set_title(f"r(t), K={summary['K']:.3f}")
    ax.set_xlabel("t")
    ax.set_ylabel("r")
    fig.tight_layout()
    fig.savefig(output_dir / "r_timeseries.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["abs_delta_theta"], linewidth=0.6)
    ax.scatter(peaks, df["abs_delta_theta"].iloc[peaks], s=10)
    ax.set_title("Phase Drift + Iota Events")
    ax.set_xlabel("sample")
    ax.set_ylabel("abs(delta_theta)")
    fig.tight_layout()
    fig.savefig(output_dir / "phase_drift_events.png", dpi=150)
    plt.close(fig)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(df["alpha"], df["beta"], df["gamma"], linewidth=0.3)
    ax.set_title("PCA Field Projection")
    ax.set_xlabel("alpha")
    ax.set_ylabel("beta")
    ax.set_zlabel("gamma")
    fig.tight_layout()
    fig.savefig(output_dir / "pca_projection.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(df["r"], df["abs_delta_theta"], s=1, alpha=0.3)
    ax.set_title("Phase Cloud")
    ax.set_xlabel("r")
    ax.set_ylabel("abs(delta_theta)")
    fig.tight_layout()
    fig.savefig(output_dir / "phase_cloud.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(lyap_df["t"], lyap_df["lyapunov_running_estimate"])
    ax.axhline(0.0, linewidth=1)
    ax.set_title(f"Lyapunov Running Estimate: {summary['lyapunov_estimate']:.6f}")
    ax.set_xlabel("t")
    ax.set_ylabel("lambda(t)")
    fig.tight_layout()
    fig.savefig(output_dir / "lyapunov_running.png", dpi=150)
    plt.close(fig)


def extract_phase_boundary(df: pd.DataFrame):
    drift_idx = df["abs_delta_theta_std"].idxmax()
    events_idx = df["transition_rate"].idxmax()

    return {
        "max_drift_boundary": df.loc[drift_idx].to_dict(),
        "max_event_boundary": df.loc[events_idx].to_dict(),
    }


def save_sweep_plots(df: pd.DataFrame, output_dir: Path):
    def line(y, name, title):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(df["K"], df[y], marker="o")
        ax.set_title(title)
        ax.set_xlabel("K")
        ax.set_ylabel(y)
        fig.tight_layout()
        fig.savefig(output_dir / name, dpi=180)
        plt.close(fig)

    line("r_mean", "r_mean_vs_K.png", "Mean Synchronization vs K")
    line("abs_delta_theta_std", "drift_std_vs_K.png", "Phase Drift STD vs K")
    line("iota_percent", "iota_percent_vs_K.png", "Iota Percent vs K")
    line("transition_rate", "transition_rate_vs_K.png", "Transition Rate vs K")
    line("lyapunov_estimate", "lyapunov_vs_K.png", "Lyapunov Estimate vs K")

    fig, ax = plt.subplots(figsize=(7, 5))
    sc = ax.scatter(
        df["r_mean"],
        df["abs_delta_theta_std"],
        c=df["K"],
        s=90,
    )
    ax.set_title("Phase Diagram: r_mean vs Drift STD")
    ax.set_xlabel("r_mean")
    ax.set_ylabel("abs_delta_theta_std")
    plt.colorbar(sc, label="K")
    fig.tight_layout()
    fig.savefig(output_dir / "phase_diagram_K.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    sc = ax.scatter(
        df["r_mean"],
        df["abs_delta_theta_std"],
        c=df["lyapunov_estimate"],
        s=90,
    )
    ax.set_title("Phase Diagram Colored by Lyapunov")
    ax.set_xlabel("r_mean")
    ax.set_ylabel("abs_delta_theta_std")
    plt.colorbar(sc, label="lyapunov")
    fig.tight_layout()
    fig.savefig(output_dir / "phase_diagram_lyapunov.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    sc = ax.scatter(
        df["lyapunov_estimate"],
        df["transition_rate"],
        c=df["K"],
        s=90,
    )
    ax.axvline(0.0, linewidth=1)
    ax.set_title("Event Rate vs Lyapunov")
    ax.set_xlabel("lyapunov_estimate")
    ax.set_ylabel("transition_rate")
    plt.colorbar(sc, label="K")
    fig.tight_layout()
    fig.savefig(output_dir / "event_rate_vs_lyapunov.png", dpi=180)
    plt.close(fig)


def make_boundary_gif(df: pd.DataFrame, output_dir: Path):
    try:
        import imageio.v2 as imageio
    except Exception:
        print("imageio not available; skipping GIF.")
        return

    frames = []
    tmp_dir = output_dir / "_gif_frames"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    for i in range(1, len(df) + 1):
        part = df.iloc[:i]

        fig, ax = plt.subplots(figsize=(7, 5))
        sc = ax.scatter(
            part["r_mean"],
            part["abs_delta_theta_std"],
            c=part["K"],
            s=90,
            vmin=df["K"].min(),
            vmax=df["K"].max(),
        )
        ax.set_xlim(df["r_mean"].min() * 0.9, df["r_mean"].max() * 1.05)
        ax.set_ylim(0, df["abs_delta_theta_std"].max() * 1.15)
        ax.set_xlabel("r_mean")
        ax.set_ylabel("abs_delta_theta_std")
        ax.set_title("Phase Boundary Sweep")
        plt.colorbar(sc, label="K")
        fig.tight_layout()

        frame_path = tmp_dir / f"frame_{i:03d}.png"
        fig.savefig(frame_path, dpi=120)
        plt.close(fig)

        frames.append(imageio.imread(frame_path))

    imageio.mimsave(output_dir / "phase_boundary_sweep.gif", frames, fps=2)


def main():
    timestamp = int(time.time())

    base_output = (
        Path(__file__).parent
        / "outputs"
        / "kuramoto_v6"
        / "master_runs"
        / f"run_{timestamp}"
    )

    runs_dir = base_output / "runs"
    sweep_dir = base_output / "sweep"
    runs_dir.mkdir(parents=True, exist_ok=True)
    sweep_dir.mkdir(parents=True, exist_ok=True)

    K_values = np.linspace(0.5, 3.0, 12)

    summaries = []

    for K in K_values:
        print(f"\n=== K={K:.3f} ===")

        config = KuramotoConfig(coupling_k=float(K))
        run_id = f"K_{K:.3f}".replace(".", "_")
        run_dir = runs_dir / run_id

        summary = run_single(config, run_dir)
        summaries.append(summary)

    df = pd.DataFrame(summaries)
    df.to_csv(sweep_dir / "sweep_results.csv", index=False)

    boundary = extract_phase_boundary(df)
    with open(sweep_dir / "phase_boundary.json", "w", encoding="utf-8") as f:
        json.dump(boundary, f, indent=2)

    save_sweep_plots(df, sweep_dir)
    make_boundary_gif(df, sweep_dir)

    print("\n--- MASTER V6 COMPLETE ---")
    print(f"Saved to: {base_output}")
    print("\nPhase boundary:")
    print(json.dumps(boundary, indent=2))


if __name__ == "__main__":
    main()
