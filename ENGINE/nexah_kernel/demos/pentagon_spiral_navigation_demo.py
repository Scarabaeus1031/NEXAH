"""
Pentagon Spiral Navigation Demo
===============================

This demo combines two navigation structures inside the NEXAH kernel:

1. Pentagon domain navigation (structural space)
2. Spiral attractor dynamics (state space)

The system moves across structural domains while its spatial state
spirals toward the attractor Q°.

Kernel principle illustrated:

    state_(t+1) = F(state_t | G, L, Q°)

G   = structural graph
L   = regime landscape
Q°  = attractor / reference frame
"""

import math
import random

from ..state_dynamics import ObservationFrame, StateDynamics


# --------------------------------------------------
# Structural Diagram
# --------------------------------------------------

print("""
NEXAH Pentagon + Spiral Navigation

            Analysis
         /             \\
   Simulation       Applications
        \\             /
         Navigation — Discovery
                 |
                Q°

Spatial dynamics: spiral convergence toward Q°
""")


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

print("\nPentagon Domains\n")
for d in domains:
    print("-", d)

print("\nAttractor\n")
print("-", attractor)


# --------------------------------------------------
# Initial state
# --------------------------------------------------

state = {
    "x": 6.0,
    "y": 0.0,
    "domain": random.choice(domains)
}

print("\nInitial State\n")
print(state)


# --------------------------------------------------
# Spiral dynamics
# --------------------------------------------------

def spiral_step(x, y):

    r = math.sqrt(x*x + y*y)
    angle = math.atan2(y, x)

    # inward spiral
    r *= 0.87
    angle += 0.45

    new_x = r * math.cos(angle)
    new_y = r * math.sin(angle)

    return new_x, new_y


# --------------------------------------------------
# Pentagon transition
# --------------------------------------------------

def pentagon_transition(state):

    x = state["x"]
    y = state["y"]
    domain = state["domain"]

    # spatial update
    x, y = spiral_step(x, y)

    radius = math.sqrt(x*x + y*y)

    # structural update
    if domain != attractor:

        idx = domains.index(domain)

        # allow attractor only near the center
        if radius < 1.2 and random.random() < 0.35:
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
# Simulation
# --------------------------------------------------

steps = 40

trajectory = dynamics.trajectory(state, steps)

print("\nPentagon + Spiral Navigation\n")

for t, s in enumerate(trajectory):

    x = s["x"]
    y = s["y"]
    domain = s["domain"]

    r = math.sqrt(x*x + y*y)

    print(
        f"t={t:02d}  "
        f"x={x:6.3f}  y={y:6.3f}  "
        f"r={r:5.3f}  "
        f"domain={domain}"
    )

    if r < 0.7 or domain == attractor:

        print("\nSystem reached attractor region Q°\n")
        break
