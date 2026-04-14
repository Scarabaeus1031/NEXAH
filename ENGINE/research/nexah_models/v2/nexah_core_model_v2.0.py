import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt


"""
NEXAH multi-node core model (minimal collective-dynamics testbed)

Purpose
-------
This script extends the stripped single-node test into a small coupled system.
The goal is to test whether early-warning geometry emerges more clearly from
collective dynamics than from a single local oscillator.

What this model includes
------------------------
- N coupled nonlinear nodes
- slow stress ramp
- weak heterogeneity across nodes
- Kuramoto-like coupling through node phases / states
- aggregate observable for comparison with a classical voltage proxy
- geometric early-warning indicators on the aggregate trajectory
- synchronization-loss indicators across the node ensemble

What this model does NOT include
--------------------------------
- real IEEE network topology
- symbolic layers
- action / control logic

This is a scientific core testbed for the question:
    Does collective structure generate an earlier split signal?

How to use later
----------------
1. Run this synthetic model first.
2. Check whether a split appears before the classical threshold.
3. Replace the synthetic stress / voltage proxy with real IEEE data later.
"""


@dataclass
class MultiNodeParams:
    dt: float = 0.01
    t_end: float = 120.0

    # Network size
    n_nodes: int = 8

    # Node dynamics
    alpha: float = 0.55
    beta: float = 0.24
    gamma: float = 0.16
    omega: float = 1.15

    # Coupling and heterogeneity
    coupling_k: float = 0.34
    state_coupling_k: float = 0.08
    heterogeneity: float = 0.06
    seed: int = 7

    # Stress ramp
    stress_gain: float = 0.0105
    stress_start: float = 10.0
    split_push_start: float = 45.0
    split_push_gain: float = 0.22

    # Classical voltage proxy
    v0: float = 1.0
    v_floor: float = 0.12
    collapse_midpoint: float = 79.5
    collapse_sharpness: float = 0.22

    # Indicator windows
    smooth_window: int = 31
    rolling_window: int = 140

    # Detection thresholds
    curvature_z_thresh: float = 1.8
    lyapunov_z_thresh: float = 1.6
    winding_rate_thresh: float = 0.040
    sync_loss_z_thresh: float = 1.2
    score_thresh: float = 2.15

    # Classical threshold
    voltage_threshold: float = 0.70


@dataclass
class DetectionResult:
    split_time: Optional[float]
    classic_time: Optional[float]
    lead_time: Optional[float]
    diagnostics: Dict[str, np.ndarray]


def moving_average(x: np.ndarray, window: int) -> np.ndarray:
    if window <= 1:
        return x.copy()
    kernel = np.ones(window, dtype=float) / window
    return np.convolve(x, kernel, mode="same")


def rolling_mean_std(x: np.ndarray, window: int) -> Tuple[np.ndarray, np.ndarray]:
    mean = np.zeros_like(x)
    std = np.zeros_like(x)
    n = len(x)
    for i in range(n):
        lo = max(0, i - window + 1)
        seg = x[lo:i + 1]
        mean[i] = seg.mean()
        s = seg.std()
        std[i] = s if s > 1e-9 else 1e-9
    return mean, std


def zscore_rolling(x: np.ndarray, window: int) -> np.ndarray:
    mean, std = rolling_mean_std(x, window)
    return (x - mean) / std


def order_parameter(c: np.ndarray) -> float:
    # Kuramoto-like coherence computed from node states interpreted as phases.
    z = np.exp(1j * c)
    return np.abs(np.mean(z))


