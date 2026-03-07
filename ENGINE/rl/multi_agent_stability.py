import matplotlib.pyplot as plt
import numpy as np


class MultiAgentStability:
    """
    Simulate multiple agents acting on the same stability environment.
    """

    def __init__(self, env, agents):
        """
        agents = dict(name -> agent_object)
        """
        self.env = env
        self.agents = agents

    def run(self, start_state, steps=10):
        """
        Run each agent from the same start state.
        """

        trajectories = {}

        for name, agent in self.agents.items():

            state = self.env.reset(start_state)

            traj = [state]

            for _ in range(steps):

                # choose action
                if hasattr(agent, "choose_action"):
                    action = agent.choose_action(state)
                elif hasattr(agent, "run_policy"):
                    # deterministic learned policy
                    action = max(
                        self.env.available_actions(),
                        key=lambda a: agent.q[state][a]
                    )
                else:
                    action = self.env.sample_action()

                next_state, reward, done, info = self.env.step(action)

                traj.append(next_state)

                state = next_state

                if done:
                    break

            trajectories[name] = traj

        return trajectories

    def plot(self, trajectories, title="Multi-Agent Stability Trajectories"):
        """
        Plot all agent trajectories on the stability landscape.
        """

        states = list(self.env.risk_map.keys())
        values = [self.env.risk_map[s] for s in states]

        x = np.arange(len(states))
        y = np.zeros(len(states))
        z = np.array(values)

        fig = plt.figure(figsize=(12, 7))
        ax = fig.add_subplot(111, projection="3d")

        ax.plot(x, y, z, linewidth=2)
        ax.scatter(x, y, z, s=200)

        for i, s in enumerate(states):
            ax.text(x[i], y[i], z[i], s, fontsize=9)

        colors = ["red", "green", "orange", "purple"]

        for idx, (name, traj) in enumerate(trajectories.items()):

            xs = []
            ys = []
            zs = []

            for s in traj:

                if s in states:
                    i = states.index(s)

                    xs.append(i)
                    ys.append(0)
                    zs.append(self.env.risk_map[s])

            ax.plot(
                xs,
                ys,
                zs,
                linewidth=3,
                label=name,
                color=colors[idx % len(colors)]
            )

        ax.set_xlabel("State Index")
        ax.set_ylabel("Agent Axis")
        ax.set_zlabel("Stability")
        ax.set_title(title)

        ax.legend()

        plt.show()
