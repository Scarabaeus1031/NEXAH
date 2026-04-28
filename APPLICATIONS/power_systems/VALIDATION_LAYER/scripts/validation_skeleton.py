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
                "start": item["start"],
                "end": item["end"],
                "peak": item["peak"],
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
# CLUSTERING
# ============================================================

def cluster_shapes(X, n_clusters=3):
    if len(X) < n_clusters:
        return None, None

    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10)
    cluster_ids = kmeans.fit_predict(X)

    return cluster_ids, kmeans.cluster_centers_


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
        start, end, _ = events[0]
        t_nexah = t[start]
        width = t[end] - t[start]
    else:
        t_nexah = None
        width = 0.0

    lead_classical = compute_lead_time(t_collapse, t_classical)
    lead_nexah = compute_lead_time(t_collapse, t_nexah)

    snr = np.max(curvature) / (np.std(curvature[:stable_idx]) + 1e-8)

    shapes = extract_event_shapes(t, curvature, events)

    alignment = 0.0
    if len(shapes) > 0:
        resampled = resample_shapes(shapes)
        mean_shape = compute_mean_shape(resampled)
        alignment = compute_alignment(resampled, mean_shape)

    return {
        "scenario": scenario_name,
        "delta": (lead_nexah - lead_classical) if (lead_classical is not None and lead_nexah is not None) else None,
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
            f"{fmt(r['delta']):<10} "
            f"{r['events']:<8} "
            f"{fmt(r['width']):<8} "
            f"{fmt(r['alignment']):<10} "
            f"{r['class']:<12}"
        )


# ============================================================
# VISUALS
# ============================================================

def plot_overlay(all_shapes):
    plt.figure(figsize=(8, 5))

    for label, shapes in all_shapes.items():
        for item in shapes:
            plt.plot(item["t_norm"], item["shape"], alpha=0.3, label=label)

    handles, labels = plt.gca().get_legend_handles_labels()
    unique = dict(zip(labels, handles))

    plt.legend(unique.values(), unique.keys())
    plt.title("Event Shape Overlay")
    plt.xlabel("Normalized time")
    plt.ylabel("Normalized curvature")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_shape_space(coords, labels):
    plt.figure(figsize=(6, 6))

    color_map = {
        "smooth": "orange",
        "nonlinear": "green",
        "noisy": "blue",
    }

    for (x, y), label in zip(coords, labels):
        plt.scatter(x, y, color=color_map.get(label, "black"), alpha=0.75)

    for label, color in color_map.items():
        plt.scatter([], [], color=color, label=label)

    plt.legend()
    plt.title("Shape Space (PCA)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_shape_clusters(coords, labels, cluster_ids):
    plt.figure(figsize=(6, 6))

    for (x, y), cid in zip(coords, cluster_ids):
        plt.scatter(x, y, c=f"C{cid}", alpha=0.75)

    plt.title("Shape Space Clusters")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_cluster_mean_shapes(X, cluster_ids):
    plt.figure(figsize=(8, 5))

    for cid in np.unique(cluster_ids):
        cluster_shapes = X[cluster_ids == cid]
        mean_shape = np.mean(cluster_shapes, axis=0)

        t = np.linspace(0, 1, len(mean_shape))
        plt.plot(t, mean_shape, label=f"Cluster {cid}", linewidth=2)

    plt.title("Mean Shape per Cluster")
    plt.xlabel("Normalized time")
    plt.ylabel("Mean normalized curvature")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_shape_trajectory(coords, labels, event_meta):
    plt.figure(figsize=(7, 6))

    color_map = {
        "smooth": "orange",
        "nonlinear": "green",
        "noisy": "blue",
    }

    # Scatter all points
    for (x, y), label in zip(coords, labels):
        plt.scatter(x, y, color=color_map.get(label, "black"), alpha=0.75)

    # Connect events within each scenario by event order
    for scenario in sorted(set(labels)):
        idx = [
            i for i, meta in enumerate(event_meta)
            if meta["scenario"] == scenario
        ]

        idx = sorted(idx, key=lambda i: event_meta[i]["event_index"])

        if len(idx) > 1:
            xs = coords[idx, 0]
            ys = coords[idx, 1]
            plt.plot(
                xs,
                ys,
                color=color_map.get(scenario, "black"),
                alpha=0.6,
                linewidth=1.5,
                marker="o",
                label=f"{scenario} path"
            )

            for local_order, i in enumerate(idx):
                plt.text(
                    coords[i, 0],
                    coords[i, 1],
                    str(event_meta[i]["event_index"]),
                    fontsize=8
                )

    plt.title("Shape Space Trajectories")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.grid(alpha=0.3)

    handles, legend_labels = plt.gca().get_legend_handles_labels()
    unique = dict(zip(legend_labels, handles))
    plt.legend(unique.values(), unique.keys())

    plt.tight_layout()
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

    coords, labels, X, _, event_meta = compute_shape_space(all_shapes)

    if coords is not None:
        plot_shape_space(coords, labels)

        cluster_ids, centers = cluster_shapes(X)

        if cluster_ids is not None:
            plot_shape_clusters(coords, labels, cluster_ids)
            plot_cluster_mean_shapes(X, cluster_ids)

        plot_shape_trajectory(coords, labels, event_meta)
