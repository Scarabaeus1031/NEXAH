import numpy as np
import matplotlib.pyplot as plt

# ============================================
# FIELD DEFINITION (THE CORE)
# ============================================

def nexah_field(v, dv):
    """
    Continuous vector field instead of control.
    Returns acceleration (d2v).
    """

    # ---- REGION CLASSIFICATION ----
    if v > 0.85:
        region = "core"
    elif v > 0.7:
        region = "transition"
    else:
        region = "danger"

    # ---- FIELD DYNAMICS ----
    if region == "core":
        # gentle stabilization
        d2v = -0.2 * dv - 0.1 * (v - 0.9)

    elif region == "transition":
        # guided drift (soft shaping)
        d2v = -0.4 * dv - 0.3 * (v - 0.85)

    else:
        # danger zone → strong repulsion
        d2v = -0.6 * dv + 1.2 * (0.75 - v)

    return d2v


# ============================================
# SIMULATION (FLOW THROUGH FIELD)
# ============================================

def simulate_nexah_v6(t, v0):
    dt = t[1] - t[0]

    v = np.zeros_like(t)
    dv = np.zeros_like(t)

    v[0] = v0
    dv[0] = 0

    for i in range(1, len(t)):
        d2v = nexah_field(v[i-1], dv[i-1])

        dv[i] = dv[i-1] + d2v * dt
        v[i] = v[i-1] + dv[i] * dt

        # numerical stability
        v[i] = np.clip(v[i], 0, 1.2)

    return v, dv


# ============================================
# ORIGINAL COLLAPSE SYSTEM (REFERENCE)
# ============================================

def generate_original(t, mode="collapse"):
    if mode == "collapse":
        return 1 / (1 + np.exp((t - 60) / 4))

    elif mode == "slow_collapse":
        return 1 / (1 + np.exp((t - 50) / 10))

    elif mode == "partial_collapse":
        return 0.5 + 0.5 / (1 + np.exp((t - 70) / 3))

    elif mode == "multi_step":
        v = 1 / (1 + np.exp((t - 55) / 6))
        v += 0.1 * np.sin(t / 5)
        return np.clip(v, 0, 1)

    else:
        return np.ones_like(t)


# ============================================
# COLLAPSE DETECTION
# ============================================

def detect_collapse(t, v):
    threshold = 0.7
    for i in range(len(v)):
        if v[i] < threshold:
            return t[i]
    return None


# ============================================
# VISUALIZATION
# ============================================

def plot_case(t, v_orig, v_ctrl, dv_ctrl, name):

    fig, axs = plt.subplots(1, 3, figsize=(18, 4))

    # --- TRAJECTORY ---
    axs[0].plot(t, v_orig, label="original")
    axs[0].plot(t, v_ctrl, '--', label="field-driven")
    axs[0].axhline(0.7, linestyle='--', label="threshold")
    axs[0].set_title(f"{name} — Trajectory")
    axs[0].legend()

    # --- PHASE SPACE ---
    axs[1].plot(dv_ctrl, np.gradient(dv_ctrl), linewidth=1)
    axs[1].axvline(0)
    axs[1].axhline(0)
    axs[1].set_title("Phase Space")

    # --- ENERGY ---
    energy = dv_ctrl**2
    axs[2].plot(t, energy)
    axs[2].set_title("Energy")

    plt.tight_layout()
    plt.show()


# ============================================
# FIELD VISUALIZATION (KEY PART)
# ============================================

def plot_field():

    v_vals = np.linspace(0.4, 1.1, 40)
    dv_vals = np.linspace(-0.05, 0.05, 40)

    V, DV = np.meshgrid(v_vals, dv_vals)

    D2V = np.zeros_like(V)

    for i in range(V.shape[0]):
        for j in range(V.shape[1]):
            D2V[i, j] = nexah_field(V[i, j], DV[i, j])

    plt.figure(figsize=(6,6))
    plt.streamplot(V, DV, DV, D2V, density=1.2)
    plt.title("NEXAH v6 — Field Geometry")
    plt.xlabel("v")
    plt.ylabel("dv")
    plt.show()


# ============================================
# RUN EXPERIMENTS
# ============================================

t = np.linspace(0, 120, 500)

cases = ["collapse", "slow_collapse", "partial_collapse", "multi_step"]

for case in cases:

    v_orig = generate_original(t, case)
    v_ctrl, dv_ctrl = simulate_nexah_v6(t, v_orig[0])

    t_orig = detect_collapse(t, v_orig)
    t_ctrl = detect_collapse(t, v_ctrl)

    print(f"\n=== Case: {case} ===")
    print(f"original collapse: {t_orig}")
    print(f"field result: {t_ctrl}")

    if t_ctrl is None:
        print("→ no collapse (field-stabilized)")
    else:
        print(f"delay: {t_ctrl - t_orig:.2f}s")

    plot_case(t, v_orig, v_ctrl, dv_ctrl, case)


# ============================================
# FIELD VIEW
# ============================================

plot_field()