def simulate_multinode(params: MultiNodeParams) -> Dict[str, np.ndarray]:
    rng = np.random.default_rng(params.seed)

    t = np.arange(0.0, params.t_end + params.dt, params.dt)
    n_t = len(t)
    n = params.n_nodes

    c = np.zeros((n_t, n))
    v = np.zeros((n_t, n))
    phi = np.zeros((n_t, n))
    stress = np.zeros(n_t)
    coherence = np.zeros(n_t)
    fragmentation = np.zeros(n_t)

    alpha_i = params.alpha * (1.0 + params.heterogeneity * rng.normal(size=n))
    beta_i = params.beta * (1.0 + params.heterogeneity * rng.normal(size=n))
    gamma_i = params.gamma * (1.0 + params.heterogeneity * rng.normal(size=n))
    omega_i = params.omega * (1.0 + params.heterogeneity * rng.normal(size=n))

    c[0, :] = np.linspace(-0.24, 0.24, n)
    v[0, :] = 0.02 * rng.normal(size=n)
    phi[0, :] = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)

    for k in range(n_t - 1):
        tk = t[k]

        stress[k] = params.stress_gain * max(0.0, tk - params.stress_start)
        split_push = params.split_push_gain / (1.0 + np.exp(-(tk - params.split_push_start) / 4.0))

        c_now = c[k, :]
        v_now = v[k, :]
        phi_now = phi[k, :]

        mean_c = np.mean(c_now)
        mean_v = np.mean(v_now)

        coherence[k] = order_parameter(c_now)
        fragmentation[k] = np.std(c_now)

        for i in range(n):
            coupling_phase = np.sum(np.sin(c_now - c_now[i])) / n
            coupling_state = mean_c - c_now[i]
            push_term = split_push * (c_now[i] - mean_c)

            dc = v_now[i]
            dv = (
                alpha_i[i] * (v_now[i] - c_now[i])
                + beta_i[i] * v_now[i] * (1.0 - c_now[i] ** 2)
                + gamma_i[i] * math.sin(phi_now[i])
                + params.coupling_k * coupling_phase
                + params.state_coupling_k * coupling_state
                + stress[k]
                + push_term
            )

            c[k + 1, i] = c_now[i] + params.dt * dc
            v[k + 1, i] = v_now[i] + params.dt * dv
            phi[k + 1, i] = phi_now[i] + params.dt * omega_i[i]

    coherence[-1] = order_parameter(c[-1, :])
    fragmentation[-1] = np.std(c[-1, :])
    stress[-1] = stress[-2]

    c_mean = np.mean(c, axis=1)
    v_mean = np.mean(v, axis=1)
    c_std = np.std(c, axis=1)
    v_std = np.std(v, axis=1)

    voltage = params.v_floor + (params.v0 - params.v_floor) / (
        1.0 + np.exp(params.collapse_sharpness * (t - params.collapse_midpoint))
    )

    return {
        "t": t,
        "c_nodes": c,
        "v_nodes": v,
        "phi_nodes": phi,
        "c_mean": c_mean,
        "v_mean": v_mean,
        "c_std": c_std,
        "v_std": v_std,
        "coherence": coherence,
        "fragmentation": fragmentation,
        "stress": stress,
        "voltage": voltage,
    }


