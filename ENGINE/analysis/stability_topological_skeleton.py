import numpy as np
import matplotlib.pyplot as plt


class StabilityTopologicalSkeleton:
    """
    Extract a topological skeleton of the stability landscape.

    Uses critical points and gradient flow connections
    to approximate the Morse-Smale structure.
    """

    def __init__(self, X, Y, Z, maxima, minima, saddles):

        self.X = X
        self.Y = Y
        self.Z = Z

        self.maxima = np.array(maxima)
        self.minima = np.array(minima)
        self.saddles = np.array(saddles)

        gy, gx = np.gradient(Z)

        self.gx = gx
        self.gy = gy


    def _grad(self, x, y):

        ix = np.argmin(np.abs(self.X[0] - x))
        iy = np.argmin(np.abs(self.Y[:,0] - y))

        return self.gx[iy, ix], self.gy[iy, ix]


    def _follow_flow(self, start, steps=120, dt=0.05):

        x,y = start

        traj=[(x,y)]

        for _ in range(steps):

            gx,gy = self._grad(x,y)

            x += dt*gx
            y += dt*gy

            traj.append((x,y))

        return np.array(traj)


    def compute(self):

        skeleton_paths = []

        for s in self.saddles:

            traj_up = self._follow_flow(s)
            traj_down = self._follow_flow(s, steps=120, dt=-0.05)

            skeleton_paths.append(traj_up)
            skeleton_paths.append(traj_down)

        return skeleton_paths


    def plot(self, paths):

        plt.figure(figsize=(8,6))

        plt.contourf(self.X, self.Y, self.Z, 40, cmap="viridis")

        for p in paths:

            plt.plot(p[:,0], p[:,1], color="white", linewidth=1.5)

        if len(self.maxima)>0:
            plt.scatter(
                self.maxima[:,0],
                self.maxima[:,1],
                color="red",
                s=80,
                label="Maxima"
            )

        if len(self.minima)>0:
            plt.scatter(
                self.minima[:,0],
                self.minima[:,1],
                color="blue",
                s=60,
                label="Minima"
            )

        if len(self.saddles)>0:
            plt.scatter(
                self.saddles[:,0],
                self.saddles[:,1],
                color="white",
                s=60,
                label="Saddles"
            )

        plt.title("Topological Skeleton of Stability Landscape")

        plt.legend()

        plt.colorbar()

        plt.show()
