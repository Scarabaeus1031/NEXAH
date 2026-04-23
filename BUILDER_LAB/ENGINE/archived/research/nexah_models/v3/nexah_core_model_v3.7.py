import numpy as np
import matplotlib.pyplot as plt
import csv


# =========================
# HELPERS
# =========================

def zscore(x):
    x = np.array(x, dtype=float)
    return (x - np.mean(x)) / (np.std(x) + 1e-8)


def moving_average(x, w):
    x = np.asarray(x, dtype=float)
    if w <= 1:
        return x
    kernel = np.ones(w, dtype=float) / w
    return np.convolve(x, kernel, mode="same")


# =========================
# LOAD IEEE-LIKE DATA
# =========================

def load_ieee_csv(path="data/ieee_sample.csv"):
    t, v = [], []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t.append(float(row["time"]))
            v.append(float(row["voltage"]))
    return np.array(t), np.array(v)


# =========================
# CLASSICAL DETECTION
# =========================

def classical_detection(voltage, t, threshold=0.7):
    idx = np.where(voltage < threshold)[0]
    return t[idx[0]] if len(idx) > 0 else None


# =========================
# MULTI-NODE FIELD BUILD
# =========================

def build_multinode_field(
    voltage,
    n_nodes=8,
    noise_scale=0.003,
    lag_strength=0.002,
    spread_gain=0.04,
    seed=42,
):
    """
    Build a small ensemble of node-like signals from one base voltage signal.

    Idea:
    - all nodes share the same base collapse trend
    - each node gets slight phase / lag / gain / noise differences
    - spread increases with system stress
    """
    rng = np.random.default_rng(seed)

    N = len(voltage)
    x = np.linspace(0.0, 1.0, N)

    # stress proxy from voltage drop
    stress = 1.0 - voltage
    stress = np.clip(stress, 0.0, 1.0)

    nodes = np.zeros((N, n_nodes), dtype=float)

    for j in range(n_nodes):
        gain_j = 1.0 + rng.normal(0.0, 0.01)
        noise_j = rng.normal(0.0, noise_scale, size=N)

        # small structured lag / deformation
        phase_j = rng.uniform(-0.5, 0.5)
        deform = lag_strength * np.sin(2 * np.pi * (x * (1.0 + 0.05 * j) + phase_j))

        # stress-dependent spread
        spread = spread_gain * stress * rng.normal(0.0, 1.0, size=N)

        node = gain_j * voltage + deform + spread + noise_j
        nodes[:, j] = node

    return nodes


# =========================
# NEXAH DETECTION v3.7
# =========================

