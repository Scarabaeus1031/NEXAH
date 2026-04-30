"""
Pentagon Navigation Demo
========================

This example illustrates navigation across five structural domains
arranged as a pentagon around a central attractor Q°.

The system moves across structural domains until it converges
toward the attractor.

This demonstrates the NEXAH kernel navigation principle:

    state_(t+1) = F(state_t | G, L, Q°)

where

G   = structural graph
L   = regime landscape
Q°  = attractor / reference frame

Domains:

Analysis
Applications
Discovery
Navigation
Simulation
"""

import random

from ..state_dynamics import ObservationFrame, StateDynamics


# --------------------------------------------------
# Structural Diagram
# --------------------------------------------------

print("""
NEXAH Pentagon Navigation Structure

            Analysis
         /             \\
   Simulation       Applications
        \\             /
         Navigation — Discovery
                 |
                Q°
""")


print("""
Kernel Dynamics

state_(t+1) = F(state_t | G, L, Q°)

G  : structural graph
L  : regime landscape
Q° : attractor / reference frame
""")


# --------------------------------------------------
# Observation Frame
# --------------------------------------------------

frame = ObservationFrame(
    dimensions=["domain", "time"],
    metrics=["distance_to_Q"]
)

print("\nObservation Frame\n")
print(frame.describe())


# --------------------------------------------------
# Pentagon Domains
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
# Transition Rule
# --------------------------------------------------

def pentagon_transition(state):
    """
    Move around the pentagon or converge to the attractor.
    """

    if state == attractor:
        return attractor

    idx = domains.index(state)

    # probability to jump toward attractor
    if random.random() < 0.15:
        return attractor

    # otherwise move along the pentagon
    next_idx = (idx + 1) % len(domains)

    return domains[next_idx]


dynamics = StateDynamics(
    transition=pentagon_transition,
    frame=frame
)


# --------------------------------------------------
# Initial State
# --------------------------------------------------

initial_state = random.choice(domains)

print("\nInitial Domain\n")
print(initial_state)


# --------------------------------------------------
# Simulate Navigation
# --------------------------------------------------

steps = 20

trajectory = dynamics.trajectory(initial_state, steps)

print("\nPentagon Navigation Trajectory\n")

for t, state in enumerate(trajectory):

    print(f"t={t:02d}  domain={state}")

    if state == attractor:
        print("\nSystem converged to attractor Q°\n")
        break
