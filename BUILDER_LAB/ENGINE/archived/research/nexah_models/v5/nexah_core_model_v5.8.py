import numpy as np
import matplotlib.pyplot as plt


# -------------------------------
# Detection (wie v5.7 stabil)
# -------------------------------
def detect_split(t, v):
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    for i in range(10, len(v)):
        score = -dv[i] + 0.5 * (-d2v[i])

        if dv[i] > -0.002:
            continue

        if score > 0.01:
            return t[i]

    return None


# -------------------------------
# NEW: Controlled Oscillation
# -------------------------------
def apply_control_v58(t, v, split_t, target=0.85):

    v_ctrl = v.copy()
    dt = t[1] - t[0]

    k = 0.08          # base correction
    damping = 0.015   # damping
    omega = 0.25      # oscillation frequency

    for i in range(1, len(t)):

        if split_t is None or t[i] < split_t:
            continue

        error = v_ctrl[i-1] - target
        dv = v_ctrl[i-1] - v_ctrl[i-2] if i > 1 else 0

        # -----------------------
        # ENERGY (important)
        # -----------------------
        energy = dv**2

        # -----------------------
        # Oscillation amplitude
        # -----------------------
        amp = 0.02 + 0.2 * energy

        oscillation = amp * np.sin(omega * (t[i] - split_t))

        # -----------------------
        # Control law
        # -----------------------
        control = -k * error - damping * dv + oscillation

        v_ctrl[i] = v_ctrl[i-1] + control * dt

    return v_ctrl


# -------------------------------
# Collapse detection
# -------------------------------
def find_collapse(t, v, threshold=0.7):
    for i in range(len(v)):
        if v[i] < threshold:
            return t[i]
    return None


# -------------------------------
# Simulation cases
# -------------------------------
def simulate_case(case):

    t = np.linspace(0, 120, 1000)

    if case == "collapse":
        v = 1 / (1 + np.exp((t - 60)/5))

    elif case == "slow_collapse":
        v = 1 / (1 + np.exp((t - 55)/12))

    elif case == "partial_collapse":
        v = 1 - 0.5 / (1 + np.exp(-(t - 70)/4))

    elif case == "multi_step":
        v = 1 - 0.3/(1+np.exp(-(t-50)/5)) - 0.3/(1+np.exp(-(t-75)/5))

    else:
        v = np.ones_like(t)

    return t, v


# -------------------------------
# Energy
# -------------------------------
def compute_energy(t, v):
    dv = np.gradient(v, t)
    return dv**2


# -------------------------------
# Visualization
# -------------------------------
def plot_case(case):

    t, v = simulate_case(case)

    split = detect_split(t, v)
    v_ctrl = apply_control_v58(t, v, split)

    collapse_orig = find_collapse(t, v)
    collapse_ctrl = find_collapse(t, v_ctrl)

    energy = compute_energy(t, v)

    print(f"\n=== Case: {case} ===")
    print(f"split: {split}")
    print(f"original collapse: {collapse_orig}")
    print(f"controlled collapse: {collapse_ctrl}")

    if collapse_ctrl is None:
        print("→ stable oscillation regime")

    # -----------------------
    # PLOTS
    # -----------------------
    plt.figure(figsize=(15, 4))

    # Trajectory
    plt.subplot(1, 3, 1)
    plt.plot(t, v, label="original")
    plt.plot(t, v_ctrl, "--", label="controlled (oscillating)")
    if split:
        plt.axvline(split, color="red", linestyle=":", label="split")
    plt.axhline(0.7, color="black", linestyle="--", label="threshold")
    plt.title(f"{case} – Trajectory")
    plt.legend()

    # Phase space
    dv = np.gradient(v, t)
    d2v = np.gradient(dv, t)

    plt.subplot(1, 3, 2)
    plt.plot(dv, d2v)
    plt.axhline(0, color="black")
    plt.axvline(0, color="black")
    plt.title("Phase Space")

    # Energy
    plt.subplot(1, 3, 3)
    plt.plot(t, energy)
    plt.title("Energy")

    plt.tight_layout()
    plt.show()


# -------------------------------
# RUN
# -------------------------------
for case in ["collapse", "slow_collapse", "partial_collapse", "multi_step"]:
    plot_case(case)
