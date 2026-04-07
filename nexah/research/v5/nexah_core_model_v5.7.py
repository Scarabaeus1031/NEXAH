import numpy as np
import matplotlib.pyplot as plt


# =========================
# SIGNALS
# =========================

def generate_signal(case, t):
    if case == "collapse":
        return 1 / (1 + np.exp((t - 65) / 5))

    elif case == "slow_collapse":
        return 1 / (1 + np.exp((t - 60) / 12))

    elif case == "partial_collapse":
        return 1 - 0.5 * (1 / (1 + np.exp(-(t - 70) / 6)))

    elif case == "multi_step":
        return (
            1
            - 0.3 * (1 / (1 + np.exp(-(t - 55) / 6)))
            - 0.3 * (1 / (1 + np.exp(-(t - 78) / 6)))
        )

    return np.ones_like(t)


# =========================
# DERIVATIVES / ENERGY
# =========================

def compute_derivatives(v, t):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)
    return dv, d2v


def compute_energy(v, t):
    dv, d2v = compute_derivatives(v, t)
    return dv**2 + 0.5 * d2v**2


# =========================
# DETECTOR (v5.6)
# =========================

def detect_split(t, v):
    dv, d2v = compute_derivatives(v, t)
    energy = dv**2 + 0.5 * d2v**2

    for i in range(20, len(v)):
        if t[i] < 25:
            continue

        score = -dv[i] + 0.3 * (-d2v[i])

        phi = np.arctan2(d2v[i-10:i], dv[i-10:i] + 1e-8)
        lotus = 1 / (1 + np.std(phi))

        final = score * lotus

        curvature = np.mean(d2v[i-15:i])
        sign_flip = np.sign(dv[i]) != np.sign(dv[i-5])
        energy_rise = energy[i] > np.mean(energy[i-10:i])

        if abs(dv[i]) < 5e-4:
            continue

        if final > 0.008 or curvature < -5e-4 or sign_flip or energy_rise:
            return t[i]

    return None


# =========================
# CONTROL FIELD v5.7
# =========================

def control_field(v, dv, d2v, energy, target):

    # 🎯 TARGET ERROR
    state_error = v - target

    # velocity target: slow drift toward target
    target_dv = -0.003 * state_error

    velocity_error = dv - target_dv

    # adaptive gains
    if energy < 0.00003:
        k1, k2 = 0.4, 0.03
    elif energy < 0.0001:
        k1, k2 = 0.7, 0.06
    else:
        k1, k2 = 1.0, 0.12

    control = -k1 * velocity_error - k2 * d2v

    # 🔥 LIMIT (critical!)
    control = np.clip(control, -0.02, 0.02)

    # 🔥 SOFT LANDING near target
    if abs(state_error) < 0.05:
        control *= 0.3

    return control


# =========================
# SIMULATION
# =========================

def simulate(case, target=0.6):

    t = np.linspace(0, 120, 800)
    dt = t[1] - t[0]

    v = generate_signal(case, t)
    split = detect_split(t, v)

    v_ctrl = v.copy()
    dv_ctrl = np.gradient(v_ctrl, t)

    if split is None:
        return t, v, v_ctrl, split

    idx = np.searchsorted(t, split)

    for i in range(max(idx, 20), len(t)-1):

        dv = dv_ctrl[i]
        d2v = (dv_ctrl[i] - dv_ctrl[i-1]) / dt
        energy = dv**2 + 0.5 * d2v**2

        u = control_field(v_ctrl[i], dv, d2v, energy, target)

        dv_ctrl[i+1] = dv_ctrl[i] + u * dt
        v_ctrl[i+1] = v_ctrl[i] + dv_ctrl[i+1] * dt

    return t, v, v_ctrl, split


# =========================
# COLLAPSE DETECTION
# =========================

def detect_collapse(t, v, threshold=0.7):
    idx = np.where(v < threshold)[0]
    if len(idx) == 0:
        return None
    return t[idx[0]]


# =========================
# PLOTS
# =========================

def plot_case(t, v, v_ctrl, split, case):

    dv, d2v = compute_derivatives(v, t)
    energy = compute_energy(v, t)

    plt.figure(figsize=(14, 4))

    # trajectory
    plt.subplot(1, 3, 1)
    plt.plot(t, v, label="original")
    plt.plot(t, v_ctrl, "--", label="controlled")
    if split:
        plt.axvline(split, color="red", linestyle=":")
    plt.axhline(0.7, color="black", linestyle="--")
    plt.title(f"{case} – Trajectory")
    plt.legend()

    # phase
    plt.subplot(1, 3, 2)
    plt.plot(dv, d2v)
    plt.axhline(0, color="black")
    plt.axvline(0, color="black")
    plt.title("Phase Space")

    # energy
    plt.subplot(1, 3, 3)
    plt.plot(t, energy)
    plt.title("Energy")

    plt.tight_layout()
    plt.show()


# =========================
# RUN
# =========================

def run(case):

    t, v, v_ctrl, split = simulate(case, target=0.6)

    t_orig = detect_collapse(t, v)
    t_ctrl = detect_collapse(t, v_ctrl)

    print(f"\n=== Case: {case} ===")
    print("split:", split)
    print("original collapse:", t_orig)
    print("controlled collapse:", t_ctrl)

    if t_orig and t_ctrl:
        print("delay:", t_ctrl - t_orig)

    elif t_ctrl is None:
        print("→ stabilized near target")

    plot_case(t, v, v_ctrl, split, case)


if __name__ == "__main__":

    for case in ["collapse", "slow_collapse", "partial_collapse", "multi_step"]:
        run(case)
