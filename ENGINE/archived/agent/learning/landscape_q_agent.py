import numpy as np


class LandscapeQAgent:
    """
    Q-Learning agent for navigating a stability landscape.
    """

    def __init__(
        self,
        env,
        grid_size=40,
        alpha=0.1,
        gamma=0.95,
        epsilon=0.2
    ):

        self.env = env

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.grid_size = grid_size

        self.actions = env.actions

        self.q = {}

    def _state_key(self, position):
        """
        Discretize continuous position to grid cell.
        """

        x, y = position

        ix = int((x - self.env.x_min) /
                 (self.env.x_max - self.env.x_min) * self.grid_size)

        iy = int((y - self.env.y_min) /
                 (self.env.y_max - self.env.y_min) * self.grid_size)

        return (ix, iy)

    def _get_q(self, state):

        if state not in self.q:
            self.q[state] = np.zeros(len(self.actions))

        return self.q[state]

    def choose_action(self, state):

        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)

        qvals = self._get_q(state)

        return self.actions[np.argmax(qvals)]

    def train(self, episodes=1000, max_steps=100):

        for ep in range(episodes):

            state_pos = self.env.reset()

            state = self._state_key(state_pos)

            for _ in range(max_steps):

                action = self.choose_action(state)

                new_pos, reward, done, _ = self.env.step(action)

                new_state = self._state_key(new_pos)

                qvals = self._get_q(state)
                qnext = self._get_q(new_state)

                a_idx = self.actions.index(action)

                qvals[a_idx] += self.alpha * (
                    reward + self.gamma * np.max(qnext) - qvals[a_idx]
                )

                state = new_state

                if done:
                    break

    def run(self, start=None, steps=50):

        pos = self.env.reset(start)

        trajectory = [pos]

        state = self._state_key(pos)

        for _ in range(steps):

            qvals = self._get_q(state)

            action = self.actions[np.argmax(qvals)]

            pos, reward, done, _ = self.env.step(action)

            trajectory.append(pos)

            state = self._state_key(pos)

            if done:
                break

        return np.array(trajectory)
