import numpy as np
import matplotlib.pyplot as plt


class StabilityEigenmodes:
    """
    Computes eigenmodes of the stability landscape.

    Treats the stability surface Z as a discretized operator
    and extracts dominant spatial eigenmodes.
    """

    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z

    def compute(self, k=6):
        """
        Compute top-k eigenmodes.
        """

        Z = self.Z

        nx, ny = Z.shape

        M = Z.reshape(nx * ny)

        cov = np.outer(M, M)

        eigvals, eigvecs = np.linalg.eigh(cov)

        idx = np.argsort(eigvals)[::-1]

        eigvals = eigvals[idx][:k]
        eigvecs = eigvecs[:, idx][:, :k]

        modes = []

        for i in range(k):
            mode = eigvecs[:, i].reshape(nx, ny)
            modes.append(mode)

        return eigvals, modes

    def plot(self, modes):

        n = len(modes)

        plt.figure(figsize=(12, 6))

        for i, mode in enumerate(modes):

            plt.subplot(2, (n + 1) // 2, i + 1)

            plt.contourf(self.X, self.Y, mode, levels=30, cmap="coolwarm")

            plt.title(f"Eigenmode {i+1}")

        plt.tight_layout()

        plt.show()
