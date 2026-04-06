# nexah_core_model_v4.5.1.py

import numpy as np

# -----------------------------
# Synthetic scenarios
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

    else:
        return np.ones_like(t)


# -----------------------------
# Core Detection (unchanged)
# -----------------------------
def detect_split(t, v, threshold=2.5):
    dv = np.gradient(v)
    dv2 = np.gradient(dv)

    deviation = np.abs(dv) + np.abs(dv2)
    z = (deviation - np.mean(deviation)) / (np.std(deviation) + 1e-6)

    idx = np.where(z > threshold)[0]
    return t[idx[0]] if len(idx) > 0 else None


def detect_classic(t, v, threshold=0.7):
    idx = np.where(v < threshold)[0]
    return t[idx[0]] if len(idx) > 0 else None


# -----------------------------
# 🔥 FIXED Irreversibility (Trend-based)
# -----------------------------
def is_irreversible(t, v, split_time, window=30, slope_tol=1e-4):
    if split_time is None:
        return False

    idx = np.searchsorted(t, split_time)

    if idx + window >= len(v):
        return False

    segment = v[idx:idx+window]
    time_seg = t[idx:idx+window]

    # linear slope
    slope = np.polyfit(time_seg, segment, 1)[0]

    # real collapse = continues downward
    if slope < -slope_tol:
        return True

    return False


# -----------------------------
# Run experiment
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

        # 🔥 NEW FILTER
        if not is_irreversible(t, v, split):
            split = None

        if split is not None:
            detections += 1

        if split is not None and classic is not None:
            leads.append(classic - split)

    print(f"\n=== Case: {case} ===")

    if len(leads) > 0:
        print(f"detection rate: {detections/runs:.2f}")
        print(f"mean lead: {np.mean(leads):.2f}s")
        print(f"std lead:  {np.std(leads):.2f}s")
    else:
        print(f"detection rate: {detections/runs:.2f}")
        print("no valid leads")

    return detections / runs, leads


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
