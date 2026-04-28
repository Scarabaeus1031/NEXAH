# ============================================================
# 🧪 NEXAH — Experiment 007
# Statistical Validation of Motion Instability
#
# Goal:
# Check if pre-collapse instability is reproducible
# or just random coincidence.
# ============================================================

import numpy as np
from scipy.ndimage import gaussian_filter1d


# ============================================================
# CORE
# ============================================================

def sustained_first_crossing(mask, t, min_samples=3):
    mask = np.asarray(mask, dtype=bool)

    for i in range(0, len(mask) - min_samples + 1):
        if np.all(mask[i:i + min_samples]):
            return t[i]

    return None


# ============================================================
# SCENARIO (WITH VARIABLE NOISE)
# ============================================================

def make_synthetic_scenario(noise_scale=0.01, seed=None):

    if seed is not None:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()

    t = np.linspace(0, 100, 500)

    # base collapse curve
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    # noise
    V += noise_scale * rng.normal(size=len(t))

    return {"time": t, "voltage": V}


# ============================================================
# PIPELINE (same as run_006)
# ============================================================

def compute_curvature(data, sigma=2):

    t = data["time"]
    V = data["voltage"]

    V_smooth = gaussian_filter1d(V, sigma)
    dv_dt = gaussian_filter1d(np.gradient(V_smooth, t), sigma)
    d2v_dt2 = gaussian_filter1d(np.gradient(dv_dt, t), sigma)

    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    curvature = gaussian_filter1d(
        np.linalg.norm(np.gradient(np.gradient(x, axis=0), axis=0), axis=1),
        sigma
    )

    t_collapse = sustained_first_crossing(V_smooth < 0.7, t)

    return t, curvature, t_collapse


def build_windows(curvature, t, window_size=40, step=2):

    windows = []
    times = []

    for start in range(0, len(curvature) - window_size, step):
        end = start + window_size
        seg = curvature[start:end]

        seg_min = np.min(seg)
        seg_max = np.max(seg)

        if seg_max - seg_min < 1e-10:
            seg_norm = np.zeros_like(seg)
        else:
            seg_norm = (seg - seg_min) / (seg_max - seg_min)

        windows.append(seg_norm)
        times.append(t[start + window_size // 2])

    return np.array(windows), np.array(times)


def compute_shape_space(X):

    if len(X) < 3:
        return None

    Xc = X - np.mean(X, axis=0)
    _, _, Vt = np.linalg.svd(Xc, full_matrices=False)

    return Xc @ Vt[:2].T


def compute_angle_metric(coords):

    angles = []

    for i in range(1, len(coords) - 1):
        v1 = coords[i] - coords[i - 1]
        v2 = coords[i + 1] - coords[i]

        n1 = np.linalg.norm(v1)
        n2 = np.linalg.norm(v2)

        if n1 < 1e-10 or n2 < 1e-10:
            continue

        cos_angle = np.dot(v1, v2) / (n1 * n2)
        cos_angle = np.clip(cos_angle, -1, 1)

        angles.append(np.arccos(cos_angle))

    return np.array(angles)


def detect_warning(metric, times, t_collapse, k=2.0):

    stable_idx = int(0.3 * len(metric))

    if stable_idx < 5:
        return None

    threshold = np.mean(metric[:stable_idx]) + k * np.std(metric[:stable_idx])

    mask = (metric > threshold) & (times < t_collapse)

    idx = np.where(mask)[0]

    if len(idx) == 0:
        return None

    return times[idx[0]]


# ============================================================
# SINGLE RUN
# ============================================================

def run_single(noise_scale=0.01, seed=None):

    data = make_synthetic_scenario(noise_scale=noise_scale, seed=seed)

    t, curvature, t_collapse = compute_curvature(data)

    if t_collapse is None:
        return None

    windows, times = build_windows(curvature, t)

    coords = compute_shape_space(windows)

    if coords is None:
        return None

    angles = compute_angle_metric(coords)

    angle_times = times[1:-1]

    t_warning = detect_warning(angles, angle_times, t_collapse)

    if t_warning is None:
        return {
            "detected": False,
            "lead_time": None
        }

    return {
        "detected": True,
        "lead_time": t_collapse - t_warning
    }


# ============================================================
# STATISTICS
# ============================================================

def run_statistical_experiment(n_runs=50, noise_scale=0.01):

    results = []

    for i in range(n_runs):
        res = run_single(noise_scale=noise_scale, seed=i)
        if res is not None:
            results.append(res)

    return results


def summarize(results):

    detected = [r for r in results if r["detected"]]
    missed = [r for r in results if not r["detected"]]

    lead_times = [r["lead_time"] for r in detected if r["lead_time"] is not None]

    print("\n=== STATISTICAL RESULTS ===\n")

    print("Total runs:", len(results))
    print("Detections:", len(detected))
    print("Missed    :", len(missed))

    if len(lead_times) > 0:
        print("\nLead time stats:")
        print("  mean:", np.mean(lead_times))
        print("  std :", np.std(lead_times))
        print("  max :", np.max(lead_times))
        print("  min :", np.min(lead_times))
    else:
        print("\nNo valid lead times detected.")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    results = run_statistical_experiment(
        n_runs=50,
        noise_scale=0.01
    )

    summarize(results)
