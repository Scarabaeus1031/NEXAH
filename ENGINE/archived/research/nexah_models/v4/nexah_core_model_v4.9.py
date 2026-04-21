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
# Vendissimal state mapping
# -----------------------------
def vendissimal_state(dv, d2v, scale, accel_scale):
    if abs(dv) < 0.5 * scale:
        return 0
    elif dv < -1.5 * scale:
        if d2v < -1.0 * accel_scale:
            return -2
        return -1
    elif dv > 1.5 * scale:
        return +1
    return 0


# -----------------------------
# Phase space (spiral)
# -----------------------------
def compute_phase_space(dv, d2v):
    r = np.abs(dv)
    phi = np.arctan2(d2v, dv + 1e-8)
    return r, phi


# -----------------------------
# Lotus Gate detection
# -----------------------------
def detect_lotus_gate(t, v):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    scale = np.std(dv) + 1e-6
    accel_scale = np.std(d2v) + 1e-6

    states = []
    phis = []

    for i in range(len(v)):
        s = vendissimal_state(dv[i], d2v[i], scale, accel_scale)
        _, phi = compute_phase_space(dv[i], d2v[i])

        states.append(s)
        phis.append(phi)

    # detect transition pattern
    for i in range(10, len(v)-5):
        window = states[i-5:i]

        # pattern: stable → drift → acceleration
        if 0 in window and -1 in window and -2 in window:
            # phase stability check (lotus gate)
            phi_window = phis[i-5:i]
            if np.std(phi_window) < 0.5:
                return t[i]

    return None


# -----------------------------
# Classic threshold
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

        split = detect_lotus_gate(t, v)
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
