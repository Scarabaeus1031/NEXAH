import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt


"""
NEXAH core test script (minimal scientific core)

Purpose
-------
Test whether a stripped-down geometric early-warning model can detect an
instability / split earlier than a classical voltage-threshold method.

This script does NOT depend on any symbolic layers.
It only uses:
- a minimal nonlinear dynamical core
- curvature-like geometry
- a Lyapunov proxy
- a winding / sign-change instability proxy

What it does
------------
1. Simulates a minimal driven nonlinear system with a slowly increasing stress.
2. Computes geometric indicators from the trajectory.
3. Detects an early-warning "split" event when the indicators jointly rise.
4. Compares that detection to a classical voltage-collapse threshold.
5. Plots the result.

You can later replace the synthetic system input with real IEEE time series.
"""


@dataclass
class CoreParams:
    dt: float = 0.01
    t_end: float = 120.0

    # Minimal dynamical core
    alpha: float = 0.55       # linear coupling / drift term
    beta: float = 0.22        # Van der Pol-like nonlinearity
    gamma: float = 0.18       # phase forcing strength
    omega: float = 1.2        # external phase rate

    # Stress ramp: increases instability pressure over time
    stress_gain: float = 0.010
    stress_start: float = 8.0

    # Synthetic voltage collapse model (benchmark proxy)
    v0: float = 1.0
    v_floor: float = 0.12
    collapse_midpoint: float = 79.5
    collapse_sharpness: float = 0.22

    # Indicator windows
    smooth_window: int = 31
    rolling_window: int = 120

    # Detection thresholds (initial placeholders)
    curvature_z_thresh: float = 2.2
    lyapunov_z_thresh: float = 1.8
    winding_rate_thresh: float = 0.055
    score_thresh: float = 2.35

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
        segment = x[lo:i + 1]
        mean[i] = segment.mean()
        std_i = segment.std()
        std[i] = std_i if std_i > 1e-9 else 1e-9
    return mean, std


def zscore_rolling(x: np.ndarray, window: int) -> np.ndarray:
    mean, std = rolling_mean_std(x, window)
    return (x - mean) / std


def simulate_core(params: CoreParams) -> Dict[str, np.ndarray]:
    t = np.arange(0.0, params.t_end + params.dt, params.dt)
    n = len(t)

    c = np.zeros(n)
    v = np.zeros(n)
    phi = np.zeros(n)
    stress = np.zeros(n)

    c[0] = 0.12
    v[0] = 0.01
    phi[0] = 0.0

    for i in range(n - 1):
        ti = t[i]

        # Slowly increasing external stress to force a transition.
        stress[i] = params.stress_gain * max(0.0, ti - params.stress_start)

        # Phase driver
        phi[i + 1] = phi[i] + params.dt * params.omega

        # Minimal stripped-down dynamics
        dc = v[i]
        dv = (
            params.alpha * (v[i] - c[i])
            + params.beta * v[i] * (1.0 - c[i] ** 2)
            + params.gamma * math.sin(phi[i])
            + stress[i]
        )

        c[i + 1] = c[i] + params.dt * dc
        v[i + 1] = v[i] + params.dt * dv

    stress[-1] = stress[-2]

    # Synthetic classical voltage trajectory, intended as a baseline proxy.
    # Replace this with real voltage data for actual IEEE runs.
    voltage = params.v_floor + (params.v0 - params.v_floor) / (
        1.0 + np.exp(params.collapse_sharpness * (t - params.collapse_midpoint))
    )

    return {
        "t": t,
        "c": c,
        "v": v,
        "phi": phi,
        "stress": stress,
        "voltage": voltage,
    }


def compute_indicators(sim: Dict[str, np.ndarray], params: CoreParams) -> Dict[str, np.ndarray]:
    t = sim["t"]
    c = sim["c"]
    v = sim["v"]
    dt = params.dt

    # First and second derivatives from simulated trajectory.
    dc = np.gradient(c, dt)
    d2c = np.gradient(dc, dt)

    # Curvature-like geometric quantity for a 1D observed path c(t).
    curvature = np.abs(d2c) / np.power(1.0 + dc ** 2, 1.5)
    curvature = moving_average(curvature, params.smooth_window)

    # Lyapunov proxy: local speed / expansion proxy.
    lyapunov_proxy = np.abs(v)
    lyapunov_proxy = moving_average(lyapunov_proxy, params.smooth_window)

    # Winding proxy: sign-change density in v.
    sign_v = np.sign(v)
    sign_v[sign_v == 0] = 1
    sign_changes = np.zeros_like(v)
    sign_changes[1:] = (sign_v[1:] != sign_v[:-1]).astype(float)
    winding_rate = moving_average(sign_changes / max(dt, 1e-9), params.smooth_window)

    curvature_z = zscore_rolling(curvature, params.rolling_window)
    lyapunov_z = zscore_rolling(lyapunov_proxy, params.rolling_window)

    # Composite score: intentionally simple and inspectable.
    score = (
        0.95 * np.maximum(curvature_z, 0.0)
        + 0.90 * np.maximum(lyapunov_z, 0.0)
        + 2.00 * np.maximum(winding_rate - params.winding_rate_thresh, 0.0)
    )

    return {
        "t": t,
        "curvature": curvature,
        "lyapunov_proxy": lyapunov_proxy,
        "winding_rate": winding_rate,
        "curvature_z": curvature_z,
        "lyapunov_z": lyapunov_z,
        "score": score,
    }


