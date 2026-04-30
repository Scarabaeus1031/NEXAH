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
    elif case == "multi_step":
        return 1 - 0.3/(1+np.exp(-(t-60)/6)) - 0.3/(1+np.exp(-(t-80)/6))
    return np.ones_like(t)


# -----------------------------
# Detector (v4.9.3)
# -----------------------------
def detect_split(t, v):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    window = 10

    for i in range(window, len(v)):

        if t[i] < 30:
            continue

        score = -dv[i] + 0.5 * (-d2v[i])

        phi_window = np.arctan2(d2v[i-window:i], dv[i-window:i] + 1e-8)
        lotus = 1 / (1 + np.std(phi_window))

        final_score = score * lotus

        if abs(dv[i]) < 0.005:
            continue

        trend = np.mean(dv[i-5:i])
        if trend > -0.01:
            continue

        if final_score > 0.02:
            return t[i]

    return None


# -----------------------------
# Simulation with Control (FIXED)
# -----------------------------
def simulate_with_control(case):

    t = np.linspace(0, 120, 1200)
    dt = t[1] - t[0]

    v = generate_signal(case, t)
    v_controlled = v.copy()

    split_time = detect_split(t, v)

    if split_time is None:
        return t, v, v_controlled, split_time

    idx = np.searchsorted(t, split_time)

    # initial velocity
    dv = np.gradient(v_controlled, t)

    for i in range(idx, len(t) - 1):

        d2v = (dv[i] - dv[i-1]) / dt

        # CONTROL (stable)
        control = -2.0 * dv[i] - 0.5 * d2v

        # integrate dynamics
        dv[i+1] = dv[i] + control * dt
        v_controlled[i+1] = v_controlled[i] + dv[i+1] * dt

    return t, v, v_controlled, split_time


# -----------------------------
# Evaluate
# -----------------------------
def evaluate(case):

    t, v, v_ctrl, split = simulate_with_control(case)

    collapse_original = np.where(v < 0.7)[0]
    collapse_ctrl = np.where(v_ctrl < 0.7)[0]

    t_orig = t[collapse_original[0]] if len(collapse_original) > 0 else None
    t_ctrl = t[collapse_ctrl[0]] if len(collapse_ctrl) > 0 else None

    print(f"\n=== Case: {case} ===")
    print(f"split detected at: {split}")
    print(f"original collapse: {t_orig}")
    print(f"controlled collapse: {t_ctrl}")

    if t_orig is not None and t_ctrl is not None:
        print(f"delay: {t_ctrl - t_orig:.2f}s")
    else:
        print("no collapse or fully stabilized")


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    cases = [
        "collapse",
        "slow_collapse",
        "partial_collapse",
        "multi_step",
    ]

    for case in cases:
        evaluate(case)
