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
        for i in range(0, len(traj), self.sample_step):
            self.nodes.append(f"s{i}")

        self.edges = {}
        for i in range(len(self.nodes) - 1):
            self.edges.setdefault(self.nodes[i], []).append(self.nodes[i+1])

    def states(self):
        return self.nodes

    def transitions(self):
        return self.edges

    def regimes(self):
        return {s: "CHAOTIC_FLOW" for s in self.nodes}

    def metadata(self):
        return {
            "system": "Lorenz Attractor",
            "type": "chaotic_dynamical_system"
        }