def detect_split(sim: Dict[str, np.ndarray], ind: Dict[str, np.ndarray], params: CoreParams) -> DetectionResult:
    t = sim["t"]
    voltage = sim["voltage"]

    curvature_z = ind["curvature_z"]
    lyapunov_z = ind["lyapunov_z"]
    winding_rate = ind["winding_rate"]
    score = ind["score"]

    split_mask = (
        (curvature_z > params.curvature_z_thresh)
        & (lyapunov_z > params.lyapunov_z_thresh)
        & (winding_rate > params.winding_rate_thresh)
        & (score > params.score_thresh)
    )

    split_idx = int(np.argmax(split_mask)) if np.any(split_mask) else None
    split_time = float(t[split_idx]) if split_idx is not None and split_mask[split_idx] else None

    classic_mask = voltage < params.voltage_threshold
    classic_idx = int(np.argmax(classic_mask)) if np.any(classic_mask) else None
    classic_time = float(t[classic_idx]) if classic_idx is not None and classic_mask[classic_idx] else None

    if split_time is not None and classic_time is not None:
        lead_time = classic_time - split_time
    else:
        lead_time = None

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


def plot_result(result: DetectionResult, params: CoreParams, savepath: Optional[str] = None) -> None:
    d = result.diagnostics
    t = d["t"]

    fig, axes = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

    axes[0].plot(t, d["voltage"], label="Classical voltage proxy")
    axes[0].axhline(params.voltage_threshold, linestyle="--", label="Classical threshold")
    if result.classic_time is not None:
        axes[0].axvline(result.classic_time, linestyle=":", label=f"Classic detection = {result.classic_time:.2f}s")
    if result.split_time is not None:
        axes[0].axvline(result.split_time, linestyle="-.", label=f"NEXAH split = {result.split_time:.2f}s")
    axes[0].set_ylabel("Voltage")
    axes[0].legend(loc="best")
    axes[0].set_title("NEXAH Core vs Classical Threshold")

    axes[1].plot(t, d["c"], label="State c(t)")
    axes[1].plot(t, d["v"], label="Drift v(t)")
    axes[1].set_ylabel("State / Drift")
    axes[1].legend(loc="best")

    axes[2].plot(t, d["curvature_z"], label="Curvature z-score")
    axes[2].plot(t, d["lyapunov_z"], label="Lyapunov proxy z-score")
    axes[2].axhline(params.curvature_z_thresh, linestyle="--", label="Curvature threshold")
    axes[2].axhline(params.lyapunov_z_thresh, linestyle=":", label="Lyapunov threshold")
    axes[2].set_ylabel("Z-score")
    axes[2].legend(loc="best")

    axes[3].plot(t, d["winding_rate"], label="Winding-rate proxy")
    axes[3].plot(t, d["score"], label="Composite split score")
    axes[3].axhline(params.winding_rate_thresh, linestyle="--", label="Winding threshold")
    axes[3].axhline(params.score_thresh, linestyle=":", label="Score threshold")
    axes[3].set_ylabel("Score / Rate")
    axes[3].set_xlabel("Time [s]")
    axes[3].legend(loc="best")

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


def run_once(params: Optional[CoreParams] = None, savepath: Optional[str] = None) -> DetectionResult:
    params = params or CoreParams()
    sim = simulate_core(params)
    ind = compute_indicators(sim, params)
    result = detect_split(sim, ind, params)

    print("NEXAH core test result")
    print("----------------------")
    print(f"Split time:   {result.split_time}")
    print(f"Classic time: {result.classic_time}")
    print(f"Lead time:    {result.lead_time}")

    plot_result(result, params, savepath=savepath)
    return result


def sensitivity_scan() -> List[Tuple[float, float, Optional[float]]]:
    """
    Minimal threshold scan to see whether lead time is robust.
    Returns tuples of:
        (stress_gain, collapse_midpoint, lead_time)
    """
    outputs: List[Tuple[float, float, Optional[float]]] = []

    for stress_gain in [0.008, 0.010, 0.012]:
        for collapse_midpoint in [76.0, 79.5, 83.0]:
            params = CoreParams(
                stress_gain=stress_gain,
                collapse_midpoint=collapse_midpoint,
            )
            sim = simulate_core(params)
            ind = compute_indicators(sim, params)
            result = detect_split(sim, ind, params)
            outputs.append((stress_gain, collapse_midpoint, result.lead_time))

    print("\nSensitivity scan")
    print("----------------")
    for stress_gain, collapse_midpoint, lead_time in outputs:
        print(
            f"stress_gain={stress_gain:.3f} | "
            f"collapse_midpoint={collapse_midpoint:.1f} | "
            f"lead_time={lead_time}"
        )

    return outputs


if __name__ == "__main__":
    # Main demo run
    run_once(savepath=None)

    # Optional rough robustness check
    sensitivity_scan()
