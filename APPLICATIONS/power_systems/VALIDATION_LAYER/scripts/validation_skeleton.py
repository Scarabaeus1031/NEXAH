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
# Shape extraction
# ============================================================

def extract_event_shapes(t, curvature, events):
    shapes = []

    for (start, end, peak) in events:
        seg = curvature[start:end]
        if len(seg) < 5:
            continue

        seg_norm = seg / (np.max(seg) + 1e-8)
        t_norm = np.linspace(0, 1, len(seg))

        shapes.append((t_norm, seg_norm))

    return shapes


# ============================================================
# FIELD METRICS
# ============================================================

def resample_shapes(shapes, n=50):
    resampled = []
    target_t = np.linspace(0, 1, n)

    for t_norm, seg in shapes:
        interp = np.interp(target_t, t_norm, seg)
        resampled.append(interp)

    return np.array(resampled)


def compute_mean_shape(resampled):
    return np.mean(resampled, axis=0)


def compute_alignment(resampled, mean_shape):
    areas = [np.mean(np.abs(s - mean_shape)) for s in resampled]
    return float(np.mean(areas))


# ============================================================
# SINGLE RUN
# ============================================================

def run_validation(data, scenario_name="scenario"):

    t = np.asarray(data["time"])
    V = np.asarray(data["voltage"])

    V_threshold = 0.7
    dv_threshold = -0.02
    stable_fraction = 0.30
    sigma = 2

    stable_idx = int(stable_fraction * len(t))

    # --- signals ---
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

    threshold = np.mean(curvature[:stable_idx]) + 2 * np.std(curvature[:stable_idx])

    # --- detections ---
    t_collapse = sustained_first_crossing(V_smooth < V_threshold, t)
    t_classical = sustained_first_crossing(dv_dt < dv_threshold, t)

    events = extract_events(curvature, threshold)

    if events:
        start, end, _ = events[0]
        t_nexah = t[start]
        width = t[end] - t[start]
    else:
        t_nexah = None
        width = 0.0

    lead_classical = compute_lead_time(t_collapse, t_classical)
    lead_nexah = compute_lead_time(t_collapse, t_nexah)

    # --- metrics ---
    snr = np.max(curvature) / (np.std(curvature[:stable_idx]) + 1e-8)

    shapes = extract_event_shapes(t, curvature, events)

    alignment = 0.0
    if len(shapes) > 0:
        resampled = resample_shapes(shapes)
        mean_shape = compute_mean_shape(resampled)
        alignment = compute_alignment(resampled, mean_shape)

    return {
        "scenario": scenario_name,
        "Δ": (lead_nexah - lead_classical) if (lead_classical and lead_nexah) else None,
        "events": len(events),
        "width": width,
        "snr": snr,
        "alignment": alignment
    }, shapes


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_transition(result):

    alignment = result["alignment"]
    events = result["events"]

    if alignment < 0.15 and events <= 2:
        return "STRUCTURAL"

    if events >= 4 or alignment > 0.3:
        return "NOISE"

    return "AMBIGUOUS"


# ============================================================
# MULTI RUN
# ============================================================

def run_multi():

    scenarios = ["smooth", "nonlinear", "noisy"]

    results = []
    all_shapes = {}

    for s in scenarios:
        print(f"\n=== RUN: {s} ===")

        data = make_synthetic_scenario(s)
        res, shapes = run_validation(data, s)

        res["class"] = classify_transition(res)

        print(res)

        results.append(res)
        all_shapes[s] = shapes

    return results, all_shapes


# ============================================================
# TABLE
# ============================================================

def print_table(results):

    print("\n=== MULTI-SCENARIO RESULTS ===\n")

    header = f"{'Scenario':<12} {'Δ':<10} {'Events':<8} {'Width':<8} {'Align':<10} {'Class':<12}"
    print(header)
    print("-" * len(header))

    for r in results:

        def fmt(x):
            return f"{x:.3f}" if x is not None else "None"

        print(
            f"{r['scenario']:<12} "
            f"{fmt(r['Δ']):<10} "
            f"{r['events']:<8} "
            f"{fmt(r['width']):<8} "
            f"{fmt(r['alignment']):<10} "
            f"{r['class']:<12}"
        )


# ============================================================
# VISUAL
# ============================================================

def plot_overlay(all_shapes):
    plt.figure(figsize=(8, 5))

    for label, shapes in all_shapes.items():
        for t_norm, seg in shapes:
            plt.plot(t_norm, seg, alpha=0.3, label=label)

    handles, labels = plt.gca().get_legend_handles_labels()
    unique = dict(zip(labels, handles))

    plt.legend(unique.values(), unique.keys())
    plt.title("Event Shape Overlay")
    plt.grid(alpha=0.3)
    plt.show()


# ============================================================
# SCENARIOS
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
# MAIN
# ============================================================

if __name__ == "__main__":

    results, all_shapes = run_multi()

    print_table(results)

    plot_overlay(all_shapes)
