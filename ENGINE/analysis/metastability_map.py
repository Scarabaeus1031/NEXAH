import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


class MetastabilityMap:
    """
    Estimate metastable transitions between basins.

    Transition cost = stability barrier between basins.
    """

    def __init__(self, X, Y, Z, basin_map, maxima, edges):

        self.X = X
        self.Y = Y
        self.Z = Z

        self.basin_map = basin_map
        self.maxima = maxima
        self.edges = edges

    def compute(self):
        """
        Estimate barrier heights between neighboring basins.
        """

        transitions = {}

        for a, b in self.edges:

            mask_a = self.basin_map == a
            mask_b = self.basin_map == b

            Za = np.max(self.Z[mask_a])
            Zb = np.max(self.Z[mask_b])

            # approximate barrier = difference between peaks
            barrier = abs(Za - Zb)

            transitions[(a, b)] = barrier

        return transitions

    def plot(self, transitions):

        G = nx.Graph()

        for i in range(len(self.maxima)):
            G.add_node(f"M{i}")

        for (a, b), barrier in transitions.items():

            G.add_edge(
                f"M{a}",
                f"M{b}",
                weight=barrier
            )

        pos = {}

        for i, (x, y) in enumerate(self.maxima):
            pos[f"M{i}"] = (x, y)

        weights = [G[u][v]["weight"] for u, v in G.edges()]

        plt.figure(figsize=(9, 7))

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="tomato",
            node_size=900,
            font_color="white",
            edge_color=weights,
            edge_cmap=plt.cm.viridis,
            width=3
        )

        plt.title("Metastability Map (Barrier Strength)")

        plt.show()
