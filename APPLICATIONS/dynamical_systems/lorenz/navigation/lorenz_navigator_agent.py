"""
Lorenz Navigator Agent

This script builds a simple navigation agent on top of the
Lorenz chaos topography.

Idea:
- compute / estimate a chaos field over the (x, z) plane
- let an agent move along the negative gradient of chaos
- visualize the path of the agent through the chaos landscape

This is the first true Lorenz Navigator prototype.
"""

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Output folder
# ---------------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


# ---------------------------------------------------------
# Lorenz parameters
# ---------------------------------------------------------

sigma = 10.0
rho = 28.0
beta = 8 / 3


# ---------------------------------------------------------
# Lorenz system
# ---------------------------------------------------------

def lorenz(state):
    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return np.array([dx, dy, dz])


# ---------------------------------------------------------
# Chaos measure via lobe switch count
# ---------------------------------------------------------

def chaos_measure(x0, z0, dt=0.01, steps=3000):
    state = np.array([x0, 0.0, z0], dtype=float)

    last_lobe = np.sign(state[0])
    if last_lobe == 0:
        last_lobe = 1

    switches = 0

    for _ in range(steps):
        state = state + dt * lorenz(state)

        new_lobe = np.sign(state[0])
        if new_lobe == 0:
            new_lobe = last_lobe

        if new_lobe != last_lobe:
            switches += 1
            last_lobe = new_lobe

    return switches


# ---------------------------------------------------------
# Build chaos topography
# ---------------------------------------------------------

def build_chaos_map(resolution=100):
    x_vals = np.linspace(-20, 20, resolution)
    z_vals = np.linspace(0, 50, resolution)

    chaos_map = np.zeros((resolution, resolution), dtype=float)

    for i, x in enumerate(x_vals):
        print(f"row {i + 1} / {resolution}")

        for j, z in enumerate(z_vals):
            chaos_map[j, i] = chaos_measure(x, z)

    return x_vals, z_vals, chaos_map


# ---------------------------------------------------------
# Bilinear sampling helper
# ---------------------------------------------------------

def sample_field(x, z, x_vals, z_vals, field):
    if x <= x_vals[0]:
        x = x_vals[0]
    if x >= x_vals[-1]:
        x = x_vals[-1]
    if z <= z_vals[0]:
        z = z_vals[0]
    if z >= z_vals[-1]:
        z = z_vals[-1]

    ix = np.searchsorted(x_vals, x) - 1
    iz = np.searchsorted(z_vals, z) - 1

    ix = np.clip(ix, 0, len(x_vals) - 2)
    iz = np.clip(iz, 0, len(z_vals) - 2)

    x1, x2 = x_vals[ix], x_vals[ix + 1]
    z1, z2 = z_vals[iz], z_vals[iz + 1]

    q11 = field[iz, ix]
    q21 = field[iz, ix + 1]
    q12 = field[iz + 1, ix]
    q22 = field[iz + 1, ix + 1]

    tx = 0.0 if x2 == x1 else (x - x1) / (x2 - x1)
    tz = 0.0 if z2 == z1 else (z - z1) / (z2 - z1)

    a = q11 * (1 - tx) + q21 * tx
    b = q12 * (1 - tx) + q22 * tx

    return a * (1 - tz) + b * tz


# ---------------------------------------------------------
# Gradient estimation on chaos field
# ---------------------------------------------------------

def chaos_gradient(x, z, x_vals, z_vals, chaos_map, eps=0.2):
    c0 = sample_field(x, z, x_vals, z_vals, chaos_map)
    cx = sample_field(x + eps, z, x_vals, z_vals, chaos_map)
    cz = sample_field(x, z + eps, x_vals, z_vals, chaos_map)

    dc_dx = (cx - c0) / eps
    dc_dz = (cz - c0) / eps

    return np.array([dc_dx, dc_dz])


# ---------------------------------------------------------
# Navigator agent
# ---------------------------------------------------------

def run_agent(x_vals, z_vals, chaos_map, start_x=0.0, start_z=27.0, steps=120, lr=0.35):
    x = float(start_x)
    z = float(start_z)

    path = [(x, z)]

    for _ in range(steps):
        grad = chaos_gradient(x, z, x_vals, z_vals, chaos_map)

        # move toward lower chaos
        x = x - lr * grad[0]
        z = z - lr * grad[1]

        # keep agent in field
        x = np.clip(x, x_vals[0], x_vals[-1])
        z = np.clip(z, z_vals[0], z_vals[-1])

        path.append((x, z))

    return np.array(path)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    print("\nBuilding Lorenz chaos map for navigator...\n")

    x_vals, z_vals, chaos_map = build_chaos_map(resolution=100)

    print("\nRunning navigator agent...\n")

    agent_path = run_agent(
        x_vals,
        z_vals,
        chaos_map,
        start_x=0.0,
        start_z=27.0,
        steps=120,
        lr=0.35
    )

    # -----------------------------------------------------
    # Plot: chaos topography + navigator path
    # -----------------------------------------------------

    plt.figure(figsize=(10, 8))

    plt.imshow(
        chaos_map,
        extent=[x_vals.min(), x_vals.max(), z_vals.min(), z_vals.max()],
        origin="lower",
        cmap="plasma",
        aspect="auto"
    )

    plt.colorbar(label="Lobe Switch Count")

    plt.plot(
        agent_path[:, 0],
        agent_path[:, 1],
        color="cyan",
        linewidth=2.5,
        marker="o",
        markersize=3,
        label="Navigator Path"
    )

    plt.scatter(
        agent_path[0, 0],
        agent_path[0, 1],
        s=80,
        color="white",
        edgecolor="black",
        label="Start"
    )

    plt.scatter(
        agent_path[-1, 0],
        agent_path[-1, 1],
        s=80,
        color="lime",
        edgecolor="black",
        label="End"
    )

    plt.xlabel("X")
    plt.ylabel("Z")
    plt.title("Lorenz Navigator Agent on Chaos Topography")
    plt.legend()

    file_output = f"{OUTPUT_DIR}/lorenz_navigator_agent_{timestamp}.png"
    plt.savefig(file_output, dpi=300, bbox_inches="tight")
    print("saved:", file_output)

    plt.show()
    plt.close()

    # -----------------------------------------------------
    # Print path summary
    # -----------------------------------------------------

    start_chaos = sample_field(agent_path[0, 0], agent_path[0, 1], x_vals, z_vals, chaos_map)
    end_chaos = sample_field(agent_path[-1, 0], agent_path[-1, 1], x_vals, z_vals, chaos_map)

    print("\nNavigator summary:")
    print(f"start position: ({agent_path[0,0]:.3f}, {agent_path[0,1]:.3f})")
    print(f"end position:   ({agent_path[-1,0]:.3f}, {agent_path[-1,1]:.3f})")
    print(f"start chaos:    {start_chaos:.3f}")
    print(f"end chaos:      {end_chaos:.3f}")
    print(f"chaos reduction:{start_chaos - end_chaos:.3f}\n")


if __name__ == "__main__":
    main()
