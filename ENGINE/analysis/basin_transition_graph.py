import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


class BasinTransitionGraph:
    """
    Build a transition graph between attraction basins.

    Two basins are connected if they touch along the segmentation boundary.
    """

    def __init__(self, basin_map, maxima):
        self.basin_map = basin_map
        self.maxima = maxima

    def compute(self):
        """
        Detect adjacency between basins.
        """

        ny, nx_ = self.basin_map.shape
        edges = set()

        for i in range(ny - 1):
            for j in range(nx_ - 1):

                a = self.basin_map[i, j]
                b = self.basin_map[i + 1, j]
                c = self.basin_map[i, j + 1]

                if a != b:
                    edges.add(tuple(sorted((a, b))))

                if a != c:
                    edges.add(tuple(sorted((a, c))))

        return sorted(edges)

    def plot(self, edges):
        """
        Plot basin transition graph.
        """

        G = nx.Graph()

        for i in range(len(self.maxima)):
            G.add_node(f"M{i}")

        for a, b in edges:
            G.add_edge(f"M{a}", f"M{b}")

        pos = {}

        for i, (x, y) in enumerate(self.maxima):
            pos[f"M{i}"] = (x, y)

        plt.figure(figsize=(9, 7))

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=900,
            node_color="tomato",
            font_color="white",
            edge_color="black",
            width=2
        )

        plt.title("Basin Transition Graph")
        plt.xlabel("Axis X")
        plt.ylabel("Axis Y")

        plt.show()
