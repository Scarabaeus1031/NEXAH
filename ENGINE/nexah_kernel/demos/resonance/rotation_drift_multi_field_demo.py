"""
Rotation Drift Multi-Field Demo
===============================

Explores interference between multiple rotational drift systems.

Example:

135°
137°
139°

Each creates its own rosette field.
Overlay reveals interference structure.
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Parameters
# --------------------------------------------------

n_symmetry = 5
radius = 5

drifts_deg = [0.0, 2.0, 4.0]

colors = ["red", "green", "blue"]

iterations = 3500


# --------------------------------------------------
# Base angle
# --------------------------------------------------

base_angle = 2*np.pi/n_symmetry


fig, ax = plt.subplots(figsize=(7,7))


for drift_deg, col in zip(drifts_deg, colors):

    drift = np.deg2rad(drift_deg)

    k = np.arange(iterations)

    theta = k * (base_angle + drift)

    r = radius * (0.7 + 0.3*np.cos(k*0.01))

    x = r*np.cos(theta)
    y = r*np.sin(theta)

    ax.plot(x,y, lw=1.0, alpha=0.8, color=col,
            label=f"drift {drift_deg}°")


# guide circle
t = np.linspace(0,2*np.pi,500)
ax.plot(radius*np.cos(t), radius*np.sin(t), alpha=0.1)


ax.set_aspect("equal")
ax.set_xlim(-6.5,6.5)
ax.set_ylim(-6.5,6.5)

ax.legend()

ax.set_title(
    f"Rotation Drift Interference (n={n_symmetry})"
)

plt.show()
