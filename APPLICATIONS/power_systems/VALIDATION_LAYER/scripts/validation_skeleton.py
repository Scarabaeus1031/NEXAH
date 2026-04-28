import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ============================================================
# ⚡ NEXAH Validation Skeleton (Curvature + Flow Field)
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


# ============================================================
# 🔥 NEW: Data-driven Flow Field
# ============================================================

def compute_flow_field(V, dv_dt, t, grid_size=25):
    x = V
    y = dv_dt

    dx = np.gradient(x, t)
    dy = np.gradient(y, t)

    xi = np.linspace(np.min(x), np.max(x), grid_size)
    yi = np.linspace(np.min(y), np.max(y), grid_size)

    U = np.zeros((grid_size, grid_size))
    Vv = np.zeros((grid_size, grid_size))
    counts = np.zeros((grid_size, grid_size))

    for i in range(len(x)):
        ix = np.searchsorted(xi, x[i]) - 1
        iy = np.searchsorted(yi, y[i]) - 1

        if 0 <= ix < grid_size and 0 <= iy < grid_size:
            U[iy, ix] += dx[i]
            Vv[iy, ix] += dy[i]
            counts[iy, ix] += 1

    mask = counts > 0
    U[mask] /= counts[mask]
    Vv[mask] /= counts[mask]

    return xi, yi, U, Vv


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
    # Signals
    # -----------------------------
    distance = np.linalg.norm(x - mu_stable, axis=1)

    d_dist = np.gradient(distance, t)
    d_dist = gaussian_filter1d(d_dist, sigma=smooth_sigma)

    # 🔥 Curvature
    dx_dt = np.gradient(x, axis=0)
    d2x_dt2 = np.gradient(dx_dt, axis=0)

    curvature = np.linalg.norm(d2x_dt2, axis=1)
    curvature = gaussian_filter1d(curvature, sigma=smooth_sigma)

    # -----------------------------
    # Thresholds
    # -----------------------------
    curvature_stable = curvature[:stable_idx]
    curvature_threshold = np.mean(curvature_stable) + 2.0 * np.std(curvature_stable)

    # -----------------------------
    # Detection
    # -----------------------------
    collapse_mask = V_smooth < V_threshold
    classical_mask = dv_dt < dv_threshold
    nexah_mask = curvature > curvature_threshold

    t_collapse = sustained_first_crossing(collapse_mask, t, sustained_samples)
    t_classical = sustained_first_crossing(classical_mask, t, sustained_samples)
    t_nexah = sustained_first_crossing(nexah_mask, t, sustained_samples)

    lead_classical = compute_lead_time(t_collapse, t_classical)
    lead_nexah = compute_lead_time(t_collapse, t_nexah)

    print("\n=== NEXAH CURVATURE + FLOW VALIDATION ===")
    print(f"Scenario:    {scenario_name}")
    print(f"Collapse:    {t_collapse}")
    print(f"Classical:   {t_classical} -> Δt = {lead_classical}")
    print(f"NEXAH(curv): {t_nexah} -> Δt = {lead_nexah}")

    # -----------------------------
    # 🔥 Compute Flow Field
    # -----------------------------
    xi, yi, U, Vv = compute_flow_field(V_smooth, dv_dt, t)
    X, Y = np.meshgrid(xi, yi)

    # -----------------------------
    # Plot
    # -----------------------------
    fig, axs = plt.subplots(4, 1, figsize=(11, 12))

    # Voltage
    axs[0].plot(t, V_smooth)
    axs[0].axhline(V_threshold, linestyle=":")

    if t_collapse:
        axs[0].axvline(t_collapse, linestyle="--", label="Collapse")
    if t_classical:
        axs[0].axvline(t_classical, linestyle="--", label="Classical")
    if t_nexah:
        axs[0].axvline(t_nexah, linestyle="--", label="NEXAH")

    axs[0].set_title("Voltage")
    axs[0].legend()

    # Distance
    axs[1].plot(t, distance)
    axs[1].axvspan(t[0], t[stable_idx], alpha=0.1)
    axs[1].set_title("Distance")

    # Curvature
    axs[2].plot(t, curvature, label="Curvature")
    axs[2].axhline(curvature_threshold, linestyle="--", label="Threshold")

    if t_nexah:
        axs[2].axvline(t_nexah, linestyle="--")

    axs[2].set_title("Curvature (NEXAH Signal)")
    axs[2].legend()

    # 🔥 State Space + Flow Field
    axs[3].quiver(X, Y, U, Vv, alpha=0.4)
    sc = axs[3].scatter(V_smooth, dv_dt, c=curvature, s=8)

    axs[3].set_title("State Space + Local Flow Field")
    axs[3].set_xlabel("Voltage")
    axs[3].set_ylabel("dV/dt")

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
# Scenario
# ============================================================

def make_synthetic_scenario(kind="nonlinear", n=500):
    t = np.linspace(0, 100, n)

    V = 1.0 - 0.002 * t - 0.0005 * t**2

    if kind == "nonlinear":
        precursor = 0.015 * np.exp((t - 16) / 4.0)
        precursor = precursor * (t < 25)

        oscillation = 0.01 * np.sin(0.8 * t)
        oscillation = oscillation * (t < 25)

        V += precursor + oscillation

    elif kind == "noisy":
        rng = np.random.default_rng(7)
        V += 0.01 * rng.normal(size=len(t))

    return {"time": t, "voltage": V}


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    data = make_synthetic_scenario("nonlinear")
    run_validation(data, scenario_name="flow_test")
