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
# Event extraction
# ============================================================

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
# Basin concentration
# ============================================================

def compute_event_concentration(V_smooth, curvature, curvature_threshold, num_bins=10):
    """
    Measures how localized NEXAH events are in state/basin space.

    concentration = max event-bin count / total event count

    High concentration:
        events are localized in few regions

    Low concentration:
        events are spread across many regions
    """

    bins = np.linspace(np.min(V_smooth), np.max(V_smooth), num_bins + 1)
    basin = np.digitize(V_smooth, bins) - 1
    basin = np.clip(basin, 0, num_bins - 1)

    event_mask = curvature > curvature_threshold
    event_basins = basin[event_mask]

    if len(event_basins) == 0:
        return 0.0

    _, counts = np.unique(event_basins, return_counts=True)
    concentration = np.max(counts) / np.sum(counts)

    return float(concentration)


# ============================================================
# SINGLE VALIDATION RUN
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
    # Classical detection
    # -----------------------------
    t_collapse = sustained_first_crossing(V_smooth < V_threshold, t, sustained_samples)
    t_classical = sustained_first_crossing(dv_dt < dv_threshold, t, sustained_samples)

    # -----------------------------
    # Event-based NEXAH detection
    # -----------------------------
    events = extract_events(curvature, curvature_threshold, min_length=3)

    if len(events) > 0:
        start_idx, end_idx, peak = events[0]
        t_nexah = t[start_idx]
        width = t[end_idx] - t[start_idx]
    else:
        t_nexah = None
        width = 0.0

    # -----------------------------
    # Lead times
    # -----------------------------
    lead_classical = compute_lead_time(t_collapse, t_classical)
    lead_nexah = compute_lead_time(t_collapse, t_nexah)

    # -----------------------------
    # Metrics
    # -----------------------------
    signal_strength = np.max(curvature)
    noise_level = np.std(curvature[:stable_idx])
    snr = signal_strength / (noise_level + 1e-8)

    num_events = len(events)

    coherence = 0.0
    if num_events > 0:
        coherence = width / num_events

    concentration = compute_event_concentration(
        V_smooth,
        curvature,
        curvature_threshold,
        num_bins=10
    )

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
        "num_events": num_events,
        "coherence": float(coherence),
        "concentration": float(concentration),
    }

    return result


# ============================================================
# MULTI SCENARIO RUNNER
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
# TABLE OUTPUT
# ============================================================

def print_results_table(results):

    print("\n=== MULTI-SCENARIO RESULTS ===\n")

    header = (
        f"{'Scenario':<12} "
        f"{'Lead C':<10} "
        f"{'Lead N':<10} "
        f"{'Δ':<10} "
        f"{'Width':<10} "
        f"{'Events':<10} "
        f"{'Coh':<10} "
        f"{'Conc':<10} "
        f"{'SNR':<10}"
    )

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
            f"{r['num_events']:<10} "
            f"{fmt(r['coherence']):<10} "
            f"{fmt(r['concentration']):<10} "
            f"{fmt(r['snr']):<10}"
        )


# ============================================================
# SCENARIOS
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
# MAIN
# ============================================================

if __name__ == "__main__":

    results = run_multi_scenarios()
    print_results_table(results)
