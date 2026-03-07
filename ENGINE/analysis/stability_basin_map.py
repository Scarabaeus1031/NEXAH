import matplotlib.pyplot as plt
import numpy as np


class StabilityBasinMap:
    """
    Analyze basin of attraction for a policy on the stability landscape.
    """

    def __init__(self, env, agent):
        self.env = env
        self.agent = agent

    def simulate(self, start_state, steps=15):
        """
        Run the learned policy from a given start state.
        """

        state = self.env.reset(start_state)

        trajectory = [state]

        for _ in range(steps):

            actions = self.env.available_actions()

            action = max(
                actions,
                key=lambda a: self.agent.q[state][a]
            )

            next_state, reward, done, info = self.env.step(action)

            trajectory.append(next_state)

            state = next_state

            if done:
                break

        return trajectory

    def compute_basins(self, steps=15):
        """
        Run simulation from every start state.
        """

        results = {}

        for state in self.env.states:

            traj = self.simulate(state, steps)

            final_state = traj[-1]

            results[state] = {
                "trajectory": traj,
                "final_state": final_state,
                "final_stability": self.env.risk_map.get(final_state, 0)
            }

        return results

    def print_report(self, results):

        print("\nSTABILITY BASIN MAP\n")
        print("-" * 40)

        for state, data in results.items():

            final = data["final_state"]
            stability = data["final_stability"]

            print(f"{state:20} → {final:20} (stability={stability})")

    def plot(self, results, title="Stability Basin Map"):
        """
        Visualize basin results on the stability landscape.
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

        for start, data in results.items():

            traj = data["trajectory"]

            xs = []
            ys = []
            zs = []

            for s in traj:

                if s in states:
                    idx = states.index(s)

                    xs.append(idx)
                    ys.append(0)
                    zs.append(self.env.risk_map[s])

            ax.plot(xs, ys, zs, linewidth=2)

        ax.set_xlabel("State Index")
        ax.set_ylabel("Basin Axis")
        ax.set_zlabel("Stability")
        ax.set_title(title)

        plt.show()
