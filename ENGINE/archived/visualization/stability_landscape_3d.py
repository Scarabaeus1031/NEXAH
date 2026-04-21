import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class StabilitySurface3D:
    """
    Creates a smooth 3D stability landscape surface
    based on discrete system states.

    Higher values = more stable
    Lower values = closer to collapse
    """

    def __init__(self, risk_map):
        self.risk_map = risk_map

    def plot(self, title="NEXAH Stability Surface"):

        states = list(self.risk_map.keys())
        values = np.array([self.risk_map[s] for s in states])

        n = len(states)

        # create surface grid
        x = np.linspace(0, n - 1, 100)
        y = np.linspace(-1, 1, 100)

        X, Y = np.meshgrid(x, y)

        # interpolate stability values across surface
        Z = np.interp(X, np.arange(n), values)

        # create curved valley effect
        Z = Z - (Y ** 2 * 2)

        fig = plt.figure(figsize=(13, 8))
        ax = fig.add_subplot(111, projection="3d")

        surf = ax.plot_surface(
            X,
            Y,
            Z,
            cmap="viridis",
            linewidth=0,
            antialiased=True,
            alpha=0.9
        )

        # plot real system states
        ax.scatter(
            np.arange(n),
            np.zeros(n),
            values,
            color="red",
            s=100
        )

        for i, state in enumerate(states):
            ax.text(i, 0, values[i], state, fontsize=9)

        ax.set_xlabel("State Index")
        ax.set_ylabel("System Axis")
        ax.set_zlabel("Stability")

        ax.set_title(title)

        fig.colorbar(surf, shrink=0.5, aspect=10)

        plt.show()
