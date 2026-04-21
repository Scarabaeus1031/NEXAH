import numpy as np
import matplotlib.pyplot as plt


# =========================
# HELPERS
# =========================

def moving_average(x, w):
    x = np.asarray(x, dtype=float)
    if w <= 1:
        return x
    kernel = np.ones(w, dtype=float) / w
    return np.convolve(x, kernel, mode="same")


def classical_detection(voltage, t, threshold=0.7):
    idx = np.where(voltage < threshold)[0]
    return t[idx[0]] if len(idx) > 0 else None


# =========================
# SIGNAL GENERATORS
# =========================

def make_time(T=120.0, dt=0.1):
    return np.arange(0.0, T, dt)


def signal_collapse(t, midpoint=73.0, steepness=0.18, noise=0.002, seed=None):
    rng = np.random.default_rng(seed)
    voltage = 1.0 / (1.0 + np.exp(steepness * (t - midpoint)))
    voltage += rng.normal(0.0, noise, size=len(t))
    return voltage


def signal_stable_flat(t, level=1.0, noise=0.002, seed=None):
    rng = np.random.default_rng(seed)
    voltage = np.full_like(t, level, dtype=float)
    voltage += rng.normal(0.0, noise, size=len(t))
    return voltage


def signal_random_walk(t, level=1.0, step_scale=0.0015, noise=0.001, seed=None):
    rng = np.random.default_rng(seed)
    steps = rng.normal(0.0, step_scale, size=len(t))
    walk = np.cumsum(steps)
    voltage = level + walk
    voltage += rng.normal(0.0, noise, size=len(t))
    voltage = np.clip(voltage, 0.75, 1.05)
    return voltage


def signal_noise_only(t, level=1.0, noise=0.006, seed=None):
    rng = np.random.default_rng(seed)
    voltage = np.full_like(t, level, dtype=float)
    voltage += rng.normal(0.0, noise, size=len(t))
    return voltage


# =========================
# NEXAH v4 DETECTOR
# =========================

def nexah_v4_detect(t, voltage, baseline_end=50.0, deviation_th=3.0):
    dv = np.gradient(voltage, t)
    d2v = np.gradient(dv, t)

    v_s = moving_average(voltage, 7)
    dv_s = moving_average(dv, 7)
    d2v_s = moving_average(d2v, 7)

    X = np.column_stack([v_s, dv_s, d2v_s])

    idx = np.where(t < baseline_end)[0]
    X0 = X[idx]

    mu = np.mean(X0, axis=0)
    cov = np.cov(X0.T) + 1e-6 * np.eye(3)
    cov_inv = np.linalg.inv(cov)

    diff = X - mu
    dist = np.sqrt(np.einsum("ij,jk,ik->i", diff, cov_inv, diff))
    dist_s = moving_average(dist, 9)

    base_mean = np.mean(dist_s[idx])
    base_std = np.std(dist_s[idx]) + 1e-8
    deviation_z = moving_average((dist_s - base_mean) / base_std, 9)

    dv2 = np.gradient(voltage, t)
    d2v2 = np.gradient(dv2, t)
    local_stress = np.where(dv2 < 0, (-dv2) + 0.5 * np.abs(d2v2), 0.0)
    local_stress_s = moving_average(local_stress, 9)

    ls_mean = np.mean(local_stress_s[idx])
    ls_std = np.std(local_stress_s[idx]) + 1e-8
    local_stress_z = (local_stress_s - ls_mean) / ls_std

    MIN_TIME = 10.0
    voltage_gate_level = 0.95
    local_stress_th = 2.0

    PERSISTENCE = 8
    REQUIRED_RATIO = 0.75

    split_time = None

    for i in range(len(t)):
        if t[i] < MIN_TIME:
            continue

        voltage_gate = voltage[i] < voltage_gate_level

        condition_now = (
            voltage_gate
            and (
                (deviation_z[i] > deviation_th)
                or (
                    deviation_z[i] > 2.2
                    and local_stress_z[i] > local_stress_th
                )
            )
        )

        if condition_now:
            end = min(i + PERSISTENCE, len(t))
            window = (
                (deviation_z[i:end] > deviation_th)
                | (
                    (deviation_z[i:end] > 2.2)
                    & (local_stress_z[i:end] > local_stress_th)
                )
            )
            if np.mean(window) >= REQUIRED_RATIO:
                split_time = t[i]
                break

    metrics = {
        "voltage_s": v_s,
        "dv_s": dv_s,
        "d2v_s": d2v_s,
        "manifold_distance": dist_s,
        "deviation_z": deviation_z,
        "local_stress_z": local_stress_z,
    }

    return split_time, metrics


