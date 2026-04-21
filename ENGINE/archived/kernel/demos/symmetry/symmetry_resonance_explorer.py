"""
Symmetry Resonance Explorer
===========================

Interactive exploration of rotational symmetry systems.

Parameters you can adjust:

    n_symmetry
    angular drift
    radial modulation

This reveals emergent resonance patterns such as:

- rosettes
- spiral flowers
- quasi-periodic rings
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# --------------------------------------------------
# Initial parameters
# --------------------------------------------------

n_symmetry = 5
drift_deg = 2.0
radius = 5
iterations = 4000


# --------------------------------------------------
# Generate pattern
# --------------------------------------------------

def generate_pattern(n, drift_deg):

    base_angle = 2*np.pi/n
    drift = np.deg2rad(drift_deg)

    k = np.arange(iterations)

    theta = k*(base_angle + drift)

    r = radius*(0.7 + 0.3*np.cos(k*0.01))

    x = r*np.cos(theta)
    y = r*np.sin(theta)

    return x,y


# --------------------------------------------------
# Plot
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(7,7))
plt.subplots_adjust(bottom=0.25)

x,y = generate_pattern(n_symmetry, drift_deg)

line, = ax.plot(x,y, lw=1.2)

ax.set_aspect("equal")
ax.set_xlim(-6.5,6.5)
ax.set_ylim(-6.5,6.5)

ax.set_title("Symmetry Resonance Explorer")


# guide circle
t = np.linspace(0,2*np.pi,400)
ax.plot(radius*np.cos(t), radius*np.sin(t), alpha=0.15)


# --------------------------------------------------
# Sliders
# --------------------------------------------------

ax_n = plt.axes([0.25,0.12,0.55,0.03])
ax_drift = plt.axes([0.25,0.07,0.55,0.03])

slider_n = Slider(ax_n,"n symmetry",3,20,valinit=n_symmetry,valstep=1)
slider_drift = Slider(ax_drift,"drift°",0,10,valinit=drift_deg)


# --------------------------------------------------
# Update
# --------------------------------------------------

def update(val):

    n = int(slider_n.val)
    drift = slider_drift.val

    x,y = generate_pattern(n,drift)

    line.set_data(x,y)

    fig.canvas.draw_idle()


slider_n.on_changed(update)
slider_drift.on_changed(update)


plt.show()
