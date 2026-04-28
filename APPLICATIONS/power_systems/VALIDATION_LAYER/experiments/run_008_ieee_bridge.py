# ============================================================
# 🧪 NEXAH — Experiment 008
# IEEE Bridge Validation
#
# Goal:
# Replace synthetic V(t) with voltage trajectory from an IEEE test case.
#
# Requires:
#   pip install pandapower
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

try:
    import pandapower as pp
    import pandapower.networks as pn
except ImportError:
    raise ImportError(
        "pandapower is required for this experiment.\n"
        "Install with: pip install pandapower"
    )


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
# IEEE SIMULATION
# ============================================================

def simulate_ieee_voltage(case="ieee14", n_steps=500, load_start=1.0, load_rate=0.004):
    """
    Generate voltage trajectory from IEEE test case by increasing load scaling.
    Output:
        t, min voltage Vmin(t), load scaling trajectory
    """

    if case == "ieee14":
        net = pn.case14()
    elif case == "ieee30":
        net = pn.case30()
    elif case == "ieee57":
        net = pn.case57()
    else:
        raise ValueError(f"Unsupported case: {case}")

    t = np.linspace(0, 100, n_steps)

    voltages = []
    load_scales = []

    for ti in t:
        scale = load_start + load_rate * ti
        load_scales.append(scale)

        net.load["scaling"] = scale

        try:
            pp.runpp(net, numba=False, init="results")
            v_min = float(net.res_bus.vm_pu.min())
        except Exception:
            # If power flow fails, treat as voltage collapse
            v_min = np.nan

        voltages.append(v_min)

    V = np.array(voltages)

    # Replace failed power flow with last valid drop continuation
    if np.any(np.isnan(V)):
        first_nan = np.where(np.isnan(V))[0][0]
        if first_nan > 0:
            V[first_nan:] = V[first_nan - 1] - np.linspace(
                0.01,
                0.5,
                len(V) - first_nan
            )
        else:
            V[:] = 0.0

    return {
        "time": t,
        "voltage": V,
        "load_scale": np.array(load_scales),
        "case": case,
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
        sigma=sigma
    )

    d2v_dt2 = gaussian_filter1d(
        np.gradient(dv_dt, t),
        sigma=sigma
    )

    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    curvature = gaussian_filter1d(
        np.linalg.norm(
            np.gradient(np.gradient(x, axis=0), axis=0),
            axis=1
        ),
        sigma=sigma
    )

    return t, V_smooth, dv_dt, curvature


# ============================================================
# CONTINUOUS SHAPE WINDOWS
# ============================================================

def build_sliding_windows(signal, t, window_size=40, step=2):
    windows = []
    window_times = []

    for start in range(0, len(signal) - window_size, step):
        end = start + window_size
        segment = signal[start:end]

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
# SHAPE SPACE
# ============================================================

def compute_shape_space(X):
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
    diffs = np.diff(coords, axis=0)
    return np.linalg.norm(diffs, axis=1)


def compute_motion_angle(coords):
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

def first_warning(metric, times, t_collapse, stable_fraction=0.3, k=2.0):
    stable_idx = int(stable_fraction * len(metric))

    if stable_idx < 5:
        return None, None

    threshold = np.mean(metric[:stable_idx]) + k * np.std(metric[:stable_idx])

    mask = metric > threshold

    if t_collapse is not None:
        mask = mask & (times < t_collapse)

    idx = np.where(mask)[0]

    if len(idx) == 0:
        return None, threshold

    return times[idx[0]], threshold


# ============================================================
# VISUALIZATION
# ============================================================

