# ============================================================
# 🧭 NEXAH v14 — Flow Field Animation
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


# ------------------------------------------------------------
# FLOW FIELD (dx/dt)
# ------------------------------------------------------------

def compute_flow_vectors(states, bins=25):
    x = states[:, 0]
    v = states[:, 1]

    H, xedges, yedges = np.histogram2d(x, v, bins=bins)
    H = H.T + 1e-6

    gy, gx = np.gradient(H)

    xc = 0.5 * (xedges[:-1] + xedges[1:])
    yc = 0.5 * (yedges[:-1] + yedges[1:])

    Xc, Yc = np.meshgrid(xc, yc)

    return Xc, Yc, gx, gy


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def run_flow_field_animation(
    n=500,
    n_basins=10,
    risk_threshold=0.65,
    interval=30,
    trail=80,
):
    # ----------------------------
    # DATA
    # ----------------------------
    x = generate_signal(n=n)
    risk = compute_risk(x)

    states = build_state_space(x)
    v = states[:, 1]

    levels = compute_adaptive_levels(x, n_basins=n_basins)
    basins = assign_basins(x, levels)

    high_risk = risk > risk_threshold

    # ----------------------------
    # FLOW FIELD
    # ----------------------------
    Xc, Yc, gx, gy = compute_flow_vectors(states)

    # normalize for nicer arrows
    mag = np.sqrt(gx**2 + gy**2) + 1e-8
    gx /= mag
    gy /= mag

    # ----------------------------
    # FIGURE
    # ----------------------------
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))
    ax_state, ax_basin = axs

    # ----------------------------
    # STATE SPACE
    # ----------------------------
    ax_state.plot(x, v, color="gray", alpha=0.2)

    # 🔥 FLOW FIELD
    ax_state.quiver(
        Xc,
        Yc,
        gx,
        gy,
        color="black",
        alpha=0.4,
        scale=30
    )

    state_trail, = ax_state.plot([], [], color="purple", linewidth=2)
    state_dot, = ax_state.plot([], [], "o", color="black")

    ax_state.set_xlim(np.min(x) - 0.2, np.max(x) + 0.2)
    ax_state.set_ylim(np.min(v) - 0.05, np.max(v) + 0.05)
    ax_state.set_title("State Space + Flow Field")

    # ----------------------------
    # BASIN SPACE
    # ----------------------------
    ax_basin.plot(basins, color="green", alpha=0.3)

    basin_trail, = ax_basin.plot([], [], color="green", linewidth=2)
    basin_dot, = ax_basin.plot([], [], "o", color="black")

    ax_basin.set_xlim(0, n)
    ax_basin.set_ylim(np.min(basins) - 1, np.max(basins) + 1)
    ax_basin.set_title("Basin Space")

    # ----------------------------
    # ANIMATION
    # ----------------------------
    def update(frame):
        start = max(0, frame - trail)
        t_range = np.arange(start, frame + 1)

        # state
        state_trail.set_data(x[start:frame+1], v[start:frame+1])
        state_dot.set_data([x[frame]], [v[frame]])

        # basin
        basin_trail.set_data(t_range, basins[start:frame+1])
        basin_dot.set_data([frame], [basins[frame]])

        # risk highlight
        if high_risk[frame]:
            size, color = 9, "red"
        else:
            size, color = 5, "black"

        for dot in [state_dot, basin_dot]:
            dot.set_markersize(size)
            dot.set_color(color)

        fig.suptitle(
            f"NEXAH v14 — t={frame} | basin={basins[frame]} | risk={risk[frame]:.3f}"
        )

        return (
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
    # EXPORT
    # ----------------------------
    save = True

    if save:
        import os
        os.makedirs("outputs", exist_ok=True)

        print("Saving outputs/nexah_flow_field.gif ...")

        anim.save(
            "outputs/nexah_flow_field.gif",
            writer="pillow",
            fps=30
        )

        print("Done.")

    plt.show()


if __name__ == "__main__":
    run_flow_field_animation()
