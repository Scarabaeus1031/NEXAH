import matplotlib.pyplot as plt


class GlobalStabilityAtlas:
    """
    Computes the global stability atlas of the system.

    For every start state, follow the learned RL policy
    and determine where the system converges.
    """

    def __init__(self, env, agent, max_steps=20):
        self.env = env
        self.agent = agent
        self.max_steps = max_steps

    def compute(self):

        atlas = {}

        for state in self.env.states:

            self.env.reset(state)

            current = state
            trajectory = [current]

            for _ in range(self.max_steps):

                actions = self.env.actions

                # greedy action from Q-table
                action = max(
                    actions,
                    key=lambda a: self.agent.q[current][a]
                )

                next_state, reward, done, info = self.env.step(action)

                trajectory.append(next_state)

                current = next_state

                if done:
                    break

            atlas[state] = trajectory

        return atlas

    def print_report(self, atlas):

        print("\nGLOBAL STABILITY ATLAS\n")
        print("----------------------------------------")

        for start, traj in atlas.items():

            end = traj[-1]

            print(f"{start:20} → {end}")

    def plot(self, atlas):

        fig, ax = plt.subplots(figsize=(10,6))

        starts = list(atlas.keys())
        ends = [atlas[s][-1] for s in starts]

        ax.scatter(range(len(starts)), [0]*len(starts), s=150)

        for i, s in enumerate(starts):

            ax.text(i,0,s)

            ax.annotate(
                ends[i],
                (i,0),
                (i,0.3),
                arrowprops=dict(arrowstyle="->")
            )

        ax.set_title("NEXAH Global Stability Atlas")
        ax.set_yticks([])
        ax.set_xlabel("Start States")

        plt.show()
