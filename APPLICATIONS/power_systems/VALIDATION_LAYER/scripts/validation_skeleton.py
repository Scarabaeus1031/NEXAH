import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ============================================================
# ⚡ NEXAH Validation Skeleton (Curvature Upgrade)
# ============================================================


def sustained_first_crossing(mask, t, min_samples=3):
    mask = np.asarray(mask, dtype=bool)

    if min_samples <= 1:
        idx = np.where(mask)[0]
        return t[idx[0]] if len(idx) > 0 else None

    for i in range(0, len(mask) - min_samples + 1):
        if np.all(mask[i:i + min_samples]):
            return t[i]

    return None


def compute_lead_time(t_collapse, t_detection):
    if t_collapse is None or t_detection is None:
        return None
    return t_collapse - t_detection


def run_validation(data,
                   output_dir="APPLICATIONS/power_systems/VALIDATION_LAYER/outputs",
                   scenario_name="synthetic_validation"):

    t = np.asarray(data["time"])
    V = np.asarray(data["voltage"])

    os.makedirs(output_dir, exist_ok=True)

    # -----------------------------
    # Parameters
    # -----------------------------
    V_threshold = 0.7
    dv_threshold = -0.02

    stable_fraction = 0.30
    smooth_sigma = 2
    sustained_samples = 3

    stable_idx = int(stable_fraction * len(t))

    # -----------------------------
    # Features
    # -----------------------------
    V_smooth = gaussian_filter1d(V, sigma=smooth_sigma)

    dv_dt = np.gradient(V_smooth, t)
    dv_dt = gaussian_filter1d(dv_dt, sigma=smooth_sigma)

    d2v_dt2 = np.gradient(dv_dt, t)
    d2v_dt2 = gaussian_filter1d(d2v_dt2, sigma=smooth_sigma)

    # -----------------------------
    # State
    # -----------------------------
    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    x_stable = x[:stable_idx]
    mu_stable = np.mean(x_stable, axis=0)

    # -----------------------------
    # Distance (baseline signal)
    # -----------------------------
    distance = np.linalg.norm(x - mu_stable, axis=1)

    d_dist = np.gradient(distance, t)
    d_dist = gaussian_filter1d(d_dist, sigma=smooth_sigma)

    # -----------------------------
    # 🔥 NEW: Curvature Signal
    # -----------------------------
    dx_dt = np.gradient(x, axis=0)
    d2x_dt2 = np.gradient(dx_dt, axis=0)

    curvature = np.linalg.norm(d2x_dt2, axis=1)
    curvature = gaussian_filter1d(curvature, sigma=smooth_sigma)

    # -----------------------------
    # Thresholds (ONLY stable region!)
    # -----------------------------
    curvature_stable = curvature[:stable_idx]

    curvature_threshold = (
        np.mean(curvature_stable)
        + 2.0 * np.std(curvature_stable)
    )

    # -----------------------------
    # Detection
    # -----------------------------
    collapse_mask = V_smooth < V_threshold
    classical_mask = dv_dt < dv_threshold
    nexah_mask = curvature > curvature_threshold  # ← KEY CHANGE

    t_collapse = sustained_first_crossing(collapse_mask, t, sustained_samples)
    t_classical = sustained_first_crossing(classical_mask, t, sustained_samples)
    t_nexah = sustained_first_crossing(nexah_mask, t, sustained_samples)

    lead_classical = compute_lead_time(t_collapse, t_classical)
    lead_nexah = compute_lead_time(t_collapse, t_nexah)

    # -----------------------------
    # Output
    # -----------------------------
    print("\n=== NEXAH CURVATURE VALIDATION ===")
    print(f"Scenario:    {scenario_name}")
    print(f"Collapse:    {t_collapse}")
    print(f"Classical:   {t_classical} -> Δt = {lead_classical}")
    print(f"NEXAH(curv): {t_nexah} -> Δt = {lead_nexah}")

    # -----------------------------
    # Plot
    # -----------------------------
    fig, axs = plt.subplots(4, 1, figsize=(11, 12))

    # Voltage
    axs[0].plot(t, V_smooth)
    axs[0].axhline(V_threshold, linestyle=":")

    if t_collapse:
        axs[0].axvline(t_collapse, linestyle="--")
    if t_classical:
        axs[0].axvline(t_classical, linestyle="--")
    if t_nexah:
        axs[0].axvline(t_nexah, linestyle="--")

    axs[0].set_title("Voltage")

    # Distance
    axs[1].plot(t, distance)
    axs[1].axvspan(t[0], t[stable_idx], alpha=0.1)
    axs[1].set_title("Distance")

    # Curvature (NEW CORE)
    axs[2].plot(t, curvature)
    axs[2].axhline(curvature_threshold, linestyle="--")

    if t_nexah:
        axs[2].axvline(t_nexah, linestyle="--")

    axs[2].set_title("Curvature (NEXAH Signal)")

    # State space
    sc = axs[3].scatter(V_smooth, dv_dt, c=curvature, s=8)
    axs[3].set_title("State Space (colored by curvature)")

    plt.colorbar(sc, ax=axs[3])

    plt.tight_layout()
    plt.show()

    return {
        "t_collapse": t_collapse,
        "t_classical": t_classical,
        "t_nexah": t_nexah,
        "lead_classical": lead_classical,
        "lead_nexah": lead_nexah,
    }


# ============================================================
# Synthetic scenarios
# ============================================================

def make_synthetic_scenario(kind="precursor", n=500):
    t = np.linspace(0, 100, n)

    V = 1.0 - 0.002 * t - 0.0005 * t**2

    if kind == "precursor":
        precursor = 0.02 * np.exp((t - 18) / 5.0)
        precursor = precursor * (t < 25)
        V += precursor

    return {"time": t, "voltage": V}


if __name__ == "__main__":
    data = make_synthetic_scenario("precursor")
    run_validation(data, scenario_name="curvature_test")
