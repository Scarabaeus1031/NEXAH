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
# Synthetic scenario (same baseline)
# ============================================================

def make_synthetic_scenario(n=500):
    t = np.linspace(0, 100, n)
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
    V += 0.01 * np.sin(0.8 * t) * (t < 25)

    return t, V


# ============================================================
# STATE + ANGLE
# ============================================================

def compute_state_and_angle(t, V):
    sigma = 2

    V_smooth = gaussian_filter1d(V, sigma=sigma)
    dv_dt = gaussian_filter1d(np.gradient(V_smooth, t), sigma=sigma)
    d2v_dt2 = gaussian_filter1d(np.gradient(dv_dt, t), sigma=sigma)

    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    # velocities (first difference)
    dx = np.diff(x, axis=0)

    # compute angle between consecutive direction vectors
    angles = []

    for i in range(1, len(dx)):
        v1 = dx[i - 1]
        v2 = dx[i]

        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 < 1e-8 or norm2 < 1e-8:
            angles.append(0.0)
            continue

        cos_angle = np.dot(v1, v2) / (norm1 * norm2)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)

        angle = np.arccos(cos_angle)
        angles.append(angle)

    # pad to match length
    angles = np.array([0.0, 0.0] + angles)

    angle_smooth = gaussian_filter1d(angles, sigma=2)

    return V_smooth, angle_smooth


# ============================================================
# MAIN
# ============================================================

def run():
    print("\n=== RUN 012 — ANGLE SIGNAL ANALYSIS ===")

    # -----------------------
    # Data
    # -----------------------
    t, V = make_synthetic_scenario()
    V_smooth, angle = compute_state_and_angle(t, V)

    # -----------------------
    # Threshold
    # -----------------------
    baseline = angle[:100]
    angle_threshold = np.mean(baseline) + 2 * np.std(baseline)

    # -----------------------
    # Detection
    # -----------------------
    V_threshold = 0.7

    t_collapse = sustained_first_crossing(V_smooth < V_threshold, t)
    t_angle = sustained_first_crossing(angle > angle_threshold, t)

    lead_angle = compute_lead_time(t_collapse, t_angle)

    print("\n=== RESULTS ===")
    print(f"t_angle:    {t_angle}")
    print(f"t_collapse: {t_collapse}")
    print(f"Lead (Angle): {lead_angle}")

    # -----------------------
    # Plot
    # -----------------------
    plt.figure(figsize=(10, 5))

    plt.plot(t, V_smooth, label="Voltage V(t)", color="blue")

    # normalize for plotting
    angle_norm = angle / (np.max(angle) + 1e-8)
    plt.plot(t, angle_norm, label="Normalized angle(t)", color="purple")

    if t_angle is not None:
        plt.axvline(t_angle, linestyle="--", color="purple", label="Angle warning")

    if t_collapse is not None:
        plt.axvline(t_collapse, linestyle="-", color="black", label="Collapse")

    plt.title("Angle-Based Early Warning vs Collapse")
    plt.xlabel("Time (simulation steps)")
    plt.ylabel("Signal (normalized)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # -----------------------
    # Save
    # -----------------------
    out_dir = "outputs/run_012_angle_signal"
    os.makedirs(out_dir, exist_ok=True)

    fig_path = os.path.join(out_dir, "figure_01_angle_vs_time.png")
    plt.savefig(fig_path, dpi=150)

    results = {
        "t_angle": t_angle,
        "t_collapse": t_collapse,
        "lead_angle": lead_angle
    }

    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved to: {out_dir}")


# ============================================================

if __name__ == "__main__":
    run()
