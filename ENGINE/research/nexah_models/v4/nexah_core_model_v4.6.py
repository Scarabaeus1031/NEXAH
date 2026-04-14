# nexah_core_model_v4.6.py

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
# Phase space embedding
# -----------------------------
def compute_phase_space(v):
    dv = np.gradient(v)
    dv2 = np.gradient(dv)
    return np.vstack([v, dv, dv2]).T


# -----------------------------
# 🔥 Drift detection in phase space
# -----------------------------
def compute_drift_score(X, window=30):

    scores = []

    for i in range(len(X)):

        if i + window >= len(X):
            scores.append(0)
            continue

        segment = X[i:i+window]

        # displacement
        start = segment[0]
        end = segment[-1]
        drift = np.linalg.norm(end - start)

        # path length
        path = np.sum(np.linalg.norm(np.diff(segment, axis=0), axis=1))

        # coherence: straight vs chaotic
        coherence = drift / (path + 1e-6)

        # magnitude + structure
        score = drift * coherence

        scores.append(score)

    return np.array(scores)


# -----------------------------
# Detection
# -----------------------------
def detect_split(t, v, threshold=0.02):

    X = compute_phase_space(v)
    scores = compute_drift_score(X)

    idx = np.where(scores > threshold)[0]

    return t[idx[0]] if len(idx) > 0 else None


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

        split = detect_split(t, v)
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
    else:
        print("no valid leads")

    return detections/20, leads


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
        "stable_flat"
    ]

    for case in cases:
        run_case(case)
