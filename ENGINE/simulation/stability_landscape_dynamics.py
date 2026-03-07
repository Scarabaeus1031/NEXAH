import numpy as np
import matplotlib.pyplot as plt


class StabilityLandscapeDynamics:

    def __init__(self, X, Y, Z):

        self.X = X
        self.Y = Y
        self.Z = Z.copy()

    def evolve(self, steps=50, drift=0.01):

        history = []

        Z = self.Z.copy()

        for _ in range(steps):

            noise = np.random.normal(0, drift, Z.shape)

            gx, gy = np.gradient(Z)

            Z = Z + noise - 0.01*(gx**2 + gy**2)

            history.append(Z.copy())

        return history

    def plot(self, Z):

        plt.figure(figsize=(8,6))

        plt.contourf(self.X, self.Y, Z, levels=40, cmap="viridis")

        plt.title("Dynamic Stability Landscape")

        plt.colorbar()

        plt.show()

    def animate(self, history, step=5):

        for i in range(0, len(history), step):

            plt.clf()

            plt.contourf(
                self.X,
                self.Y,
                history[i],
                levels=40,
                cmap="viridis"
            )

            plt.pause(0.1)

        plt.show()
