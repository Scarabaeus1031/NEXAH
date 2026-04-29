import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "outputs" / "run_016_hybrid_detector"


# ============================================================
# Utils
# ============================================================

def sustained_first_crossing(mask, t, min_samples=3):
    mask = np.asarray(mask, dtype=bool)

    for i in range(0, len(mask) - min_samples + 1):
        if np.all(mask[i:i + min_samples]):
            return float(t[i])

    return None


def compute_lead_time(t_collapse, t_detection):
    if t_collapse is None or t_detection is None:
        return None
    return float(t_collapse - t_detection)


def normalize_signal(x):
    x = np.asarray(x, dtype=float)
    xmax = np.max(np.abs(x)) + 1e-8
    return x / xmax


# ============================================================
# Scenario
# ============================================================

def make_synthetic_scenario(kind="nonlinear", n=500):
    t = np.linspace(0, 100, n)
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    if kind == "nonlinear":
        V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
        V += 0.01 * np.sin(0.8 * t) * (t < 25)

    elif kind == "noisy":
        rng = np.random.default_rng(7)
        V += 0.01 * rng.normal(size=len(t))

    return t, V


# ============================================================
# Signals
# ============================================================

def compute_signals(t, V, sigma=2):
    V_smooth = gaussian_filter1d(V, sigma=sigma)
    dv_dt = gaussian_filter1d(np.gradient(V_smooth, t), sigma=sigma)
    d2v_dt2 = gaussian_filter1d(np.gradient(dv_dt, t), sigma=sigma)

    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    # kappa(t): local event curvature
    kappa = gaussian_filter1d(
        np.linalg.norm(np.gradient(np.gradient(x, axis=0), axis=0), axis=1),
        sigma=sigma,
    )

    # drift(t): motion magnitude in reconstructed state space
    dx = np.diff(x, axis=0)
    drift = np.linalg.norm(dx, axis=1)
    drift = np.concatenate([[0.0], drift])
    drift = gaussian_filter1d(drift, sigma=sigma)

    # angle(t): directional change
    angles = []

    for i in range(1, len(dx)):
        v1 = dx[i - 1]
        v2 = dx[i]

        n1 = np.linalg.norm(v1)
        n2 = np.linalg.norm(v2)

        if n1 < 1e-8 or n2 < 1e-8:
            angles.append(0.0)
            continue

        cos_angle = np.dot(v1, v2) / (n1 * n2)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)

        angles.append(np.arccos(cos_angle))

    angle = np.array([0.0, 0.0] + angles)
    angle = gaussian_filter1d(angle, sigma=sigma)

    return V_smooth, kappa, drift, angle


# ============================================================
# Hybrid detector
# ============================================================

def compute_threshold(signal, baseline_slice):
    baseline = signal[baseline_slice]
    return float(np.mean(baseline) + 2.0 * np.std(baseline))


