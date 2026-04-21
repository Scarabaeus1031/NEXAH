# nexah_core_model_v4.5.4.py

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
# Features
# -----------------------------
def compute_deviation(v):
    dv = np.gradient(v)
    dv2 = np.gradient(dv)

    deviation = np.abs(dv) + np.abs(dv2)
    z = (deviation - np.mean(deviation)) / (np.std(deviation) + 1e-6)

    return z


# -----------------------------
# Soft Score Model
# -----------------------------
def compute_scores(t, v):

    z = compute_deviation(v)

    dv = np.gradient(v)

    scores = []

    for i in range(len(t)):

        # --- detection ---
        detect_score = z[i]

        # --- local slope ---
        slope_score = max(0, -dv[i] * 50)

        # --- persistence (short window) ---
        w = 10
        if i + w < len(z):
            persistence = np.mean(z[i:i+w] > 1.0)
        else:
            persistence = 0

        # --- combined ---
        score = (
            0.7 * detect_score +
            0.5 * slope_score +
            0.6 * persistence
        )

        scores.append(score)

    return np.array(scores)


# -----------------------------
# Detection
# -----------------------------
def detect_split(t, v, threshold=3.5):

    scores = compute_scores(t, v)

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

    results = {}

    for case in cases:
        rate, leads = run_case(case)
        results[case] = (rate, leads)

    print("\n=== Overall Summary ===")
    for k, (rate, leads) in results.items():
        mean_lead = np.mean(leads) if len(leads) > 0 else None
        print(f"{k:16} | detect_rate={rate:.2f} | lead_mean={mean_lead}")
