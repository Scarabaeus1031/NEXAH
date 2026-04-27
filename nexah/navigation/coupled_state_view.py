# ============================================================
# 🧭 NEXAH v12 — Coupled State View
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from nexah.navigation.state_space_control import (
    generate_signal,
    compute_risk,
    build_state_space,
    compute_adaptive_levels,
    assign_basins,
)


# ------------------------------------------------------------
# HELPER: colored trajectory
# ------------------------------------------------------------

def plot_colored_trajectory(x, v, color_values, cmap="viridis", linewidth=2):
    """
    Draw trajectory in state space with color encoding.
    """

    points = np.array([x, v]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    lc = LineCollection(segments, cmap=cmap)
    lc.set_array(color_values[:-1])
    lc.set_linewidth(linewidth)

    return lc


# ------------------------------------------------------------
# MAIN DEMO
# ------------------------------------------------------------

def demo():
    # --- DATA ---
    x = generate_signal()
    v = np.gradient(x)
    risk = compute_risk(x)

    states = build_state_space(x)

    # --- BASINS ---
    levels = compute_adaptive_levels(x, n_basins=10)
    basins = assign_basins(x, levels)

    # --------------------------------------------------------
    # FIGURE
    # --------------------------------------------------------

    fig = plt.figure(figsize=(14, 10))

    # --------------------------------------------------------
    # (1) TIME DOMAIN
    # --------------------------------------------------------

    ax1 = plt.subplot(3, 1, 1)

    ax1.plot(x, color="blue", alpha=0.7, label="x(t)")

    peaks = np.where(risk > 0.65)[0]
    ax1.scatter(peaks, x[peaks], color="red", s=20, label="High Risk")

    for level in levels:
        ax1.axhline(level, color="gray", alpha=0.08)

    ax1.set_title("Time Domain (x)")
    ax1.legend()


    # --------------------------------------------------------
    # (2) STATE SPACE — COUPLED VIEW
    # --------------------------------------------------------

    ax2 = plt.subplot(3, 1, 2)

    lc = plot_colored_trajectory(
        x,
        v,
        color_values=basins,   # color = basin
        cmap="plasma",
        linewidth=2,
    )

    ax2.add_collection(lc)

    ax2.set_xlim(np.min(x), np.max(x))
    ax2.set_ylim(np.min(v), np.max(v))

    ax2.set_title("State Space (x, v) — colored by basin")

    # highlight high risk
    ax2.scatter(x[peaks], v[peaks], color="red", s=20)

    plt.colorbar(lc, ax=ax2, label="Basin Index")


    # --------------------------------------------------------
    # (3) BASIN vs TIME
    # --------------------------------------------------------

    ax3 = plt.subplot(3, 1, 3)

    ax3.plot(basins, color="green", label="Basin(t)")

    ax3.scatter(peaks, basins[peaks], color="red", s=20)

    ax3.set_title("Basin Space (discrete)")
    ax3.set_xlabel("time")

    ax3.legend()


    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------

if __name__ == "__main__":
    demo()
