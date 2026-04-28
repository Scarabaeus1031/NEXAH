import os
import json
import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from sklearn.cluster import KMeans


# ============================================================
# OUTPUT SETUP
# ============================================================

def create_output_dir(base="APPLICATIONS/power_systems/VALIDATION_LAYER/outputs"):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(base, f"run_{timestamp}")
    os.makedirs(path, exist_ok=True)
    return path


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

    for (start, end, _) in events:
        seg = curvature[start:end]

        if len(seg) < 5:
            continue

        seg_norm = seg / (np.max(seg) + 1e-8)
        t_norm = np.linspace(0, 1, len(seg))

        shapes.append((t_norm, seg_norm))

    return shapes


# ============================================================
# Shape processing
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
    return float(np.mean([np.mean(np.abs(s - mean_shape)) for s in resampled]))


# ============================================================
# SHAPE SPACE (PCA)
# ============================================================

def compute_shape_space(all_shapes, n=50):

    X, labels = [], []

    for scenario, shapes in all_shapes.items():
        if len(shapes) == 0:
            continue

        resampled = resample_shapes(shapes, n=n)

        for r in resampled:
            X.append(r)
            labels.append(scenario)

    if len(X) < 2:
        return None, None, None

    X = np.array(X)

    X_centered = X - np.mean(X, axis=0)
    _, _, Vt = np.linalg.svd(X_centered, full_matrices=False)

    coords = X_centered @ Vt[:2].T

    return coords, labels, X


# ============================================================
# CLUSTERING
# ============================================================

def cluster_shapes(X, n_clusters=3):

    if X is None or len(X) < n_clusters:
        return None

    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    return kmeans.fit_predict(X)


# ============================================================
# VALIDATION
# ============================================================

def run_validation(data, scenario):

    t = np.asarray(data["time"])
    V = np.asarray(data["voltage"])

    sigma = 2
    stable_idx = int(0.3 * len(t))

    # --- signals ---
    V_smooth = gaussian_filter1d(V, sigma)
    dv_dt = gaussian_filter1d(np.gradient(V_smooth, t), sigma)

    x = np.vstack([
        V_smooth,
        dv_dt,
        gaussian_filter1d(np.gradient(dv_dt, t), sigma)
    ]).T

    curvature = gaussian_filter1d(
        np.linalg.norm(np.gradient(np.gradient(x, axis=0), axis=0), axis=1),
        sigma
    )

    threshold = np.mean(curvature[:stable_idx]) + 2 * np.std(curvature[:stable_idx])

    # --- detections ---
    t_collapse = sustained_first_crossing(V_smooth < 0.7, t)
    t_classical = sustained_first_crossing(dv_dt < -0.02, t)

    events = extract_events(curvature, threshold)

    if events:
        start, end, _ = events[0]
        t_nexah = t[start]
        width = t[end] - t[start]
    else:
        t_nexah = None
        width = 0

    lead_classical = compute_lead_time(t_collapse, t_classical)
    lead_nexah = compute_lead_time(t_collapse, t_nexah)

    if lead_classical is None or lead_nexah is None:
        delta = None
    else:
        delta = lead_nexah - lead_classical

    # --- metrics ---
    snr = np.max(curvature) / (np.std(curvature[:stable_idx]) + 1e-8)

    shapes = extract_event_shapes(t, curvature, events)

    alignment = 0.0
    if len(shapes) > 0:
        res = resample_shapes(shapes)
        alignment = compute_alignment(res, compute_mean_shape(res))

    return {
        "scenario": scenario,
        "delta": delta,
        "events": len(events),
        "width": float(width),
        "snr": float(snr),
        "alignment": float(alignment)
    }, shapes


# ============================================================
# VISUALS (SAVED)
# ============================================================

def save_overlay(all_shapes, path):

    plt.figure(figsize=(8, 5))

    for label, shapes in all_shapes.items():
        for t_norm, seg in shapes:
            plt.plot(t_norm, seg, alpha=0.3)

    plt.title("Event Shape Overlay")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(path, "overlay.png"))
    plt.close()


def save_shape_space(coords, labels, path):

    plt.figure(figsize=(6, 6))

    for (x, y), l in zip(coords, labels):
        plt.scatter(x, y, label=l, alpha=0.7)

    plt.title("Shape Space (PCA)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(path, "shape_space.png"))
    plt.close()


def save_clusters(coords, cluster_ids, path):

    plt.figure(figsize=(6, 6))

    for (x, y), cid in zip(coords, cluster_ids):
        plt.scatter(x, y, c=f"C{cid}", alpha=0.7)

    plt.title("Shape Clusters")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(path, "clusters.png"))
    plt.close()


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(results, path):

    # JSON
    with open(os.path.join(path, "results.json"), "w") as f:
        json.dump(results, f, indent=2)

    # CSV
    keys = results[0].keys()
    with open(os.path.join(path, "results.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)


# ============================================================
# SCENARIOS
# ============================================================

def make_synthetic_scenario(kind):

    np.random.seed(7)

    t = np.linspace(0, 100, 500)
    V = 1 - 0.002 * t - 0.0005 * t**2

    if kind == "nonlinear":
        V += 0.015 * np.exp((t - 16) / 4) * (t < 25)
        V += 0.01 * np.sin(0.8 * t) * (t < 25)

    elif kind == "noisy":
        V += 0.01 * np.random.normal(size=len(t))

    return {"time": t, "voltage": V}


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    output_dir = create_output_dir()

    scenarios = ["smooth", "nonlinear", "noisy"]

    results = []
    all_shapes = {}

    for s in scenarios:
        data = make_synthetic_scenario(s)
        res, shapes = run_validation(data, s)

        results.append(res)
        all_shapes[s] = shapes

        print(res)

    save_results(results, output_dir)
    save_overlay(all_shapes, output_dir)

    coords, labels, X = compute_shape_space(all_shapes)

    if coords is not None:
        save_shape_space(coords, labels, output_dir)

        cluster_ids = cluster_shapes(X)
        if cluster_ids is not None:
            save_clusters(coords, cluster_ids, output_dir)

    print(f"\nSaved to: {output_dir}")