def nexah_detection_v37(t, voltage, nodes):
    """
    Hybrid detection:
    - local channel: dv + d2v
    - global channel: sync loss / node spread
    - phase gate: only allow trigger once system is in stress region
    - soft persistence
    """

    # ----- local collapse geometry -----
    dv = np.gradient(voltage, t)
    d2v = np.gradient(dv, t)

    curvature = np.abs(d2v)
    lyapunov_proxy = np.abs(dv)

    curvature_z = zscore(curvature)
    lyapunov_z = zscore(lyapunov_proxy)

    collapse_signal = np.where(
        dv < 0,
        (-dv) + np.abs(d2v),
        0.0
    )
    collapse_z = zscore(collapse_signal)

    local_score_raw = curvature_z + lyapunov_z + 0.8 * collapse_z
    local_score = moving_average(local_score_raw, 7)

    # ----- global collective structure -----
    node_mean = np.mean(nodes, axis=1)
    node_std = np.std(nodes, axis=1)

    # simple coherence proxy: low std -> high coherence
    coherence = 1.0 / (1.0 + node_std)

    sync_loss = (1.0 - coherence) + 1.4 * node_std
    sync_loss_z = zscore(sync_loss)
    sync_loss_smooth = moving_average(sync_loss_z, 9)

    # ----- hybrid score -----
    hybrid_score = 0.65 * local_score + 0.85 * sync_loss_smooth
    hybrid_score = moving_average(hybrid_score, 9)

    # ----- gates -----
    MIN_TIME = 10.0
    voltage_gate_level = 0.95

    # thresholds
    local_th = 2.2
    sync_th = 1.2
    hybrid_th = 1.8

    # persistence
    PERSISTENCE = 6
    REQUIRED_RATIO = 0.75

    split_time = None

    for i in range(len(t)):
        if t[i] < MIN_TIME:
            continue

        voltage_gate = voltage[i] < voltage_gate_level

        condition_now = (
            voltage_gate
            and (
                (hybrid_score[i] > hybrid_th)
                or (
                    local_score[i] > local_th
                    and sync_loss_smooth[i] > sync_th
                )
            )
        )

        if condition_now:
            end = min(i + PERSISTENCE, len(t))
            window = (
                (
                    hybrid_score[i:end] > hybrid_th
                )
                | (
                    (local_score[i:end] > local_th)
                    & (sync_loss_smooth[i:end] > sync_th)
                )
            )

            if np.mean(window) >= REQUIRED_RATIO:
                split_time = t[i]
                break

    metrics = {
        "dv": dv,
        "d2v": d2v,
        "curvature_z": curvature_z,
        "lyapunov_z": lyapunov_z,
        "collapse_z": collapse_z,
        "local_score": local_score,
        "node_mean": node_mean,
        "node_std": node_std,
        "coherence": coherence,
        "sync_loss_z": sync_loss_z,
        "sync_loss_smooth": sync_loss_smooth,
        "hybrid_score": hybrid_score,
    }

    return split_time, metrics


# =========================
# MAIN
# =========================

def run():
    t, voltage = load_ieee_csv("data/ieee_sample.csv")

    nodes = build_multinode_field(
        voltage,
        n_nodes=8,
        noise_scale=0.003,
        lag_strength=0.002,
        spread_gain=0.04,
        seed=42,
    )

    split, metrics = nexah_detection_v37(t, voltage, nodes)
    classic = classical_detection(voltage, t, threshold=0.7)

    lead = None
    if split is not None and classic is not None:
        lead = classic - split

    print("\nNEXAH v3.7 IEEE result")
    print("----------------------")
    print(f"split:   {split}")
    print(f"classic: {classic}")
    print(f"lead:    {lead}")

    # ----- plots -----
    fig, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    # 1) voltage
    axes[0].plot(t, voltage, label="voltage")
    if split is not None:
        axes[0].axvline(split, color="green", label="split")
    if classic is not None:
        axes[0].axvline(classic, color="red", label="classic")
    axes[0].axhline(0.7, linestyle="--", alpha=0.5)
    axes[0].axhline(0.95, linestyle=":", alpha=0.4, label="voltage gate")
    axes[0].set_title("NEXAH v3.7 – IEEE Detection (Hybrid Local + Global)")
    axes[0].set_ylabel("Voltage")
    axes[0].legend()

    # 2) multi-node field
    axes[1].plot(t, metrics["node_mean"], label="node mean")
    axes[1].fill_between(
        t,
        metrics["node_mean"] - metrics["node_std"],
        metrics["node_mean"] + metrics["node_std"],
        alpha=0.25,
        label="node spread"
    )
    axes[1].set_ylabel("Field")
    axes[1].legend()

    # 3) local metrics
    axes[2].plot(t, metrics["local_score"], label="local score")
    axes[2].plot(t, metrics["collapse_z"], label="collapse z", alpha=0.8)
    axes[2].set_ylabel("Local")
    axes[2].legend()

    # 4) global / hybrid metrics
    axes[3].plot(t, metrics["sync_loss_smooth"], label="sync loss")
    axes[3].plot(t, metrics["hybrid_score"], label="hybrid score")
    axes[3].set_ylabel("Global / Hybrid")
    axes[3].set_xlabel("Time")
    axes[3].legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run()
