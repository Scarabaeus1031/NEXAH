import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class TrajectoryOnSurface:

    def __init__(self, risk_map):
        self.risk_map = risk_map

    def plot(self, trajectory, title="NEXAH Agent Trajectory on Stability Surface"):

        states = list(self.risk_map.keys())
        values = np.array([self.risk_map[s] for s in states])

        n = len(states)

        # Surface grid
        x = np.linspace(0, n - 1, 120)
        y = np.linspace(-1, 1, 120)

        X, Y = np.meshgrid(x, y)

        Z = np.interp(X, np.arange(n), values)

        # valley curvature
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
            values,
            color="black",
            s=80
        )

        for i, state in enumerate(states):
            ax.text(i, 0, values[i], state)

        # convert trajectory states → coordinates
        traj_x = []
        traj_y = []
        traj_z = []

        for s in trajectory:

            if s not in self.risk_map:
                continue

            idx = states.index(s)

            traj_x.append(idx)
            traj_y.append(0)
            traj_z.append(self.risk_map[s])

        # plot agent trajectory
        ax.plot(
            traj_x,
            traj_y,
            traj_z,
            color="red",
            linewidth=3,
            marker="o"
        )

        ax.set_xlabel("State Index")
        ax.set_ylabel("System Axis")
        ax.set_zlabel("Stability")

        ax.set_title(title)

        fig.colorbar(surf, shrink=0.5, aspect=10)

        plt.show()
