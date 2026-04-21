"""
NEXAH Temporal Stability Field

Dynamic landscape evolution over time
"""

import numpy as np


class TemporalLandscape:

    def __init__(self, size=50):
        self.size = size
        self.rng = np.random.default_rng()

        self.peaks = [
            {
                "pos": np.array([
                    self.rng.uniform(10,40),
                    self.rng.uniform(10,40)
                ]),
                "velocity": self.rng.uniform(-0.3, 0.3, size=2),
                "height": self.rng.uniform(3, 8)
            }
            for _ in range(3)
        ]

    def step(self):
        """Update peak positions"""

        for p in self.peaks:
            p["pos"] += p["velocity"]

            # bounce at boundaries
            for i in range(2):
                if p["pos"][i] < 0 or p["pos"][i] > self.size:
                    p["velocity"][i] *= -1

    def generate(self):
        """Generate landscape at current time"""

        x = np.linspace(0, self.size-1, self.size)
        y = np.linspace(0, self.size-1, self.size)
        X, Y = np.meshgrid(x, y)

        Z = np.zeros_like(X)

        for p in self.peaks:
            px, py = p["pos"]
            h = p["height"]

            Z += h * np.exp(-((X - px)**2 + (Y - py)**2) / 50)

        return Z
