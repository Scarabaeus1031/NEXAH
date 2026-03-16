import numpy as np
import matplotlib.pyplot as plt


class StabilityKoopmanOperator:
    """
    Koopman operator approximation for stability dynamics.

    Approximates linear evolution of observables over the stability landscape.
    """

    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z

    def compute(self):

        Z = self.Z

        nx, ny = Z.shape

        data = Z.reshape(nx * ny)

        data_next = np.roll(data, 1)

        A = np.vstack([data, data_next]).T

        C = A.T @ A

        eigvals, eigvecs = np.linalg.eig(C)

        return eigvals, eigvecs

    def plot_spectrum(self, eigvals):

        plt.figure(figsize=(6, 6))

        plt.scatter(eigvals.real, eigvals.imag, color="black")

        plt.axhline(0)
        plt.axvline(0)

        plt.title("Koopman Spectrum")

        plt.xlabel("Real")
        plt.ylabel("Imaginary")

        plt.show()
