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


# -----------------------------
# Attractor / boundary model
# -----------------------------
def fit_attractor(X, baseline_fraction=0.35):
    n = len(X)
    n0 = max(10, int(n * baseline_fraction))
    X0 = X[:n0]

    center = np.mean(X0, axis=0)
    cov = np.cov(X0.T) + 1e-6 * np.eye(X0.shape[1])
    inv_cov = np.linalg.inv(cov)

    # Mahalanobis distance of baseline cloud to its own center
    d0 = mahalanobis_distance(X0, center, inv_cov)

    # Boundary estimate from baseline regime
    boundary = np.mean(d0) + 3.0 * np.std(d0)

    return center, inv_cov, boundary


def mahalanobis_distance(X, center, inv_cov):
    diff = X - center
    return np.sqrt(np.einsum("ij,jk,ik->i", diff, inv_cov, diff))


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

    # distance from attractor
    dist = mahalanobis_distance(X, center, inv_cov)

    # boundary score
    boundary_score = dist / (boundary + 1e-6)

    # drift score
    drift_score = compute_drift_score(X, window=30)

    # local directionality
    dv = np.gradient(v)
    directionality = np.zeros(len(v))
    w = 20
    for i in range(len(v)):
        if i + w >= len(v):
            directionality[i] = 0.0
        else:
            seg = dv[i:i+w]
            directionality[i] = np.abs(np.mean(np.sign(seg)))

    # normalize components
    drift_n = drift_score / (np.max(drift_score) + 1e-6)

    # only count boundary overflow above stable region
    boundary_excess = np.maximum(boundary_score - 1.0, 0.0)

    # combined score
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
# Experiment
# -----------------------------
def run_case(case, runs=20):
    leads = []
    detections = 0

    for _ in range(runs):
        t = np.linspace(0, 120, 1200)

        v = generate_signal(case, t)
        v += np.random.normal(0, 0.002, size=len(v))

        split, _ = detect_split(t, v)
        classic = detect_classic(t, v)

        if split is not None:
            detections += 1

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

    return detections / 20, leads


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
        rate, leads = run_case(case)
        results[case] = (rate, leads)

    print("\n=== Overall Summary ===")
    for k, (rate, leads) in results.items():
        mean_lead = np.mean(leads) if len(leads) > 0 else None
        print(f"{k:16} | detect_rate={rate:.2f} | lead_mean={mean_lead}")
