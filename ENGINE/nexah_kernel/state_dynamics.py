"""
State Dynamics
==============

Defines the dynamical evolution of system states inside the NEXAH Kernel.

The kernel treats systems as evolving state spaces:

    state_t → state_(t+1)

This module introduces two fundamental structures:

ObservationFrame
    Defines how system states are interpreted (reference frame Q°).

StateDynamics
    Defines the transition rule describing how states evolve over time.
"""

from dataclasses import dataclass
from typing import Callable, Any, Dict, List


class ObservationFrame:
    """
    Defines the observation frame for system interpretation.

    The observation frame specifies the coordinate system in which
    system states are measured and compared.
    """

    def __init__(self, dimensions: List[str] = None, metrics: List[str] = None):

        self.dimensions = dimensions or []
        self.metrics = metrics or []

    def describe(self) -> Dict[str, List[str]]:
        """
        Return a description of the observation frame.
        """

        return {
            "dimensions": self.dimensions,
            "metrics": self.metrics,
        }


@dataclass
class StateDynamics:
    """
    Describes how system states evolve.

    state_(t+1) = F(state_t)
    """

    transition: Callable[[Any], Any]
    frame: ObservationFrame | None = None

    def step(self, state: Any) -> Any:
        """
        Compute the next state in the dynamical system.
        """

        return self.transition(state)

    def trajectory(self, initial_state: Any, steps: int):
        """
        Generate a trajectory of states.
        """

        state = initial_state
        trajectory = [state]

        for _ in range(steps):
            state = self.step(state)
            trajectory.append(state)

        return trajectory

    def simulate(self, initial_state: Any, steps: int):
        """
        Alias for trajectory simulation.

        Useful for navigation experiments and regime exploration.
        """

        return self.trajectory(initial_state, steps)

    def simulate_until(self, initial_state: Any, condition: Callable[[Any], bool], max_steps: int = 100):
        """
        Simulate the system until a condition is met.

        Example:
            stop when system enters a stable regime.
        """

        state = initial_state
        trajectory = [state]

        for _ in range(max_steps):

            if condition(state):
                break

            state = self.step(state)
            trajectory.append(state)

        return trajectory
