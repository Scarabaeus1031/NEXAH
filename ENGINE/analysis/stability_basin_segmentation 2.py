import numpy as np
import matplotlib.pyplot as plt


class StabilityBasinSegmentation:
    """
    Segment a stability landscape into attraction basins.

    Each grid point is assigned to the nearest detected maximum.
    """

    def __init__(self, X, Y, Z, maxima):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.maxima = maxima

    def compute(self):
        """
        Assign each point of the landscape to the nearest maximum.
        """

        if not self.maxima:
            raise ValueError("No maxima provided for basin segmentation.")

        ny, nx = self.Z.shape
        basin_map = np.zeros((ny, nx), dtype=int)

        maxima_arr = np.array(self.maxima)

        for i in range(ny):
            for j in range(nx):

                point = np.array([self.X[i, j], self.Y[i, j]])

                distances = np.linalg.norm(maxima_arr - point, axis=1)

                basin_map[i, j] = np.argmin(distances)

        return basin_map

    def plot(self, basin_map):
        """
        Plot basin segmentation on top of the stability contour.
        """

        plt.figure(figsize=(9, 7))

        plt.contourf(
            self.X,
            self.Y,
            basin_map,
            levels=len(self.maxima),
            cmap="tab20",
            alpha=0.65
        )

        plt.contour(
            self.X,
            self.Y,
            self.Z,
            levels=20,
            colors="black",
            linewidths=0.5,
            alpha=0.5
        )

        maxima_arr = np.array(self.maxima)

        plt.scatter(
            maxima_arr[:, 0],
            maxima_arr[:, 1],
            color="red",
            s=100,
            label="Maxima"
        )

        for i, (x, y) in enumerate(self.maxima):
            plt.text(x, y, f"M{i}", color="white", fontsize=9, ha="center", va="center")

        plt.title("Stability Basin Segmentation")
        plt.xlabel("Axis X")
        plt.ylabel("Axis Y")
        plt.legend()

        plt.show()
