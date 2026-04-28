# ============================================================
# 🧪 NEXAH — Experiment 009
# IEEE Collapse Sweep
#
# Goal:
# Sweep load_rate values on IEEE test cases and test whether
# continuous shape-flow metrics respond before voltage collapse.
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


def safe_lead_time(t_collapse, t_warning):
    if t_collapse is None or t_warning is None:
        return None
    return t_collapse - t_warning


def fmt(x):
    return f"{x:.3f}" if x is not None else "None"


# ============================================================
# IEEE NETWORK
# ============================================================

def make_network(case="ieee14"):
    if case == "ieee14":
        return pn.case14()
    if case == "ieee30":
        return pn.case30()
    if case == "ieee57":
        return pn.case57()
    raise ValueError(f"Unsupported IEEE case: {case}")


# ============================================================
# IEEE SIMULATION
# ============================================================

def simulate_ieee_voltage(
    case="ieee14",
    n_steps=500,
    load_start=1.0,
    load_rate=0.004,
    fail_drop=0.5,
):
    """
    Increase load scaling linearly and record min bus voltage.

    If power flow fails, we treat that as numerical collapse and
    continue with a synthetic drop continuation only for plotting.
    """

    net = make_network(case)
    t = np.linspace(0, 100, n_steps)

    voltages = []
    load_scales = []
    pf_failed_at = None

    for idx, ti in enumerate(t):
        scale = load_start + load_rate * ti
        load_scales.append(scale)

        net.load["scaling"] = scale

        try:
            pp.runpp(net, numba=False, init="results")
            v_min = float(net.res_bus.vm_pu.min())
        except Exception:
            v_min = np.nan
            if pf_failed_at is None:
                pf_failed_at = ti

        voltages.append(v_min)

    V = np.array(voltages, dtype=float)

    # Continue after PF failure for visualization only
    if np.any(np.isnan(V)):
        first_nan = np.where(np.isnan(V))[0][0]

        if first_nan > 0:
            V[first_nan:] = V[first_nan - 1] - np.linspace(
                0.01,
                fail_drop,
                len(V) - first_nan
            )
        else:
            V[:] = 0.0

    return {
        "time": t,
        "voltage": V,
        "load_scale": np.array(load_scales),
        "case": case,
        "load_rate": load_rate,
        "pf_failed_at": pf_failed_at,
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
# WARNING DETECTION
# ============================================================

def first_warning(metric, times, t_collapse=None, stable_fraction=0.3, k=2.0):
    stable_idx = int(stable_fraction * len(metric))

    if stable_idx < 5:
        return None, None

    threshold = np.mean(metric[:stable_idx]) + k * np.std(metric[:stable_idx])

    mask = metric > threshold

    # If collapse exists, only count pre-collapse warnings.
    if t_collapse is not None:
        mask = mask & (times < t_collapse)

    idx = np.where(mask)[0]

    if len(idx) == 0:
        return None, threshold

    return times[idx[0]], threshold


# ============================================================
# SINGLE SWEEP RUN
# ============================================================

def analyze_ieee_run(
    case="ieee14",
    load_rate=0.004,
    voltage_threshold=0.7,
    window_size=40,
    step=2,
    sigma=2,
    k=2.0,
):
    data = simulate_ieee_voltage(
        case=case,
        load_rate=load_rate,
    )

    t, V, dv_dt, curvature = compute_curvature_signal(
        data,
        sigma=sigma,
    )

    # Collapse definition:
    # either voltage crosses threshold OR PF fails
    t_voltage_collapse = sustained_first_crossing(V < voltage_threshold, t)
    t_pf_failure = data["pf_failed_at"]

    collapse_candidates = [
        x for x in [t_voltage_collapse, t_pf_failure]
        if x is not None
    ]

    t_collapse = min(collapse_candidates) if collapse_candidates else None

    windows, window_times = build_sliding_windows(
        curvature,
        t,
        window_size=window_size,
        step=step,
    )

    coords = compute_shape_space(windows)

    if coords is None:
        return None

    speed = compute_motion_speed(coords)
    speed_times = window_times[1:]

    angle = compute_motion_angle(coords)
    angle_times = window_times[1:-1]

    t_speed_warning, speed_threshold = first_warning(
        speed,
        speed_times,
        t_collapse=t_collapse,
        stable_fraction=0.3,
        k=k,
    )

    t_angle_warning, angle_threshold = first_warning(
        angle,
        angle_times,
        t_collapse=t_collapse,
        stable_fraction=0.3,
        k=k,
    )

    result = {
        "case": case,
        "load_rate": load_rate,
        "min_voltage": float(np.min(V)),
        "pf_failed_at": t_pf_failure,
        "voltage_collapse": t_voltage_collapse,
        "collapse": t_collapse,
        "speed_warning": t_speed_warning,
        "angle_warning": t_angle_warning,
        "speed_lead": safe_lead_time(t_collapse, t_speed_warning),
        "angle_lead": safe_lead_time(t_collapse, t_angle_warning),
        "mean_speed": float(np.mean(speed)),
        "max_speed": float(np.max(speed)),
        "mean_angle": float(np.mean(angle)),
        "max_angle": float(np.max(angle)),
    }

    artifacts = {
        "t": t,
        "V": V,
        "dv_dt": dv_dt,
        "curvature": curvature,
        "coords": coords,
        "window_times": window_times,
        "speed": speed,
        "speed_times": speed_times,
        "angle": angle,
        "angle_times": angle_times,
        "speed_threshold": speed_threshold,
        "angle_threshold": angle_threshold,
    }

    return result, artifacts


# ============================================================
# VISUALIZATION
# ============================================================

def plot_best_run(result, artifacts):
    t = artifacts["t"]
    V = artifacts["V"]
    dv_dt = artifacts["dv_dt"]
    curvature = artifacts["curvature"]

    coords = artifacts["coords"]
    window_times = artifacts["window_times"]

    speed = artifacts["speed"]
    speed_times = artifacts["speed_times"]
    angle = artifacts["angle"]
    angle_times = artifacts["angle_times"]

    speed_threshold = artifacts["speed_threshold"]
    angle_threshold = artifacts["angle_threshold"]

    t_collapse = result["collapse"]
    t_speed_warning = result["speed_warning"]
    t_angle_warning = result["angle_warning"]

    # --------------------------------------------------------
    # Figure 1: Voltage + signals
    # --------------------------------------------------------
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axs[0].plot(t, V, label="min voltage")
    axs[0].axhline(0.7, linestyle="--", label="collapse threshold")

    if t_collapse is not None:
        axs[0].axvline(t_collapse, linestyle="--", label="collapse")
    if t_angle_warning is not None:
        axs[0].axvline(t_angle_warning, linestyle=":", label="angle warning")
    if t_speed_warning is not None:
        axs[0].axvline(t_speed_warning, linestyle=":", label="speed warning")

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

    plt.suptitle(
        f"IEEE Signals — {result['case']} load_rate={result['load_rate']}"
    )
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Figure 2: Shape flow
    # --------------------------------------------------------
    plt.figure(figsize=(7, 6))

    sc = plt.scatter(
        coords[:, 0],
        coords[:, 1],
        c=window_times,
        s=18,
        alpha=0.85,
    )

    plt.plot(coords[:, 0], coords[:, 1], alpha=0.35)

    if t_collapse is not None:
        idx = np.argmin(np.abs(window_times - t_collapse))
        plt.scatter(
            coords[idx, 0],
            coords[idx, 1],
            marker="x",
            s=120,
            label="collapse region",
        )

    if t_angle_warning is not None:
        idx = np.argmin(np.abs(window_times - t_angle_warning))
        plt.scatter(
            coords[idx, 0],
            coords[idx, 1],
            marker="o",
            s=90,
            label="angle warning",
        )

    if t_speed_warning is not None:
        idx = np.argmin(np.abs(window_times - t_speed_warning))
        plt.scatter(
            coords[idx, 0],
            coords[idx, 1],
            marker="s",
            s=90,
            label="speed warning",
        )

    plt.title(
        f"IEEE Shape Flow — {result['case']} load_rate={result['load_rate']}"
    )
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.colorbar(sc, label="time")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Figure 3: Motion metrics
    # --------------------------------------------------------
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

    axs[1].plot(angle_times, angle, label="direction-change angle")
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

    plt.suptitle(
        f"IEEE Motion Metrics — {result['case']} load_rate={result['load_rate']}"
    )
    plt.tight_layout()
    plt.show()


# ============================================================
# SWEEP
# ============================================================

def run_sweep(
    case="ieee14",
    load_rates=None,
    plot_best=True,
):
    if load_rates is None:
        load_rates = [
            0.004,
            0.006,
            0.008,
            0.010,
            0.012,
            0.015,
            0.020,
            0.030,
        ]

    results = []
    artifacts_by_rate = {}

    print("\n=== NEXAH EXPERIMENT 009: IEEE COLLAPSE SWEEP ===")
    print(f"Case: {case}\n")

    for lr in load_rates:
        print(f"--- load_rate={lr} ---")

        out = analyze_ieee_run(
            case=case,
            load_rate=lr,
        )

        if out is None:
            print("  skipped: not enough data")
            continue

        result, artifacts = out
        results.append(result)
        artifacts_by_rate[lr] = artifacts

        print(
            f"  minV={result['min_voltage']:.3f} "
            f"collapse={fmt(result['collapse'])} "
            f"speed_warn={fmt(result['speed_warning'])} "
            f"angle_warn={fmt(result['angle_warning'])} "
            f"speed_lead={fmt(result['speed_lead'])} "
            f"angle_lead={fmt(result['angle_lead'])}"
        )

    print("\n=== SUMMARY TABLE ===\n")

    header = (
        f"{'rate':<8} {'minV':<8} {'collapse':<10} "
        f"{'s_warn':<10} {'a_warn':<10} "
        f"{'s_lead':<10} {'a_lead':<10}"
    )

    print(header)
    print("-" * len(header))

    for r in results:
        print(
            f"{r['load_rate']:<8.3f} "
            f"{r['min_voltage']:<8.3f} "
            f"{fmt(r['collapse']):<10} "
            f"{fmt(r['speed_warning']):<10} "
            f"{fmt(r['angle_warning']):<10} "
            f"{fmt(r['speed_lead']):<10} "
            f"{fmt(r['angle_lead']):<10}"
        )

    # Plot best run:
    # Prefer one with collapse and positive angle lead.
    candidates = [
        r for r in results
        if r["collapse"] is not None and r["angle_lead"] is not None
    ]

    if plot_best and len(candidates) > 0:
        best = max(candidates, key=lambda r: r["angle_lead"])
        artifacts = artifacts_by_rate[best["load_rate"]]

        print("\nPlotting best candidate:")
        print(best)

        plot_best_run(best, artifacts)

    elif plot_best:
        print("\nNo collapse + warning candidate found for plotting.")

    return results


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_sweep(
        case="ieee14",
        load_rates=[
            0.004,
            0.006,
            0.008,
            0.010,
            0.012,
            0.015,
            0.020,
            0.030,
            0.040,
            0.050,
        ],
        plot_best=True,
    )
