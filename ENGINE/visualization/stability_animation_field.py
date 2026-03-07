import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class StabilityAnimationField:
    """
    Animated stability field for NEXAH.

    Shows a stability surface that changes over time while an agent
    trajectory is plotted on top of it.
    """

    def __init__(self, risk_map):
        self.risk_map = risk_map
        self.states = list(risk_map.keys())
        self.values = np.array([risk_map[s] for s in self.states])

    def plot(self, trajectory, frames=40, title="NEXAH Stability Animation Field"):

        n = len(self.states)

        x = np.linspace(0, n - 1, 120)
        y = np.linspace(-1, 1, 120)
        X, Y = np.meshgrid(x, y)

        fig = plt.figure(figsize=(13, 8))
        ax = fig.add_subplot(111, projection="3d")

        traj_x = []
        traj_y = []
        traj_z = []

        for s in trajectory:
            if s in self.risk_map:
                idx = self.states.index(s)
                traj_x.append(idx)
                traj_y.append(0)
                traj_z.append(self.risk_map[s])

        def compute_surface(t):
            stress_wave = 0.8 * np.sin(2 * np.pi * (X / max(n - 1, 1)) + t / 4.0)
            base = np.interp(X, np.arange(n), self.values)
            Z = base - (Y ** 2 * 2) - stress_wave
            return Z

        def update(frame):
            ax.clear()

            Z = compute_surface(frame)

            surf = ax.plot_surface(
                X,
                Y,
                Z,
                cmap="viridis",
                linewidth=0,
                antialiased=True,
                alpha=0.88
            )

            ax.scatter(
                np.arange(n),
                np.zeros(n),
                self.values,
                color="black",
                s=70
            )

            for i, s in enumerate(self.states):
                ax.text(i, 0, self.values[i], s, fontsize=9)

            step = min(frame, len(traj_x) - 1)

            if step >= 0:
                ax.plot(
                    traj_x[:step + 1],
                    traj_y[:step + 1],
                    traj_z[:step + 1],
                    color="red",
                    linewidth=3,
                    marker="o"
                )

                ax.scatter(
                    [traj_x[step]],
                    [traj_y[step]],
                    [traj_z[step]],
                    color="red",
                    s=120
                )

            ax.set_xlabel("State Index")
            ax.set_ylabel("System Axis")
            ax.set_zlabel("Stability")
            ax.set_title(f"{title}\nFrame {frame + 1}/{frames}")

            ax.set_xlim(0, n - 1)
            ax.set_ylim(-1, 1)

            zmin = min(self.values) - 3
            zmax = max(self.values) + 1
            ax.set_zlim(zmin, zmax)

            return []

        anim = FuncAnimation(
            fig,
            update,
            frames=frames,
            interval=250,
            blit=False
        )

        plt.show()

        return anim

def save(self, trajectory, filename="stability_animation.gif", frames=40):

    from matplotlib.animation import FuncAnimation, PillowWriter

    n = len(self.states)

    x = np.linspace(0, n - 1, 120)
    y = np.linspace(-1, 1, 120)
    X, Y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(13, 8))
    ax = fig.add_subplot(111, projection="3d")

    traj_x = []
    traj_y = []
    traj_z = []

    for s in trajectory:
        idx = self.states.index(s)
        traj_x.append(idx)
        traj_y.append(0)
        traj_z.append(self.risk_map[s])

    def compute_surface(t):
        stress_wave = 0.8 * np.sin(2 * np.pi * (X / max(n - 1, 1)) + t / 4.0)
        base = np.interp(X, np.arange(n), self.values)
        Z = base - (Y ** 2 * 2) - stress_wave
        return Z

    def update(frame):

        ax.clear()

        Z = compute_surface(frame)

        ax.plot_surface(
            X,
            Y,
            Z,
            cmap="viridis",
            linewidth=0,
            antialiased=True,
            alpha=0.9
        )

        ax.plot(
            traj_x,
            traj_y,
            traj_z,
            color="red",
            linewidth=3,
            marker="o"
        )

        ax.set_title("NEXAH Stability Field Animation")

    anim = FuncAnimation(fig, update, frames=frames, interval=200)

    anim.save(filename, writer=PillowWriter(fps=10))

    print("Saved animation:", filename)
