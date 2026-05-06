import numpy as np
import matplotlib.pyplot as plt


class StabilityFlowDynamics:
    """
    Simulate continuous flow on a stability landscape.

    By default:
        dx/dt = +grad(Z)
        dy/dt = +grad(Z)

    This drives trajectories uphill toward stability peaks.

    Set ascent=False for downhill flow.
    """

    def __init__(self, X, Y, Z, dt=0.05, steps=200, ascent=True):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.dt = dt
        self.steps = steps
        self.ascent = ascent

        dZ_dy, dZ_dx = np.gradient(self.Z)
        self.dZ_dx = dZ_dx
        self.dZ_dy = dZ_dy

        self.x_min = X.min()
        self.x_max = X.max()
        self.y_min = Y.min()
        self.y_max = Y.max()

    def _gradient_at(self, x, y):
        """
        Return gradient at nearest grid point.
        """

        ix = np.argmin(np.abs(self.X[0] - x))
        iy = np.argmin(np.abs(self.Y[:, 0] - y))

        gx = self.dZ_dx[iy, ix]
        gy = self.dZ_dy[iy, ix]

        return gx, gy

    def simulate(self, start):
        """
        Simulate one trajectory from a start point.
        """

        x, y = start
        traj = [(x, y)]

        sign = 1.0 if self.ascent else -1.0

        for _ in range(self.steps):
            gx, gy = self._gradient_at(x, y)

            x = x + sign * self.dt * gx
            y = y + sign * self.dt * gy

            x = np.clip(x, self.x_min, self.x_max)
            y = np.clip(y, self.y_min, self.y_max)

            traj.append((x, y))

        return np.array(traj)

    def simulate_many(self, starts):
        """
        Simulate several trajectories.
        """

        return [self.simulate(start) for start in starts]

    def plot(self, trajectories, title="Stability Flow Dynamics"):
        """
        Plot trajectories on top of the landscape contour.
        """

        plt.figure(figsize=(9, 7))

        plt.contourf(
            self.X,
            self.Y,
            self.Z,
            levels=40,
            cmap="viridis"
        )

        for traj in trajectories:
            plt.plot(
                traj[:, 0],
                traj[:, 1],
                linewidth=2
            )
            plt.scatter(
                traj[0, 0],
                traj[0, 1],
                s=50
            )

        plt.xlabel("Axis X")
        plt.ylabel("Axis Y")
        plt.title(title)
        plt.colorbar(label="Stability")

        plt.show()
