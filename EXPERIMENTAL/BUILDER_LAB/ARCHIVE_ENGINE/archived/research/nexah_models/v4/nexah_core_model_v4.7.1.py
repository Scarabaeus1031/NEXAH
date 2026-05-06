import numpy as np


# -----------------------------
# Signals
# -----------------------------
def generate_signal(case, t):
    if case == "collapse":
        return 1 - 1 / (1 + np.exp(-(t - 70) / 5))

    elif case == "slow_collapse":
        return 1 - 1 / (1 + np.exp(-(t - 65) / 10))

    elif case == "partial_collapse":
        return 1 - 0.5 / (1 + np.exp(-(t - 70) / 5))

    elif case == "fake_collapse":
        dip = 0.2 * np.exp(-((t - 70) / 10) ** 2)
        return 1 - dip

    elif case == "multi_step":
        return 1 - 0.3/(1+np.exp(-(t-60)/6)) - 0.3/(1+np.exp(-(t-80)/6))

    elif case == "stable_flat":
        return np.ones_like(t)

    return np.ones_like(t)


# -----------------------------
# Phase space
# -----------------------------
def compute_phase_space(v):
    dv = np.gradient(v)
    dv2 = np.gradient(dv)
    return np.vstack([v, dv, dv2]).T


def mahalanobis_distance(X, center, inv_cov):
    diff = X - center
    return np.sqrt(np.einsum("ij,jk,ik->i", diff, inv_cov, diff))


def fit_attractor(X, baseline_fraction=0.35):
    n = len(X)
    n0 = max(10, int(n * baseline_fraction))
    X0 = X[:n0]

    center = np.mean(X0, axis=0)
    cov = np.cov(X0.T) + 1e-6 * np.eye(X0.shape[1])
    inv_cov = np.linalg.inv(cov)

    d0 = mahalanobis_distance(X0, center, inv_cov)
    boundary = np.mean(d0) + 3.0 * np.std(d0)

    return center, inv_cov, boundary


# -----------------------------
# Drift / coherence
# -----------------------------
def compute_drift_score(X, window=30):
    scores = np.zeros(len(X))

    for i in range(len(X)):
        if i + window >= len(X):
            scores[i] = 0.0
            continue

        segment = X[i:i+window]
        start = segment[0]
        end = segment[-1]

        drift = np.linalg.norm(end - start)
        path = np.sum(np.linalg.norm(np.diff(segment, axis=0), axis=1))
        coherence = drift / (path + 1e-6)

        scores[i] = drift * coherence

    return scores


# -----------------------------
# v4.6.1 detector
# -----------------------------
def detect_split(t, v,
                 drift_threshold=0.02,
                 boundary_margin=1.05,
                 combined_threshold=1.2):
    X = compute_phase_space(v)

    center, inv_cov, boundary = fit_attractor(X, baseline_fraction=0.35)

    dist = mahalanobis_distance(X, center, inv_cov)
    boundary_score = dist / (boundary + 1e-6)

    drift_score = compute_drift_score(X, window=30)

    dv = np.gradient(v)
    directionality = np.zeros(len(v))
    w = 20
    for i in range(len(v)):
        if i + w >= len(v):
            directionality[i] = 0.0
        else:
            seg = dv[i:i+w]
            directionality[i] = np.abs(np.mean(np.sign(seg)))

    drift_n = drift_score / (np.max(drift_score) + 1e-6)
    boundary_excess = np.maximum(boundary_score - 1.0, 0.0)

    combined = (
        0.9 * drift_n +
        1.1 * boundary_excess +
        0.7 * directionality
    )

    split = None

    for i in range(len(t)):
        if t[i] < 10:
            continue

        cond = (
            (drift_n[i] > drift_threshold)
            and (boundary_score[i] > boundary_margin)
            and (combined[i] > combined_threshold)
        )

        if cond:
            split = t[i]
            break

    info = {
        "X": X,
        "center": center,
        "boundary": boundary,
        "dist": dist,
        "boundary_score": boundary_score,
        "drift_score": drift_score,
        "drift_n": drift_n,
        "directionality": directionality,
        "combined": combined,
    }

    return split, info


def detect_classic(t, v, threshold=0.7):
    idx = np.where(v < threshold)[0]
    return t[idx[0]] if len(idx) > 0 else None


# -----------------------------
# NEW: time-aware trajectory typing
# -----------------------------
def time_to_drop(seg_t, seg, frac):
    """
    Time until frac of the observed total drop is reached.
    frac = 0.1 means 10% of total drop, etc.
    """
    start_v = seg[0]
    end_v = seg[-1]
    total_drop = start_v - end_v

    if total_drop <= 1e-6:
        return None

    target = start_v - frac * total_drop
    idx = np.where(seg <= target)[0]
    if len(idx) == 0:
        return None

    return seg_t[idx[0]] - seg_t[0]


