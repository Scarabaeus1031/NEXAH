"""
Monte Carlo Spiral Navigation Demo
==================================

This demo extends the pentagon_spiral_navigation_demo by running
many simulations of the same dynamics.

Each simulation follows the kernel transition rule:

    state_(t+1) = F(state_t | G, L, Q°)

The Monte Carlo experiment measures how quickly trajectories
converge to the attractor region.

The underlying transition dynamics are identical to the
pentagon_spiral_navigation_demo.
"""

import math
import random

import matplotlib.pyplot as plt

from ..state_dynamics import ObservationFrame, StateDynamics


# --------------------------------------------------
# Observation Frame
# --------------------------------------------------

frame = ObservationFrame(
    dimensions=["x", "y", "domain", "time"],
    metrics=["distance_to_Q"]
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

attractor = "Q°"


# --------------------------------------------------
# Spiral dynamics (same as previous demo)
# --------------------------------------------------

def spiral_step(x, y):

    r = math.sqrt(x*x + y*y)
    angle = math.atan2(y, x)

    r *= 0.85
    angle += 0.4

    new_x = r * math.cos(angle)
    new_y = r * math.sin(angle)

    return new_x, new_y


# --------------------------------------------------
# Pentagon transition (same dynamics)
# --------------------------------------------------

def pentagon_transition(state):

    x = state["x"]
    y = state["y"]
    domain = state["domain"]

    x, y = spiral_step(x, y)

    if domain != attractor:

        idx = domains.index(domain)

        if random.random() < 0.12:
            domain = attractor
        else:
            domain = domains[(idx + 1) % len(domains)]

    return {
        "x": x,
        "y": y,
        "domain": domain
    }


dynamics = StateDynamics(
    transition=pentagon_transition,
    frame=frame
)


# --------------------------------------------------
# Monte Carlo simulation
# --------------------------------------------------

runs = 200
max_steps = 40

steps_to_attractor = []
final_positions = []


for run in range(runs):

    state = {
        "x": 6.0,
        "y": 0.0,
        "domain": random.choice(domains)
    }

    trajectory = dynamics.trajectory(state, max_steps)

    for step, s in enumerate(trajectory):

        x = s["x"]
        y = s["y"]

        r = math.sqrt(x*x + y*y)

        if r < 0.8 or s["domain"] == attractor:

            steps_to_attractor.append(step)
            final_positions.append((x, y))
            break


# --------------------------------------------------
# Statistics
# --------------------------------------------------

mean_steps = sum(steps_to_attractor) / len(steps_to_attractor)

print("\nMonte Carlo Results\n")
print("runs:", runs)
print("mean steps to attractor:", round(mean_steps, 2))


# --------------------------------------------------
# Visualization
# --------------------------------------------------

xs = [p[0] for p in final_positions]
ys = [p[1] for p in final_positions]

plt.figure(figsize=(6,6))

plt.scatter(xs, ys, alpha=0.6)

plt.scatter([0],[0], marker="*", s=300)

plt.title("Monte Carlo Attractor Convergence")
plt.xlabel("x")
plt.ylabel("y")

plt.gca().set_aspect("equal")

plt.show()
