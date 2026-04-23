import numpy as np
import matplotlib.pyplot as plt


class StabilityTransitionPaths:
    """
    Compute approximate transition paths between attractors.

    Uses gradient descent / ascent along the stability surface
    to approximate minimum-energy transition routes.
    """

    def __init__(self, X, Y, Z, dt=0.05, steps=200):

        self.X = X
        self.Y = Y
        self.Z = Z

        self.dt = dt
        self.steps = steps

        gy, gx = np.gradient(Z)

        self.gx = gx
        self.gy = gy

    def _grad(self, x, y):

        ix = np.argmin(np.abs(self.X[0] - x))
        iy = np.argmin(np.abs(self.Y[:,0] - y))

        return self.gx[iy,ix], self.gy[iy,ix]

    def compute_path(self, start, target):

        x,y = start
        tx,ty = target

        traj = [(x,y)]

        for _ in range(self.steps):

            gx,gy = self._grad(x,y)

            dx = tx-x
            dy = ty-y

            x += self.dt*(dx + 0.3*gx)
            y += self.dt*(dy + 0.3*gy)

            traj.append((x,y))

            if np.linalg.norm([x-tx,y-ty]) < 0.05:
                break

        return np.array(traj)

    def compute_network(self, attractors):

        paths = []

        for i in range(len(attractors)):
            for j in range(i+1,len(attractors)):

                path = self.compute_path(attractors[i],attractors[j])

                paths.append(path)

        return paths

    def plot(self, attractors, paths):

        plt.figure(figsize=(8,6))

        plt.contourf(self.X,self.Y,self.Z,40,cmap="viridis")

        for p in paths:
            plt.plot(p[:,0],p[:,1],linewidth=2,color="white")

        plt.scatter(
            attractors[:,0],
            attractors[:,1],
            color="red",
            s=80
        )

        plt.title("Stability Transition Paths")

        plt.colorbar()

        plt.show()
