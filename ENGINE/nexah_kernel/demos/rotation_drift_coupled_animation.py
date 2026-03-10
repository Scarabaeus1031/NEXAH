"""
Rotation Drift Coupled Animation
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --------------------------------------------------
# parameters
# --------------------------------------------------

n = 5
radius = 5
iterations = 3000
drift_max = 6.0

fig, ax = plt.subplots(figsize=(7,7))

line, = ax.plot([], [], lw=1)

ax.set_xlim(-6,6)
ax.set_ylim(-6,6)
ax.set_aspect("equal")

# guide circle
t = np.linspace(0, 2*np.pi, 400)
ax.plot(radius*np.cos(t), radius*np.sin(t), alpha=0.1)

# --------------------------------------------------
# pattern generator
# --------------------------------------------------

def generate_pattern(drift_deg):

    base_angle = 2*np.pi/n
    drift = np.deg2rad(drift_deg)

    k = np.arange(iterations)

    theta = k * (base_angle + drift)

    r = radius * (0.7 + 0.3*np.cos(k*0.02))

    x = r*np.cos(theta)
    y = r*np.sin(theta)

    return x, y


# --------------------------------------------------
# animation
# --------------------------------------------------

def update(frame):

    drift = frame * drift_max / 180

    x, y = generate_pattern(drift)

    line.set_data(x, y)

    ax.set_title(f"Rotation Drift Coupled | drift={drift:.2f}°")

    return line,


ani = FuncAnimation(
    fig,
    update,
    frames=180,
    interval=40,
    blit=True
)

plt.show()
