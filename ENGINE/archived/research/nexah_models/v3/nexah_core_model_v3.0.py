import math
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List

import numpy as np
import matplotlib.pyplot as plt


# =========================
# PARAMETERS
# =========================

@dataclass
class MultiNodeParams:
    dt: float = 0.01
    t_end: float = 120.0

    n_nodes: int = 8

    alpha: float = 0.55
    beta: float = 0.24
    gamma: float = 0.16
    omega: float = 1.15

    coupling_k: float = 0.34
    state_coupling_k: float = 0.08
    heterogeneity: float = 0.06
    seed: int = 7

    stress_gain: float = 0.0105
    stress_start: float = 10.0
    split_push_start: float = 45.0
    split_push_gain: float = 0.22

    v0: float = 1.0
    v_floor: float = 0.12
    collapse_midpoint: float = 79.5
    collapse_sharpness: float = 0.22

    smooth_window: int = 31
    rolling_window: int = 140

    curvature_z_thresh: float = 1.7
    lyapunov_z_thresh: float = 1.5
    winding_rate_thresh: float = 0.030
    sync_loss_z_thresh: float = 0.9
    score_thresh: float = 1.85

    warmup_time: float = 20.0
    score_smooth_window: int = 25
    winding_smooth_window: int = 50

    persistence_window: int = 60
    persistence_fraction: float = 0.60

    voltage_threshold: float = 0.70


# =========================
# UTILS
# =========================

def moving_average(x, w):
    if w <= 1:
        return x
    return np.convolve(x, np.ones(w)/w, mode="same")


def rolling_mean_std(x, window):
    mean = np.zeros_like(x)
    std = np.zeros_like(x)
    for i in range(len(x)):
        lo = max(0, i - window)
        seg = x[lo:i+1]
        mean[i] = seg.mean()
        std[i] = max(seg.std(), 1e-9)
    return mean, std


def zscore_rolling(x, window):
    m, s = rolling_mean_std(x, window)
    return (x - m) / s


def persistent_true(mask, window=50, fraction=0.6):
    out = np.zeros_like(mask, dtype=bool)
    needed = int(window * fraction)
    for i in range(len(mask)):
        lo = max(0, i - window)
        if np.sum(mask[lo:i+1]) >= needed:
            out[i] = True
    return out


def order_parameter(c):
    return np.abs(np.mean(np.exp(1j * c)))


# =========================
# SIMULATION
# =========================

def simulate(params: MultiNodeParams):
    rng = np.random.default_rng(params.seed)

    t = np.arange(0, params.t_end, params.dt)
    n = params.n_nodes

    c = np.zeros((len(t), n))
    v = np.zeros((len(t), n))
    phi = np.zeros((len(t), n))

    coherence = np.zeros(len(t))
    fragmentation = np.zeros(len(t))

    c[0] = np.linspace(-0.2, 0.2, n)
    phi[0] = np.linspace(0, 2*np.pi, n)

    for k in range(len(t)-1):
        tk = t[k]

        stress = params.stress_gain * max(0, tk - params.stress_start)
        split_push = params.split_push_gain / (1 + np.exp(-(tk - params.split_push_start)/4))

        mean_c = np.mean(c[k])

        coherence[k] = order_parameter(c[k])
        fragmentation[k] = np.std(c[k])

        for i in range(n):
            coupling = np.mean(np.sin(c[k] - c[k][i]))
            dc = v[k][i]
            dv = (
                params.alpha * (v[k][i] - c[k][i])
                + params.beta * v[k][i]*(1-c[k][i]**2)
                + params.gamma * math.sin(phi[k][i])
                + params.coupling_k * coupling
                + params.state_coupling_k * (mean_c - c[k][i])
                + stress
                + split_push*(c[k][i]-mean_c)
            )

            c[k+1][i] = c[k][i] + params.dt * dc
            v[k+1][i] = v[k][i] + params.dt * dv
            phi[k+1][i] = phi[k][i] + params.dt * params.omega

    coherence[-1] = order_parameter(c[-1])
    fragmentation[-1] = np.std(c[-1])

    c_mean = np.mean(c, axis=1)
    v_mean = np.mean(v, axis=1)

    voltage = params.v_floor + (params.v0 - params.v_floor) / (
        1 + np.exp(params.collapse_sharpness * (t - params.collapse_midpoint))
    )

    return dict(
        t=t,
        c_mean=c_mean,
        v_mean=v_mean,
        coherence=coherence,
        fragmentation=fragmentation,
        voltage=voltage
    )


# =========================
# INDICATORS
# =========================

def compute_indicators(sim, params):
    t = sim["t"]
    c = sim["c_mean"]
    v = sim["v_mean"]
    dt = params.dt

    dc = np.gradient(c, dt)
    d2c = np.gradient(dc, dt)

    curvature = np.abs(d2c) / (1 + dc**2)**1.5
    curvature = moving_average(curvature, params.smooth_window)

    lyap = np.abs(v) + 0.5*np.abs(np.gradient(v, dt))
    lyap = moving_average(lyap, params.smooth_window)

    sign = np.sign(v)
    sign[sign==0]=1
    flips = (sign[1:] != sign[:-1]).astype(float)
    winding = np.concatenate([[0], flips])
    winding = moving_average(winding, params.winding_smooth_window)

    sync_loss = (1 - sim["coherence"]) + 0.75 * sim["fragmentation"]
    sync_loss = moving_average(sync_loss, params.smooth_window)

    curvature_z = zscore_rolling(curvature, params.rolling_window)
    lyap_z = zscore_rolling(lyap, params.rolling_window)
    sync_z = zscore_rolling(sync_loss, params.rolling_window)

    score_raw = (
        0.8*np.maximum(curvature_z-0.25,0)
        + 0.75*np.maximum(lyap_z-0.25,0)
        + 1.1*np.maximum(sync_z-0.15,0)
        + 2.2*np.maximum(winding-params.winding_rate_thresh,0)
    )

    score = moving_average(score_raw, params.score_smooth_window)

    return dict(
        t=t,
        curvature_z=curvature_z,
        lyap_z=lyap_z,
        sync_z=sync_z,
        winding=winding,
        score=score
    )


# =========================
# DETECTION
# =========================

def detect(sim, ind, params):
    t = sim["t"]

    warm = t > params.warmup_time

    gate = (
        (ind["curvature_z"] > params.curvature_z_thresh)
        & (ind["sync_z"] > params.sync_loss_z_thresh)
    )

    pre = warm & (ind["score"] > params.score_thresh) & gate

    mask = persistent_true(pre, params.persistence_window, params.persistence_fraction)

    split = t[np.argmax(mask)] if np.any(mask) else None

    classic_mask = sim["voltage"] < params.voltage_threshold
    classic = t[np.argmax(classic_mask)] if np.any(classic_mask) else None

    lead = (classic - split) if split and classic else None

    return split, classic, lead, mask


# =========================
# MAIN
# =========================

def run():
    p = MultiNodeParams()
    sim = simulate(p)
    ind = compute_indicators(sim, p)

    split, classic, lead, mask = detect(sim, ind, p)

    print("\nNEXAH v3.0 result")
    print("------------------")
    print("split:", split)
    print("classic:", classic)
    print("lead:", lead)

    plt.figure(figsize=(10,6))
    plt.plot(sim["t"], sim["voltage"], label="voltage")
    plt.axhline(p.voltage_threshold, linestyle="--")

    if split:
        plt.axvline(split, color="green", label="split")
    if classic:
        plt.axvline(classic, color="red", label="classic")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    run()