def compute_indicators(sim: Dict[str, np.ndarray], params: MultiNodeParams) -> Dict[str, np.ndarray]:
    t = sim["t"]
    c_mean = sim["c_mean"]
    v_mean = sim["v_mean"]
    coherence = sim["coherence"]
    fragmentation = sim["fragmentation"]
    dt = params.dt

    dc = np.gradient(c_mean, dt)
    d2c = np.gradient(dc, dt)

    curvature = np.abs(d2c) / np.power(1.0 + dc ** 2, 1.5)
    curvature = moving_average(curvature, params.smooth_window)

    lyapunov_proxy = np.abs(v_mean) + 0.5 * np.abs(np.gradient(v_mean, dt))
    lyapunov_proxy = moving_average(lyapunov_proxy, params.smooth_window)

    sign_v = np.sign(v_mean)
    sign_v[sign_v == 0] = 1
    sign_changes = np.zeros_like(v_mean)
    sign_changes[1:] = (sign_v[1:] != sign_v[:-1]).astype(float)
    winding_rate = moving_average(sign_changes / max(dt, 1e-9), params.smooth_window)

    sync_loss = (1.0 - coherence) + 0.75 * fragmentation
    sync_loss = moving_average(sync_loss, params.smooth_window)

    curvature_z = zscore_rolling(curvature, params.rolling_window)
    lyapunov_z = zscore_rolling(lyapunov_proxy, params.rolling_window)
    sync_loss_z = zscore_rolling(sync_loss, params.rolling_window)

    score = (
        0.85 * np.maximum(curvature_z, 0.0)
        + 0.85 * np.maximum(lyapunov_z, 0.0)
        + 2.50 * np.maximum(winding_rate - params.winding_rate_thresh, 0.0)
        + 1.10 * np.maximum(sync_loss_z, 0.0)
    )

    return {
        "t": t,
        "curvature": curvature,
        "lyapunov_proxy": lyapunov_proxy,
        "winding_rate": winding_rate,
        "sync_loss": sync_loss,
        "curvature_z": curvature_z,
        "lyapunov_z": lyapunov_z,
        "sync_loss_z": sync_loss_z,
        "score": score,
    }


def detect_split(sim: Dict[str, np.ndarray], ind: Dict[str, np.ndarray], params: MultiNodeParams) -> DetectionResult:
    t = sim["t"]
    voltage = sim["voltage"]

    score = ind["score"]
    sync_loss_z = ind["sync_loss_z"]
    curvature_z = ind["curvature_z"]
    lyapunov_z = ind["lyapunov_z"]
    winding_rate = ind["winding_rate"]

    split_mask = (
        (score > params.score_thresh)
        & (
            ((sync_loss_z > params.sync_loss_z_thresh) & (curvature_z > params.curvature_z_thresh))
            | ((sync_loss_z > params.sync_loss_z_thresh) & (lyapunov_z > params.lyapunov_z_thresh))
            | (winding_rate > params.winding_rate_thresh * 1.25)
        )
    )

    split_idx = int(np.argmax(split_mask)) if np.any(split_mask) else None
    split_time = float(t[split_idx]) if split_idx is not None and split_mask[split_idx] else None

    classic_mask = voltage < params.voltage_threshold
    classic_idx = int(np.argmax(classic_mask)) if np.any(classic_mask) else None
    classic_time = float(t[classic_idx]) if classic_idx is not None and classic_mask[classic_idx] else None

    lead_time = classic_time - split_time if split_time is not None and classic_time is not None else None

    diagnostics = {
        **sim,
        **ind,
        "split_mask": split_mask.astype(float),
        "classic_mask": classic_mask.astype(float),
    }

    return DetectionResult(
        split_time=split_time,
        classic_time=classic_time,
        lead_time=lead_time,
        diagnostics=diagnostics,
    )


