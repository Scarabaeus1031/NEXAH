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
# 🔥 Data-driven Flow Field
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
    mu_stable = np.mean(x[:stable_idx], axis=0)

    # -----------------------------
    # Signals
    # -----------------------------
    distance = np.linalg.norm(x - mu_stable, axis=1)

    dx_dt = np.gradient(x, axis=0)
    d2x_dt2 = np.gradient(dx_dt, axis=0)

    curvature = np.linalg.norm(d2x_dt2, axis=1)
    curvature = gaussian_filter1d(curvature, sigma=smooth_sigma)

    # -----------------------------
    # Thresholds
    # -----------------------------
    curvature_threshold = (
        np.mean(curvature[:stable_idx]) +
        2.0 * np.std(curvature[:stable_idx])
    )

    # -----------------------------
    # Detection
    # -----------------------------
    t_collapse = sustained_first_crossing(V_smooth < V_threshold, t, sustained_samples)
    t_classical = sustained_first_crossing(dv_dt < dv_threshold, t, sustained_samples)
    t_nexah = sustained_first_crossing(curvature > curvature_threshold, t, sustained_samples)

    lead_classical = compute_lead_time(t_collapse, t_classical)
    lead_nexah = compute_lead_time(t_collapse, t_nexah)

    print("\n=== NEXAH VALIDATION ===")
    print(f"Collapse:    {t_collapse}")
    print(f"Classical:   {t_classical} → Δt = {lead_classical}")
    print(f"NEXAH:       {t_nexah} → Δt = {lead_nexah}")

    # -----------------------------
    # Flow Field
    # -----------------------------
    xi, yi, U, Vv = compute_flow_field(V_smooth, dv_dt, t)
    X, Y = np.meshgrid(xi, yi)

    # -----------------------------
    # PAPER FIGURE
    # -----------------------------
    fig, axs = plt.subplots(3, 1, figsize=(10, 10))

    # Panel A — Signal comparison
    axs[0].plot(t, dv_dt, label="dv/dt", alpha=0.7)
    axs[0].plot(t, curvature, label="curvature", linewidth=2)

    axs[0].axhline(dv_threshold, linestyle=":", label="dv/dt threshold")
    axs[0].axhline(curvature_threshold, linestyle="--", label="curvature threshold")

    if t_classical:
        axs[0].axvline(t_classical, linestyle=":", label="classical detect")
    if t_nexah:
        axs[0].axvline(t_nexah, linestyle="--", label="NEXAH detect")
    if t_collapse:
        axs[0].axvline(t_collapse, linestyle="-.", label="collapse")

    axs[0].set_title("Signal Comparison")
    axs[0].legend()

    # Panel B — State space
    sc = axs[1].scatter(V_smooth, dv_dt, c=curvature, s=10)
    axs[1].set_title("State Space")
    axs[1].set_xlabel("Voltage")
    axs[1].set_ylabel("dV/dt")
    plt.colorbar(sc, ax=axs[1])

    # Panel C — Flow (zoom)
    mask = (V_smooth > 0.3) & (V_smooth < 1.1)

    axs[2].quiver(X, Y, U, Vv, alpha=0.4)
    axs[2].scatter(V_smooth[mask], dv_dt[mask], c=curvature[mask], s=15)

    axs[2].set_title("Flow Field (Transition Corridor)")
    axs[2].set_xlabel("Voltage")
    axs[2].set_ylabel("dV/dt")

    plt.tight_layout()
    plt.show()

    # -----------------------------
    # METRICS
    # -----------------------------
    print("\n--- METRICS ---")

    print(f"Lead Classical: {lead_classical}")
    print(f"Lead NEXAH:     {lead_nexah}")

    if lead_classical and lead_nexah:
        print(f"Improvement:    {lead_nexah - lead_classical}")

    print(f"Curvature peak: {np.max(curvature)}")
    print(f"dv/dt min:      {np.min(dv_dt)}")

    width = np.sum(curvature > curvature_threshold) * (t[1] - t[0])
    print(f"Event width:    {width:.2f}")

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
        precursor *= (t < 25)

        oscillation = 0.01 * np.sin(0.8 * t)
        oscillation *= (t < 25)

        V += precursor + oscillation

    return {"time": t, "voltage": V}


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    data = make_synthetic_scenario("nonlinear")
    run_validation(data, scenario_name="final_validation")
