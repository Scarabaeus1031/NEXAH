import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

# =========================================
# ⚡ NEXAH Validation Skeleton (v2)
# - includes EARLY SIGNAL FIX (d/dt distance)
# =========================================

def run_validation(data):

    # -----------------------------------------
    # INPUT
    # -----------------------------------------
    t = data["time"]
    V = data["voltage"]

    # -----------------------------------------
    # PARAMETERS (FIXED — no tuning)
    # -----------------------------------------
    V_threshold = 0.7
    dv_threshold = -0.02

    # stable window (first 30%)
    stable_idx = int(0.3 * len(t))

    # -----------------------------------------
    # FEATURE EXTRACTION
    # -----------------------------------------
    V_smooth = gaussian_filter1d(V, sigma=2)

    dv_dt = np.gradient(V_smooth, t)
    dv_dt = gaussian_filter1d(dv_dt, sigma=2)

    d2v_dt2 = np.gradient(dv_dt, t)

    # -----------------------------------------
    # NEXAH STATE
    # -----------------------------------------
    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    # stable reference
    mu_stable = np.mean(x[:stable_idx], axis=0)

    # distance signal
    distance = np.linalg.norm(x - mu_stable, axis=1)

    # -----------------------------------------
    # 🔥 EARLY WARNING SIGNAL (KEY FIX)
    # -----------------------------------------
    d_dist = np.gradient(distance, t)
    d_dist = gaussian_filter1d(d_dist, sigma=2)

    # threshold (fixed)
    dd_mean = np.mean(d_dist)
    dd_std = np.std(d_dist)
    dd_threshold = dd_mean + 2 * dd_std

    # -----------------------------------------
    # DETECTION FUNCTIONS
    # -----------------------------------------
    def first_crossing(signal, condition):
        idx = np.where(condition(signal))[0]
        return t[idx[0]] if len(idx) > 0 else None

    # collapse (ground truth)
    t_collapse = first_crossing(V, lambda x: x < V_threshold)

    # classical detection
    t_classical = first_crossing(dv_dt, lambda x: x < dv_threshold)

    # NEXAH detection (NEW)
    t_nexah = first_crossing(d_dist, lambda x: x > dd_threshold)

    # -----------------------------------------
    # LEAD TIMES
    # -----------------------------------------
    def compute_lead(t_det):
        if t_det is None or t_collapse is None:
            return None
        return t_collapse - t_det

    lead_classical = compute_lead(t_classical)
    lead_nexah = compute_lead(t_nexah)

    print("\n=== LEAD TIMES ===")
    print(f"Collapse:   {t_collapse}")
    print(f"Classical:  {t_classical} → Δt = {lead_classical}")
    print(f"NEXAH:      {t_nexah} → Δt = {lead_nexah}")

    # -----------------------------------------
    # PLOT — GOLDEN FIGURE
    # -----------------------------------------
    fig, axs = plt.subplots(4, 1, figsize=(10, 12))

    # (1) Voltage
    axs[0].plot(t, V)
    axs[0].set_title("Voltage V(t)")

    if t_collapse:
        axs[0].axvline(t_collapse, linestyle="--", label="Collapse")
    if t_classical:
        axs[0].axvline(t_classical, linestyle="--", label="Classical")
    if t_nexah:
        axs[0].axvline(t_nexah, linestyle="--", label="NEXAH")

    axs[0].legend()

    # (2) Distance
    axs[1].plot(t, distance)
    axs[1].set_title("Distance to Stable Region")

    # (3) Distance Derivative (KEY)
    axs[2].plot(t, d_dist)
    axs[2].axhline(dd_threshold, linestyle="--", label="Threshold")

    if t_nexah:
        axs[2].axvline(t_nexah, linestyle="--", label="NEXAH")

    axs[2].set_title("d/dt Distance (Early Warning)")
    axs[2].legend()

    # (4) State Space
    sc = axs[3].scatter(V_smooth, dv_dt, c=d_dist, s=6)
    axs[3].set_xlabel("Voltage")
    axs[3].set_ylabel("dV/dt")
    axs[3].set_title("State Space (colored by d/dt distance)")

    plt.colorbar(sc, ax=axs[3])

    plt.tight_layout()
    plt.show()

    # -----------------------------------------
    # RETURN
    # -----------------------------------------
    return {
        "t_collapse": t_collapse,
        "t_classical": t_classical,
        "t_nexah": t_nexah,
        "lead_classical": lead_classical,
        "lead_nexah": lead_nexah,
    }


# =========================================
# TEST RUN (replace with real data)
# =========================================
if __name__ == "__main__":

    t = np.linspace(0, 100, 500)

    # synthetic collapse
    V = 1.0 - 0.002*t - 0.0005*t**2

    data = {
        "time": t,
        "voltage": V
    }

    run_validation(data)
