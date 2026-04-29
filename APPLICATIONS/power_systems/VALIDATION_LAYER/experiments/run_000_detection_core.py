import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from sklearn.cluster import KMeans


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

    for event_index, (start, end, peak) in enumerate(events):
        seg = curvature[start:end]

        if len(seg) < 5:
            continue

        seg_norm = seg / (np.max(seg) + 1e-8)
        t_norm = np.linspace(0, 1, len(seg))

        shapes.append({
            "event_index": event_index,
            "start": start,
            "end": end,
            "peak": peak,
            "t_norm": t_norm,
            "shape": seg_norm,
        })

    return shapes


# ============================================================
# Shape processing
# ============================================================

def resample_shapes(shapes, n=50):
    resampled = []
    target_t = np.linspace(0, 1, n)

    for item in shapes:
        interp = np.interp(target_t, item["t_norm"], item["shape"])
        resampled.append(interp)

    return np.array(resampled)


def compute_mean_shape(resampled):
    return np.mean(resampled, axis=0)


def compute_alignment(resampled, mean_shape):
    areas = [np.mean(np.abs(s - mean_shape)) for s in resampled]
    return float(np.mean(areas))


# ============================================================
# SHAPE SPACE (PCA)
# ============================================================

def compute_shape_space(all_shapes, n=50):
    X = []
    labels = []
    event_meta = []

    for scenario, shapes in all_shapes.items():
        if len(shapes) == 0:
            continue

        resampled = resample_shapes(shapes, n=n)

        for r, item in zip(resampled, shapes):
            X.append(r)
            labels.append(scenario)
            event_meta.append({
                "scenario": scenario,
                "event_index": item["event_index"],
            })

    X = np.array(X)

    if len(X) < 2:
        return None, None, None, None, None

    X_mean = np.mean(X, axis=0)
    X_centered = X - X_mean

    U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
    coords = X_centered @ Vt[:2].T

    return coords, labels, X, Vt, event_meta


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

    t_collapse = sustained_first_crossing(V_smooth < V_threshold, t)
    t_classical = sustained_first_crossing(dv_dt < dv_threshold, t)

    events = extract_events(curvature, threshold)

    if events:
        t_nexah = t[events[0][0]]
    else:
        t_nexah = None

    return t, V_smooth, curvature, t_nexah, t_classical, t_collapse


# ============================================================
# 🔥 KEY FIGURE (DETECTION TIMELINE)
# ============================================================

def plot_detection_timeline(data):
    t, V, curvature, t_nexah, t_classical, t_collapse = run_validation(data)

    plt.figure(figsize=(10, 5))

    plt.plot(t, V, label="Voltage V(t)", linewidth=2)
    plt.plot(t, curvature / np.max(curvature), label="Normalized κ(t)", alpha=0.7)

    if t_nexah is not None:
        plt.axvline(t_nexah, linestyle="--", label="NEXAH")

    if t_classical is not None:
        plt.axvline(t_classical, linestyle="--", label="Classical")

    if t_collapse is not None:
        plt.axvline(t_collapse, linestyle="-", linewidth=2, label="Collapse")

    plt.title("Detection Timeline")
    plt.xlabel("Time (simulation steps)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("\n=== DETECTION TIMES ===")
    print(f"NEXAH:     {t_nexah}")
    print(f"Classical: {t_classical}")
    print(f"Collapse:  {t_collapse}")

    if t_collapse:
        print("Lead (NEXAH):", t_collapse - t_nexah if t_nexah else None)
        print("Lead (Classical):", t_collapse - t_classical if t_classical else None)


# ============================================================
# SCENARIO
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

    print("\n=== RUN DETECTION TIMELINE ===")

    data = make_synthetic_scenario("nonlinear")
    plot_detection_timeline(data)
