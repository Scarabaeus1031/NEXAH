import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class PolicyComparisonSurface:
    """
    Visualize multiple policy trajectories on the same
    stability landscape surface.
    """

    def __init__(self, risk_map):
        self.risk_map = risk_map
        self.states = list(risk_map.keys())
        self.values = np.array([risk_map[s] for s in self.states])

    def plot(self, trajectories, title="NEXAH Policy Comparison"):

        n = len(self.states)

        # create surface grid
        x = np.linspace(0, n - 1, 120)
        y = np.linspace(-1, 1, 120)

        X, Y = np.meshgrid(x, y)

        Z = np.interp(X, np.arange(n), self.values)

        # valley shape
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
            alpha=0.85
        )

        # plot system states
        ax.scatter(
            np.arange(n),
            np.zeros(n),
            self.values,
            color="black",
            s=80
        )

        for i, s in enumerate(self.states):
            ax.text(i, 0, self.values[i], s)

        # colors for different policies
        colors = [
            "red",
            "blue",
            "orange",
            "purple",
            "green",
            "cyan"
        ]

        for idx, (label, trajectory) in enumerate(trajectories.items()):

            traj_x = []
            traj_y = []
            traj_z = []

            for s in trajectory:

                if s not in self.risk_map:
                    continue

                state_index = self.states.index(s)

                traj_x.append(state_index)
                traj_y.append(0)
                traj_z.append(self.risk_map[s])

            ax.plot(
                traj_x,
                traj_y,
                traj_z,
                color=colors[idx % len(colors)],
                linewidth=3,
                marker="o",
                label=label
            )

        ax.set_xlabel("State Index")
        ax.set_ylabel("System Axis")
        ax.set_zlabel("Stability")

        ax.set_title(title)

        ax.legend()

        fig.colorbar(surf, shrink=0.5, aspect=10)

        plt.show()
