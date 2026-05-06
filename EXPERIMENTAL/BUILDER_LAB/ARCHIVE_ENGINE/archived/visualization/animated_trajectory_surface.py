import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D


class AnimatedTrajectorySurface:

    def __init__(self, risk_map):
        self.risk_map = risk_map
        self.states = list(risk_map.keys())
        self.values = np.array([risk_map[s] for s in self.states])

    def plot(self, trajectory, title="NEXAH Animated Stability Navigation"):

        n = len(self.states)

        # surface grid
        x = np.linspace(0, n - 1, 120)
        y = np.linspace(-1, 1, 120)

        X, Y = np.meshgrid(x, y)

        Z = np.interp(X, np.arange(n), self.values)

        # create valley shape
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

        ax.set_xlabel("State Index")
        ax.set_ylabel("System Axis")
        ax.set_zlabel("Stability")
        ax.set_title(title)

        # convert trajectory → coordinates
        traj_x = []
        traj_y = []
        traj_z = []

        for s in trajectory:
            if s in self.risk_map:
                idx = self.states.index(s)
                traj_x.append(idx)
                traj_y.append(0)
                traj_z.append(self.risk_map[s])

        line, = ax.plot([], [], [], color="red", linewidth=3)
        point, = ax.plot([], [], [], marker="o", color="red", markersize=10)

        def update(frame):

            line.set_data(traj_x[:frame+1], traj_y[:frame+1])
            line.set_3d_properties(traj_z[:frame+1])

            point.set_data(traj_x[frame:frame+1], traj_y[frame:frame+1])
            point.set_3d_properties(traj_z[frame:frame+1])

            return line, point

        anim = FuncAnimation(
            fig,
            update,
            frames=len(traj_x),
            interval=800,
            blit=False
        )

        plt.show()
