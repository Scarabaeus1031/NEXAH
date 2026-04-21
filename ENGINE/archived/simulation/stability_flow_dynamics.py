import numpy as np

class StabilityFlowDynamics:

    def __init__(self, X, Y, Z, dt=0.05, steps=200, ascent=True):

        self.X = X
        self.Y = Y
        self.Z = Z
        self.dt = dt
        self.steps = steps
        self.ascent = ascent

        dy, dx = np.gradient(Z)

        self.dx = dx
        self.dy = dy

    def _grad(self, x, y):

        ix = np.argmin(np.abs(self.X[0] - x))
        iy = np.argmin(np.abs(self.Y[:,0] - y))

        return self.dx[iy,ix], self.dy[iy,ix]

    def simulate(self, start):

        x,y = start

        traj = [(x,y)]

        s = 1 if self.ascent else -1

        for _ in range(self.steps):

            gx,gy = self._grad(x,y)

            x += s*self.dt*gx
            y += s*self.dt*gy

            traj.append((x,y))

        return np.array(traj)

    def simulate_many(self, starts):

        return [self.simulate(s) for s in starts]
