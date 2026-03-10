"""
Pentagon Navigation Demo

This example illustrates navigation across five structural domains
arranged as a pentagon around a central attractor Q°.

Each step moves the system along the pentagon structure until the
system converges toward the central attractor.

The demo illustrates how trajectories can move across structural
domains before stabilizing at the attractor.

Domains:

Analysis
Applications
Discovery
Navigation
Simulation

Center:

Q° (reference frame / attractor)
"""

import random

from ..state_dynamics import ObservationFrame, StateDynamics


# --------------------------------------------------
# ASCII Pentagon Structure
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


# --------------------------------------------------
# Observation Frame (Q° reference frame)
# --------------------------------------------------

frame = ObservationFrame(
    dimensions=["domain", "time"],
    metrics=["distance_to_Q"]
)

print("\nObservation Frame\n")
print(frame.describe())


# --------------------------------------------------
# Define pentagon domains
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
# Transition rule
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

    # otherwise move to next domain
    next_idx = (idx + 1) % len(domains)

    return domains[next_idx]


dynamics = StateDynamics(
    transition=pentagon_transition,
    frame=frame
)


# --------------------------------------------------
# Initial state
# --------------------------------------------------

initial_state = random.choice(domains)

print("\nInitial Domain\n")
print(initial_state)


# --------------------------------------------------
# Simulate trajectory
# --------------------------------------------------

steps = 20

trajectory = dynamics.trajectory(initial_state, steps)

print("\nPentagon Navigation Trajectory\n")

for t, state in enumerate(trajectory):

    print(f"t={t:02d}  domain={state}")

    if state == attractor:
        print("\nSystem converged to attractor Q°\n")
        break
