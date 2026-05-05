#!/usr/bin/env python3

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

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
    t_max: float = 500.0
    dt: float = 0.01
    transient_fraction: float = 0.1
    random_seed: int = 42


# =========================
# CORE SIM
# =========================

def kuramoto_rhs(_t, phases, omega, K):
    z = np.mean(np.exp(1j * phases))
    r = np.abs(z)
    psi = np.angle(z)
    return omega + K * r * np.sin(psi - phases)


def simulate(config: KuramotoConfig):
    rng = np.random.default_rng(config.random_seed)

    omega = rng.normal(0, 1, config.n_oscillators)
    omega -= omega.mean()

    phases0 = rng.uniform(-np.pi, np.pi, config.n_oscillators)

    t_eval = np.arange(0, config.t_max + config.dt, config.dt)

    sol = solve_ivp(
        kuramoto_rhs,
        (0, config.t_max),
        phases0,
        t_eval=t_eval,
        args=(omega, config.coupling_k),
        method="DOP853"
    )

    if not sol.success:
        raise RuntimeError("Integration failed")

    return sol.t, sol.y.T


# =========================
# LYAPUNOV
# =========================

def simulate_perturbed(config, epsilon=1e-6):
    t, phases = simulate(config)

    perturbed = phases.copy()
    perturbed[0] += epsilon

    return t, phases, perturbed


def compute_lyapunov(t, p1, p2):
    diff = np.linalg.norm(p1 - p2, axis=1)
    diff = np.clip(diff, 1e-12, None)
    log_diff = np.log(diff)

    # linear fit on early segment
    window = int(0.2 * len(t))
    slope = np.polyfit(t[:window], log_diff[:window], 1)[0]

    return log_diff, slope


# =========================
# MAIN PIPELINE
# =========================

def run_experiment(config: KuramotoConfig):

    # OUTPUT
    base_dir = Path(__file__).parent / "outputs" / "kuramoto_v5" / "runs"
    run_id = f"K_{config.coupling_k:.3f}_{int(time.time())}".replace(".", "_")

    out = base_dir / run_id
    out.mkdir(parents=True, exist_ok=True)

    print(f"\nRunning K={config.coupling_k}")
    print(f"Saving → {out}")

    # =========================
    # SIMULATION
    # =========================

    t, phases = simulate(config)

    cut = int(len(t) * config.transient_fraction)
    t = t[cut:]
    phases = phases[cut:]

    # =========================
    # OBSERVABLES
    # =========================

    z = np.mean(np.exp(1j * phases), axis=1)
    r = np.abs(z)
    psi = np.unwrap(np.angle(z))

    dr = np.gradient(r, config.dt)
    dpsi = np.gradient(psi, config.dt)

    states = np.column_stack([r, dr, dpsi])

    # =========================
    # PCA
    # =========================

    pca = PCA(n_components=3)
    proj = pca.fit_transform(states)

    alpha, beta, gamma = proj[:,0], proj[:,1], proj[:,2]

    # =========================
    # PHASE
    # =========================

    theta = np.unwrap(np.arctan2(gamma, beta))
    dtheta = np.diff(theta, prepend=theta[0])
    abs_d = np.abs(dtheta)

    # =========================
    # IOTA LOGIC (V4)
    # =========================

    mean = np.mean(abs_d)
    std = np.std(abs_d)

    theta_th = mean + 0.5 * std
    iota_th  = mean + 2.5 * std

    regimes = np.full(len(abs_d), "Theta", dtype=object)
    regimes[(abs_d > theta_th) & (dtheta > 0)] = "Tao"
    regimes[(abs_d > theta_th) & (dtheta < 0)] = "Dao"
    regimes[abs_d >= iota_th] = "Iota"

    peaks, _ = find_peaks(abs_d, height=iota_th, distance=50)

    # =========================
    # LYAPUNOV
    # =========================

    t_l, p1, p2 = simulate_perturbed(config)
    log_diff, lyap = compute_lyapunov(t_l, p1, p2)

    # =========================
    # SAVE DATA
    # =========================

    df = pd.DataFrame({
        "t": t,
        "r": r,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "abs_delta_theta": abs_d,
        "regime": regimes
    })

    df.to_csv(out / "data.csv", index=False)

    summary = {
        "K": config.coupling_k,
        "iota_percent": float((regimes == "Iota").mean()*100),
        "transition_rate": float(len(peaks)/len(df)),
        "r_mean": float(r.mean()),
        "abs_delta_theta_std": float(abs_d.std()),
        "lyapunov_estimate": float(lyap),
        "n_events": int(len(peaks))
    }

    with open(out / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # =========================
    # PLOTS
    # =========================

    # r(t)
    plt.figure(figsize=(10,4))
    plt.plot(t, r)
    plt.title("r(t)")
    plt.savefig(out / "r_timeseries.png", dpi=150)
    plt.close()

    # phase drift
    plt.figure(figsize=(10,4))
    plt.plot(abs_d)
    plt.scatter(peaks, abs_d[peaks], s=10)
    plt.title("phase drift + events")
    plt.savefig(out / "phase_drift.png", dpi=150)
    plt.close()

    # PCA
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(alpha, beta, gamma, linewidth=0.3)
    plt.savefig(out / "pca_projection.png", dpi=150)
    plt.close()

    # phase cloud
    plt.figure(figsize=(6,5))
    plt.scatter(r, abs_d, s=1, alpha=0.3)
    plt.xlabel("r")
    plt.ylabel("abs_delta_theta")
    plt.savefig(out / "phase_cloud.png", dpi=150)
    plt.close()

    # lyapunov plot
    plt.figure(figsize=(8,4))
    plt.plot(t_l, log_diff)
    plt.title(f"Lyapunov ≈ {lyap:.4f}")
    plt.savefig(out / "lyapunov.png", dpi=150)
    plt.close()

    return summary


# =========================
# MAIN
# =========================

def main():
    config = KuramotoConfig()
    summary = run_experiment(config)

    print("\n--- RUN COMPLETE ---")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
