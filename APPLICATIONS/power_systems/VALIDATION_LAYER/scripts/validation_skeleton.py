import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

# =========================================
# ⚡ NEXAH Validation Skeleton
# =========================================

# -----------------------------------------
# INPUT (hook to your pipeline)
# -----------------------------------------
# Expected structure:
# data = {
#     "time": np.array,
#     "voltage": np.array
# }

def run_validation(data):

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
    # smoothing to avoid unfair dv/dt noise
    V_smooth = gaussian_filter1d(V, sigma=2)

    dv_dt = np.gradient(V_smooth, t)
    d2v_dt2 = np.gradient(dv_dt, t)

    # -----------------------------------------
    # NEXAH STATE
    # -----------------------------------------
    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    # stable reference
    mu_stable = np.mean(x[:stable_idx], axis=0)

    # distance signal
    distance = np.linalg.norm(x - mu_stable, axis=1)

    # fixed threshold (no tuning!)
    dist_mean = np.mean(distance)
    dist_std = np.std(distance)
    dist_threshold = dist_mean + 2 * dist_std

    # -----------------------------------------
    # DETECTION FUNCTIONS
    # -----------------------------------------
    def first_crossing(signal, condition):
        idx = np.where(condition(signal))[0]
        return t[idx[0]] if len(idx) > 0 else None

    # collapse
    t_collapse = first_crossing(V, lambda x: x < V_threshold)

    # classical
    t_classical = first_crossing(dv_dt, lambda x: x < dv_threshold)

    # NEXAH
    t_nexah = first_crossing(distance, lambda x: x > dist_threshold)

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
    # PLOT 1 — Voltage
    # -----------------------------------------
    plt.figure()
    plt.plot(t, V, label="Voltage")

    if t_collapse:
        plt.axvline(t_collapse, linestyle="--", label="Collapse")

    if t_classical:
        plt.axvline(t_classical, linestyle="--", label="Classical")

    if t_nexah:
        plt.axvline(t_nexah, linestyle="--", label="NEXAH")

    plt.title("Voltage + Detection")
    plt.legend()

    # -----------------------------------------
    # PLOT 2 — Distance (NEXAH Signal)
    # -----------------------------------------
    plt.figure()
    plt.plot(t, distance, label="Distance")
    plt.axhline(dist_threshold, linestyle="--", label="Threshold")

    if t_nexah:
        plt.axvline(t_nexah, linestyle="--", label="NEXAH detection")

    plt.title("NEXAH Distance Signal")
    plt.legend()

    # -----------------------------------------
    # PLOT 3 — State Space
    # -----------------------------------------
    plt.figure()
    plt.scatter(V_smooth, dv_dt, c=t, s=5)

    plt.xlabel("Voltage")
    plt.ylabel("dV/dt")
    plt.title("State Space (Trajectory)")

    plt.colorbar(label="Time")

    # -----------------------------------------
    # OPTIONAL — Golden Line Plot
    # -----------------------------------------
    plt.figure()

    y = [1, 1, 1]
    x_vals = []

    labels = []

    if t_classical:
        x_vals.append(t_classical)
        labels.append("Classical")

    if t_nexah:
        x_vals.append(t_nexah)
        labels.append("NEXAH")

    if t_collapse:
        x_vals.append(t_collapse)
        labels.append("Collapse")

    for xv, label in zip(x_vals, labels):
        plt.axvline(xv, linestyle="--", label=label)

    plt.yticks([])
    plt.title("Golden Line — Detection Timing")
    plt.legend()

    plt.show()

    # -----------------------------------------
    # RETURN RESULTS
    # -----------------------------------------
    return {
        "t_collapse": t_collapse,
        "t_classical": t_classical,
        "t_nexah": t_nexah,
        "lead_classical": lead_classical,
        "lead_nexah": lead_nexah,
    }


# =========================================
# EXAMPLE USAGE (replace with your loader)
# =========================================
if __name__ == "__main__":

    # Dummy example (replace!)
    t = np.linspace(0, 100, 500)
    V = 1.0 - 0.002*t - 0.0005*t**2  # artificial collapse

    data = {
        "time": t,
        "voltage": V
    }

    run_validation(data)
