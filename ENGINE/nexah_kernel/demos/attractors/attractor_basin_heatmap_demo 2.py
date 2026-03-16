"""
Attractor Basin Heatmap Demo
============================

This demo estimates the attractor basin of Q° by running many
spiral navigation trajectories from different starting points.

For each initial point in a 2D grid, the system is iterated until:

- it reaches the attractor region, or
- the maximum number of steps is exceeded

The result is visualized as a heatmap showing how quickly each
initial condition converges toward Q°.

Kernel principle illustrated:

    state_(t+1) = F(state_t | G, L, Q°)

This demo extends the spiral navigation and Monte Carlo demos
toward a spatial stability map of the attractor basin.
"""

import math

import matplotlib.pyplot as plt
import numpy as np

from ..state_dynamics import ObservationFrame, StateDynamics


# --------------------------------------------------
# Observation Frame
# --------------------------------------------------

frame = ObservationFrame(
    dimensions=["x", "y", "time"],
    metrics=["distance_to_Q", "steps_to_attractor"]
)

print("\nObservation Frame\n")
print(frame.describe())


# --------------------------------------------------
# Kernel description
# --------------------------------------------------

print("""
NEXAH Attractor Basin Heatmap

Kernel equation

state_(t+1) = F(state_t | G, L, Q°)

This demo evaluates convergence across a grid of initial states.
""")


# --------------------------------------------------
# Spiral dynamics
# --------------------------------------------------

def spiral_step(x, y):
    """
    Spiral contraction toward the origin.
    """

    r = math.sqrt(x * x + y * y)
    angle = math.atan2(y, x)

    r *= 0.90
    angle += 0.35

    new_x = r * math.cos(angle)
    new_y = r * math.sin(angle)

    return new_x, new_y


def transition_rule(state):
    """
    State transition for heatmap evaluation.
    """

    x, y = state
    return spiral_step(x, y)


dynamics = StateDynamics(
    transition=transition_rule,
    frame=frame
)


# --------------------------------------------------
# Grid parameters
# --------------------------------------------------

xmin, xmax = -6.0, 6.0
ymin, ymax = -6.0, 6.0

resolution = 60
max_steps = 40
attractor_radius = 0.8

xs = np.linspace(xmin, xmax, resolution)
ys = np.linspace(ymin, ymax, resolution)

heatmap = np.full((resolution, resolution), max_steps, dtype=float)


# --------------------------------------------------
# Basin evaluation
# --------------------------------------------------

for iy, y0 in enumerate(ys):
    for ix, x0 in enumerate(xs):

        state = (x0, y0)

        for step in range(max_steps):

            x, y = state
            r = math.sqrt(x * x + y * y)

            if r < attractor_radius:
                heatmap[iy, ix] = step
                break

            state = dynamics.step(state)


# --------------------------------------------------
# Statistics
# --------------------------------------------------

reachable = heatmap < max_steps
reachable_count = int(np.sum(reachable))
total_count = resolution * resolution

print("\nHeatmap Statistics\n")
print("grid resolution:", resolution, "x", resolution)
print("total initial states:", total_count)
print("reachable attractor states:", reachable_count)

if reachable_count > 0:
    mean_steps = float(np.mean(heatmap[reachable]))
    print("mean steps to attractor:", round(mean_steps, 2))
else:
    print("mean steps to attractor: n/a")


# --------------------------------------------------
# Visualization
# --------------------------------------------------

plt.figure(figsize=(7, 6))

im = plt.imshow(
    heatmap,
    origin="lower",
    extent=[xmin, xmax, ymin, ymax],
    aspect="equal"
)

plt.colorbar(im, label="steps to attractor")

# mark Q°
plt.scatter([0], [0], marker="*", s=250)

# attractor region
circle = plt.Circle((0, 0), attractor_radius, fill=False)
plt.gca().add_patch(circle)

plt.title("NEXAH Attractor Basin Heatmap")
plt.xlabel("x")
plt.ylabel("y")

plt.tight_layout()
plt.show()
