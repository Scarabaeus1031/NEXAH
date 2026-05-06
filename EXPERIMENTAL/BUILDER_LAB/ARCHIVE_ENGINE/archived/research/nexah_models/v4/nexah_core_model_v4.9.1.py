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
# Core detector (continuous)
# -----------------------------
def detect_nexah_v491(t, v):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    base_score = -dv + 0.5 * (-d2v)

    # rolling phase (Lotus soft factor)
    window = 10
    final_score = np.zeros_like(base_score)

    for i in range(window, len(v)):
        phi_window = np.arctan2(d2v[i-window:i], dv[i-window:i] + 1e-8)
        lotus = 1 / (1 + np.std(phi_window))

        final_score[i] = base_score[i] * lotus

    # normalize
    final_score /= (np.std(final_score) + 1e-6)

    # threshold
    idx = np.where(final_score > 2.5)[0]

    return t[idx[0]] if len(idx) > 0 else None


# -----------------------------
# Classic
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

        split = detect_nexah_v491(t, v)
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
