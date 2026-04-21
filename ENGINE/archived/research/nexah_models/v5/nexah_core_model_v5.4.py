import numpy as np
import matplotlib.pyplot as plt


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
# Detector (v5.4 with multi-step)
# -----------------------------
def detect_split(t, v):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    window = 10

    for i in range(window, len(v)):

        if t[i] < 30:
            continue

        # ---- main detection ----
        score = -dv[i] + 0.5 * (-d2v[i])

        phi_window = np.arctan2(d2v[i-window:i], dv[i-window:i] + 1e-8)
        lotus = 1 / (1 + np.std(phi_window))

        final_score = score * lotus

        if abs(dv[i]) > 0.005:
            trend = np.mean(dv[i-5:i])
            if trend < -0.01 and final_score > 0.02:
                return t[i]

        # ---- multi-step detection ----
        local_drops = 0
        for j in range(i-20, i):
            if dv[j] < -0.004:
                local_drops += 1

        if local_drops > 6:
            return t[i]

    return None


# -----------------------------
# Simulation with Optimal Control
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

    dv = np.gradient(v_controlled, t)

    for i in range(idx, len(t) - 1):

        d2v = (dv[i] - dv[i-1]) / dt

        # ---- energy ----
        energy = dv[i]**2 + 0.1 * d2v**2

        if energy < 0.00002:
            control = 0.0
        else:
            # ---- optimal control ----
            target_dv = -0.002
            error = dv[i] - target_dv

            control = -0.8 * error - 0.1 * d2v

        # ---- integrate ----
        dv[i+1] = dv[i] + control * dt
        v_controlled[i+1] = v_controlled[i] + dv[i+1] * dt

    return t, v, v_controlled, split_time


# -----------------------------
# Visuals
# -----------------------------
def plot_trajectory(t, v, v_ctrl, split):
    plt.figure(figsize=(10,5))

    plt.plot(t, v, label="original", linewidth=2)
    plt.plot(t, v_ctrl, label="controlled", linestyle="--")

    if split:
        plt.axvline(split, color="red", linestyle=":", label="split")

    plt.axhline(0.7, color="black", linestyle="--", label="collapse threshold")

    plt.legend()
    plt.title("NEXAH Control Trajectory")
    plt.xlabel("time")
    plt.ylabel("state")

    plt.show()


def plot_phase_space(v, t):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    plt.figure(figsize=(6,6))
    plt.plot(dv, d2v)

    plt.xlabel("dv")
    plt.ylabel("d2v")
    plt.title("Phase Space")

    plt.axhline(0, color="black")
    plt.axvline(0, color="black")

    plt.show()


def plot_energy(t, v):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    energy = dv**2 + 0.1 * d2v**2

    plt.figure(figsize=(10,4))
    plt.plot(t, energy)

    plt.title("System Energy")
    plt.xlabel("time")

    plt.show()


# -----------------------------
# Evaluation
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

    # ---- show visuals ----
    plot_trajectory(t, v, v_ctrl, split)
    plot_phase_space(v, t)
    plot_energy(t, v)


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
