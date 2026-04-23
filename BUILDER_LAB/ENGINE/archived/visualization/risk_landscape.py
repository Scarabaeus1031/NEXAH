import matplotlib.pyplot as plt
import networkx as nx


class RiskLandscape:
    """
    Visualizes the system state graph with risk levels and regimes.
    """

    def __init__(self, graph, risk_map, regimes):
        self.graph = graph
        self.risk_map = risk_map
        self.regimes = regimes

    def build_networkx_graph(self):
        """
        Convert StateGraph to NetworkX graph.
        """

        G = nx.DiGraph()

        for node in self.graph.nodes:
            G.add_node(node)

        for source in self.graph.nodes:
            for target in self.graph.neighbors(source):
                G.add_edge(source, target)

        return G

    def regime_color(self, node):
        """
        Assign color based on regime.
        """

        if node in self.regimes.get("stable", []):
            return "green"

        if node in self.regimes.get("stress", []):
            return "orange"

        if node in self.regimes.get("failure", []):
            return "red"

        return "gray"

    def plot(self, path=None):
        """
        Plot the risk landscape.
        """

        G = self.build_networkx_graph()

        pos = nx.spring_layout(G, seed=42)

        colors = [self.regime_color(node) for node in G.nodes]

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=colors,
            node_size=2000,
            font_size=10,
            font_weight="bold",
            arrows=True,
        )

        if path:

            edges = list(zip(path[:-1], path[1:]))

            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=edges,
                edge_color="blue",
                width=3,
            )

        plt.title("NEXAH Risk Landscape")
        plt.show()