def plot_voltage(t, V, dv_dt, curvature, t_collapse, t_angle_warning):
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axs[0].plot(t, V, label="min voltage")
    axs[0].axhline(0.7, linestyle="--", label="collapse threshold")

    if t_collapse is not None:
        axs[0].axvline(t_collapse, linestyle="--", label="collapse")

    if t_angle_warning is not None:
        axs[0].axvline(t_angle_warning, linestyle=":", label="NEXAH warning")

    axs[0].set_ylabel("Vmin [p.u.]")
    axs[0].legend()
    axs[0].grid(alpha=0.3)

    axs[1].plot(t, dv_dt, label="dV/dt")
    axs[1].set_ylabel("dV/dt")
    axs[1].legend()
    axs[1].grid(alpha=0.3)

    axs[2].plot(t, curvature, label="curvature")
    axs[2].set_ylabel("curvature")
    axs[2].set_xlabel("time")
    axs[2].legend()
    axs[2].grid(alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_shape_flow(coords, window_times, t_collapse):
    plt.figure(figsize=(7, 6))

    sc = plt.scatter(
        coords[:, 0],
        coords[:, 1],
        c=window_times,
        s=18,
        alpha=0.85
    )

    plt.plot(coords[:, 0], coords[:, 1], alpha=0.35)

    if t_collapse is not None:
        idx = np.argmin(np.abs(window_times - t_collapse))
        plt.scatter(
            coords[idx, 0],
            coords[idx, 1],
            marker="x",
            s=120,
            label="collapse region"
        )

    plt.title("IEEE Shape Flow")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.colorbar(sc, label="time")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_motion_metrics(speed_times, speed, angle_times, angles,
                        t_collapse, t_speed_warning, speed_threshold,
                        t_angle_warning, angle_threshold):

    fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    axs[0].plot(speed_times, speed, label="shape-space speed")

    if speed_threshold is not None:
        axs[0].axhline(speed_threshold, linestyle="--", label="speed threshold")

    if t_speed_warning is not None:
        axs[0].axvline(t_speed_warning, linestyle=":", label="speed warning")

    if t_collapse is not None:
        axs[0].axvline(t_collapse, linestyle="--", label="collapse")

    axs[0].set_ylabel("speed")
    axs[0].legend()
    axs[0].grid(alpha=0.3)

    axs[1].plot(angle_times, angles, label="direction-change angle")

    if angle_threshold is not None:
        axs[1].axhline(angle_threshold, linestyle="--", label="angle threshold")

    if t_angle_warning is not None:
        axs[1].axvline(t_angle_warning, linestyle=":", label="angle warning")

    if t_collapse is not None:
        axs[1].axvline(t_collapse, linestyle="--", label="collapse")

    axs[1].set_xlabel("time")
    axs[1].set_ylabel("angle [rad]")
    axs[1].legend()
    axs[1].grid(alpha=0.3)

    plt.suptitle("IEEE Continuous Shape-Flow Metrics")
    plt.tight_layout()
    plt.show()


# ============================================================
# EXPERIMENT
# ============================================================

def run_experiment(case="ieee14"):
    print("\n=== NEXAH EXPERIMENT 008: IEEE BRIDGE ===")
    print(f"Case: {case}")

    data = simulate_ieee_voltage(case=case)

    t, V, dv_dt, curvature = compute_curvature_signal(data)

    t_collapse = sustained_first_crossing(V < 0.7, t)

    windows, window_times = build_sliding_windows(
        curvature,
        t,
        window_size=40,
        step=2
    )

    coords = compute_shape_space(windows)

    if coords is None:
        print("Not enough shape windows.")
        return

    speed = compute_motion_speed(coords)
    speed_times = window_times[1:]

    angles = compute_motion_angle(coords)
    angle_times = window_times[1:-1]

    t_speed_warning, speed_threshold = first_warning(
        speed,
        speed_times,
        t_collapse,
        stable_fraction=0.3,
        k=2.0
    )

    t_angle_warning, angle_threshold = first_warning(
        angles,
        angle_times,
        t_collapse,
        stable_fraction=0.3,
        k=2.0
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
    print("Min voltage:", float(np.min(V)))
    print("Mean speed:", float(np.mean(speed)))
    print("Max speed: ", float(np.max(speed)))
    print("Mean angle:", float(np.mean(angles)))
    print("Max angle: ", float(np.max(angles)))

    plot_voltage(t, V, dv_dt, curvature, t_collapse, t_angle_warning)
    plot_shape_flow(coords, window_times, t_collapse)
    plot_motion_metrics(
        speed_times,
        speed,
        angle_times,
        angles,
        t_collapse,
        t_speed_warning,
        speed_threshold,
        t_angle_warning,
        angle_threshold
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # Try:
    #   "ieee14"
    #   "ieee30"
    #   "ieee57"

    run_experiment("ieee14")
