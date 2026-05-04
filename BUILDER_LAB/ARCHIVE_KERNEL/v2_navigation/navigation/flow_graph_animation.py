# ============================================================
# 🧭 NEXAH v15 — Flow + Transition Graph Animation
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
    compute_basin_centers,
)

from nexah.navigation.transition_graph import build_transition_graph


def run_flow_graph_animation(
    n=500,
    n_basins=10,
    risk_threshold=0.65,
    interval=30,
    trail=80,
):
    x = generate_signal(n=n)
    risk = compute_risk(x)

    states = build_state_space(x)
    v = states[:, 1]

    levels = compute_adaptive_levels(x, n_basins=n_basins)
    basins = assign_basins(x, levels)

    centers = compute_basin_centers(states, basins)
    graph = build_transition_graph(basins)

    high_risk = risk > risk_threshold

    fig, axs = plt.subplots(2, 1, figsize=(11, 10))
    ax_state, ax_basin = axs

    # --------------------------------------------------------
    # STATE SPACE BACKGROUND
    # --------------------------------------------------------
    ax_state.plot(x, v, color="gray", alpha=0.2, linewidth=1)

    # Basin centers
    for b, c in centers.items():
        ax_state.scatter(c[0], c[1], s=80, color="black", alpha=0.7)
        ax_state.text(c[0], c[1], f" {b}", fontsize=9)

    # Transition graph edges in state space
    for source, targets in graph.items():
        if source not in centers:
            continue

        x0, y0 = centers[source]

        for target, data in targets.items():
            if target not in centers:
                continue
            if target == source:
                continue

            x1, y1 = centers[target]

            prob = data["probability"]
            width = 0.5 + 4.0 * prob

            ax_state.annotate(
                "",
                xy=(x1, y1),
                xytext=(x0, y0),
                arrowprops=dict(
                    arrowstyle="->",
                    lw=width,
                    alpha=0.35,
                    color="orange",
                ),
            )

    state_trail, = ax_state.plot([], [], color="purple", linewidth=2)
    state_dot, = ax_state.plot([], [], "o", color="black")

    ax_state.set_xlim(np.min(x) - 0.25, np.max(x) + 0.25)
    ax_state.set_ylim(np.min(v) - 0.06, np.max(v) + 0.06)
    ax_state.set_title("State Space + Transition Graph")
    ax_state.set_xlabel("x")
    ax_state.set_ylabel("v")

    # --------------------------------------------------------
    # BASIN SPACE
    # --------------------------------------------------------
    ax_basin.plot(basins, color="green", alpha=0.3)

    basin_trail, = ax_basin.plot([], [], color="green", linewidth=2)
    basin_dot, = ax_basin.plot([], [], "o", color="black")

    ax_basin.set_xlim(0, n)
    ax_basin.set_ylim(np.min(basins) - 1, np.max(basins) + 1)
    ax_basin.set_title("Basin Space + Regime Motion")
    ax_basin.set_xlabel("time")

    def update(frame):
        start = max(0, frame - trail)
        t_range = np.arange(start, frame + 1)

        state_trail.set_data(x[start:frame + 1], v[start:frame + 1])
        state_dot.set_data([x[frame]], [v[frame]])

        basin_trail.set_data(t_range, basins[start:frame + 1])
        basin_dot.set_data([frame], [basins[frame]])

        if high_risk[frame]:
            size, color = 9, "red"
        else:
            size, color = 5, "black"

        state_dot.set_markersize(size)
        basin_dot.set_markersize(size)
        state_dot.set_color(color)
        basin_dot.set_color(color)

        current_basin = int(basins[frame])

        fig.suptitle(
            f"NEXAH v15 — t={frame} | basin={current_basin} | risk={risk[frame]:.3f}",
            fontsize=12,
        )

        return state_trail, state_dot, basin_trail, basin_dot

    anim = FuncAnimation(
        fig,
        update,
        frames=n,
        interval=interval,
        repeat=True,
    )

    plt.tight_layout()

    save = True

    if save:
        import os
        os.makedirs("outputs", exist_ok=True)

        print("Saving outputs/nexah_flow_graph.gif ...")
        anim.save("outputs/nexah_flow_graph.gif", writer="pillow", fps=30)
        print("Done.")

    plt.show()

    return anim


if __name__ == "__main__":
    run_flow_graph_animation()
