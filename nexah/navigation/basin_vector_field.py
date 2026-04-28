# ============================================================
# 🧭 NEXAH v21 — Basin Vector Field + Flow Animation
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from nexah.navigation.state_space_control import (
    generate_signal,
    compute_risk,
    compute_adaptive_levels,
    assign_basins,
)

# ------------------------------------------------------------
# BUILD DATA
# ------------------------------------------------------------

def build_field_data(n=500, n_basins=10):
    x = generate_signal(n=n)
    risk = compute_risk(x)

    dx = np.gradient(x)

    levels = compute_adaptive_levels(x, n_basins=n_basins)
    basins = assign_basins(x, levels)

    records = []

    for t in range(len(basins) - 1):
        basin = int(basins[t])
        next_basin = int(basins[t + 1])

        direction = int(np.sign(dx[t]))
        delta = next_basin - basin

        records.append((basin, direction, delta))

    return records, basins


# ------------------------------------------------------------
# BUILD VECTOR FIELD
# ------------------------------------------------------------

def build_vector_field(records):
    field = {}

    for basin, direction, delta in records:
        key = (basin, direction)

        if key not in field:
            field[key] = []

        field[key].append(delta)

    # compute mean delta
    field_mean = {}

    for key, values in field.items():
        field_mean[key] = np.mean(values)

    return field_mean


# ------------------------------------------------------------
# VISUALIZE STATIC FIELD
# ------------------------------------------------------------

def plot_vector_field(field):
    plt.figure(figsize=(10, 4))

    basins = sorted(set([k[0] for k in field.keys()]))

    for basin in basins:
        for direction in [-1, 1]:
            if (basin, direction) in field:
                delta = field[(basin, direction)]

                # arrow
                plt.arrow(
                    basin,
                    0,
                    0.4 * direction,
                    delta,
                    head_width=0.15,
                    length_includes_head=True,
                    alpha=0.7,
                )

    plt.axhline(0, color="gray", linestyle="--", alpha=0.5)
    plt.title("NEXAH v21 — Basin Vector Field")
    plt.xlabel("Basin")
    plt.ylabel("Expected Delta")
    plt.grid(alpha=0.2)

    plt.show()


# ------------------------------------------------------------
# FLOW SIMULATION
# ------------------------------------------------------------

def simulate_flow(field, start_basin=5, steps=100):
    basin = start_basin
    direction = 1

    trajectory = [basin]

    for _ in range(steps):
        key = (basin, direction)

        if key in field:
            delta = field[key]
        else:
            delta = 0

        # stochastic variation
        noise = np.random.normal(scale=0.3)
        step = delta + noise

        # update basin
        basin = int(np.clip(round(basin + step), 0, 9))

        # update direction
        direction = int(np.sign(step))
        if direction == 0:
            direction = np.random.choice([-1, 1])

        trajectory.append(basin)

    return trajectory


# ------------------------------------------------------------
# ANIMATION
# ------------------------------------------------------------

def animate_flow(field):
    traj = simulate_flow(field, start_basin=5, steps=200)

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.set_xlim(0, len(traj))
    ax.set_ylim(0, 10)
    ax.set_title("NEXAH v21 — Flow in Basin Field")

    line, = ax.plot([], [], color="blue", linewidth=2)
    dot, = ax.plot([], [], "o", color="red")

    def update(frame):

    x = np.arange(frame + 1)

    y = traj[:frame + 1]

    line.set_data(x, y)

    dot.set_data([frame], [traj[frame]])

    return line, dot

    anim = FuncAnimation(
        fig,
        update,
        frames=len(traj) - 1,
        interval=40,
        repeat=True,
    )

    # SAVE GIF
    save = True

    if save:
        import os
        os.makedirs("outputs", exist_ok=True)

        print("Saving outputs/nexah_v21_flow.gif ...")

        anim.save(
            "outputs/nexah_v21_flow.gif",
            writer="pillow",
            fps=25,
        )

        print("Done.")

    plt.show()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():
    records, basins = build_field_data()

    field = build_vector_field(records)

    print("\n--- Vector Field (sample) ---")
    for k in list(field.keys())[:10]:
        print(k, "→", field[k])

    plot_vector_field(field)
    animate_flow(field)


if __name__ == "__main__":
    main()
