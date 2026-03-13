"""
NEXAH Adapter Demo Runner

This script demonstrates how external system adapters can be connected
to the NEXAH framework.

It loads several example adapters and prints their structural state graphs.
"""

"""
NEXAH Adapter Demo Runner
"""

import numpy as np
from scipy.integrate import odeint
from ..base_adapter import NexahAdapter


def lorenz(state, t, sigma=10.0, rho=28.0, beta=8/3):
    x, y, z = state
    return [
        sigma * (y - x),
        x * (rho - z) - y,
        x * y - beta * z
    ]


class LorenzAdapter(NexahAdapter):

    def __init__(self, steps=2000, sample_step=20):
        self.steps = steps
        self.sample_step = sample_step
        self._build_trajectory()

    def _build_trajectory(self):

        t = np.linspace(0, 30, self.steps)
        traj = odeint(lorenz, [1.0, 1.0, 1.0], t)

        self.nodes = []
        self.edges = {}
        self.node_states = {}

        for i in range(0, len(traj), self.sample_step):

            node = f"s{i}"
            self.nodes.append(node)

            x, y, z = traj[i]
            self.node_states[node] = (x, y, z)

        for i in range(len(self.nodes) - 1):
            self.edges.setdefault(self.nodes[i], []).append(self.nodes[i + 1])

    # -----------------------------------------------------------
    # Graph API
    # -----------------------------------------------------------

    def states(self):
        return self.nodes

    def transitions(self):
        return self.edges

    # -----------------------------------------------------------
    # Regime Detection
    # -----------------------------------------------------------

    def regimes(self):

        regimes = {}

        for node, (x, y, z) in self.node_states.items():

            if abs(x) > 25 or abs(y) > 25 or z > 45:
                regimes[node] = "ESCAPE"

            elif x < -5:
                regimes[node] = "LEFT_ATTRACTOR"

            elif x > 5:
                regimes[node] = "RIGHT_ATTRACTOR"

            else:
                regimes[node] = "TRANSITION"

        return regimes

    # -----------------------------------------------------------
    # Optional NEXAH API
    # -----------------------------------------------------------

    def initial_state(self):
        return self.nodes[0]

    def risk_targets(self):

        regimes = self.regimes()

        return [
            node for node, r in regimes.items()
            if r == "ESCAPE"
        ]

    def metadata(self):
        return {
            "system": "Lorenz Attractor",
            "type": "chaotic_dynamical_system",
            "dimension": 3
        }
