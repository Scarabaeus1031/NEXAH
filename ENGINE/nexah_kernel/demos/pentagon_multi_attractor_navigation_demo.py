"""
Pentagon Multi-Attractor Navigation Demo
========================================

This demo combines structural navigation across the NEXAH pentagon
domains with a spatial landscape containing multiple attractors.

Each step updates:

1) spatial state (x,y) toward the nearest attractor
2) structural domain navigation across the pentagon

Kernel principle:

    state_(t+1) = F(state_t | G, L, {Q_i})

G  = pentagon domain graph
L  = spatial attractor landscape
Qᵢ = multiple attractors
"""

import math
import random

from ..state_dynamics import ObservationFrame, StateDynamics


# --------------------------------------------------
# Parameters
# --------------------------------------------------

STEP_SIZE = 0.18
NOISE = 0.04
ATTRACTOR_RADIUS = 0.15
MAX_STEPS = 40


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

print("\nPentagon Domains\n")
for d in domains:
    print("-", d)


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
# Distance
# --------------------------------------------------

def distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx*dx + dy*dy)


# --------------------------------------------------
# Transition rule
# --------------------------------------------------

def pentagon_multi_attractor_transition(state):

    x = state["x"]
    y = state["y"]
    domain = state["domain"]

    # ----------------------------
    # spatial attractor dynamics
    # ----------------------------

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

    # ----------------------------
    # pentagon navigation
    # ----------------------------

    idx = domains.index(domain)

    if random.random() < 0.2:
        domain = domains[(idx + 1) % len(domains)]

    return {
        "x": x,
        "y": y,
        "domain": domain
    }


dynamics = StateDynamics(
    transition=pentagon_multi_attractor_transition,
    frame=frame
)


# --------------------------------------------------
# Initial state
# --------------------------------------------------

state = {
    "x": 0.0,
    "y": -4.0,
    "domain": random.choice(domains)
}

print("\nInitial State\n")
print(state)


# --------------------------------------------------
# Simulation
# --------------------------------------------------

trajectory = dynamics.trajectory(state, MAX_STEPS)

print("\nPentagon Multi-Attractor Navigation\n")

for t, s in enumerate(trajectory):

    x = s["x"]
    y = s["y"]
    domain = s["domain"]

    closest = None
    best_dist = float("inf")

    for name, pos in attractors.items():

        d = distance((x,y), pos)

        if d < best_dist:
            best_dist = d
            closest = name

    print(
        f"t={t:02d}  "
        f"x={x:.3f}  "
        f"y={y:.3f}  "
        f"domain={domain}  "
        f"closest={closest}"
    )

    if best_dist < ATTRACTOR_RADIUS:

        print(f"\nSystem entered attractor basin {closest}\n")
        break
