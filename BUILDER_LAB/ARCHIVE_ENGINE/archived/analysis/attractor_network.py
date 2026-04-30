import matplotlib.pyplot as plt
import networkx as nx


class AttractorNetwork:
    """
    Build a directed network of state transitions
    under the learned RL policy.
    """

    def __init__(self, env, agent, max_steps=10):

        self.env = env
        self.agent = agent
        self.max_steps = max_steps

    def compute(self):

        edges = []

        for state in self.env.states:

            self.env.reset(state)

            current = state

            for _ in range(self.max_steps):

                actions = self.env.actions

                action = max(
                    actions,
                    key=lambda a: self.agent.q[current][a]
                )

                next_state, reward, done, info = self.env.step(action)

                edges.append((current, next_state))

                current = next_state

                if done:
                    break

        return edges

    def plot(self, edges):

        G = nx.DiGraph()

        G.add_edges_from(edges)

        plt.figure(figsize=(8,6))

        pos = nx.spring_layout(G, seed=42)

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=2000,
            node_color="lightblue",
            font_size=9,
            arrows=True
        )

        plt.title("NEXAH Attractor Network")

        plt.show()
