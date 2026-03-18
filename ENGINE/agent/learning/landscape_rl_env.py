import numpy as np


class LandscapeRLEnv:
    """
    Reinforcement Learning environment operating on
    a generated stability landscape.

    State = position (x,y)
    Reward = stability value at that position
    """

    def __init__(self, X, Y, Z, step_size=0.2):

        self.X = X
        self.Y = Y
        self.Z = Z

        self.step_size = step_size

        self.x_min = X.min()
        self.x_max = X.max()

        self.y_min = Y.min()
        self.y_max = Y.max()

        self.position = None

        self.actions = [
            "up",
            "down",
            "left",
            "right"
        ]

    def reset(self, start=None):

        if start is None:

            x = np.random.uniform(self.x_min, self.x_max)
            y = np.random.uniform(self.y_min, self.y_max)

        else:

            x, y = start

        self.position = np.array([x, y])

        return self.position

    def step(self, action):

        x, y = self.position

        if action == "up":
            y += self.step_size

        elif action == "down":
            y -= self.step_size

        elif action == "left":
            x -= self.step_size

        elif action == "right":
            x += self.step_size

        x = np.clip(x, self.x_min, self.x_max)
        y = np.clip(y, self.y_min, self.y_max)

        self.position = np.array([x, y])

        reward = self._stability(x, y)

        done = reward > np.percentile(self.Z, 95)

        return self.position, reward, done, {}

    def _stability(self, x, y):

        ix = (np.abs(self.X[0] - x)).argmin()
        iy = (np.abs(self.Y[:,0] - y)).argmin()

        return self.Z[iy, ix]
