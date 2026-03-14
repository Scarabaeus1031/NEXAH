"""
Lorenz Navigation Analysis

Generates three diagnostic plots:

1) 3D Lorenz navigation comparison
2) 2D phase projection (x-z)
3) Lobe-switch timeline

All images are saved automatically.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import datetime


# ---------------------------------------------------------
# output folder
# ---------------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"

os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


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
# stability potential
# ---------------------------------------------------------

def stability_potential(x, z):

    left = np.array([-8, 27])
    right = np.array([8, 27])

    p = np.array([x, z])

    d_left = np.linalg.norm(p - left)
    d_right = np.linalg.norm(p - right)

    return min(d_left, d_right)


# ---------------------------------------------------------
# gradient estimation
# ---------------------------------------------------------

def gradient_estimate(x, z, eps=0.01):

    v = stability_potential(x, z)

    dx = (stability_potential(x + eps, z) - v) / eps
    dz = (stability_potential(x, z + eps) - v) / eps

    return np.array([dx, dz])


# ---------------------------------------------------------
# simulation
# ---------------------------------------------------------

def simulate(control=False, stabilizer=False):

    dt = 0.01
    steps = 12000

    state = np.array([0.1, 0.0, 26.0])

    traj = []

    for _ in range(steps):

        dx = lorenz(state)

        if control:

            grad = gradient_estimate(state[0], state[2])

            control_force = np.array([-grad[0], 0, -grad[1]])

            dx += 0.5 * control_force

        if stabilizer:

            if abs(state[0]) < 3:

                lobe_push = np.sign(state[0]) * 5

                dx[0] += lobe_push

        state = state + dt * dx

        traj.append(state.copy())

    return np.array(traj)


# ---------------------------------------------------------
# run simulations
# ---------------------------------------------------------

traj_free = simulate(False)
traj_grad = simulate(True)
traj_stab = simulate(True, True)


# ---------------------------------------------------------
# 1) 3D navigation plot
# ---------------------------------------------------------

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection="3d")

ax.plot(traj_free[:,0],traj_free[:,1],traj_free[:,2],alpha=0.3,label="Uncontrolled")
ax.plot(traj_grad[:,0],traj_grad[:,1],traj_grad[:,2],alpha=0.7,label="Gradient")
ax.plot(traj_stab[:,0],traj_stab[:,1],traj_stab[:,2],linewidth=2,label="Gradient+Stabilizer")

ax.set_title("Lorenz Navigation (NEXAH)")
ax.legend()

file_3d = f"{OUTPUT_DIR}/lorenz_navigation_3D_{timestamp}.png"
plt.savefig(file_3d,dpi=300,bbox_inches="tight")
print("saved:",file_3d)

plt.close()


# ---------------------------------------------------------
# 2) 2D phase projection (x-z)
# ---------------------------------------------------------

plt.figure(figsize=(7,6))

plt.plot(traj_free[:,0],traj_free[:,2],alpha=0.3,label="Uncontrolled")
plt.plot(traj_grad[:,0],traj_grad[:,2],alpha=0.7,label="Gradient")
plt.plot(traj_stab[:,0],traj_stab[:,2],linewidth=2,label="Gradient+Stabilizer")

plt.xlabel("X")
plt.ylabel("Z")
plt.title("Lorenz Phase Projection (X-Z)")
plt.legend()

file_phase = f"{OUTPUT_DIR}/lorenz_phase_projection_{timestamp}.png"
plt.savefig(file_phase,dpi=300,bbox_inches="tight")
print("saved:",file_phase)

plt.close()


# ---------------------------------------------------------
# 3) lobe switch timeline
# ---------------------------------------------------------

def lobe_sequence(traj):

    return np.sign(traj[:,0])


lobe_free = lobe_sequence(traj_free)
lobe_grad = lobe_sequence(traj_grad)
lobe_stab = lobe_sequence(traj_stab)


plt.figure(figsize=(10,4))

plt.plot(lobe_free,label="Uncontrolled",alpha=0.4)
plt.plot(lobe_grad,label="Gradient",alpha=0.8)
plt.plot(lobe_stab,label="Gradient+Stabilizer",linewidth=2)

plt.title("Lorenz Lobe Switch Timeline")
plt.xlabel("Time Step")
plt.ylabel("Lobe (-1 left / +1 right)")
plt.legend()

file_timeline = f"{OUTPUT_DIR}/lorenz_lobe_timeline_{timestamp}.png"
plt.savefig(file_timeline,dpi=300,bbox_inches="tight")
print("saved:",file_timeline)

plt.close()


print("\nNavigation analysis complete.")