def plot_result(result: DetectionResult, params: MultiNodeParams, savepath: Optional[str] = None) -> None:
    d = result.diagnostics
    t = d["t"]

    fig, axes = plt.subplots(5, 1, figsize=(12, 14), sharex=True)

    axes[0].plot(t, d["voltage"], label="Classical voltage proxy")
    axes[0].axhline(params.voltage_threshold, linestyle="--", label="Classical threshold")
    if result.classic_time is not None:
        axes[0].axvline(result.classic_time, linestyle=":", label=f"Classic detection = {result.classic_time:.2f}s")
    if result.split_time is not None:
        axes[0].axvline(result.split_time, linestyle="-.", label=f"NEXAH split = {result.split_time:.2f}s")
    axes[0].set_ylabel("Voltage")
    axes[0].set_title("NEXAH Multi-Node Core vs Classical Threshold")
    axes[0].legend(loc="best")

    axes[1].plot(t, d["c_mean"], label="Mean state")
    axes[1].plot(t, d["v_mean"], label="Mean drift")
    axes[1].fill_between(t, d["c_mean"] - d["c_std"], d["c_mean"] + d["c_std"], alpha=0.2, label="State spread")
    axes[1].set_ylabel("Mean / Spread")
    axes[1].legend(loc="best")

    axes[2].plot(t, d["coherence"], label="Coherence")
    axes[2].plot(t, d["fragmentation"], label="Fragmentation")
    axes[2].plot(t, d["sync_loss_z"], label="Sync-loss z-score")
    axes[2].axhline(params.sync_loss_z_thresh, linestyle="--", label="Sync-loss threshold")
    axes[2].set_ylabel("Collective")
    axes[2].legend(loc="best")

    axes[3].plot(t, d["curvature_z"], label="Curvature z-score")
    axes[3].plot(t, d["lyapunov_z"], label="Lyapunov z-score")
    axes[3].axhline(params.curvature_z_thresh, linestyle="--", label="Curvature threshold")
    axes[3].axhline(params.lyapunov_z_thresh, linestyle=":", label="Lyapunov threshold")
    axes[3].set_ylabel("Geometry")
    axes[3].legend(loc="best")

    axes[4].plot(t, d["winding_rate"], label="Winding-rate proxy")
    axes[4].plot(t, d["score"], label="Composite split score")
    axes[4].axhline(params.winding_rate_thresh, linestyle="--", label="Winding threshold")
    axes[4].axhline(params.score_thresh, linestyle=":", label="Score threshold")
    axes[4].set_ylabel("Score / Rate")
    axes[4].set_xlabel("Time [s]")
    axes[4].legend(loc="best")

    summary = []
    if result.split_time is not None:
        summary.append(f"split={result.split_time:.2f}s")
    if result.classic_time is not None:
        summary.append(f"classic={result.classic_time:.2f}s")
    if result.lead_time is not None:
        summary.append(f"lead={result.lead_time:.2f}s")
    if summary:
        fig.suptitle(" | ".join(summary), fontsize=12)

    fig.tight_layout()
    if savepath:
        fig.savefig(savepath, dpi=160, bbox_inches="tight")
    plt.show()


def run_once(params: Optional[MultiNodeParams] = None, savepath: Optional[str] = None) -> DetectionResult:
    params = params or MultiNodeParams()
    sim = simulate_multinode(params)
    ind = compute_indicators(sim, params)
    result = detect_split(sim, ind, params)

    print("NEXAH multi-node core test result")
    print("---------------------------------")
    print(f"Nodes:        {params.n_nodes}")
    print(f"Split time:   {result.split_time}")
    print(f"Classic time: {result.classic_time}")
    print(f"Lead time:    {result.lead_time}")

    plot_result(result, params, savepath=savepath)
    return result


def sensitivity_scan() -> List[Tuple[int, float, float, Optional[float]]]:
    outputs: List[Tuple[int, float, float, Optional[float]]] = []

    for n_nodes in [5, 8, 12]:
        for coupling_k in [0.24, 0.34, 0.46]:
            for split_push_gain in [0.16, 0.22, 0.30]:
                params = MultiNodeParams(
                    n_nodes=n_nodes,
                    coupling_k=coupling_k,
                    split_push_gain=split_push_gain,
                )
                sim = simulate_multinode(params)
                ind = compute_indicators(sim, params)
                result = detect_split(sim, ind, params)
                outputs.append((n_nodes, coupling_k, split_push_gain, result.lead_time))

    print("\nSensitivity scan")
    print("----------------")
    for n_nodes, coupling_k, split_push_gain, lead_time in outputs:
        print(
            f"n_nodes={n_nodes:2d} | coupling={coupling_k:.2f} | "
            f"split_push={split_push_gain:.2f} | lead_time={lead_time}"
        )

    return outputs


if __name__ == "__main__":
    run_once(savepath=None)
    sensitivity_scan()
