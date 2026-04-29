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
# Synthetic scenario (same as before)
# ============================================================

def make_synthetic_scenario(n=500):
    t = np.linspace(0, 100, n)
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    # add nonlinear bump (pre-collapse instability)
    V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
    V += 0.01 * np.sin(0.8 * t) * (t < 25)

    return t, V


# ============================================================
# Drift / motion signal
# ============================================================

def compute_state_and_drift(t, V):
    sigma = 2

    V_smooth = gaussian_filter1d(V, sigma=sigma)
    dv_dt = gaussian_filter1d(np.gradient(V_smooth, t), sigma=sigma)
    d2v_dt2 = gaussian_filter1d(np.gradient(dv_dt, t), sigma=sigma)

    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    # drift = movement in state space
    dx = np.diff(x, axis=0)
    drift = np.linalg.norm(dx, axis=1)

    # pad to same length
    drift = np.concatenate([[0], drift])

    drift_smooth = gaussian_filter1d(drift, sigma=2)

    return V_smooth, drift_smooth


# ============================================================
# MAIN
# ============================================================

def run():
    print("\n=== RUN 011 — DRIFT SIGNAL ANALYSIS ===")

    # -----------------------
    # Data
    # -----------------------
    t, V = make_synthetic_scenario()

    V_smooth, drift = compute_state_and_drift(t, V)

    # -----------------------
    # Thresholds
    # -----------------------
    V_threshold = 0.7
    drift_threshold = np.mean(drift[:100]) + 2 * np.std(drift[:100])

    # -----------------------
    # Detection
    # -----------------------
    t_collapse = sustained_first_crossing(V_smooth < V_threshold, t)
    t_drift = sustained_first_crossing(drift > drift_threshold, t)

    lead_drift = compute_lead_time(t_collapse, t_drift)

    print("\n=== RESULTS ===")
    print(f"t_drift:    {t_drift}")
    print(f"t_collapse: {t_collapse}")
    print(f"Lead (Drift): {lead_drift}")

    # -----------------------
    # Plot
    # -----------------------
    plt.figure(figsize=(10, 5))

    plt.plot(t, V_smooth, label="Voltage V(t)", color="blue")
    plt.plot(t, drift / np.max(drift), label="Normalized drift(t)", color="red")

    if t_drift is not None:
        plt.axvline(t_drift, linestyle="--", label="Drift warning", color="red")

    if t_collapse is not None:
        plt.axvline(t_collapse, linestyle="-", label="Collapse", color="black")

    plt.title("Drift-Based Early Warning vs Collapse")
    plt.xlabel("Time (simulation steps)")
    plt.ylabel("Signal (normalized)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # -----------------------
    # Save outputs
    # -----------------------
    out_dir = "outputs/run_011_drift_signal"
    os.makedirs(out_dir, exist_ok=True)

    fig_path = os.path.join(out_dir, "figure_01_drift_vs_time.png")
    plt.savefig(fig_path, dpi=150)

    results = {
        "t_drift": t_drift,
        "t_collapse": t_collapse,
        "lead_drift": lead_drift
    }

    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved to: {out_dir}")


# ============================================================

if __name__ == "__main__":
    run()
