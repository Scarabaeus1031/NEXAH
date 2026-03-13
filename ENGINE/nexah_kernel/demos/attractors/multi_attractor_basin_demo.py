"""
Multi-Attractor Basin Demo
==========================

This demo extends the NEXAH spiral attractor model to multiple attractors.

Instead of a single global attractor Q°, the system now contains several
competing attractors.

Each initial state converges toward the nearest attractor basin.

Kernel principle:

    state_(t+1) = F(state_t | G, L, {Q_i})

The resulting heatmap shows the basin structure of the system.
"""

import math
import numpy as np
import matplotlib.pyplot as plt

from ..state_dynamics import ObservationFrame, StateDynamics


# --------------------------------------------------
# Observation frame
# --------------------------------------------------

frame = ObservationFrame(
    dimensions=["x", "y", "time"],
    metrics=["distance_to_Q"]
)

print("\nObservation Frame\n")
print(frame.describe())


# --------------------------------------------------
# Define attractors
# --------------------------------------------------

attractors = [
    (-3.0, 0.0),
    (3.0, 0.0),
    (0.0, 3.5)
]

print("\nAttractors\n")
for i, a in enumerate(attractors):
    print(f"Q{i+1}° =", a)


# --------------------------------------------------
# Dynamics
# --------------------------------------------------

def step_toward_attractor(x, y, ax, ay):

    dx = ax - x
    dy = ay - y

    x += 0.12 * dx
    y += 0.12 * dy

    return x, y


def transition(state):

    x, y = state

    # choose nearest attractor
    distances = [
        math.sqrt((x-ax)**2 + (y-ay)**2)
        for ax, ay in attractors
    ]

    idx = int(np.argmin(distances))

    ax, ay = attractors[idx]

    return step_toward_attractor(x, y, ax, ay)


dynamics = StateDynamics(
    transition=transition,
    frame=frame
)


# --------------------------------------------------
# Grid
# --------------------------------------------------

xmin, xmax = -6, 6
ymin, ymax = -6, 6

resolution = 150
max_steps = 60
radius = 0.4

xs = np.linspace(xmin, xmax, resolution)
ys = np.linspace(ymin, ymax, resolution)

basin = np.zeros((resolution, resolution))


# --------------------------------------------------
# Basin evaluation
# --------------------------------------------------

for iy, y0 in enumerate(ys):
    for ix, x0 in enumerate(xs):

        state = (x0, y0)

        for step in range(max_steps):

            x, y = state

            for i, (ax, ay) in enumerate(attractors):

                if math.sqrt((x-ax)**2 + (y-ay)**2) < radius:
                    basin[iy, ix] = i + 1
                    break

            if basin[iy, ix] > 0:
                break

            state = dynamics.step(state)


# --------------------------------------------------
# Plot
# --------------------------------------------------

plt.figure(figsize=(7,6))

plt.imshow(
    basin,
    origin="lower",
    extent=[xmin, xmax, ymin, ymax],
    cmap="tab10"
)

plt.colorbar(label="attractor index")

for i, (ax, ay) in enumerate(attractors):

    plt.scatter(ax, ay, marker="*", s=250)
    plt.text(ax+0.1, ay+0.1, f"Q{i+1}°")

plt.title("NEXAH Multi-Attractor Basin Map")
plt.xlabel("x")
plt.ylabel("y")

plt.tight_layout()
plt.show()
