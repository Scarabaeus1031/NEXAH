import numpy as np
import matplotlib.pyplot as plt


class GlobalStabilityStructure:
    """
    Unified visualization of the stability landscape.

    Combines:
    - stability contour
    - basin segmentation
    - critical points
    - transition graph
    """

    def __init__(self, X, Y, Z, basin_map, maxima, minima, saddles, edges):

        self.X = X
        self.Y = Y
        self.Z = Z

        self.basin_map = basin_map
        self.maxima = maxima
        self.minima = minima
        self.saddles = saddles
        self.edges = edges

    def plot(self):

        plt.figure(figsize=(10, 8))

        # stability contour
        plt.contourf(
            self.X,
            self.Y,
            self.Z,
            levels=40,
            cmap="viridis",
            alpha=0.8
        )

        # basin segmentation overlay
        plt.contour(
            self.X,
            self.Y,
            self.basin_map,
            levels=len(self.maxima),
            colors="white",
            linewidths=0.8,
            alpha=0.6
        )

        # maxima
        if self.maxima:
            m = np.array(self.maxima)
            plt.scatter(m[:,0], m[:,1], color="red", s=120, label="Maxima")

        # minima
        if self.minima:
            m = np.array(self.minima)
            plt.scatter(m[:,0], m[:,1], color="blue", s=100, label="Minima")

        # saddles
        if self.saddles:
            s = np.array(self.saddles)
            plt.scatter(s[:,0], s[:,1], color="white", s=80, label="Saddles")

        # transition edges
        for a, b in self.edges:

            x1, y1 = self.maxima[a]
            x2, y2 = self.maxima[b]

            plt.plot(
                [x1, x2],
                [y1, y2],
                color="black",
                linewidth=1.5,
                alpha=0.7
            )

        plt.title("Global Stability Structure")

        plt.xlabel("Axis X")
        plt.ylabel("Axis Y")

        plt.legend()
        plt.colorbar(label="Stability")

        plt.show()
