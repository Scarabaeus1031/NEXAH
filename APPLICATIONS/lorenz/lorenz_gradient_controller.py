"""
Lorenz Gradient Controller

Demonstrates how the NEXAH framework can steer a chaotic Lorenz
trajectory using a stability gradient and a separatrix avoidance rule.

Comparison:
- uncontrolled Lorenz trajectory
- gradient-steered Lorenz trajectory
- lobe-stabilized trajectory
"""

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Lorenz parameters
# ---------------------------------------------------------

sigma = 10
rho = 28
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
# Approximate stability potential
# ---------------------------------------------------------

def stability_potential(x, z):

    left = np.array([-8, 27])
    right = np.array([8, 27])

    p = np.array([x, z])

    d_left = np.linalg.norm(p - left)
    d_right = np.linalg.norm(p - right)

    return min(d_left, d_right)


# ---------------------------------------------------------
# Numerical gradient of potential
# ---------------------------------------------------------

def gradient_estimate(x, z, eps=0.01):

    v = stability_potential(x, z)

    dx = (stability_potential(x + eps, z) - v) / eps
    dz = (stability_potential(x, z + eps) - v) / eps

    return np.array([dx, dz])


# ---------------------------------------------------------
# Simulation
# ---------------------------------------------------------

def simulate(control=False, lobe_stabilizer=False):

    dt = 0.01
    steps = 12000

    state = np.array([0.1, 0.0, 26.0])

    trajectory = []

    for _ in range(steps):

        dx = lorenz(state)

        # -------------------------------
        # Gradient steering
        # -------------------------------

        if control:

            grad = gradient_estimate(state[0], state[2])

            control_force = np.array([-grad[0], 0, -grad[1]])

            dx += 0.5 * control_force

        # -------------------------------
        # Lobe stabilization
        # -------------------------------

        if lobe_stabilizer:

            if abs(state[0]) < 3:

                lobe_push = np.sign(state[0]) * 5

                dx[0] += lobe_push

        state = state + dt * dx

        trajectory.append(state.copy())

    return np.array(trajectory)


# ---------------------------------------------------------
# Run simulations
# ---------------------------------------------------------

traj_free = simulate(control=False)

traj_gradient = simulate(control=True)

traj_stabilized = simulate(control=True, lobe_stabilizer=True)


# ---------------------------------------------------------
# Plot comparison
# ---------------------------------------------------------

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")

ax.plot(
    traj_free[:, 0],
    traj_free[:, 1],
    traj_free[:, 2],
    alpha=0.35,
    label="Uncontrolled",
)

ax.plot(
    traj_gradient[:, 0],
    traj_gradient[:, 1],
    traj_gradient[:, 2],
    alpha=0.7,
    label="Gradient Controlled",
)

ax.plot(
    traj_stabilized[:, 0],
    traj_stabilized[:, 1],
    traj_stabilized[:, 2],
    linewidth=2,
    label="Gradient + Lobe Stabilizer",
)

ax.set_title("Lorenz Gradient Navigation (NEXAH Controller)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.legend()

# ---------------------------------------------------------
# Save figure
# ---------------------------------------------------------

output_path = "APPLICATIONS/outputs/lorenz_navigation/lorenz_gradient_navigation.png"

plt.savefig(output_path, dpi=300, bbox_inches="tight")

print("saved:", output_path)

plt.show()
