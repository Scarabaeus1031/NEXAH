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
# NEXAH v4.9.2 Detector
# -----------------------------
def detect_nexah_v492(t, v):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    window = 10

    for i in range(window, len(v)):

        score = -dv[i] + 0.5 * (-d2v[i])

        phi_window = np.arctan2(d2v[i-window:i], dv[i-window:i] + 1e-8)
        lotus = 1 / (1 + np.std(phi_window))

        final_score = score * lotus

        # Activation guard
        if abs(dv[i]) < 0.001:
            continue

        # Trend filter
        trend = np.mean(dv[i-5:i])
        if trend > -0.002:
            continue

        # Threshold
        if final_score > 0.015:
            return t[i]

    return None


# -----------------------------
# Classic Detector
# -----------------------------
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

        split = detect_nexah_v492(t, v)
        classic = detect_classic(t, v)

        if split is not None:
            detections += 1

        if split is not None and classic is not None:
            leads.append(classic - split)

    print(f"\n=== Case: {case} ===")
    print(f"detection rate: {detections/runs:.2f}")

    if len(leads) > 0:
        print(f"mean lead: {np.mean(leads):.2f}s")
        print(f"std lead:  {np.std(leads):.2f}s")
        print(f"min lead:  {np.min(leads):.2f}s")
        print(f"max lead:  {np.max(leads):.2f}s")
    else:
        print("no valid leads")


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

    for case in cases:
        run_case(case)
