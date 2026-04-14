import numpy as np
import matplotlib.pyplot as plt


# =========================
# SIGNAL GENERATORS
# =========================

def generate_signal(case, t):
    if case == "collapse":
        return 1.0 / (1.0 + np.exp((t - 65.0) / 5.0))

    elif case == "slow_collapse":
        return 1.0 / (1.0 + np.exp((t - 60.0) / 12.0))

    elif case == "partial_collapse":
        # starts near 1.0, ends near 0.5
        return 1.0 - 0.5 * (1.0 / (1.0 + np.exp(-(t - 70.0) / 6.0)))

    elif case == "multi_step":
        return (
            1.0
            - 0.3 * (1.0 / (1.0 + np.exp(-(t - 55.0) / 6.0)))
            - 0.3 * (1.0 / (1.0 + np.exp(-(t - 78.0) / 6.0)))
        )

    elif case == "stable_flat":
        return np.ones_like(t)

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
# V5.6 DETECTOR
# =========================

def detect_split_v56(t, v):
    dv, d2v = compute_derivatives(v, t)
    energy = dv**2 + 0.5 * d2v**2

    for i in range(20, len(v)):
        if t[i] < 25:
            continue

        # ---- Base score ----
        score = -dv[i] + 0.3 * (-d2v[i])

        # ---- Lotus / phase coherence ----
        phi = np.arctan2(d2v[i-10:i], dv[i-10:i] + 1e-8)
        lotus = 1.0 / (1.0 + np.std(phi))

        final = score * lotus

        # ---- Curvature memory ----
        curvature_trend = np.mean(d2v[i-15:i])

        # ---- Sign flip / regime switch ----
        sign_flip = np.sign(dv[i]) != np.sign(dv[i-5])

        # ---- Energy precursor ----
        energy_rise = energy[i] > np.mean(energy[i-10:i])

        # ---- Activation guard ----
        if abs(dv[i]) < 5e-4:
            continue

        # ---- Detection logic ----
        if (
            final > 0.008
            or curvature_trend < -5e-4
            or sign_flip
            or energy_rise
        ):
            return t[i]

    return None


# =========================
# CONTROL FIELD (V5.6)
# =========================

def control_field(v_now, dv_now, d2v_now, energy_now, energy_mean_prev, regime_boost=0.0):
    """
    NEXAH field-style control:
    - low energy  -> soft guidance
    - mid energy  -> medium stabilization
    - high energy -> strong stabilization
    - regime_boost adds extra control for multi-step / curvature transitions
    """

    # Target drift: allow slight negative drift, not full stop
    target_dv = -0.002
    error = dv_now - target_dv

    if energy_now < 0.00003:
        k_err = 0.35
        k_acc = 0.03
    elif energy_now < 0.00010:
        k_err = 0.60
        k_acc = 0.06
    else:
        k_err = 0.95
        k_acc = 0.12

    control = -k_err * error - k_acc * d2v_now

    # Energy precursor reinforcement
    if energy_now > energy_mean_prev:
        control += -0.08 * error

    # Regime-sensitive reinforcement
    control += regime_boost

    return control


# =========================
# SIMULATION WITH CONTROL
# =========================

def simulate_with_control(case):
    t = np.linspace(0.0, 120.0, 800)
    dt = t[1] - t[0]

    v = generate_signal(case, t)
    split_time = detect_split_v56(t, v)

    v_ctrl = v.copy()

    if split_time is None:
        return t, v, v_ctrl, split_time

    idx = np.searchsorted(t, split_time)

    # initialize controlled velocity from uncontrolled signal
    dv_ctrl = np.gradient(v_ctrl, t)

    for i in range(max(idx, 20), len(t) - 1):
        d2v_now = (dv_ctrl[i] - dv_ctrl[i - 1]) / dt
        energy_now = dv_ctrl[i]**2 + 0.5 * d2v_now**2
        energy_mean_prev = np.mean(
            (dv_ctrl[i-10:i] ** 2) + 0.5 * (np.gradient(dv_ctrl[i-10:i], t[i-10:i]) ** 2)
        )

        # ---- multi-step / regime boost ----
        regime_boost = 0.0

        if i > 8:
            # curvature jump
            d2v_prev = (dv_ctrl[i - 5] - dv_ctrl[i - 6]) / dt
            curvature_change = d2v_now - d2v_prev

            # sign-flip / local regime change
            sign_flip = np.sign(dv_ctrl[i]) != np.sign(dv_ctrl[i - 5])

            if curvature_change > 0.001:
                regime_boost += -0.10 * (dv_ctrl[i] + 0.002)

            if sign_flip:
                regime_boost += -0.06 * (dv_ctrl[i] + 0.002)

        # ---- control ----
        u = control_field(
            v_now=v_ctrl[i],
            dv_now=dv_ctrl[i],
            d2v_now=d2v_now,
            energy_now=energy_now,
            energy_mean_prev=energy_mean_prev,
            regime_boost=regime_boost,
        )

        # ---- integrate dynamics ----
        dv_ctrl[i + 1] = dv_ctrl[i] + u * dt
        v_ctrl[i + 1] = v_ctrl[i] + dv_ctrl[i + 1] * dt

    return t, v, v_ctrl, split_time


# =========================
# COLLAPSE TIME
# =========================

def detect_collapse_time(t, v, threshold=0.7):
    idx = np.where(v < threshold)[0]
    if len(idx) == 0:
        return None
    return t[idx[0]]


# =========================
# VISUALS
# =========================

def plot_case(t, v, v_ctrl, split_time, title_prefix=""):
    dv, d2v = compute_derivatives(v, t)
    energy = compute_energy(v, t)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    # Trajectory
    axes[0].plot(t, v, label="original")
    axes[0].plot(t, v_ctrl, "--", label="controlled")
    if split_time is not None:
        axes[0].axvline(split_time, color="red", linestyle=":", label="split")
    axes[0].axhline(0.7, color="black", linestyle="--", label="collapse threshold")
    axes[0].set_title("Trajectory")
    axes[0].legend()

    # Phase space
    axes[1].plot(dv, d2v)
    axes[1].axhline(0.0, color="black")
    axes[1].axvline(0.0, color="black")
    axes[1].set_title("Phase Space")
    axes[1].set_xlabel("dv")
    axes[1].set_ylabel("d2v")

    # Energy
    axes[2].plot(t, energy)
    axes[2].set_title("Energy")
    axes[2].set_xlabel("time")

    if title_prefix:
        fig.suptitle(title_prefix)

    plt.tight_layout()
    plt.show()


# =========================
# EVALUATION
# =========================

def evaluate_case(case):
    t, v, v_ctrl, split_time = simulate_with_control(case)

    t_orig = detect_collapse_time(t, v)
    t_ctrl = detect_collapse_time(t, v_ctrl)

    print(f"\n=== Case: {case} ===")
    print(f"split detected at: {split_time}")
    print(f"original collapse: {t_orig}")
    print(f"controlled collapse: {t_ctrl}")

    if t_orig is not None and t_ctrl is not None:
        print(f"delay: {t_ctrl - t_orig:.2f}s")
    elif t_orig is not None and t_ctrl is None:
        print("no collapse or stabilized")
    else:
        print("no collapse in baseline")

    plot_case(t, v, v_ctrl, split_time, title_prefix=f"NEXAH v5.6 — {case}")


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    for case in ["collapse", "slow_collapse", "partial_collapse", "multi_step"]:
        evaluate_case(case)
