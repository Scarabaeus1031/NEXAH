# ============================================================
# 🧭 NEXAH — Multi-View Demo (v11)
# ============================================================
#
# Purpose:
# Visualize the SAME system in multiple representations:
#
# 1. Time Domain        → x(t)
# 2. State Space        → (x, v)
# 3. Basin Space        → discrete states
#
# Key Insight:
# The system does NOT change.
# The representation changes.
#
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

from nexah.navigation.state_space_control import (
    generate_signal,
    compute_risk,
    build_state_space,
    compute_adaptive_levels,
    assign_basins,
)


# ------------------------------------------------------------
# MAIN DEMO
# ------------------------------------------------------------

def multiview_demo(n=500, n_basins=10):

    # --- signal ---
    x = generate_signal(n=n)
    risk = compute_risk(x)

    # --- state space ---
    states = build_state_space(x)
    v = states[:, 1]

    # --- basins ---
    levels = compute_adaptive_levels(x, n_basins=n_basins)
    basins = assign_basins(x, levels)

    # --- high-risk points ---
    peaks = np.where(risk > 0.65)[0]

    # --------------------------------------------------------
    # PLOT
    # --------------------------------------------------------

    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # ========================================================
    # 1. TIME VIEW
    # ========================================================

    axs[0].plot(x, label="x(t)", color="blue", alpha=0.7)

    axs[0].scatter(
        peaks,
        x[peaks],
        color="red",
        s=20,
        label="High Risk"
    )

    for lvl in levels:
        axs[0].axhline(lvl, color="gray", alpha=0.1)

    axs[0].set_title("Time Domain (x)")
    axs[0].legend()

    # ========================================================
    # 2. STATE SPACE
    # ========================================================

    axs[1].plot(states[:, 0], states[:, 1], color="black", alpha=0.6)

    axs[1].scatter(
        states[peaks, 0],
        states[peaks, 1],
        color="red",
        s=20
    )

    axs[1].set_title("State Space (x, v)")
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("v")

    # ========================================================
    # 3. BASIN VIEW
    # ========================================================

    axs[2].plot(basins, color="green", alpha=0.7)

    axs[2].scatter(
        peaks,
        basins[peaks],
        color="red",
        s=20
    )

    axs[2].set_title("Basin Space (discrete states)")
    axs[2].set_xlabel("time")

    # --------------------------------------------------------
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# OPTIONAL: SCALE EFFECT (your "breathing" observation)
# ------------------------------------------------------------

def scaling_demo():

    x = generate_signal()

    fig, axs = plt.subplots(2, 1, figsize=(12, 6))

    # original
    axs[0].plot(x)
    axs[0].set_title("Original")

    # scaled (compressed)
    x_scaled = (x - np.mean(x)) * 0.5

    axs[1].plot(x_scaled)
    axs[1].set_title("Scaled (shrunk)")

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------

if __name__ == "__main__":
    multiview_demo()
