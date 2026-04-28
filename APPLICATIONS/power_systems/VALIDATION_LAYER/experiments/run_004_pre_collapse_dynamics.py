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


def compute_lead_time(t_collapse, t_detection):
    if t_collapse is None or t_detection is None:
        return None
    return t_collapse - t_detection


# ============================================================
# EVENT EXTRACTION
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
# SHAPE EXTRACTION
# ============================================================

def extract_event_shapes(t, curvature, events):
    shapes = []
    times = []

    for (start, end, _) in events:
        seg = curvature[start:end]
        if len(seg) < 5:
            continue

        seg_norm = seg / (np.max(seg) + 1e-8)
        t_norm = np.linspace(0, 1, len(seg))

        shapes.append((t_norm, seg_norm))
        times.append(t[start])  # 🔥 event time

    return shapes, times


# ============================================================
# SHAPE PROCESSING
# ============================================================

def resample_shapes(shapes, n=50):
    resampled = []
    target_t = np.linspace(0, 1, n)

    for t_norm, seg in shapes:
        interp = np.interp(target_t, t_norm, seg)
        resampled.append(interp)

    return np.array(resampled)


def compute_shape_space(shapes, n=50):

    if len(shapes) < 2:
        return None, None

    X = resample_shapes(shapes, n=n)

    X_centered = X - np.mean(X, axis=0)
    _, _, Vt = np.linalg.svd(X_centered, full_matrices=False)

    coords = X_centered @ Vt[:2].T

    return coords, X


# ============================================================
# VALIDATION PIPELINE
# ============================================================

def run_validation(data):

    t = np.asarray(data["time"])
    V = np.asarray(data["voltage"])

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

    # collapse detection
    t_collapse = sustained_first_crossing(V_smooth < 0.7, t)

    # events
    events = extract_events(curvature, threshold)

    shapes, event_times = extract_event_shapes(t, curvature, events)

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

def plot_pre_post_trajectory(coords, event_times, t_collapse):

    plt.figure(figsize=(7, 6))

    coords = np.array(coords)
    event_times = np.array(event_times)

    pre = event_times < t_collapse
    post = event_times >= t_collapse

    # PRE-collapse
    plt.scatter(coords[pre, 0], coords[pre, 1],
                c="blue", label="pre-collapse", s=60)

    # POST-collapse
    plt.scatter(coords[post, 0], coords[post, 1],
                c="red", label="post-collapse", s=60)

    # connect trajectory
    for i in range(len(coords) - 1):
        plt.plot(coords[i:i+2, 0], coords[i:i+2, 1],
                 color="gray", alpha=0.4)

    plt.title("Pre vs Post Collapse Dynamics (Shape Space)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n=== RUN: pre-collapse dynamics ===\n")

    data = make_synthetic_scenario("noisy")  # 🔥 test noisy first

    shapes, event_times, t_collapse = run_validation(data)

    print("t_collapse:", t_collapse)
    print("events:", len(shapes))

    coords, X = compute_shape_space(shapes)

    if coords is not None:
        plot_pre_post_trajectory(coords, event_times, t_collapse)
