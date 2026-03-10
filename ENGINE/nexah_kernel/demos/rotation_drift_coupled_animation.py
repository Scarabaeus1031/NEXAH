"""
Symmetry Morphing Animation
===========================

Morphs between different rotational symmetries.

triangle → square → pentagon → ... → 20-fold
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# --------------------------------------------------
# Parameters
# --------------------------------------------------

radius = 5
iterations = 2500

n_min = 3
n_max = 20

fig, ax = plt.subplots(figsize=(7,7))

line, = ax.plot([],[],lw=1.2)

ax.set_xlim(-6,6)
ax.set_ylim(-6,6)
ax.set_aspect("equal")

ax.set_title("Symmetry Morphing Explorer")


# guide circle
t = np.linspace(0,2*np.pi,400)
ax.plot(radius*np.cos(t), radius*np.sin(t), alpha=0.12)


# --------------------------------------------------
# Pattern generator
# --------------------------------------------------

def generate_pattern(n):

    base_angle = 2*np.pi/n

    k = np.arange(iterations)

    theta = k*base_angle

    r = radius*(0.7 + 0.3*np.cos(k*0.02))

    x = r*np.cos(theta)
    y = r*np.sin(theta)

    return x,y


# --------------------------------------------------
# Animation
# --------------------------------------------------

def update(frame):

    n = n_min + frame % (n_max-n_min)

    x,y = generate_pattern(n)

    line.set_data(x,y)

    ax.set_title(f"Symmetry Morphing | n = {n}")

    return line,


ani = FuncAnimation(
    fig,
    update,
    frames=300,
    interval=50,
    blit=True
)

plt.show()    interval=40,
    blit=True
)

plt.show()
