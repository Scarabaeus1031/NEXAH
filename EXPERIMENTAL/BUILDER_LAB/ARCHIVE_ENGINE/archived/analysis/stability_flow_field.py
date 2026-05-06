import numpy as np
import matplotlib.pyplot as plt


class StabilityFlowField:
    """
    Visualize the directional flow of the system dynamics
    under the learned RL policy.
    """

    def __init__(self, env, agent):

        self.env = env
        self.agent = agent

    def compute(self):

        states = self.env.states
        n = len(states)

        X = np.arange(n)
        Y = np.zeros(n)

        U = np.zeros(n)
        V = np.zeros(n)

        for i, state in enumerate(states):

            actions = self.env.actions

            action = max(
                actions,
                key=lambda a: self.agent.q[state][a]
            )

            if (state, action) in self.env.action_effect:

                next_state = self.env.action_effect[(state, action)]

            else:

                next_state = self.env.delta[state]

            j = states.index(next_state)

            U[i] = j - i
            V[i] = 0

        return X, Y, U, V

    def plot(self, X, Y, U, V):

        plt.figure(figsize=(10,4))

        plt.quiver(
            X,
            Y,
            U,
            V,
            angles='xy',
            scale_units='xy',
            scale=1
        )

        for i, s in enumerate(self.env.states):

            plt.text(i,0,s,ha='center',va='bottom')

        plt.yticks([])
        plt.xlabel("System States")
        plt.title("NEXAH Stability Flow Field")

        plt.show()
