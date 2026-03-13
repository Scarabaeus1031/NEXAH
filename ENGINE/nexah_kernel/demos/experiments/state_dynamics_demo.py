"""
State Dynamics Demo

This example illustrates how system states evolve over time
using the StateDynamics module of the NEXAH kernel.

Instead of analyzing only structural graphs, the kernel can
also simulate trajectories across a state space.

The demo defines a simple dynamical rule:

    state_(t+1) = state_t + 1

This produces a trajectory that illustrates how the system
moves through its state space.

The ObservationFrame defines the reference frame (Q°)
in which the system evolution is interpreted.
"""

from ..state_dynamics import ObservationFrame, StateDynamics


# --------------------------------------------------
# Define observation frame
# --------------------------------------------------

frame = ObservationFrame(
    dimensions=["time"],
    metrics=["state_value"]
)

print("\nObservation Frame\n")
print(frame.describe())


# --------------------------------------------------
# Define transition rule
# --------------------------------------------------

def transition_rule(state):
    """
    Simple deterministic transition rule.
    """
    return state + 1


dynamics = StateDynamics(
    transition=transition_rule,
    frame=frame
)


# --------------------------------------------------
# Initial system state
# --------------------------------------------------

initial_state = 0

print("\nInitial State\n")
print(initial_state)


# --------------------------------------------------
# Simulate trajectory
# --------------------------------------------------

steps = 10

trajectory = dynamics.trajectory(initial_state, steps)

print("\nState Trajectory\n")

for t, state in enumerate(trajectory):
    print(f"t={t}  state={state}")


# --------------------------------------------------
# Example: stop condition
# --------------------------------------------------

print("\nSimulating until state >= 5\n")

def stop_condition(state):
    return state >= 5

trajectory_until = dynamics.simulate_until(
    initial_state,
    stop_condition,
    max_steps=20
)

print("\nTrajectory with stop condition\n")

for t, state in enumerate(trajectory_until):
    print(f"t={t}  state={state}")
