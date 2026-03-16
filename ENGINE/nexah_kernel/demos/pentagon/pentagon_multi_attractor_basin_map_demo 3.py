"""
Pentagon Multi-Attractor Basin Map Demo
=======================================

This demo evaluates the spatial basin structure of a multi-attractor
system used in the NEXAH kernel.

Each initial position in a grid is simulated and assigned to the
attractor it eventually reaches.

Kernel principle:

    state_(t+1) = F(state_t | G, L, {Qi})

G   = structural pentagon domains
L   = spatial attractor landscape
Qi  = competing attractors

The result is a basin map showing which attractor dominates
each region of the phase space.
"""

import math
import random
import numpy as np
import matplotlib.pyplot as plt

from ..state_dynamics import ObservationFrame, StateDynamics


# --------------------------------------------------
# Parameters
# --------------------------------------------------

STEP_SIZE = 0.18
NOISE = 0.03
ATTRACTOR_RADIUS = 0.18
MAX_STEPS = 60

xmin, xmax = -6, 6
ymin, ymax = -6, 6
resolution = 140


# --------------------------------------------------
# Observation Frame
# --------------------------------------------------

frame = ObservationFrame(
    dimensions=["x", "y", "domain", "time"],
    metrics=["distance_to_attractor"]
)

print("\nObservation Frame\n")
print(frame.describe())


# --------------------------------------------------
# Pentagon domains
# --------------------------------------------------

domains = [
    "Analysis",
    "Applications",
    "Discovery",
    "Navigation",
    "Simulation"
]


# --------------------------------------------------
# Attractors
# --------------------------------------------------

attractors = {
    "Q1°": (-4, 0),
    "Q2°": (4, 0),
    "Q3°": (0, 4)
}

print("\nAttractors\n")
for name, pos in attractors.items():
    print(name, pos)


# --------------------------------------------------
# Distance
# --------------------------------------------------

def distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx*dx + dy*dy)


# --------------------------------------------------
# Transition
# --------------------------------------------------

def transition(state):

    x = state["x"]
    y = state["y"]
    domain = state["domain"]

    # nearest attractor
    nearest = None
    nearest_dist = float("inf")

    for pos in attractors.values():

        d = distance((x,y), pos)

        if d < nearest_dist:
            nearest = pos
            nearest_dist = d

    ax, ay = nearest

    x = x + STEP_SIZE * (ax - x)
    y = y + STEP_SIZE * (ay - y)

    x += random.uniform(-NOISE, NOISE)
    y += random.uniform(-NOISE, NOISE)

    # pentagon domain update
    idx = domains.index(domain)

    if random.random() < 0.15:
        domain = domains[(idx + 1) % len(domains)]

    return {
        "x": x,
        "y": y,
        "domain": domain
    }


dynamics = StateDynamics(
    transition=transition,
    frame=frame
)


# --------------------------------------------------
# Grid simulation
# --------------------------------------------------

xs = np.linspace(xmin, xmax, resolution)
ys = np.linspace(ymin, ymax, resolution)

basin = np.zeros((resolution, resolution))


for iy, y0 in enumerate(ys):
    for ix, x0 in enumerate(xs):

        state = {
            "x": x0,
            "y": y0,
            "domain": random.choice(domains)
        }

        for step in range(MAX_STEPS):

            x = state["x"]
            y = state["y"]

            for i,(name,pos) in enumerate(attractors.items()):

                if distance((x,y),pos) < ATTRACTOR_RADIUS:
                    basin[iy,ix] = i+1
                    break

            if basin[iy,ix] != 0:
                break

            state = dynamics.step(state)


# --------------------------------------------------
# Statistics
# --------------------------------------------------

print("\nBasin statistics\n")

for i,name in enumerate(attractors.keys()):
    count = np.sum(basin == i+1)
    print(name,"basin size:",int(count))


# --------------------------------------------------
# Plot
# --------------------------------------------------

plt.figure(figsize=(7,6))

plt.imshow(
    basin,
    origin="lower",
    extent=[xmin,xmax,ymin,ymax],
    cmap="tab10"
)

plt.colorbar(label="attractor index")

for i,(name,(ax,ay)) in enumerate(attractors.items()):

    plt.scatter(ax,ay,marker="*",s=250)
    plt.text(ax+0.15,ay+0.15,name)

plt.title("NEXAH Pentagon Multi-Attractor Basin Map")
plt.xlabel("x")
plt.ylabel("y")

plt.tight_layout()
plt.show()
