import numpy as np
import matplotlib.pyplot as plt


class StabilityPhasePortrait:
    """
    Phase portrait of the stability landscape.

    Shows the vector flow induced by the stability gradient.
    """

    def __init__(self, X, Y, Z):

        self.X = X
        self.Y = Y
        self.Z = Z

    def compute_gradient(self):

        dZ_dy, dZ_dx = np.gradient(self.Z)

        return dZ_dx, dZ_dy

    def plot(self, step=5, trajectories=None):

        dZ_dx, dZ_dy = self.compute_gradient()

        plt.figure(figsize=(9,7))

        # landscape
        plt.contourf(
            self.X,
            self.Y,
            self.Z,
            levels=40,
            cmap="viridis",
            alpha=0.8
        )

        # vector field
        plt.quiver(
            self.X[::step, ::step],
            self.Y[::step, ::step],
            dZ_dx[::step, ::step],
            dZ_dy[::step, ::step],
            color="white",
            scale=50
        )

        # optional trajectories
        if trajectories is not None:

            for traj in trajectories:

                traj = np.array(traj)

                plt.plot(
                    traj[:,0],
                    traj[:,1],
                    color="red",
                    linewidth=2,
                    marker="o"
                )

        plt.title("Stability Phase Portrait")

        plt.xlabel("Axis X")
        plt.ylabel("Axis Y")

        plt.colorbar(label="Stability")

        plt.show()
