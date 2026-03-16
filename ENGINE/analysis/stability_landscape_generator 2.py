import numpy as np
import matplotlib.pyplot as plt


class StabilityLandscapeGenerator:
    """
    Generate synthetic stability landscapes.

    Useful for testing RL agents and control strategies
    on artificial dynamical systems.
    """

    def __init__(self, size=50):

        self.size = size

    def generate(self, peaks=2, noise=0.2):

        x = np.linspace(-3, 3, self.size)
        y = np.linspace(-3, 3, self.size)

        X, Y = np.meshgrid(x, y)

        Z = np.zeros_like(X)

        rng = np.random.default_rng()

        for _ in range(peaks):

            px = rng.uniform(-2, 2)
            py = rng.uniform(-2, 2)
            height = rng.uniform(2, 6)

            Z += height * np.exp(
                -((X - px) ** 2 + (Y - py) ** 2)
            )

        Z += noise * rng.normal(size=Z.shape)

        return X, Y, Z

    def plot(self, X, Y, Z):

        fig = plt.figure(figsize=(10,7))
        ax = fig.add_subplot(111, projection="3d")

        ax.plot_surface(
            X,
            Y,
            Z,
            cmap="viridis",
            linewidth=0,
            antialiased=True
        )

        ax.set_xlabel("System Axis X")
        ax.set_ylabel("System Axis Y")
        ax.set_zlabel("Stability")

        ax.set_title("Generated Stability Landscape")

        plt.show()

    def contour(self, X, Y, Z):

        plt.figure(figsize=(8,6))

        plt.contourf(
            X,
            Y,
            Z,
            levels=30,
            cmap="viridis"
        )

        plt.colorbar(label="Stability")

        plt.title("Stability Landscape Contour")

        plt.xlabel("Axis X")
        plt.ylabel("Axis Y")

        plt.show()
