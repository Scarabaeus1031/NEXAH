import numpy as np
import matplotlib.pyplot as plt
import csv


# =========================
# HELPERS
# =========================

def moving_average(x, w):
    x = np.asarray(x, dtype=float)
    if w <= 1:
        return x
    kernel = np.ones(w, dtype=float) / w
    return np.convolve(x, kernel, mode="same")


def load_ieee_csv(path="data/ieee_sample.csv"):
    t, v = [], []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t.append(float(row["time"]))
            v.append(float(row["voltage"]))
    return np.array(t, dtype=float), np.array(v, dtype=float)


def classical_detection(voltage, t, threshold=0.7):
    idx = np.where(voltage < threshold)[0]
    return t[idx[0]] if len(idx) > 0 else None


# =========================
# EMBEDDING / MANIFOLD
# =========================

def build_embedding(t, voltage):
    """
    Minimal geometric state embedding.
    """
    dv = np.gradient(voltage, t)
    d2v = np.gradient(dv, t)

    # smoothing to reduce noise sensitivity
    v_s = moving_average(voltage, 7)
    dv_s = moving_average(dv, 7)
    d2v_s = moving_average(d2v, 7)

    X = np.column_stack([v_s, dv_s, d2v_s])

    return X, {
        "voltage_s": v_s,
        "dv_s": dv_s,
        "d2v_s": d2v_s,
    }


def fit_baseline_manifold(t, X, baseline_end=50.0):
    """
    Fit the stable manifold from the early regime.
    """
    idx = np.where(t < baseline_end)[0]
    X0 = X[idx]

    mu = np.mean(X0, axis=0)
    cov = np.cov(X0.T)

    # regularize covariance for numerical stability
    cov_reg = cov + 1e-6 * np.eye(cov.shape[0])
    cov_inv = np.linalg.inv(cov_reg)

    return mu, cov_inv


def mahalanobis_distance(X, mu, cov_inv):
    """
    Pointwise Mahalanobis distance to baseline manifold.
    """
    diff = X - mu
    d = np.sqrt(np.einsum("ij,jk,ik->i", diff, cov_inv, diff))
    return d


# =========================
# NEXAH v4.0 DETECTION
# =========================

def nexah_detection_v4(t, voltage):
    """
    Manifold-based detector:
    - build embedding
    - fit stable baseline manifold
    - compute deviation score
    - gate by system stress
    - persistence
    """
    X, emb = build_embedding(t, voltage)
    mu, cov_inv = fit_baseline_manifold(t, X, baseline_end=50.0)

    dist = mahalanobis_distance(X, mu, cov_inv)
    dist_s = moving_average(dist, 9)

    # baseline stats from early regime only
    baseline_idx = np.where(t < 50.0)[0]
    base_mean = np.mean(dist_s[baseline_idx])
    base_std = np.std(dist_s[baseline_idx]) + 1e-8

    deviation_z = (dist_s - base_mean) / base_std
    deviation_z = moving_average(deviation_z, 9)

    # optional local stress channel to help phase awareness
    dv = np.gradient(voltage, t)
    d2v = np.gradient(dv, t)
    local_stress = np.where(dv < 0, (-dv) + 0.5 * np.abs(d2v), 0.0)
    local_stress_s = moving_average(local_stress, 9)

    # normalized local stress
    ls_mean = np.mean(local_stress_s[baseline_idx])
    ls_std = np.std(local_stress_s[baseline_idx]) + 1e-8
    local_stress_z = (local_stress_s - ls_mean) / ls_std

    # ----- gating -----
    MIN_TIME = 10.0
    voltage_gate_level = 0.95

    # thresholds
    deviation_th = 3.0
    local_stress_th = 2.0

    # soft persistence
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
        **emb,
        "embedding": X,
        "manifold_distance": dist,
        "manifold_distance_s": dist_s,
        "deviation_z": deviation_z,
        "local_stress_z": local_stress_z,
    }

    return split_time, metrics


# =========================
# MAIN
# =========================

def run():
    t, voltage = load_ieee_csv("data/ieee_sample.csv")

    split, metrics = nexah_detection_v4(t, voltage)
    classic = classical_detection(voltage, t, threshold=0.7)

    lead = None
    if split is not None and classic is not None:
        lead = classic - split

    print("\nNEXAH v4.0 IEEE result")
    print("----------------------")
    print(f"split:   {split}")
    print(f"classic: {classic}")
    print(f"lead:    {lead}")

    fig, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    # 1) voltage
    axes[0].plot(t, voltage, label="voltage")
    if split is not None:
        axes[0].axvline(split, color="green", label="split")
    if classic is not None:
        axes[0].axvline(classic, color="red", label="classic")
    axes[0].axhline(0.7, linestyle="--", alpha=0.5, label="classic threshold")
    axes[0].axhline(0.95, linestyle=":", alpha=0.4, label="voltage gate")
    axes[0].set_title("NEXAH v4.0 – Manifold Deviation Detector")
    axes[0].set_ylabel("Voltage")
    axes[0].legend()

    # 2) embedding channels
    axes[1].plot(t, metrics["voltage_s"], label="V")
    axes[1].plot(t, metrics["dv_s"], label="dV/dt")
    axes[1].plot(t, metrics["d2v_s"], label="d²V/dt²")
    axes[1].set_ylabel("Embedding")
    axes[1].legend()

    # 3) manifold distance
    axes[2].plot(t, metrics["manifold_distance_s"], label="manifold distance")
    axes[2].plot(t, metrics["deviation_z"], label="deviation z")
    axes[2].set_ylabel("Deviation")
    axes[2].legend()

    # 4) local stress
    axes[3].plot(t, metrics["local_stress_z"], label="local stress z")
    axes[3].set_ylabel("Stress")
    axes[3].set_xlabel("Time")
    axes[3].legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run()
