"""
NEXAH Heptagon–Octagon Interference Demo
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# --------------------------------------------------
# Parameters
# --------------------------------------------------

hept_radius = 4.5
oct_radius = 3.0

rotation_strength = 0.8

hept_weight = 1.0
oct_weight = 0.9
center_weight = 1.4

epsilon = 0.4

particles = 900
dt = 0.05

xmin, xmax = -7, 7
ymin, ymax = -7, 7


# --------------------------------------------------
# Build heptagon
# --------------------------------------------------

heptagon = {}

for i in range(7):

    angle = 2*np.pi*i/7 + np.pi/2

    x = hept_radius*np.cos(angle)
    y = hept_radius*np.sin(angle)

    heptagon[f"S{i+1}"] = (x,y)


# --------------------------------------------------
# Build octagon
# --------------------------------------------------

octagon = {}

for i in range(8):

    angle = 2*np.pi*i/8

    x = oct_radius*np.cos(angle)
    y = oct_radius*np.sin(angle)

    octagon[f"O{i+1}"] = (x,y)


center = (0,0)


# --------------------------------------------------
# Initial particles
# --------------------------------------------------

x = np.random.uniform(xmin,xmax,particles)
y = np.random.uniform(ymin,ymax,particles)


# --------------------------------------------------
# Flow
# --------------------------------------------------

def flow(x,y):

    U = np.zeros_like(x)
    V = np.zeros_like(y)

    for ax,ay in heptagon.values():

        dx = x-ax
        dy = y-ay
        d = np.sqrt(dx*dx+dy*dy)+epsilon

        U += hept_weight*(-dx/d**2)
        V += hept_weight*(-dy/d**2)

        U += hept_weight*(-rotation_strength*dy/d**2)
        V += hept_weight*( rotation_strength*dx/d**2)


    for ax,ay in octagon.values():

        dx = x-ax
        dy = y-ay
        d = np.sqrt(dx*dx+dy*dy)+epsilon

        U += oct_weight*(-dx/d**2)
        V += oct_weight*(-dy/d**2)

        U += oct_weight*( rotation_strength*dy/d**2)
        V += oct_weight*(-rotation_strength*dx/d**2)


    dx = x
    dy = y
    d = np.sqrt(dx*dx+dy*dy)+epsilon

    U += center_weight*(-dx/d**2)
    V += center_weight*(-dy/d**2)

    return U,V


# --------------------------------------------------
# Plot
# --------------------------------------------------

fig,ax = plt.subplots(figsize=(7,7))

sc = ax.scatter(x,y,s=6)


for name,(px,py) in heptagon.items():
    ax.scatter(px,py,marker="*",s=240)
    ax.text(px+0.15,py+0.15,name)

for name,(px,py) in octagon.items():
    ax.scatter(px,py,s=80)
    ax.text(px+0.15,py+0.15,name)

ax.scatter(0,0,marker="*",s=320)

ax.set_xlim(xmin,xmax)
ax.set_ylim(ymin,ymax)
ax.set_aspect("equal")

ax.set_title("NEXAH Heptagon–Octagon Interference")


# --------------------------------------------------
# Animation
# --------------------------------------------------

def update(frame):

    global x,y

    U,V = flow(x,y)

    x = x + U*dt
    y = y + V*dt

    sc.set_offsets(np.c_[x,y])

    return sc,


ani = FuncAnimation(fig,update,frames=450,interval=40,blit=True)

plt.show()
