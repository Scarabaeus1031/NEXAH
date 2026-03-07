import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


class StabilityLandscape3D:
    """
    Simple 3D stability landscape for NEXAH.

    States are placed along one axis, and their stability / risk value
    is represented as height.
    Higher values = more stable
    Lower values = closer to collapse
    """

    def __init__(self, risk_map):
        self.risk_map = risk_map

    def plot(self, title="NEXAH Stability Landscape 3D"):
        """
        Render a simple 3D landscape from the risk map.
        """

        states = list(self.risk_map.keys())
        values = [self.risk_map[s] for s in states]

        x = list(range(len(states)))
        y = [0 for _ in states]
        z = values

        fig = plt.figure(figsize=(12, 7))
        ax = fig.add_subplot(111, projection="3d")

        ax.scatter(x, y, z, s=200)

        for i, state in enumerate(states):
            ax.text(x[i], y[i], z[i], state, fontsize=9)

        ax.plot(x, y, z, linewidth=2)

        ax.set_xlabel("State Index")
        ax.set_ylabel("Landscape Axis")
        ax.set_zlabel("Stability Score")
        ax.set_title(title)

        plt.show()
