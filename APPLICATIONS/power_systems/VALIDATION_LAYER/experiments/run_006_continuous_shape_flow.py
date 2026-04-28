# ============================================================
# 🧪 NEXAH — Experiment 006
# Continuous Shape Flow
#
# Goal:
# Move from sparse event-based detection to continuous
# sliding-window trajectory analysis.
#
# Question:
# Does shape-space motion become unstable BEFORE collapse?
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ============================================================
# CORE UTILS
# ============================================================

def sustained_first_crossing(mask, t, min_samples=3):
    mask = np.asarray(mask, dtype=bool)

    for i in range(0, len(mask) - min_samples + 1):
        if np.all(mask[i:i + min_samples]):
            return t[i]

    return None


# ============================================================
# SCENARIOS
# ============================================================

def make_synthetic_scenario(kind="noisy", n=500):
    t = np.linspace(0, 100, n)

    # base collapse
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    if kind == "nonlinear":
        V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
        V += 0.01 * np.sin(0.8 * t) * (t < 25)

    elif kind == "noisy":
        rng = np.random.default_rng(7)
        V += 0.01 * rng.normal(size=len(t))

    elif kind == "smooth":
        pass

    else:
        raise ValueError(f"Unknown scenario: {kind}")

    return {
        "time": t,
        "voltage": V,
    }


# ============================================================
# FEATURE EXTRACTION
# ============================================================

def compute_curvature_signal(data, sigma=2):
    t = np.asarray(data["time"])
    V = np.asarray(data["voltage"])

    V_smooth = gaussian_filter1d(V, sigma=sigma)

    dv_dt = gaussian_filter1d(
        np.gradient(V_smooth, t),
        sigma=sigma,
    )

    d2v_dt2 = gaussian_filter1d(
        np.gradient(dv_dt, t),
        sigma=sigma,
    )

    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    curvature = gaussian_filter1d(
        np.linalg.norm(
            np.gradient(np.gradient(x, axis=0), axis=0),
            axis=1,
        ),
        sigma=sigma,
    )

    t_collapse = sustained_first_crossing(V_smooth < 0.7, t)

    return t, V_smooth, dv_dt, curvature, t_collapse


# ============================================================
# CONTINUOUS SHAPE WINDOWS
# ============================================================

