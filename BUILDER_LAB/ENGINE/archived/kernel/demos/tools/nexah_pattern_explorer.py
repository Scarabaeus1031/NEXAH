"""
NEXAH Pattern Explorer
======================

Interactive exploration of symmetry + drift patterns.

Controls:
    symmetry n
    drift
    iterations
    radius
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# --------------------------------------------------
# pattern generator
# --------------------------------------------------

def generate_pattern(n, drift_deg, iterations, radius):

    base_angle = 2*np.pi/n
    drift = np.deg2rad(drift_deg)

    k = np.arange(iterations)

    theta = k*(base_angle + drift)

    r = radius * (0.7 + 0.3*np.cos(k*0.02))

    x = r*np.cos(theta)
    y = r*np.sin(theta)

    return x, y


# --------------------------------------------------
# initial parameters
# --------------------------------------------------

n0 = 7
drift0 = 0.0
iter0 = 2000
radius0 = 5


# --------------------------------------------------
# figure
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(6,6))
plt.subplots_adjust(bottom=0.35)

x,y = generate_pattern(n0, drift0, iter0, radius0)

line, = ax.plot(x,y,lw=0.8)

ax.set_aspect("equal")
ax.set_xlim(-6,6)
ax.set_ylim(-6,6)
ax.set_title("NEXAH Pattern Explorer")

ax.axis("off")


# --------------------------------------------------
# sliders
# --------------------------------------------------

ax_n = plt.axes([0.2,0.25,0.6,0.03])
ax_d = plt.axes([0.2,0.20,0.6,0.03])
ax_i = plt.axes([0.2,0.15,0.6,0.03])
ax_r = plt.axes([0.2,0.10,0.6,0.03])

s_n = Slider(ax_n,"symmetry n",3,20,valinit=n0,valstep=1)
s_d = Slider(ax_d,"drift deg",0,10,valinit=drift0)
s_i = Slider(ax_i,"iterations",200,4000,valinit=iter0,valstep=100)
s_r = Slider(ax_r,"radius",2,8,valinit=radius0)


# --------------------------------------------------
# update function
# --------------------------------------------------

def update(val):

    n = int(s_n.val)
    drift = s_d.val
    iterations = int(s_i.val)
    radius = s_r.val

    x,y = generate_pattern(n,drift,iterations,radius)

    line.set_data(x,y)

    fig.canvas.draw_idle()


s_n.on_changed(update)
s_d.on_changed(update)
s_i.on_changed(update)
s_r.on_changed(update)


plt.show()
