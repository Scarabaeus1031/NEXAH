import os
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


def compute_lead_time(t_collapse, t_detection):
    if t_collapse is None or t_detection is None:
        return None
    return t_collapse - t_detection


# ============================================================
# 🔥 Event extraction
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
# 🔥 NEW: Event Shape Features
# ============================================================

def extract_event_shapes(t, curvature, events):
    shapes = []
    features = []

    for (start, end, peak) in events:
        segment = curvature[start:end]

        if len(segment) < 5:
            continue

        # normalize
        seg_norm = segment / (np.max(segment) + 1e-8)
        t_norm = np.linspace(0, 1, len(segment))

        shapes.append((t_norm, seg_norm))

        # --- FEATURES ---
        entry_slope = seg_norm[1] - seg_norm[0]
        exit_slope = seg_norm[-1] - seg_norm[-2]

        peak_idx = np.argmax(seg_norm)
        peak_pos = peak_idx / len(seg_norm)

        left_energy = np.sum(seg_norm[:peak_idx])
        right_energy = np.sum(seg_norm[peak_idx:])
        symmetry = left_energy / (right_energy + 1e-8)

        features.append({
            "entry_slope": entry_slope,
            "exit_slope": exit_slope,
            "peak_pos": peak_pos,
            "symmetry": symmetry
        })

    return shapes, features


def aggregate_shape_features(features):

    if len(features) == 0:
        return {
            "entry_slope_mean": 0,
            "exit_slope_mean": 0,
            "peak_pos_mean": 0,
            "symmetry_mean": 0
        }

    return {
        "entry_slope_mean": np.mean([f["entry_slope"] for f in features]),
        "exit_slope_mean": np.mean([f["exit_slope"] for f in features]),
        "peak_pos_mean": np.mean([f["peak_pos"] for f in features]),
        "symmetry_mean": np.mean([f["symmetry"] for f in features])
    }


def plot_event_overlay(all_shapes):
    plt.figure(figsize=(8, 5))

    for label, shapes in all_shapes.items():
        for t_norm, seg_norm in shapes:
            plt.plot(t_norm, seg_norm, alpha=0.4, label=label)

    handles, labels = plt.gca().get_legend_handles_labels()
    unique = dict(zip(labels, handles))

    plt.legend(unique.values(), unique.keys())

    plt.title("NEXAH Event Shape Overlay")
    plt.xlabel("Normalized Time (0 → 1)")
    plt.ylabel("Normalized Curvature")
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()


# ============================================================
# 🔬 SINGLE VALIDATION RUN
# ============================================================

def run_validation(data, scenario_name="scenario"):

    t = np.asarray(data["time"])
    V = np.asarray(data["voltage"])

    # Parameters
    V_threshold = 0.7
    dv_threshold = -0.02
    stable_fraction = 0.30
    smooth_sigma = 2
    sustained_samples = 3

    stable_idx = int(stable_fraction * len(t))

    # Features
    V_smooth = gaussian_filter1d(V, sigma=smooth_sigma)

    dv_dt = gaussian_filter1d(np.gradient(V_smooth, t), sigma=smooth_sigma)
    d2v_dt2 = gaussian_filter1d(np.gradient(dv_dt, t), sigma=smooth_sigma)

    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    # Curvature
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

    # Classical detection
    t_collapse = sustained_first_crossing(V_smooth < V_threshold, t, sustained_samples)
    t_classical = sustained_first_crossing(dv_dt < dv_threshold, t, sustained_samples)

    # NEXAH events
    events = extract_events(curvature, curvature_threshold, min_length=3)

    if len(events) > 0:
        start_idx, end_idx, peak = events[0]
        t_nexah = t[start_idx]
        width = t[end_idx] - t[start_idx]
    else:
        t_nexah = None
        width = 0.0

    # Leads
    lead_classical = compute_lead_time(t_collapse, t_classical)
    lead_nexah = compute_lead_time(t_collapse, t_nexah)

    # Metrics
    signal_strength = np.max(curvature)
    noise_level = np.std(curvature[:stable_idx])
    snr = signal_strength / (noise_level + 1e-8)

    num_events = len(events)
    coherence = width / num_events if num_events > 0 else 0.0
    concentration = width / (len(t) * (t[1] - t[0]))

    # 🔥 NEW: SHAPE FEATURES
    shapes, shape_features = extract_event_shapes(t, curvature, events)
    shape_summary = aggregate_shape_features(shape_features)

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
        "snr": float(snr),
        "num_events": num_events,
        "coherence": coherence,
        "concentration": concentration,
        **shape_summary
    }

    return result, shapes


# ============================================================
# MULTI RUN
# ============================================================

def run_multi_scenarios():

    scenarios = ["smooth", "nonlinear", "noisy"]

    results = []
    all_shapes = {}

    for s in scenarios:
        print(f"\n=== RUN: {s} ===")

        data = make_synthetic_scenario(kind=s)
        res, shapes = run_validation(data, scenario_name=s)

        print(res)
        results.append(res)
        all_shapes[s] = shapes

    return results, all_shapes


# ============================================================
# TABLE
# ============================================================

def print_results_table(results):

    print("\n=== MULTI-SCENARIO RESULTS ===\n")

    header = f"{'Scenario':<12} {'Δ':<10} {'Events':<8} {'Coh':<8} {'PeakPos':<10} {'Sym':<10}"
    print(header)
    print("-" * len(header))

    for r in results:

        def fmt(x):
            return f"{x:.3f}" if x is not None else "None"

        print(
            f"{r['scenario']:<12} "
            f"{fmt(r['improvement']):<10} "
            f"{r['num_events']:<8} "
            f"{fmt(r['coherence']):<8} "
            f"{fmt(r['peak_pos_mean']):<10} "
            f"{fmt(r['symmetry_mean']):<10}"
        )


# ============================================================
# SCENARIOS
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

    elif kind == "noisy":
        rng = np.random.default_rng(7)
        V += 0.01 * rng.normal(size=len(t))

    return {"time": t, "voltage": V}


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    results, all_shapes = run_multi_scenarios()

    print_results_table(results)

    plot_event_overlay(all_shapes)
