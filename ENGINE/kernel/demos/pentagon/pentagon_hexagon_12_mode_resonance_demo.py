"""
NEXAH Pentagon–Hexagon 12-Mode Resonance Demo

This demo highlights the resonance structure that emerges when

    5-fold symmetry (pentagon)
    6-fold symmetry (hexagon)
    center attractor

interact in a rotational field.

The interference tends to produce ~12 resonance directions.
These are drawn as reference lines.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# --------------------------------------------------
# Parameters
# --------------------------------------------------

pent_radius = 4.5
hex_radius = 3.2

rotation_strength = 0.85

pent_weight = 1.0
hex_weight = 0.9
center_weight = 1.5

epsilon = 0.4

particles = 900
dt = 0.05

xmin, xmax = -7, 7
ymin, ymax = -7, 7


# --------------------------------------------------
# Build pentagon attractors
# --------------------------------------------------

pentagon = {}

for i in range(5):

    angle = 2*np.pi*i/5 + np.pi/2

    x = pent_radius*np.cos(angle)
    y = pent_radius*np.sin(angle)

    pentagon[f"P{i+1}"] = (x,y)


# --------------------------------------------------
# Build hexagon attractors
# --------------------------------------------------

hexagon = {}

for i in range(6):

    angle = 2*np.pi*i/6 + np.pi/6

    x = hex_radius*np.cos(angle)
    y = hex_radius*np.sin(angle)

    hexagon[f"H{i+1}"] = (x,y)


center = (0.0,0.0)


# --------------------------------------------------
# Initial particle positions
# --------------------------------------------------

x = np.random.uniform(xmin,xmax,particles)
y = np.random.uniform(ymin,ymax,particles)


# --------------------------------------------------
# Flow field
# --------------------------------------------------

def flow(x,y):

    U = np.zeros_like(x)
    V = np.zeros_like(y)

    # Pentagon forces
    for ax,ay in pentagon.values():

        dx = x-ax
        dy = y-ay

        d = np.sqrt(dx*dx+dy*dy)+epsilon

        U += pent_weight*(-dx/d**2)
        V += pent_weight*(-dy/d**2)

        U += pent_weight*(-rotation_strength*dy/d**2)
        V += pent_weight*( rotation_strength*dx/d**2)


    # Hexagon forces
    for ax,ay in hexagon.values():

        dx = x-ax
        dy = y-ay

        d = np.sqrt(dx*dx+dy*dy)+epsilon

        U += hex_weight*(-dx/d**2)
        V += hex_weight*(-dy/d**2)

        U += hex_weight*( rotation_strength*dy/d**2)
        V += hex_weight*(-rotation_strength*dx/d**2)


    # Center force
    ax,ay = center

    dx = x-ax
    dy = y-ay

    d = np.sqrt(dx*dx+dy*dy)+epsilon

    U += center_weight*(-dx/d**2)
    V += center_weight*(-dy/d**2)

    return U,V


# --------------------------------------------------
# Plot setup
# --------------------------------------------------

fig,ax = plt.subplots(figsize=(7,7))

scatter = ax.scatter(x,y,s=6)


# Pentagon markers
for name,(px,py) in pentagon.items():

    ax.scatter(px,py,marker="*",s=260)
    ax.text(px+0.15,py+0.15,name)


# Hexagon markers
for name,(px,py) in hexagon.items():

    ax.scatter(px,py,marker="o",s=90)
    ax.text(px+0.15,py+0.15,name)


# Center
ax.scatter(center[0],center[1],marker="*",s=320)


# --------------------------------------------------
# Draw 12 resonance axes
# --------------------------------------------------

for i in range(12):

    angle = 2*np.pi*i/12

    x2 = 7*np.cos(angle)
    y2 = 7*np.sin(angle)

    ax.plot([0,x2],[0,y2],linestyle="--",alpha=0.25,color="gray")


ax.set_xlim(xmin,xmax)
ax.set_ylim(ymin,ymax)
ax.set_aspect("equal")

ax.set_title("NEXAH Pentagon–Hexagon 12-Mode Resonance")


# --------------------------------------------------
# Animation
# --------------------------------------------------

def update(frame):

    global x,y

    U,V = flow(x,y)

    x = x + U*dt
    y = y + V*dt

    scatter.set_offsets(np.c_[x,y])

    return scatter,


ani = FuncAnimation(
    fig,
    update,
    frames=450,
    interval=40,
    blit=True
)

plt.show()
