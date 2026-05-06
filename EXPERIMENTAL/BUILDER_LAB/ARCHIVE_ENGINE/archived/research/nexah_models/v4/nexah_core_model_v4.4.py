import numpy as np
import matplotlib.pyplot as plt


# =========================
# HELPERS
# =========================

def moving_average(x, w):
    if w <= 1:
        return x
    return np.convolve(x, np.ones(w) / w, mode="same")


def classical_detection(voltage, t, threshold=0.7):
    idx = np.where(voltage < threshold)[0]
    return t[idx[0]] if len(idx) > 0 else None


def make_time(T=120.0, dt=0.1):
    return np.arange(0.0, T, dt)


# =========================
# SIGNAL GENERATORS
# =========================

def signal_collapse(t, seed=None):
    rng = np.random.default_rng(seed)
    v = 1.0 / (1.0 + np.exp(0.18 * (t - 73)))
    v += rng.normal(0, 0.002, len(t))
    return v


def signal_slow_collapse(t, seed=None):
    rng = np.random.default_rng(seed)
    v = 1.0 / (1.0 + np.exp(0.09 * (t - 73)))
    v += rng.normal(0, 0.002, len(t))
    return v


def signal_partial_collapse(t, seed=None):
    rng = np.random.default_rng(seed)
    drop = 0.45 / (1.0 + np.exp(-0.16 * (t - 73)))
    v = 1.0 - drop
    v += rng.normal(0, 0.002, len(t))
    return v


def signal_fake_collapse(t, seed=None):
    rng = np.random.default_rng(seed)
    base = np.ones_like(t)

    # local dip and recovery, not a true collapse
    dip = 0.22 * np.exp(-0.5 * ((t - 72) / 6.0) ** 2)
    recovery = 0.18 * np.exp(-0.5 * ((t - 88) / 7.0) ** 2)

    v = base - dip + recovery
    v += rng.normal(0, 0.003, len(t))
    v = np.clip(v, 0.72, 1.05)
    return v


def signal_multi_step(t, seed=None):
    rng = np.random.default_rng(seed)

    step1 = 0.10 / (1.0 + np.exp(-0.25 * (t - 55)))
    step2 = 0.18 / (1.0 + np.exp(-0.22 * (t - 72)))
    step3 = 0.25 / (1.0 + np.exp(-0.18 * (t - 86)))

    v = 1.0 - step1 - step2 - step3
    v += rng.normal(0, 0.0025, len(t))
    return v


def signal_stable_flat(t, seed=None):
    rng = np.random.default_rng(seed)
    v = np.ones_like(t)
    v += rng.normal(0, 0.002, len(t))
    return v


# =========================
# NEXAH DETECTOR
# =========================

def nexah_detect(t, v, deviation_th=3.0, baseline_end=50.0):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    v_s = moving_average(v, 7)
    dv_s = moving_average(dv, 7)
    d2v_s = moving_average(d2v, 7)

    X = np.column_stack([v_s, dv_s, d2v_s])

    base = t < baseline_end
    mu = np.mean(X[base], axis=0)
    cov = np.cov(X[base].T) + 1e-6 * np.eye(3)
    inv = np.linalg.inv(cov)

    diff = X - mu
    dist = np.sqrt(np.einsum("ij,jk,ik->i", diff, inv, diff))
    dist = moving_average(dist, 9)

    z = (dist - np.mean(dist[base])) / (np.std(dist[base]) + 1e-8)
    z = moving_average(z, 9)

    dv2 = np.gradient(v, t)
    d2v2 = np.gradient(dv2, t)
    local_stress = np.where(dv2 < 0, (-dv2) + 0.5 * np.abs(d2v2), 0.0)
    local_stress = moving_average(local_stress, 9)

    ls_z = (local_stress - np.mean(local_stress[base])) / (np.std(local_stress[base]) + 1e-8)

    MIN_TIME = 10.0
    voltage_gate = 0.95
    local_stress_th = 2.0

    PERSISTENCE = 8
    REQUIRED_RATIO = 0.75

    split = None

    for i in range(len(t)):
        if t[i] < MIN_TIME:
            continue

        cond = (
            v[i] < voltage_gate
            and (
                (z[i] > deviation_th)
                or ((z[i] > 2.2) and (ls_z[i] > local_stress_th))
            )
        )

        if cond:
            end = min(i + PERSISTENCE, len(t))
            window = (
                (z[i:end] > deviation_th)
                | ((z[i:end] > 2.2) & (ls_z[i:end] > local_stress_th))
            )
            if np.mean(window) >= REQUIRED_RATIO:
                split = t[i]
                break

    return split, {"deviation_z": z, "local_stress_z": ls_z}


# =========================
# EVALUATION
# =========================

def run_case(case_name, generator_fn, n_runs=20, seed_offset=0):
    t = make_time()

    detections = []
    leads = []

    print(f"\n=== Case: {case_name} ===")

    for i in range(n_runs):
        v = generator_fn(t, seed=seed_offset + i)

        split, _ = nexah_detect(t, v)
        classic = classical_detection(v, t)

        detections.append(split is not None)

        if split is not None and classic is not None:
            lead = classic - split
            leads.append(lead)
            print(f"run {i:02d} | split={split:.2f} | classic={classic:.2f} | lead={lead:.2f}")
        elif split is not None:
            print(f"run {i:02d} | split={split:.2f} | classic=None")
        else:
            print(f"run {i:02d} | split=None | classic={classic}")

    result = {
        "case": case_name,
        "detection_rate": float(np.mean(detections)),
        "lead_mean": float(np.mean(leads)) if len(leads) > 0 else None,
        "lead_std": float(np.std(leads)) if len(leads) > 0 else None,
        "lead_min": float(np.min(leads)) if len(leads) > 0 else None,
        "lead_max": float(np.max(leads)) if len(leads) > 0 else None,
        "n_leads": len(leads),
    }

    print("\n--- Summary ---")
    print(f"detection rate: {result['detection_rate']:.2f}")
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
        "slow_collapse": signal_slow_collapse(t, seed=2),
        "partial_collapse": signal_partial_collapse(t, seed=3),
        "fake_collapse": signal_fake_collapse(t, seed=4),
        "multi_step": signal_multi_step(t, seed=5),
    }

    fig, axes = plt.subplots(len(examples), 1, figsize=(10, 14), sharex=True)

    for ax, (name, v) in zip(axes, examples.items()):
        split, _ = nexah_detect(t, v)
        classic = classical_detection(v, t)

        ax.plot(t, v, label="voltage")
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
    results.append(run_case("slow_collapse", signal_slow_collapse, n_runs=20, seed_offset=200))
    results.append(run_case("partial_collapse", signal_partial_collapse, n_runs=20, seed_offset=300))
    results.append(run_case("fake_collapse", signal_fake_collapse, n_runs=20, seed_offset=400))
    results.append(run_case("multi_step", signal_multi_step, n_runs=20, seed_offset=500))
    results.append(run_case("stable_flat", signal_stable_flat, n_runs=20, seed_offset=600))

    print("\n=== Overall Summary ===")
    for r in results:
        print(
            f"{r['case']:16s} | detect_rate={r['detection_rate']:.2f} "
            f"| lead_mean={r['lead_mean']}"
        )

    plot_examples()
