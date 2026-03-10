"""
Multi-Attractor Navigation Demo

This example illustrates how a system can navigate a landscape
containing multiple attractors.

Instead of converging toward a single center, the trajectory
moves through the landscape and may fall into different
attractor basins.

The demo simulates a simple 2D landscape with three attractors:

Q1°
Q2°
Q3°

Each step moves the system toward the nearest attractor while
still allowing exploration of the landscape.

This illustrates how NEXAH can analyze systems with multiple
stable regimes.
"""

import math
import random

from ..state_dynamics import ObservationFrame, StateDynamics


# --------------------------------------------------
# Observation Frame
# --------------------------------------------------

frame = ObservationFrame(
    dimensions=["x", "y", "time"],
    metrics=["distance_to_attractor"]
)

print("\nObservation Frame\n")
print(frame.describe())


# --------------------------------------------------
# Define attractors
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
# Transition rule
# --------------------------------------------------

def distance(a, b):

    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def multi_attractor_transition(state):
    """
    Move slightly toward the nearest attractor.
    """

    x, y = state

    # find nearest attractor
    nearest = None
    nearest_dist = float("inf")

    for pos in attractors.values():

        d = distance(state, pos)

        if d < nearest_dist:
            nearest = pos
            nearest_dist = d

    # move toward attractor
    ax, ay = nearest

    step = 0.2

    new_x = x + step * (ax - x)
    new_y = y + step * (ay - y)

    # small noise to keep exploration
    new_x += random.uniform(-0.05, 0.05)
    new_y += random.uniform(-0.05, 0.05)

    return (new_x, new_y)


dynamics = StateDynamics(
    transition=multi_attractor_transition,
    frame=frame
)


# --------------------------------------------------
# Initial state
# --------------------------------------------------

initial_state = (0, -4)

print("\nInitial State\n")
print(initial_state)


# --------------------------------------------------
# Simulate trajectory
# --------------------------------------------------

steps = 30

trajectory = dynamics.trajectory(initial_state, steps)

print("\nMulti-Attractor Navigation\n")

for t, state in enumerate(trajectory):

    x, y = state

    # determine closest attractor
    closest = None
    best_dist = float("inf")

    for name, pos in attractors.items():

        d = distance(state, pos)

        if d < best_dist:
            best_dist = d
            closest = name

    print(
        f"t={t:02d}  "
        f"x={x:.3f}  "
        f"y={y:.3f}  "
        f"closest_attractor={closest}"
    )
