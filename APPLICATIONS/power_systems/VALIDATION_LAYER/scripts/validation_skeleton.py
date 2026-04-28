import os
import numpy as np
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


def compute_lead_time(t_collapse, t_detection):
    if t_collapse is None or t_detection is None:
        return None
    return t_collapse - t_detection


# ============================================================
# 🔬 SINGLE VALIDATION RUN
# ============================================================

def run_validation(data, scenario_name="scenario"):

    t = np.asarray(data["time"])
    V = np.asarray(data["voltage"])

    # -----------------------------
    # Parameters (FIXED!)
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

    dv_dt = gaussian_filter1d(np.gradient(V_smooth, t), sigma=smooth_sigma)
    d2v_dt2 = gaussian_filter1d(np.gradient(dv_dt, t), sigma=smooth_sigma)

    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T
    mu_stable = np.mean(x[:stable_idx], axis=0)

    # -----------------------------
    # NEXAH signal (curvature)
    # -----------------------------
    dx_dt = np.gradient(x, axis=0)
    d2x_dt2 = np.gradient(dx_dt, axis=0)

    curvature = gaussian_filter1d(
        np.linalg.norm(d2x_dt2, axis=1),
        sigma=smooth_sigma
    )

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

    # -----------------------------
    # Metrics
    # -----------------------------
    width = np.sum(curvature > curvature_threshold) * (t[1] - t[0])

    # 🔥 NEW: Signal-to-noise ratio
    signal_strength = np.max(curvature)
    noise_level = np.std(curvature[:stable_idx])
    snr = signal_strength / (noise_level + 1e-8)

    result = {
        "scenario": scenario_name,
        "lead_classical": lead_classical,
        "lead_nexah": lead_nexah,
        "improvement": (
            lead_nexah - lead_classical
            if (lead_classical is not None and lead_nexah is not None)
            else None
        ),
        "event_width": width,
        "curvature_peak": float(signal_strength),
        "dvdt_min": float(np.min(dv_dt)),
        "snr": float(snr),
    }

    return result


# ============================================================
# 🔁 MULTI SCENARIO RUNNER
# ============================================================

def run_multi_scenarios():

    scenarios = ["smooth", "nonlinear", "noisy"]

    results = []

    for s in scenarios:
        print(f"\n=== RUN: {s} ===")

        data = make_synthetic_scenario(kind=s)
        res = run_validation(data, scenario_name=s)

        print(res)
        results.append(res)

    return results


# ============================================================
# 📊 TABLE OUTPUT
# ============================================================

def print_results_table(results):

    print("\n=== MULTI-SCENARIO RESULTS ===\n")

    header = f"{'Scenario':<12} {'Lead C':<10} {'Lead N':<10} {'Δ':<10} {'Width':<10} {'SNR':<10}"
    print(header)
    print("-" * len(header))

    for r in results:

        def fmt(x):
            return f"{x:.3f}" if x is not None else "None"

        print(
            f"{r['scenario']:<12} "
            f"{fmt(r['lead_classical']):<10} "
            f"{fmt(r['lead_nexah']):<10} "
            f"{fmt(r['improvement']):<10} "
            f"{fmt(r['event_width']):<10} "
            f"{fmt(r['snr']):<10}"
        )


# ============================================================
# 🧪 SCENARIOS
# ============================================================

def make_synthetic_scenario(kind="nonlinear", n=500):
    t = np.linspace(0, 100, n)

    V = 1.0 - 0.002 * t - 0.0005 * t**2

    if kind == "smooth":
        pass

    elif kind == "nonlinear":
        precursor = 0.015 * np.exp((t - 16) / 4.0)
        precursor *= (t < 25)

        oscillation = 0.01 * np.sin(0.8 * t)
        oscillation *= (t < 25)

        V += precursor + oscillation

    elif kind == "noisy":
        rng = np.random.default_rng(7)
        V += 0.01 * rng.normal(size=len(t))

    return {"time": t, "voltage": V}


# ============================================================
# 🚀 MAIN
# ============================================================

if __name__ == "__main__":

    results = run_multi_scenarios()
    print_results_table(results)
