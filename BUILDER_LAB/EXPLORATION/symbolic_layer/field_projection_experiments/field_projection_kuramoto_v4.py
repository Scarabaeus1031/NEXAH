#!/usr/bin/env python3

from __future__ import annotations

import json
import time
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

    t_eval = np.arange(0, config.t_max, config.dt)

    sol = solve_ivp(
        kuramoto_rhs,
        (0, config.t_max),
        phases0,
        t_eval=t_eval,
        args=(omega, config.coupling_k),
        method="DOP853"
    )

    phases = sol.y.T
    return sol.t, phases


# =========================
# PIPELINE
# =========================

def run_experiment(config: KuramotoConfig):

    # 🔥 unique run
    base_dir = Path(__file__).parent / "outputs" / "kuramoto_v4" / "runs"
    run_id = f"K_{config.coupling_k:.3f}_{int(time.time())}".replace(".", "_")
    out = base_dir / run_id
    out.mkdir(parents=True, exist_ok=True)

    t, phases = simulate(config)

    # remove transient
    cut = int(len(t) * config.transient_fraction)
    t = t[cut:]
    phases = phases[cut:]

    # order parameter
    z = np.mean(np.exp(1j * phases), axis=1)
    r = np.abs(z)
    psi = np.unwrap(np.angle(z))

    dr = np.gradient(r, config.dt)
    dpsi = np.gradient(psi, config.dt)

    states = np.column_stack([r, dr, dpsi])

    pca = PCA(n_components=3)
    proj = pca.fit_transform(states)

    beta = proj[:,1]
    gamma = proj[:,2]

    theta = np.unwrap(np.arctan2(gamma, beta))
    dtheta = np.diff(theta, prepend=theta[0])

    abs_d = np.abs(dtheta)

    # =========================
    # 🔥 NEW IOTA LOGIC
    # =========================

    mean = np.mean(abs_d)
    std = np.std(abs_d)

    theta_th = mean + 0.5*std
    iota_th  = mean + 2.5*std

    regimes = np.full(len(abs_d), "Theta", dtype=object)
    regimes[(abs_d > theta_th) & (dtheta > 0)] = "Tao"
    regimes[(abs_d > theta_th) & (dtheta < 0)] = "Dao"
    regimes[abs_d >= iota_th] = "Iota"

    # events
    peaks, _ = find_peaks(abs_d, height=iota_th, distance=50)

    # =========================
    # SAVE
    # =========================

    df = pd.DataFrame({
        "t": t,
        "r": r,
        "abs_delta_theta": abs_d,
        "regime": regimes
    })

    df.to_csv(out / "data.csv", index=False)

    summary = {
        "K": config.coupling_k,
        "iota_percent": float((regimes == "Iota").mean()*100),
        "transition_rate": float(len(peaks)/len(df)),
        "r_mean": float(r.mean()),
        "abs_delta_theta_std": float(abs_d.std())
    }

    with open(out / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    return summary
