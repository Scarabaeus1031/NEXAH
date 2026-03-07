import numpy as np
import matplotlib.pyplot as plt


class PolicySurfaceLearning:
    """
    Visualize a learned policy over the stability landscape.
    """

    def __init__(self, env, agent):
        self.env = env
        self.agent = agent

    def extract_policy(self):
        """
        Extract best action per state from Q-table.
        """

        policy = {}

        for state in self.env.states:

            actions = self.env.available_actions()

            best_action = max(
                actions,
                key=lambda a: self.agent.q[state][a]
            )

            policy[state] = best_action

        return policy

    def plot_policy_surface(self, title="Learned Policy on Stability Surface"):
        """
        Plot stability surface and overlay policy arrows.
        """

        states = list(self.env.risk_map.keys())
        values = [self.env.risk_map[s] for s in states]

        x = np.arange(len(states))
        y = np.zeros(len(states))
        z = np.array(values)

        fig = plt.figure(figsize=(12,7))
        ax = fig.add_subplot(111, projection="3d")

        ax.plot(x, y, z, linewidth=2)
        ax.scatter(x, y, z, s=200)

        for i, s in enumerate(states):
            ax.text(x[i], y[i], z[i], s, fontsize=9)

        policy = self.extract_policy()

        for i, state in enumerate(states):

            action = policy[state]

            ax.text(
                x[i],
                y[i],
                z[i] + 0.4,
                f"{action}",
                color="red",
                fontsize=8
            )

        ax.set_xlabel("State Index")
        ax.set_ylabel("Policy Axis")
        ax.set_zlabel("Stability Score")
        ax.set_title(title)

        plt.show()

    def print_policy(self):
        """
        Print learned policy.
        """

        policy = self.extract_policy()

        print("\nLEARNED POLICY\n")

        for s, a in policy.items():
            print(f"{s:20} -> {a}")
