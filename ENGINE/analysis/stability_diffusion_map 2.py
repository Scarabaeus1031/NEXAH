import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances


class StabilityDiffusionMap:

    def __init__(self, X, Y, Z):

        self.X = X
        self.Y = Y
        self.Z = Z

    def compute(self, epsilon=1.0):

        data = np.vstack([
            self.X.flatten(),
            self.Y.flatten(),
            self.Z.flatten()
        ]).T

        D = pairwise_distances(data)

        K = np.exp(-(D**2) / epsilon)

        eigvals, eigvecs = np.linalg.eigh(K)

        idx = np.argsort(eigvals)[::-1]

        eigvals = eigvals[idx]
        eigvecs = eigvecs[:, idx]

        return eigvals, eigvecs

    def plot(self, eigvecs):

        plt.figure(figsize=(6,6))

        plt.scatter(
            eigvecs[:,1],
            eigvecs[:,2],
            s=3,
            alpha=0.7
        )

        plt.title("Diffusion Map Embedding")

        plt.xlabel("Mode 1")
        plt.ylabel("Mode 2")

        plt.show()