def build_sliding_windows(signal, t, window_size=40, step=2):
    """
    Build normalized local shape windows from curvature signal.

    Each window becomes one vector.
    This creates a continuous shape trajectory.
    """

    windows = []
    window_times = []

    for start in range(0, len(signal) - window_size, step):
        end = start + window_size
        segment = signal[start:end]

        # normalize local shape
        seg_min = np.min(segment)
        seg_max = np.max(segment)

        if seg_max - seg_min < 1e-10:
            seg_norm = np.zeros_like(segment)
        else:
            seg_norm = (segment - seg_min) / (seg_max - seg_min)

        windows.append(seg_norm)
        window_times.append(t[start + window_size // 2])

    return np.array(windows), np.array(window_times)


# ============================================================
# SHAPE SPACE PCA
# ============================================================

def compute_shape_space(X):
    """
    PCA via SVD.
    Returns 2D coordinates.
    """

    if len(X) < 3:
        return None

    X_centered = X - np.mean(X, axis=0)

    _, _, Vt = np.linalg.svd(X_centered, full_matrices=False)

    coords = X_centered @ Vt[:2].T

    return coords


# ============================================================
# MOTION METRICS
# ============================================================

def compute_motion_speed(coords):
    """
    Speed = distance between consecutive shape-space points.
    """

    diffs = np.diff(coords, axis=0)
    speed = np.linalg.norm(diffs, axis=1)

    return speed


def compute_motion_angle(coords):
    """
    Angle between successive movement vectors.
    Large values indicate direction changes.
    """

    angles = []

    for i in range(1, len(coords) - 1):
        v1 = coords[i] - coords[i - 1]
        v2 = coords[i + 1] - coords[i]

        n1 = np.linalg.norm(v1)
        n2 = np.linalg.norm(v2)

        if n1 < 1e-10 or n2 < 1e-10:
            angles.append(0.0)
            continue

        cos_angle = np.dot(v1, v2) / (n1 * n2)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)

        angles.append(np.arccos(cos_angle))

    return np.array(angles)


# ============================================================
# DETECTION
# ============================================================

def first_pre_collapse_warning(metric, times, t_collapse, stable_fraction=0.3, k=2.0):
    """
    Adaptive warning based only on early stable window.
    No future leakage.
    """

    stable_idx = int(stable_fraction * len(metric))

    if stable_idx < 5:
        return None, None

    threshold = np.mean(metric[:stable_idx]) + k * np.std(metric[:stable_idx])

    warning_mask = metric > threshold

    # only accept warnings before collapse
    if t_collapse is not None:
        warning_mask = warning_mask & (times < t_collapse)

    idx = np.where(warning_mask)[0]

    if len(idx) == 0:
        return None, threshold

    return times[idx[0]], threshold


# ============================================================
# VISUALIZATION
# ============================================================

def plot_continuous_shape_flow(coords, window_times, t_collapse, title):
    plt.figure(figsize=(7, 6))

    sc = plt.scatter(
        coords[:, 0],
        coords[:, 1],
        c=window_times,
        s=18,
        alpha=0.85,
    )

    # trajectory line
    plt.plot(coords[:, 0], coords[:, 1], alpha=0.35)

    # mark collapse-nearest point
    if t_collapse is not None:
        collapse_idx = np.argmin(np.abs(window_times - t_collapse))
        plt.scatter(
            coords[collapse_idx, 0],
            coords[collapse_idx, 1],
            s=100,
            marker="x",
            label="collapse region",
        )

    plt.title(title)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.colorbar(sc, label="time")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_motion_metrics(
    metric_times,
    speed,
    angle_times,
    angles,
    t_collapse,
    t_speed_warning,
    speed_threshold,
    t_angle_warning,
    angle_threshold,
):
    plt.figure(figsize=(10, 6))

    # speed
    plt.subplot(2, 1, 1)
    plt.plot(metric_times, speed, label="shape-space speed")

    if speed_threshold is not None:
        plt.axhline(speed_threshold, linestyle="--", label="speed threshold")

    if t_speed_warning is not None:
        plt.axvline(t_speed_warning, linestyle=":", label="speed warning")

    if t_collapse is not None:
        plt.axvline(t_collapse, linestyle="--", label="collapse")

    plt.ylabel("speed")
    plt.title("Continuous Shape-Flow Metrics")
    plt.legend()
    plt.grid(alpha=0.3)

    # angle
    plt.subplot(2, 1, 2)
    plt.plot(angle_times, angles, label="direction-change angle")

    if angle_threshold is not None:
        plt.axhline(angle_threshold, linestyle="--", label="angle threshold")

    if t_angle_warning is not None:
        plt.axvline(t_angle_warning, linestyle=":", label="angle warning")

    if t_collapse is not None:
        plt.axvline(t_collapse, linestyle="--", label="collapse")

    plt.xlabel("time")
    plt.ylabel("angle [rad]")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()


# ============================================================
# EXPERIMENT
# ============================================================

def run_experiment(kind="noisy"):
    print("\n=== NEXAH EXPERIMENT 006: CONTINUOUS SHAPE FLOW ===")
    print(f"Scenario: {kind}")

    data = make_synthetic_scenario(kind)

    t, V_smooth, dv_dt, curvature, t_collapse = compute_curvature_signal(data)

    windows, window_times = build_sliding_windows(
        curvature,
        t,
        window_size=40,
        step=2,
    )

    coords = compute_shape_space(windows)

    if coords is None:
        print("Not enough windows.")
        return

    speed = compute_motion_speed(coords)
    speed_times = window_times[1:]

    angles = compute_motion_angle(coords)
    angle_times = window_times[1:-1]

    t_speed_warning, speed_threshold = first_pre_collapse_warning(
        speed,
        speed_times,
        t_collapse,
        stable_fraction=0.3,
        k=2.0,
    )

    t_angle_warning, angle_threshold = first_pre_collapse_warning(
        angles,
        angle_times,
        t_collapse,
        stable_fraction=0.3,
        k=2.0,
    )

    print("")
    print("Collapse time:", t_collapse)
    print("Speed warning:", t_speed_warning)
    print("Angle warning:", t_angle_warning)

    if t_speed_warning is not None and t_collapse is not None:
        print("Speed lead time:", t_collapse - t_speed_warning)

    if t_angle_warning is not None and t_collapse is not None:
        print("Angle lead time:", t_collapse - t_angle_warning)

    print("")
    print("Mean speed:", float(np.mean(speed)))
    print("Max speed: ", float(np.max(speed)))
    print("Mean angle:", float(np.mean(angles)))
    print("Max angle: ", float(np.max(angles)))

    plot_continuous_shape_flow(
        coords,
        window_times,
        t_collapse,
        title=f"Continuous Shape Flow — {kind}",
    )

    plot_motion_metrics(
        speed_times,
        speed,
        angle_times,
        angles,
        t_collapse,
        t_speed_warning,
        speed_threshold,
        t_angle_warning,
        angle_threshold,
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # Try:
    #   "smooth"
    #   "nonlinear"
    #   "noisy"

    run_experiment("noisy")
