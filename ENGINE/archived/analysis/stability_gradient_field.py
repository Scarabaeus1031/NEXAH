import numpy as np
import matplotlib.pyplot as plt


class StabilityGradientField:
    """
    Compute and visualize stability gradients
    of a stability landscape.
    """

    def __init__(self, X, Y, Z):

        self.X = X
        self.Y = Y
        self.Z = Z

    def compute(self):
        """
        Compute gradient field
        """

        dZ_dy, dZ_dx = np.gradient(self.Z)

        return dZ_dx, dZ_dy

    def plot(self, step=4):

        dZ_dx, dZ_dy = self.compute()

        plt.figure(figsize=(9,7))

        plt.contourf(
            self.X,
            self.Y,
            self.Z,
            levels=30,
            cmap="viridis"
        )

        plt.quiver(
            self.X[::step, ::step],
            self.Y[::step, ::step],
            dZ_dx[::step, ::step],
            dZ_dy[::step, ::step],
            color="white",
            scale=40
        )

        plt.title("Stability Gradient Field")

        plt.xlabel("Axis X")
        plt.ylabel("Axis Y")

        plt.colorbar(label="Stability")

        plt.show()
