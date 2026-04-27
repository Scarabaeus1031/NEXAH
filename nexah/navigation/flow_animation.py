# ============================================================
# 🧭 NEXAH v13 — Flow Animation
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from nexah.navigation.state_space_control import (
    generate_signal,
    compute_risk,
    build_state_space,
    compute_adaptive_levels,
    assign_basins,
)


def run_flow_animation(
    n=500,
    n_basins=10,
    risk_threshold=0.65,
    interval=30,
    trail=80,
):
    # ----------------------------
    # Data
    # ----------------------------
    x = generate_signal(n=n)
    risk = compute_risk(x)

    states = build_state_space(x)
    v = states[:, 1]

    levels = compute_adaptive_levels(x, n_basins=n_basins)
    basins = assign_basins(x, levels)

    high_risk = risk > risk_threshold

    # ----------------------------
    # Figure
    # ----------------------------
    fig, axs = plt.subplots(3, 1, figsize=(12, 10))
    ax_time, ax_state, ax_basin = axs

    # ----------------------------
    # Time Domain
    # ----------------------------
    ax_time.plot(x, color="blue", alpha=0.35)

    for lvl in levels:
        ax_time.axhline(lvl, color="gray", alpha=0.08)

    time_trail, = ax_time.plot([], [], color="blue", linewidth=2)
    time_dot, = ax_time.plot([], [], "o", color="red", markersize=6)

    ax_time.set_xlim(0, n)
    ax_time.set_ylim(np.min(x) - 0.2, np.max(x) + 0.2)
    ax_time.set_title("Time Domain")

    # ----------------------------
    # State Space
    # ----------------------------
    ax_state.plot(x, v, color="gray", alpha=0.25)

    state_trail, = ax_state.plot([], [], color="purple", linewidth=2)
    state_dot, = ax_state.plot([], [], "o", color="red", markersize=6)

    ax_state.set_xlim(np.min(x) - 0.2, np.max(x) + 0.2)
    ax_state.set_ylim(np.min(v) - 0.05, np.max(v) + 0.05)
    ax_state.set_title("State Space (x, v)")

    # ----------------------------
    # Basin Space
    # ----------------------------
    ax_basin.plot(basins, color="green", alpha=0.35)

    basin_trail, = ax_basin.plot([], [], color="green", linewidth=2)
    basin_dot, = ax_basin.plot([], [], "o", color="red", markersize=6)

    ax_basin.set_xlim(0, n)
    ax_basin.set_ylim(np.min(basins) - 1, np.max(basins) + 1)
    ax_basin.set_title("Basin Space")

    # ----------------------------
    # Animation
    # ----------------------------
    def update(frame):
        start = max(0, frame - trail)

        t_range = np.arange(start, frame + 1)

        # time
        time_trail.set_data(t_range, x[start:frame + 1])
        time_dot.set_data([frame], [x[frame]])

        # state
        state_trail.set_data(x[start:frame + 1], v[start:frame + 1])
        state_dot.set_data([x[frame]], [v[frame]])

        # basin
        basin_trail.set_data(t_range, basins[start:frame + 1])
        basin_dot.set_data([frame], [basins[frame]])

        # risk highlight
        if high_risk[frame]:
            size = 9
            color = "red"
        else:
            size = 5
            color = "black"

        time_dot.set_markersize(size)
        state_dot.set_markersize(size)
        basin_dot.set_markersize(size)

        time_dot.set_color(color)
        state_dot.set_color(color)
        basin_dot.set_color(color)

        fig.suptitle(
            f"NEXAH v13 — t={frame} | basin={basins[frame]} | risk={risk[frame]:.3f}"
        )

        return (
            time_trail,
            time_dot,
            state_trail,
            state_dot,
            basin_trail,
            basin_dot,
        )

       anim = FuncAnimation(
        fig,
        update,
        frames=n,
        interval=interval,
        repeat=True,
    )

    plt.tight_layout()

    # ----------------------------
    # OPTIONAL EXPORT
    # ----------------------------
    save = True  # <- toggle

    if save:
        import os
        os.makedirs("outputs", exist_ok=True)

        print("Saving animation to outputs/nexah_flow.gif ...")

        anim.save(
            "outputs/nexah_flow.gif",
            writer="pillow",
            fps=30
        )

        print("Done.")

    plt.show()