def run_hybrid_detector(kind="nonlinear"):
    print("\n=== RUN 016 — HYBRID DETECTOR ===")

    t, V = make_synthetic_scenario(kind=kind)
    V_smooth, kappa, drift, angle = compute_signals(t, V)

    # --------------------------------------------------------
    # Reference collapse
    # --------------------------------------------------------
    V_threshold = 0.7
    t_collapse = sustained_first_crossing(V_smooth < V_threshold, t)

    # --------------------------------------------------------
    # Detection settings
    # --------------------------------------------------------
    transient_ignore_fraction = 0.10
    transient_idx = int(transient_ignore_fraction * len(t))

    baseline_slice = slice(transient_idx, int(0.30 * len(t)))
    valid_mask = np.arange(len(t)) >= transient_idx

    # thresholds
    kappa_th = compute_threshold(kappa, baseline_slice)
    drift_th = compute_threshold(drift, baseline_slice)
    angle_th = compute_threshold(angle, baseline_slice)

    # individual activity masks
    kappa_active = (kappa > kappa_th) & valid_mask
    drift_active = (drift > drift_th) & valid_mask
    angle_active = (angle > angle_th) & valid_mask

    # hybrid rule:
    # kappa may trigger local events, but must be confirmed by drift or angle.
    hybrid_active = (
        kappa_active.astype(int)
        + drift_active.astype(int)
        + angle_active.astype(int)
    ) >= 2

    # individual detections
    t_kappa = sustained_first_crossing(kappa_active, t)
    t_drift = sustained_first_crossing(drift_active, t)
    t_angle = sustained_first_crossing(angle_active, t)
    t_hybrid = sustained_first_crossing(hybrid_active, t)

    # leads
    lead_kappa = compute_lead_time(t_collapse, t_kappa)
    lead_drift = compute_lead_time(t_collapse, t_drift)
    lead_angle = compute_lead_time(t_collapse, t_angle)
    lead_hybrid = compute_lead_time(t_collapse, t_hybrid)

    # --------------------------------------------------------
    # Print results
    # --------------------------------------------------------
    print("\n=== RESULTS ===")
    print(f"scenario:  {kind}")
    print(f"kappa:    {t_kappa} (lead {lead_kappa})")
    print(f"drift:    {t_drift} (lead {lead_drift})")
    print(f"angle:    {t_angle} (lead {lead_angle})")
    print(f"hybrid:   {t_hybrid} (lead {lead_hybrid})")
    print(f"collapse: {t_collapse}")

    print("\nINTERPRETATION:")
    print("- kappa  = local event trigger")
    print("- drift  = motion confirmation")
    print("- angle  = direction confirmation")
    print("- hybrid = confirmed instability warning")

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------
    kappa_n = normalize_signal(kappa)
    drift_n = normalize_signal(drift)
    angle_n = normalize_signal(angle)
    hybrid_n = hybrid_active.astype(float)

    plt.figure(figsize=(12, 6))

    plt.plot(t, V_smooth, color="black", linewidth=2, label="Voltage V(t)")
    plt.plot(t, kappa_n, color="orange", label="kappa(t) — event")
    plt.plot(t, drift_n, color="red", label="drift(t) — motion")
    plt.plot(t, angle_n, color="purple", label="angle(t) — direction")
    plt.plot(t, hybrid_n, color="green", alpha=0.8, label="hybrid active")

    if t_kappa is not None:
        plt.axvline(t_kappa, linestyle=":", color="orange", label="kappa detection")

    if t_drift is not None:
        plt.axvline(t_drift, linestyle="--", color="red", label="drift detection")

    if t_angle is not None:
        plt.axvline(t_angle, linestyle="-.", color="purple", label="angle detection")

    if t_hybrid is not None:
        plt.axvline(
            t_hybrid,
            linestyle="--",
            color="green",
            linewidth=2,
            label="hybrid detection",
        )

    if t_collapse is not None:
        plt.axvline(
            t_collapse,
            linestyle="-",
            color="black",
            linewidth=2,
            label="collapse",
        )

    plt.title("Hybrid Detector — Event + Motion + Direction")
    plt.xlabel("Time (simulation steps)")
    plt.ylabel("Normalized signal")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fig_path = OUT_DIR / "figure_01_hybrid_detector.png"
    plt.savefig(fig_path, dpi=150)

    results = {
        "scenario": kind,
        "t_kappa": t_kappa,
        "t_drift": t_drift,
        "t_angle": t_angle,
        "t_hybrid": t_hybrid,
        "t_collapse": t_collapse,
        "lead_kappa": lead_kappa,
        "lead_drift": lead_drift,
        "lead_angle": lead_angle,
        "lead_hybrid": lead_hybrid,
        "thresholds": {
            "kappa": kappa_th,
            "drift": drift_th,
            "angle": angle_th,
        },
        "rule": "hybrid_active = at least 2 of {kappa, drift, angle} active after transient filter",
        "transient_ignore_fraction": transient_ignore_fraction,
    }

    with open(OUT_DIR / "results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved to: {OUT_DIR}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run_hybrid_detector(kind="nonlinear")
