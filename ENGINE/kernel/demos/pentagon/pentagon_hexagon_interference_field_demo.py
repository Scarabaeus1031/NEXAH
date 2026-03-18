"""
NEXAH Pentagon–Hexagon Interference Field Demo

This demo combines two symmetry systems:

    Pentagon (5 attractors)
    Hexagon  (6 attractors)

plus a central attractor.

The interaction between these two rotational symmetry groups
creates interference patterns similar to:

    quasi-crystals
    plasma resonances
    mandala / rosette fields
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
hex_weight = 0.8
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


print("\nPentagon Attractors\n")
for k,v in pentagon.items():
    print(k,v)

print("\nHexagon Attractors\n")
for k,v in hexagon.items():
    print(k,v)

print("\nCenter\n",center)


# --------------------------------------------------
# Initial particles
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


    # Central attractor
    ax,ay = center

    dx = x-ax
    dy = y-ay

    d = np.sqrt(dx*dx+dy*dy)+epsilon

    U += center_weight*(-dx/d**2)
    V += center_weight*(-dy/d**2)

    return U,V


# --------------------------------------------------
# Plot
# --------------------------------------------------

fig,ax = plt.subplots(figsize=(7,7))

sc = ax.scatter(x,y,s=6)


# Pentagon markers
for name,(px,py) in pentagon.items():

    ax.scatter(px,py,marker="*",s=260)
    ax.text(px+0.15,py+0.15,name)


# Hexagon markers
for name,(px,py) in hexagon.items():

    ax.scatter(px,py,marker="o",s=90)
    ax.text(px+0.15,py+0.15,name)


# center
ax.scatter(center[0],center[1],marker="*",s=320)


ax.set_xlim(xmin,xmax)
ax.set_ylim(ymin,ymax)
ax.set_aspect("equal")

ax.set_title("NEXAH Pentagon–Hexagon Interference Field")


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


ani = FuncAnimation(
    fig,
    update,
    frames=450,
    interval=40,
    blit=True
)

plt.show()
