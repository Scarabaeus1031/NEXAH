"""
Lorenz Gradient Controller

Demonstrates how the NEXAH framework can gently steer a chaotic
Lorenz trajectory using the stability gradient derived from the
potential landscape.

Comparison:
- uncontrolled Lorenz trajectory
- gradient-steered Lorenz trajectory
"""

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------
# Lorenz system parameters
# ---------------------------------------------

sigma = 10
rho = 28
beta = 8 / 3


def lorenz(state):

    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return np.array([dx, dy, dz])


# ---------------------------------------------
# Simple "potential landscape"
# (approximation based on attractor lobes)
# ---------------------------------------------

def stability_potential(x, z):

    # approximate attractor centers
    left = np.array([-8, 27])
    right = np.array([8, 27])

    p = np.array([x, z])

    d_left = np.linalg.norm(p - left)
    d_right = np.linalg.norm(p - right)

    return min(d_left, d_right)


def gradient_estimate(x, z, eps=0.01):

    v = stability_potential(x, z)

    dx = (stability_potential(x + eps, z) - v) / eps
    dz = (stability_potential(x, z + eps) - v) / eps

    return np.array([dx, dz])


# ---------------------------------------------
# Simulation
# ---------------------------------------------

def simulate(control=False):

    dt = 0.01
    steps = 10000

    state = np.array([0.1, 0.0, 26.0])

    trajectory = []

    for _ in range(steps):

        dx = lorenz(state)

        if control:

            grad = gradient_estimate(state[0], state[2])

            # steer opposite gradient
            control_force = np.array([-grad[0], 0, -grad[1]])

            dx += 0.5 * control_force

        state = state + dt * dx

        trajectory.append(state.copy())

    return np.array(trajectory)


# ---------------------------------------------
# Run simulation
# ---------------------------------------------

traj_free = simulate(control=False)
traj_control = simulate(control=True)


# ---------------------------------------------
# Plot comparison
# ---------------------------------------------

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")

ax.plot(
    traj_free[:, 0],
    traj_free[:, 1],
    traj_free[:, 2],
    alpha=0.4,
    label="Uncontrolled",
)

ax.plot(
    traj_control[:, 0],
    traj_control[:, 1],
    traj_control[:, 2],
    alpha=0.9,
    label="Gradient Controlled",
)

ax.set_title("Lorenz Gradient Navigation")
ax.legend()

plt.show()
