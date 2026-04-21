"""
State Landscape Navigation Demo

This example illustrates how evolving system states interact with
a regime landscape.

The system evolves according to a transition rule:

    state_(t+1) = state_t + 1

Each state belongs to a region of the regime landscape:

- unstable region
- threshold region
- stable basin
- attractor

The demo shows how the system trajectory moves across these
regions until it reaches a stable attractor.
"""

from ..state_dynamics import ObservationFrame, StateDynamics


# --------------------------------------------------
# Observation Frame (Q° reference frame)
# --------------------------------------------------

frame = ObservationFrame(
    dimensions=["time"],
    metrics=["state_value"]
)

print("\nObservation Frame\n")
print(frame.describe())


# --------------------------------------------------
# Transition rule
# --------------------------------------------------

def transition_rule(state):
    """
    Simple forward progression rule.
    """
    return state + 1


dynamics = StateDynamics(
    transition=transition_rule,
    frame=frame
)


# --------------------------------------------------
# Define regime landscape
# --------------------------------------------------

landscape = {
    "unstable": range(0, 2),
    "threshold": range(2, 4),
    "stable": range(4, 7),
    "attractor": [7]
}


def classify_state(state):
    """
    Determine which region of the landscape the state belongs to.
    """

    for region, states in landscape.items():
        if state in states:
            return region

    return "unknown"


print("\nRegime Landscape\n")
for region, states in landscape.items():
    print(region, ":", list(states))


# --------------------------------------------------
# Initial state
# --------------------------------------------------

state = 0

print("\nInitial State\n")
print(state)


# --------------------------------------------------
# Simulate system evolution
# --------------------------------------------------

steps = 10

trajectory = dynamics.trajectory(state, steps)

print("\nState Landscape Navigation\n")

for t, state in enumerate(trajectory):

    region = classify_state(state)

    print(f"t={t}  state={state}  region={region}")

    if region == "attractor":
        print("\nAttractor reached\n")
        break
