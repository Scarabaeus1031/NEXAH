import numpy as np
import matplotlib.pyplot as plt


class StabilityLyapunovSpectrum:

    def __init__(self, X, Y, Z):

        self.X = X
        self.Y = Y
        self.Z = Z

    def compute(self):

        gx, gy = np.gradient(self.Z)

        magnitude = np.sqrt(gx**2 + gy**2)

        lyapunov = np.log(1 + magnitude)

        return lyapunov

    def plot(self, lyapunov):

        plt.figure(figsize=(8,6))

        plt.contourf(self.X, self.Y, lyapunov, levels=40, cmap="inferno")

        plt.colorbar(label="Lyapunov Exponent")

        plt.title("Lyapunov Stability Spectrum")

        plt.xlabel("X")
        plt.ylabel("Y")

        plt.show()