def classify_trajectory(t, v, split_time, lookahead=220):
    if split_time is None:
        return "stable_or_unclear", {}

    idx = np.searchsorted(t, split_time)
    end = min(len(v), idx + lookahead)

    if end - idx < 30:
        return "stable_or_unclear", {}

    seg = v[idx:end]
    seg_t = t[idx:end]

    dv = np.gradient(seg, seg_t)
    d2v = np.gradient(dv, seg_t)

    start_v = seg[0]
    min_v = np.min(seg)
    end_v = seg[-1]

    min_idx = np.argmin(seg)
    post_min = seg[min_idx:] if min_idx < len(seg) else np.array([end_v])

    max_after_min = np.max(post_min) if len(post_min) > 0 else end_v

    net_drop = start_v - end_v
    min_drop = start_v - min_v
    recovery = max_after_min - min_v
    mean_slope = np.mean(dv)
    oscillation = np.std(seg - np.linspace(seg[0], seg[-1], len(seg)))
    stepiness = np.mean(np.abs(d2v))

    # --- NEW time-aware features ---
    t10 = time_to_drop(seg_t, seg, 0.10)
    t30 = time_to_drop(seg_t, seg, 0.30)
    t60 = time_to_drop(seg_t, seg, 0.60)

    duration = seg_t[-1] - seg_t[0] + 1e-6
    drop_rate = net_drop / duration

    # early / late drop partition
    n = len(seg)
    n3 = max(3, n // 3)
    early_drop = seg[0] - np.mean(seg[:n3])
    mid_drop = np.mean(seg[:n3]) - np.mean(seg[n3:2*n3]) if 2*n3 <= n else 0.0
    late_drop = np.mean(seg[2*n3:]) - seg[-1] if 2*n3 < n else 0.0

    features = {
        "net_drop": float(net_drop),
        "min_drop": float(min_drop),
        "recovery": float(recovery),
        "mean_slope": float(mean_slope),
        "oscillation": float(oscillation),
        "stepiness": float(stepiness),
        "t10": None if t10 is None else float(t10),
        "t30": None if t30 is None else float(t30),
        "t60": None if t60 is None else float(t60),
        "drop_rate": float(drop_rate),
        "early_drop": float(early_drop),
        "mid_drop": float(mid_drop),
        "late_drop": float(late_drop),
    }

    # -----------------------------
    # RULES
    # -----------------------------

    # 1) fake recovery
    if recovery > 0.08 and end_v > start_v - 0.08:
        return "fake_recovery", features

    # 2) multi-step
    # multiple staged drops: later parts still keep dropping
    if stepiness > 0.00045 and late_drop > 0.03 and mid_drop > 0.03:
        return "multi_step", features

    # 3) partial collapse
    if 0.10 < net_drop < 0.38 and recovery < 0.06:
        return "partial_collapse", features

    # 4) slow collapse
    # takes time to achieve 30%/60% of observed drop
    if (
        mean_slope < -0.0025
        and net_drop >= 0.38
        and ((t30 is not None and t30 > 12.0) or (t60 is not None and t60 > 25.0))
    ):
        return "slow_collapse", features

    # 5) fast collapse
    if (
        net_drop >= 0.45
        and drop_rate > 0.01
        and ((t30 is not None and t30 < 10.0) or (t60 is not None and t60 < 20.0))
    ):
        return "fast_collapse", features

    return "stable_or_unclear", features


# -----------------------------
# Experiment
# -----------------------------
def run_case(case, runs=20):
    leads = []
    detections = 0
    labels = []

    for _ in range(runs):
        t = np.linspace(0, 120, 1200)

        v = generate_signal(case, t)
        v += np.random.normal(0, 0.002, size=len(v))

        split, _ = detect_split(t, v)
        classic = detect_classic(t, v)

        if split is not None:
            detections += 1

        label, _ = classify_trajectory(t, v, split)
        labels.append(label)

        if split is not None and classic is not None:
            leads.append(classic - split)

    print(f"\n=== Case: {case} ===")
    print(f"detection rate: {detections/20:.2f}")

    if len(leads) > 0:
        print(f"mean lead: {np.mean(leads):.2f}s")
        print(f"std lead:  {np.std(leads):.2f}s")
        print(f"min lead:  {np.min(leads):.2f}s")
        print(f"max lead:  {np.max(leads):.2f}s")
    else:
        print("no valid leads")

    unique, counts = np.unique(labels, return_counts=True)
    label_counts = dict(zip(unique, counts))
    print("trajectory types:", label_counts)

    return detections / 20, leads, label_counts


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    cases = [
        "collapse",
        "slow_collapse",
        "partial_collapse",
        "fake_collapse",
        "multi_step",
        "stable_flat",
    ]

    results = {}

    for case in cases:
        rate, leads, label_counts = run_case(case)
        results[case] = (rate, leads, label_counts)

    print("\n=== Overall Summary ===")
    for k, (rate, leads, label_counts) in results.items():
        mean_lead = np.mean(leads) if len(leads) > 0 else None
        print(f"{k:16} | detect_rate={rate:.2f} | lead_mean={mean_lead} | labels={label_counts}")
