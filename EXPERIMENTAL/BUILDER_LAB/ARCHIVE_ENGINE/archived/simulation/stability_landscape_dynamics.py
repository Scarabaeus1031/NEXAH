import numpy as np
import matplotlib.pyplot as plt


class StabilityLandscapeDynamics:

    def __init__(self, X, Y, Z):

        self.X = X
        self.Y = Y
        self.Z = Z

    def evolve(self, steps=50):

        history=[]

        Z=self.Z.copy()

        for _ in range(steps):

            noise = np.random.normal(0,0.02,Z.shape)

            gx,gy = np.gradient(Z)

            Z = Z + noise - 0.01*(gx**2+gy**2)

            history.append(Z.copy())

        return history

    def plot(self, Z):

        plt.figure(figsize=(8,6))

        plt.contourf(self.X,self.Y,Z,40,cmap="viridis")

        plt.title("Dynamic Stability Landscape")

        plt.colorbar()

        plt.show()
