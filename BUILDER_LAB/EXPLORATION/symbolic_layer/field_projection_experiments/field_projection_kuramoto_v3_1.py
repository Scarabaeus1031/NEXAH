#!/usr/bin/env python3
"""
field_projection_kuramoto_v3.py

NEXAH FIELD_LAYER — EXPERIMENTAL BUILD V3
(FULL VERSION — fixed output handling, no feature loss)
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


# =========================
# CONFIG
# =========================

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
    output_dir: str | None = None   # 🔥 FIX
    random_seed: int = 42


# =========================
# DYNAMICS
# =========================

def kuramoto_rhs(_t, phases, omega, K):
    z = np.mean(np.exp(1j * phases))
    r = np.abs(z)
    psi = np.angle(z)
    return omega + K * r * np.sin(psi - phases)


def simulate_kuramoto(config):
    rng = np.random.default_rng(config.random_seed)

    omega = rng.normal(config.omega_mean, config.omega_std, config.n_oscillators)
    omega -= omega.mean()

    phases0 = rng.uniform(-np.pi, np.pi, config.n_oscillators)

    t_eval = np.arange(0, config.t_max + config.dt, config.dt)

    sol = solve_ivp(
        kuramoto_rhs,
        (0, config.t_max),
        phases0,
        t_eval=t_eval,
        args=(omega, config.coupling_k),
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
    )

    if not sol.success:
        raise RuntimeError("Integration failed")

    phases = sol.y.T
    phases = np.mod(phases + np.pi, 2*np.pi) - np.pi

    return sol.t, phases, omega


# =========================
# PIPELINE
# =========================

def remove_transient(t, phases, frac):
    idx = int(len(t) * frac)
    return t[idx:], phases[idx:]


def compute_order_parameter(phases, dt):
    z = np.mean(np.exp(1j * phases), axis=1)
    r = np.abs(z)
    psi = np.unwrap(np.angle(z))

    dr_dt = np.gradient(r, dt)
    dpsi_dt = np.gradient(psi, dt)

    return r, psi, dr_dt, dpsi_dt


def build_observable_state(r, dr_dt, dpsi_dt):
    return np.column_stack([r, dr_dt, dpsi_dt])


def pca_project(states):
    pca = PCA(n_components=3)
    proj = pca.fit_transform(states)
    return proj, pca


def compute_phase(proj):
    beta = proj[:, 1]
    gamma = proj[:, 2]

    theta = np.unwrap(np.arctan2(gamma, beta))
    dtheta = np.diff(theta, prepend=theta[0])

    return theta, dtheta


def classify_regimes(delta_theta, q):
    A = np.abs(delta_theta)

    t_th = np.quantile(A, 0.35)
    i_th = np.quantile(A, q)

    reg = np.full(len(A), "Theta", dtype=object)
    reg[(A > t_th) & (delta_theta > 0)] = "Tao"
    reg[(A > t_th) & (delta_theta < 0)] = "Dao"
    reg[A >= i_th] = "Iota"

    return reg, {
        "theta_threshold_abs_delta": float(t_th),
        "iota_threshold_abs_delta": float(i_th),
        "iota_quantile": q,
    }


def detect_iota(dtheta, thr, dist, prom_q):
    A = np.abs(dtheta)
    prom = np.quantile(A, prom_q)

    peaks, _ = find_peaks(A, height=thr, distance=dist, prominence=prom)
    return peaks


# =========================
# DATA BUILD
# =========================

def build_dataframe(t, r, psi, dr_dt, dpsi_dt, proj, theta, dtheta, reg, peaks):
    df = pd.DataFrame({
        "t": t,
        "r": r,
        "psi": psi,
        "dr_dt": dr_dt,
        "dpsi_dt": dpsi_dt,
        "alpha": proj[:,0],
        "beta": proj[:,1],
        "gamma": proj[:,2],
        "theta": theta,
        "delta_theta": dtheta,
        "abs_delta_theta": np.abs(dtheta),
        "regime": reg,
        "is_iota_event": False
    })

    df.loc[peaks, "is_iota_event"] = True
    return df


def extract_iota_event_windows(df, window=100):
    events = df[df["is_iota_event"]]
    records = []

    for idx in events.index:
        start = max(0, idx - window)
        end = min(len(df)-1, idx + window)
        segment = df.iloc[start:end+1]

        records.append({
            "event_index": int(idx),
            "t_peak": float(df.loc[idx, "t"]),
            "local_density": float(segment["abs_delta_theta"].mean())
        })

    return pd.DataFrame(records)


# =========================
# OUTPUT HANDLING (FIX)
# =========================

def get_output_dir(config):
    if config.output_dir is None:
        return Path(__file__).parent / "outputs" / "kuramoto_v3"
    return Path(config.output_dir)


# =========================
# PLOTS
# =========================

def save_plots(df, out):
    out.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.plot(df["t"], df["r"])
    plt.savefig(out / "kuramoto_v3_order_parameter.png")
    plt.close()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(df["alpha"], df["beta"], df["gamma"], linewidth=0.3)
    plt.savefig(out / "kuramoto_v3_pca_projection.png")
    plt.close()


# =========================
# MAIN EXPERIMENT
# =========================

def run_experiment(config):

    out = get_output_dir(config)
    out.mkdir(parents=True, exist_ok=True)

    t, phases, omega = simulate_kuramoto(config)
    t, phases = remove_transient(t, phases, config.transient_fraction)

    r, psi, dr_dt, dpsi_dt = compute_order_parameter(phases, config.dt)

    states = build_observable_state(r, dr_dt, dpsi_dt)
    proj, pca = pca_project(states)

    theta, dtheta = compute_phase(proj)
    reg, thr = classify_regimes(dtheta, config.iota_quantile)

    peaks = detect_iota(dtheta, thr["iota_threshold_abs_delta"], config.peak_distance, config.peak_prominence_quantile)

    df = build_dataframe(t, r, psi, dr_dt, dpsi_dt, proj, theta, dtheta, reg, peaks)
    windows = extract_iota_event_windows(df, config.iota_window)

    # SAVE
    df.to_csv(out / "kuramoto_v3_field_projection.csv", index=False)
    windows.to_csv(out / "kuramoto_v3_iota_event_windows.csv", index=False)

    summary = {
        "iota_percent": float((df["regime"] == "Iota").mean()*100),
        "events": int(len(peaks)),
        "transition_rate": float(len(peaks)/len(df))
    }

    with open(out / "kuramoto_v3_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    save_plots(df, out)

    return summary


# =========================
# CLI
# =========================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--coupling-k", type=float, default=1.8)

    args = parser.parse_args()

    cfg = KuramotoConfig(
        coupling_k=args.coupling_k,
        output_dir=args.output_dir
    )

    summary = run_experiment(cfg)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