# =========================
# EVALUATION
# =========================

def run_case(case_name, generator_fn, n_runs=20, seed_offset=0):
    t = make_time()

    leads = []
    detections = []

    print(f"\n=== Case: {case_name} ===")

    for i in range(n_runs):
        voltage = generator_fn(t, seed=seed_offset + i)

        split, _ = nexah_v4_detect(t, voltage)
        classic = classical_detection(voltage, t)

        detections.append(split is not None)

        if classic is not None and split is not None:
            lead = classic - split
            leads.append(lead)
            print(f"run {i:02d} | split={split:.2f} | classic={classic:.2f} | lead={lead:.2f}")
        elif split is not None:
            print(f"run {i:02d} | split={split:.2f} | classic=None")
        else:
            print(f"run {i:02d} | split=None | classic={classic}")

    detection_rate = np.mean(detections)

    result = {
        "case": case_name,
        "runs": n_runs,
        "detection_rate": detection_rate,
        "lead_mean": np.mean(leads) if len(leads) > 0 else None,
        "lead_std": np.std(leads) if len(leads) > 0 else None,
        "lead_min": np.min(leads) if len(leads) > 0 else None,
        "lead_max": np.max(leads) if len(leads) > 0 else None,
        "n_leads": len(leads),
    }

    print("\n--- Summary ---")
    print(f"detection rate: {detection_rate:.2f}")
    if len(leads) > 0:
        print(f"mean lead: {result['lead_mean']:.2f}s")
        print(f"std lead:  {result['lead_std']:.2f}s")
        print(f"min lead:  {result['lead_min']:.2f}s")
        print(f"max lead:  {result['lead_max']:.2f}s")
    else:
        print("no valid leads")

    return result


def plot_examples():
    t = make_time()

    examples = {
        "collapse": signal_collapse(t, seed=1),
        "stable_flat": signal_stable_flat(t, seed=2),
        "random_walk": signal_random_walk(t, seed=3),
        "noise_only": signal_noise_only(t, seed=4),
    }

    fig, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    for ax, (name, voltage) in zip(axes, examples.items()):
        split, metrics = nexah_v4_detect(t, voltage)
        classic = classical_detection(voltage, t)

        ax.plot(t, voltage, label="voltage")
        if split is not None:
            ax.axvline(split, color="green", label="split")
        if classic is not None:
            ax.axvline(classic, color="red", label="classic")
        ax.set_title(name)
        ax.legend()

    axes[-1].set_xlabel("Time")
    plt.tight_layout()
    plt.show()


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    results = []

    results.append(run_case("collapse", signal_collapse, n_runs=20, seed_offset=100))
    results.append(run_case("stable_flat", signal_stable_flat, n_runs=20, seed_offset=200))
    results.append(run_case("random_walk", signal_random_walk, n_runs=20, seed_offset=300))
    results.append(run_case("noise_only", signal_noise_only, n_runs=20, seed_offset=400))

    print("\n=== Overall Summary ===")
    for r in results:
        print(
            f"{r['case']:12s} | detect_rate={r['detection_rate']:.2f} "
            f"| lead_mean={r['lead_mean']}"
        )

    plot_examples()
