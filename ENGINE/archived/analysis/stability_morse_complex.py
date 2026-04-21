import numpy as np
import matplotlib.pyplot as plt


class StabilityMorseComplex:
    """
    Morse complex of the stability landscape.

    Uses gradient flow to approximate separatrices
    between critical points.
    """

    def __init__(self, X, Y, Z, maxima, minima, saddles):

        self.X = X
        self.Y = Y
        self.Z = Z

        self.maxima = maxima
        self.minima = minima
        self.saddles = saddles

    # --------------------------------------------------
    # gradient
    # --------------------------------------------------

    def compute_gradient(self):

        dZ_dy, dZ_dx = np.gradient(self.Z)

        return dZ_dx, dZ_dy

    # --------------------------------------------------
    # gradient descent / ascent
    # --------------------------------------------------

    def integrate_flow(self, start, step=0.1, steps=200):

        dZ_dx, dZ_dy = self.compute_gradient()

        x = start[0]
        y = start[1]

        traj = []

        for _ in range(steps):

            ix = np.argmin(np.abs(self.X[0] - x))
            iy = np.argmin(np.abs(self.Y[:,0] - y))

            gx = dZ_dx[iy, ix]
            gy = dZ_dy[iy, ix]

            x = x + step * gx
            y = y + step * gy

            traj.append((x,y))

        return np.array(traj)

    # --------------------------------------------------
    # compute separatrices
    # --------------------------------------------------

    def compute(self):

        separatrices = []

        for saddle in self.saddles:

            traj = self.integrate_flow(saddle)

            separatrices.append(traj)

        return separatrices

    # --------------------------------------------------
    # plotting
    # --------------------------------------------------

    def plot(self):

        separatrices = self.compute()

        plt.figure(figsize=(8,6))

        plt.contourf(
            self.X,
            self.Y,
            self.Z,
            levels=40,
            cmap="viridis"
        )

        # separatrices
        for s in separatrices:

            plt.plot(
                s[:,0],
                s[:,1],
                color="white",
                linewidth=1.5
            )

        # critical points

        if len(self.maxima) > 0:
            xm, ym = zip(*self.maxima)
            plt.scatter(xm, ym, color="red", label="Maxima", s=80)

        if len(self.minima) > 0:
            xm, ym = zip(*self.minima)
            plt.scatter(xm, ym, color="blue", label="Minima", s=80)

        if len(self.saddles) > 0:
            xm, ym = zip(*self.saddles)
            plt.scatter(xm, ym, color="white", label="Saddles", s=80)

        plt.title("Stability Morse Complex")

        plt.xlabel("Axis X")
        plt.ylabel("Axis Y")

        plt.legend()

        plt.show()
