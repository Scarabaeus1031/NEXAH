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
# Basic derivatives
# -----------------------------
def compute_derivatives(v, t):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)
    return dv, d2v


# -----------------------------
# Regime classification per point
# -----------------------------
def classify_point(v, dv, d2v):
    if abs(dv) < 0.001:
        return "stable"

    if dv < -0.002:
        if d2v < -0.0005:
            return "acceleration"
        return "drift"

    if dv > 0.002:
        return "recovery"

    return "plateau"


# -----------------------------
# Segment into regimes
# -----------------------------
def segment_regimes(t, v):
    dv, d2v = compute_derivatives(v, t)

    regimes = []
    current = None
    start = 0

    for i in range(len(v)):
        r = classify_point(v[i], dv[i], d2v[i])

        if current is None:
            current = r
            start = i
            continue

        if r != current:
            regimes.append((current, start, i))
            current = r
            start = i

    regimes.append((current, start, len(v)))

    return regimes


# -----------------------------
# Collapse detection (simple)
# -----------------------------
def detect_split(t, v):
    dv = np.gradient(v)

    for i in range(len(v)):
        if t[i] < 10:
            continue

        if dv[i] < -0.01:
            return t[i]

    return None


def detect_classic(t, v, threshold=0.7):
    idx = np.where(v < threshold)[0]
    return t[idx[0]] if len(idx) > 0 else None


# -----------------------------
# Sequence extraction
# -----------------------------
def extract_sequence(regimes, t, split_time):
    if split_time is None:
        return []

    seq = []
    for r, s, e in regimes:
        if t[e-1] < split_time:
            continue
        seq.append(r)

    # compress repeats
    compressed = []
    for r in seq:
        if not compressed or compressed[-1] != r:
            compressed.append(r)

    return compressed


# -----------------------------
# Sequence → label
# -----------------------------
def classify_sequence(seq):
    if len(seq) == 0:
        return "stable_or_unclear"

    # normalize
    s = " ".join(seq)

    if "recovery" in s and "drift" not in s:
        return "fake_recovery"

    if s.startswith("drift acceleration"):
        return "fast_collapse"

    if "drift" in s and "acceleration" not in s:
        return "slow_collapse"

    if "plateau" in s and "drift" in s:
        return "multi_step"

    if "plateau" in s:
        return "partial_collapse"

    if "acceleration" in s:
        return "fast_collapse"

    return "stable_or_unclear"


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

        split = detect_split(t, v)
        classic = detect_classic(t, v)

        if split is not None:
            detections += 1

        regimes = segment_regimes(t, v)
        seq = extract_sequence(regimes, t, split)
        label = classify_sequence(seq)

        labels.append(label)

        if split is not None and classic is not None:
            leads.append(classic - split)

    print(f"\n=== Case: {case} ===")
    print(f"detection rate: {detections/20:.2f}")

    if len(leads) > 0:
        print(f"mean lead: {np.mean(leads):.2f}s")
        print(f"std lead:  {np.std(leads):.2f}s")
    else:
        print("no valid leads")

    unique, counts = np.unique(labels, return_counts=True)
    print("trajectory types:", dict(zip(unique, counts)))

    return detections / 20, leads, labels


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
