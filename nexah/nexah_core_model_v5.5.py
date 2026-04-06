import numpy as np
import matplotlib.pyplot as plt


# =========================
# SIGNAL GENERATORS
# =========================

def generate_collapse(t):
    return 1 / (1 + np.exp((t - 65) / 5))


def generate_slow_collapse(t):
    return 1 / (1 + np.exp((t - 60) / 12))


def generate_partial_collapse(t):
    return 1 - 0.5 * (1 / (1 + np.exp((t - 70) / 6)))


def generate_multi_step(t):
    return 1 - 0.3 * (1 / (1 + np.exp((t - 55) / 6))) \
             - 0.3 * (1 / (1 + np.exp((t - 75) / 6)))


# =========================
# DETECTION (v4.9.3 stable base)
# =========================

def detect_split(t, v):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    for i in range(10, len(v)):

        score = -dv[i] + 0.4 * (-d2v[i])

        # lotus smoothing
        phi = np.arctan2(d2v[i-10:i], dv[i-10:i] + 1e-8)
        lotus = 1 / (1 + np.std(phi))

        final = score * lotus

        # activation guard
        if abs(dv[i]) < 0.001:
            continue

        # trend filter
        if np.mean(dv[i-5:i]) > -0.002:
            continue

        if final > 0.01:
            return t[i]

    return None


# =========================
# ENERGY
# =========================

def compute_energy(dv, d2v):
    return dv**2 + 0.5 * d2v**2


# =========================
# CONTROL (v5.5 ADAPTIVE)
# =========================

def apply_control(t, v, split_time):

    if split_time is None:
        return v.copy()

    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)
    energy = compute_energy(dv, d2v)

    v_ctrl = v.copy()

    for i in range(len(v)):

        if t[i] < split_time:
            continue

        error = v_ctrl[i] - 1.0

        # =========================
        # ADAPTIVE CONTROL
        # =========================

        if energy[i] < 0.00005:
            # soft mode
            control = -0.5 * error - 0.05 * d2v[i]

        elif energy[i] < 0.00015:
            # mid mode
            control = -0.8 * error - 0.1 * d2v[i]

        else:
            # hard mode
            control = -1.2 * error - 0.2 * d2v[i]

        # =========================
        # MULTI-STEP BOOST
        # =========================

        if i > 5:
            curvature_change = d2v[i] - d2v[i-5]

            if curvature_change > 0.001:
                control += -0.3 * error   # reinforce control

        v_ctrl[i] += control

    return v_ctrl


# =========================
# COLLAPSE DETECTION
# =========================

def detect_collapse(t, v):
    for i in range(len(v)):
        if v[i] < 0.7:
            return t[i]
    return None


# =========================
# VISUALS
# =========================

def plot_case(t, v, v_ctrl, split):

    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)
    energy = compute_energy(dv, d2v)

    plt.figure(figsize=(14, 4))

    # trajectory
    plt.subplot(1, 3, 1)
    plt.plot(t, v, label="original")
    plt.plot(t, v_ctrl, "--", label="controlled")
    if split:
        plt.axvline(split, color="r", linestyle=":")
    plt.axhline(0.7, color="k", linestyle="--")
    plt.title("Trajectory")
    plt.legend()

    # phase space
    plt.subplot(1, 3, 2)
    plt.plot(dv, d2v)
    plt.axhline(0, color="k")
    plt.axvline(0, color="k")
    plt.title("Phase Space")

    # energy
    plt.subplot(1, 3, 3)
    plt.plot(t, energy)
    plt.title("Energy")

    plt.tight_layout()
    plt.show()


# =========================
# RUN TESTS
# =========================

def run_case(name, generator):

    t = np.linspace(0, 120, 500)
    v = generator(t)

    split = detect_split(t, v)
    v_ctrl = apply_control(t, v, split)

    collapse_orig = detect_collapse(t, v)
    collapse_ctrl = detect_collapse(t, v_ctrl)

    print(f"\n=== Case: {name} ===")
    print("split detected at:", split)
    print("original collapse:", collapse_orig)
    print("controlled collapse:", collapse_ctrl)

    if collapse_orig and collapse_ctrl:
        print(f"delay: {collapse_ctrl - collapse_orig:.2f}s")

    elif collapse_ctrl is None:
        print("no collapse or stabilized")

    plot_case(t, v, v_ctrl, split)


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    run_case("collapse", generate_collapse)
    run_case("slow_collapse", generate_slow_collapse)
    run_case("partial_collapse", generate_partial_collapse)
    run_case("multi_step", generate_multi_step)
