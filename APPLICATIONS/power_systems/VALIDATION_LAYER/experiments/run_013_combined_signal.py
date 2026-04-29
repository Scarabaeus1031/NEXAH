import os
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ============================================================
# Utils
# ============================================================

def sustained_first_crossing(mask, t, min_samples=3):
    mask = np.asarray(mask, dtype=bool)
    for i in range(0, len(mask) - min_samples + 1):
        if np.all(mask[i:i + min_samples]):
            return t[i]
    return None


def compute_lead_time(t_collapse, t_detection):
    if t_collapse is None or t_detection is None:
        return None
    return t_collapse - t_detection


# ============================================================
# Scenario
# ============================================================

def make_synthetic_scenario(n=500):
    t = np.linspace(0, 100, n)
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
    V += 0.01 * np.sin(0.8 * t) * (t < 25)

    return t, V


# ============================================================
# SIGNALS
# ============================================================

def compute_signals(t, V):
    sigma = 2

    V_smooth = gaussian_filter1d(V, sigma=sigma)
    dv_dt = gaussian_filter1d(np.gradient(V_smooth, t), sigma=sigma)
    d2v_dt2 = gaussian_filter1d(np.gradient(dv_dt, t), sigma=sigma)

    # state
    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    # --------------------------------------------------------
    # Curvature κ(t)
    # --------------------------------------------------------
    curvature = gaussian_filter1d(
        np.linalg.norm(np.gradient(np.gradient(x, axis=0), axis=0), axis=1),
        sigma=sigma
    )

    # --------------------------------------------------------
    # Drift (movement)
    # --------------------------------------------------------
    dx = np.diff(x, axis=0)
    drift = np.linalg.norm(dx, axis=1)
    drift = np.concatenate([[0], drift])
    drift = gaussian_filter1d(drift, sigma=2)

    # --------------------------------------------------------
    # Angle (direction change)
    # --------------------------------------------------------
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

    angles = np.array([0.0, 0.0] + angles)
    angles = gaussian_filter1d(angles, sigma=2)

    return V_smooth, curvature, drift, angles


# ============================================================
# MAIN
# ============================================================

def run():
    print("\n=== RUN 013 — COMBINED SIGNAL ANALYSIS ===")

    t, V = make_synthetic_scenario()

    V_smooth, kappa, drift, angle = compute_signals(t, V)

    # --------------------------------------------------------
    # Thresholds
    # --------------------------------------------------------
    base = slice(0, 100)

    kappa_th = np.mean(kappa[base]) + 2 * np.std(kappa[base])
    drift_th = np.mean(drift[base]) + 2 * np.std(drift[base])
    angle_th = np.mean(angle[base]) + 2 * np.std(angle[base])

    # --------------------------------------------------------
    # Collapse
    # --------------------------------------------------------
    V_threshold = 0.7
    t_collapse = sustained_first_crossing(V_smooth < V_threshold, t)

    # --------------------------------------------------------
    # Detection (with angle transient filter!)
    # --------------------------------------------------------
    start_idx = int(0.2 * len(t))
    valid_mask = np.arange(len(t)) > start_idx

    t_kappa = sustained_first_crossing(kappa > kappa_th, t)
    t_drift = sustained_first_crossing(drift > drift_th, t)
    t_angle = sustained_first_crossing((angle > angle_th) & valid_mask, t)

    # --------------------------------------------------------
    # Leads
    # --------------------------------------------------------
    lead_kappa = compute_lead_time(t_collapse, t_kappa)
    lead_drift = compute_lead_time(t_collapse, t_drift)
    lead_angle = compute_lead_time(t_collapse, t_angle)

    print("\n=== RESULTS ===")
    print(f"kappa: {t_kappa} (lead {lead_kappa})")
    print(f"drift: {t_drift} (lead {lead_drift})")
    print(f"angle: {t_angle} (lead {lead_angle})")
    print(f"collapse: {t_collapse}")

    # --------------------------------------------------------
    # Normalize for plotting
    # --------------------------------------------------------
    def norm(x):
        return x / (np.max(x) + 1e-8)

    kappa_n = norm(kappa)
    drift_n = norm(drift)
    angle_n = norm(angle)

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------
    plt.figure(figsize=(12, 6))

    plt.plot(t, V_smooth, label="Voltage V(t)", color="black", linewidth=2)

    plt.plot(t, kappa_n, label="κ(t) — event", color="orange")
    plt.plot(t, drift_n, label="drift(t) — motion", color="red")
    plt.plot(t, angle_n, label="angle(t) — direction", color="purple")

    if t_kappa:
        plt.axvline(t_kappa, linestyle=":", color="orange", label="κ detection")

    if t_drift:
        plt.axvline(t_drift, linestyle="--", color="red", label="drift detection")

    if t_angle:
        plt.axvline(t_angle, linestyle="-.", color="purple", label="angle detection")

    if t_collapse:
        plt.axvline(t_collapse, linestyle="-", color="black", label="collapse")

    plt.title("Combined Signals — Event vs Motion vs Direction")
    plt.xlabel("Time (simulation steps)")
    plt.ylabel("Normalized signal")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------
    out_dir = "outputs/run_013_combined_signal"
    os.makedirs(out_dir, exist_ok=True)

    plt.savefig(os.path.join(out_dir, "figure_01_combined.png"), dpi=150)

    results = {
        "t_kappa": t_kappa,
        "t_drift": t_drift,
        "t_angle": t_angle,
        "t_collapse": t_collapse,
        "lead_kappa": lead_kappa,
        "lead_drift": lead_drift,
        "lead_angle": lead_angle
    }

    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved to: {out_dir}")


# ============================================================

if __name__ == "__main__":
    run()
