"""
Spiral Landscape Navigation Demo

This example illustrates how a system trajectory moves through a
continuous landscape with saddle regions and an attractor.

The system evolves according to a spiral transition rule that moves
states across the landscape.

The landscape contains:

- unstable outer region
- saddle transition region
- stable basin
- central attractor (Q°)

The demo illustrates how trajectories naturally converge toward the
attractor.
"""

import math

from ..state_dynamics import ObservationFrame, StateDynamics


# --------------------------------------------------
# Observation Frame (Q° reference frame)
# --------------------------------------------------

frame = ObservationFrame(
    dimensions=["x", "y", "time"],
    metrics=["distance_to_attractor"]
)

print("\nObservation Frame\n")
print(frame.describe())


# --------------------------------------------------
# Spiral transition rule
# --------------------------------------------------

def spiral_transition(state):
    """
    Spiral contraction toward the origin.
    """

    x, y = state

    r = math.sqrt(x*x + y*y)
    angle = math.atan2(y, x)

    # rotate slightly
    angle += 0.4

    # contract radius
    r *= 0.85

    new_x = r * math.cos(angle)
    new_y = r * math.sin(angle)

    return (new_x, new_y)


dynamics = StateDynamics(
    transition=spiral_transition,
    frame=frame
)


# --------------------------------------------------
# Define landscape regions
# --------------------------------------------------

def classify_region(state):

    x, y = state
    r = math.sqrt(x*x + y*y)

    if r > 5:
        return "unstable"

    if r > 3:
        return "saddle"

    if r > 1:
        return "basin"

    return "attractor"


print("\nLandscape Regions\n")
print("unstable : r > 5")
print("saddle   : 3 < r ≤ 5")
print("basin    : 1 < r ≤ 3")
print("attractor: r ≤ 1")


# --------------------------------------------------
# Initial state
# --------------------------------------------------

initial_state = (6.0, 0.0)

print("\nInitial State\n")
print(initial_state)


# --------------------------------------------------
# Simulate trajectory
# --------------------------------------------------

steps = 25

trajectory = dynamics.trajectory(initial_state, steps)

print("\nSpiral Landscape Navigation\n")

for t, state in enumerate(trajectory):

    region = classify_region(state)

    x, y = state

    print(
        f"t={t:02d}  "
        f"x={x:.3f}  "
        f"y={y:.3f}  "
        f"region={region}"
    )

    if region == "attractor":
        print("\nAttractor Q° reached\n")
        break
