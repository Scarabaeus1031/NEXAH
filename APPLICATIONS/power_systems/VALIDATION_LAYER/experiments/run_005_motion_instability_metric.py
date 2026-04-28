import numpy as np
import matplotlib.pyplot as plt
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
# EVENT + SHAPES
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
                events.append((start, end))
        else:
            i += 1

    return events


def extract_shapes(t, curvature, events):
    shapes = []
    times = []

    for (start, end) in events:
        seg = curvature[start:end]
        if len(seg) < 5:
            continue

        seg = seg / (np.max(seg) + 1e-8)
        t_norm = np.linspace(0, 1, len(seg))

        shapes.append((t_norm, seg))
        times.append(t[start])

    return shapes, times


def resample_shapes(shapes, n=50):
    target_t = np.linspace(0, 1, n)
    X = []

    for t_norm, seg in shapes:
        X.append(np.interp(target_t, t_norm, seg))

    return np.array(X)


# ============================================================
# SHAPE SPACE
# ============================================================

def compute_shape_space(shapes):
    if len(shapes) < 3:
        return None, None

    X = resample_shapes(shapes)

    X_centered = X - np.mean(X, axis=0)
    _, _, Vt = np.linalg.svd(X_centered, full_matrices=False)

    coords = X_centered @ Vt[:2].T

    return coords, X


# ============================================================
# 🔥 MOTION INSTABILITY METRIC
# ============================================================

def compute_motion_instability(coords):
    """
    computes angle between successive movement vectors
    """

    coords = np.array(coords)

    if len(coords) < 3:
        return None

    angles = []

    for i in range(1, len(coords) - 1):
        v1 = coords[i] - coords[i - 1]
        v2 = coords[i + 1] - coords[i]

        n1 = np.linalg.norm(v1)
        n2 = np.linalg.norm(v2)

        if n1 < 1e-8 or n2 < 1e-8:
            continue

        cos_angle = np.dot(v1, v2) / (n1 * n2)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)

        angle = np.arccos(cos_angle)
        angles.append(angle)

    return np.array(angles)


# ============================================================
# VALIDATION PIPELINE
# ============================================================

def run_validation(data):

    t = data["time"]
    V = data["voltage"]

    sigma = 2
    stable_idx = int(0.3 * len(t))

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

    t_collapse = sustained_first_crossing(V_smooth < 0.7, t)

    events = extract_events(curvature, threshold)
    shapes, event_times = extract_shapes(t, curvature, events)

    return shapes, event_times, t_collapse


# ============================================================
# SCENARIO
# ============================================================

def make_synthetic_scenario(kind):

    t = np.linspace(0, 100, 500)
    V = 1 - 0.002*t - 0.0005*t**2

    if kind == "nonlinear":
        V += 0.015*np.exp((t-16)/4)*(t<25)
        V += 0.01*np.sin(0.8*t)*(t<25)

    elif kind == "noisy":
        V += 0.01*np.random.default_rng(7).normal(size=len(t))

    return {"time": t, "voltage": V}


# ============================================================
# VISUALIZATION
# ============================================================

def plot_instability(event_times, angles, t_collapse):

    # align lengths (angles are shorter)
    times = event_times[1:-1]

    plt.figure(figsize=(8, 4))

    plt.plot(times, angles, marker="o", label="instability (angle)")

    if t_collapse is not None:
        plt.axvline(t_collapse, color="red", linestyle="--", label="collapse")

    plt.xlabel("time")
    plt.ylabel("angle (rad)")
    plt.title("Motion Instability over Time")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n=== RUN: motion instability metric ===\n")

    data = make_synthetic_scenario("noisy")

    shapes, event_times, t_collapse = run_validation(data)

    print("t_collapse:", t_collapse)
    print("events:", len(shapes))

    coords, X = compute_shape_space(shapes)

    if coords is not None:

        angles = compute_motion_instability(coords)

        if angles is not None:
            plot_instability(event_times, angles, t_collapse)

            print("\nmean instability:", np.mean(angles))
            print("max instability :", np.max(angles))
