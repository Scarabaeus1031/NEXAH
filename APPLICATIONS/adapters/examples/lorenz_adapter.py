"""
NEXAH Lorenz Adapter

This adapter connects the classical Lorenz attractor to the NEXAH
framework.

The continuous Lorenz dynamics are sampled along a trajectory and
translated into a discrete state graph representation.

Pipeline:

Lorenz Dynamical System
        ↓
Sampled Trajectory
        ↓
Discrete State Nodes
        ↓
Regime Classification
        ↓
NEXAH State Graph

Regimes used in this adapter:

- LEFT_ATTRACTOR
- RIGHT_ATTRACTOR
- TRANSITION
- ESCAPE

Purpose:
This adapter serves as a Category-A benchmark for testing whether
NEXAH can interpret and navigate chaotic dynamical systems through
a regime-based graph abstraction.
"""

import numpy as np
from scipy.integrate import odeint

from APPLICATIONS.adapters.base_adapter import NexahAdapter


def lorenz(state, t, sigma=10.0, rho=28.0, beta=8 / 3):
    """
    Classical Lorenz system.
    """
    x, y, z = state
    return [
        sigma * (y - x),
        x * (rho - z) - y,
        x * y - beta * z,
    ]


class LorenzAdapter(NexahAdapter):
    """
    Adapter that converts a sampled Lorenz trajectory into a NEXAH-compatible
    discrete state graph with regime labels.
    """

    def __init__(self, steps=2000, sample_step=20):
        self.steps = steps
        self.sample_step = sample_step
        self._build_trajectory()

    def _build_trajectory(self):
        """
        Simulate the Lorenz system and convert sampled trajectory points
        into graph nodes with attached state values.
        """
        t = np.linspace(0, 30, self.steps)
        traj = odeint(lorenz, [1.0, 1.0, 1.0], t)

        self.nodes = []
        self.edges = {}
        self.node_states = {}

        for i in range(0, len(traj), self.sample_step):
            node = f"s{i}"
            self.nodes.append(node)

            x, y, z = traj[i]
            self.node_states[node] = (float(x), float(y), float(z))

        for i in range(len(self.nodes) - 1):
            self.edges.setdefault(self.nodes[i], []).append(self.nodes[i + 1])

    def states(self):
        """
        Return sampled trajectory nodes.
        """
        return self.nodes

    def transitions(self):
        """
        Return trajectory-based graph transitions.
        """
        return self.edges

    def regimes(self):
        """
        Classify each sampled node into a Lorenz regime.

        Heuristic interpretation:
        - LEFT_ATTRACTOR: trajectory on left wing
        - RIGHT_ATTRACTOR: trajectory on right wing
        - TRANSITION: central switching region
        - ESCAPE: unusually distant state
        """
        regime_map = {}

        for node, (x, y, z) in self.node_states.items():
            if abs(x) > 25 or abs(y) > 25 or z > 45:
                regime_map[node] = "ESCAPE"
            elif x < -5:
                regime_map[node] = "LEFT_ATTRACTOR"
            elif x > 5:
                regime_map[node] = "RIGHT_ATTRACTOR"
            else:
                regime_map[node] = "TRANSITION"

        return regime_map

    def initial_state(self):
        """
        Return the first sampled state as initial state.
        """
        return self.nodes[0] if self.nodes else None

    def risk_targets(self):
        """
        Treat ESCAPE states as risk targets.
        """
        return [
            node
            for node, regime in self.regimes().items()
            if regime == "ESCAPE"
        ]

    def metadata(self):
        """
        Return adapter metadata.
        """
        return {
            "system": "Lorenz Attractor",
            "type": "chaotic_dynamical_system",
            "dimension": 3,
            "steps": self.steps,
            "sample_step": self.sample_step,
        }
