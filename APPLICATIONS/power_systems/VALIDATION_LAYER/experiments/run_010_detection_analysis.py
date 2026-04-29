import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ============================================================
# Core utils
# ============================================================

def sustained_first_crossing(mask, t, min_samples=3):
    mask = np.asarray(mask, dtype=bool)
    for i in range(0, len(mask) - min_samples + 1):
        if np.all(mask[i:i + min_samples]):
            return t[i]
    return None


def extract_events(signal, threshold, min_length=3):
    mask = signal > threshold
    events = []
    i = 0

    while i < len(mask):
        if mask[i]:
            start = i
            while i < len(mask) and mask[i]:
                i += 1
            end = i

            if end - start >= min_length:
                peak = np.max(signal[start:end])
                events.append((start, end, peak))
        else:
            i += 1

    return events


# ============================================================
# Synthetic scenario
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

    return {"time": t, "voltage": V}


# ============================================================
# Detection analysis
# ============================================================

def run_detection_analysis(data):

    t = np.asarray(data["time"])
    V = np.asarray(data["voltage"])

    V_threshold = 0.7
    dv_threshold = -0.02
    sigma = 2

    V_smooth = gaussian_filter1d(V, sigma=sigma)
    dv_dt = gaussian_filter1d(np.gradient(V_smooth, t), sigma=sigma)

    x = np.vstack([
        V_smooth,
        dv_dt,
        gaussian_filter1d(np.gradient(dv_dt, t), sigma=sigma)
    ]).T

    curvature = gaussian_filter1d(
        np.linalg.norm(np.gradient(np.gradient(x, axis=0), axis=0), axis=1),
        sigma=sigma
    )

    stable_idx = int(0.3 * len(t))
    threshold = np.mean(curvature[:stable_idx]) + 2 * np.std(curvature[:stable_idx])

    # detections
    t_collapse = sustained_first_crossing(V_smooth < V_threshold, t)
    t_classical = sustained_first_crossing(dv_dt < dv_threshold, t)

    events = extract_events(curvature, threshold)
    t_nexah = t[events[0][0]] if events else None

    return t, V_smooth, curvature, t_nexah, t_classical, t_collapse


# ============================================================
# Plot
# ============================================================

def plot_detection(t, V, curvature, t_nexah, t_classical, t_collapse):

    plt.figure(figsize=(10, 5))

    plt.plot(t, V, label="Voltage V(t)", linewidth=2)
    plt.plot(t, curvature / np.max(curvature), label="Normalized κ(t)", alpha=0.7)

    if t_nexah is not None:
        plt.axvline(t_nexah, linestyle="--", label="NEXAH (event)")

    if t_classical is not None:
        plt.axvline(t_classical, linestyle="--", label="Classical (dv/dt)")

    if t_collapse is not None:
        plt.axvline(t_collapse, linestyle="-", linewidth=2, label="Collapse")

    plt.title("Detection Timeline — Event vs Instability")
    plt.xlabel("Time (simulation steps)")
    plt.ylabel("Signal (normalized)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n=== RUN 010 — DETECTION ANALYSIS ===")

    data = make_synthetic_scenario("nonlinear")

    t, V, curvature, t_nexah, t_classical, t_collapse = run_detection_analysis(data)

    plot_detection(t, V, curvature, t_nexah, t_classical, t_collapse)

    print("\n=== RESULTS ===")
    print(f"t_nexah:     {t_nexah}")
    print(f"t_classical: {t_classical}")
    print(f"t_collapse:  {t_collapse}")

    if t_collapse:
        if t_nexah:
            print("Lead (NEXAH):", t_collapse - t_nexah)
        if t_classical:
            print("Lead (Classical):", t_collapse - t_classical)

    print("\nINTERPRETATION:")
    print("- NEXAH detects local curvature events")
    print("- Classical detects slope-based changes")
    print("- Both may coincide for local instabilities")
    print("- Global instability detection requires drift-based signals")
