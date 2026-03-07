import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx


class DynamicRiskLandscape:
    """
    Animated visualization of NEXAH system navigation.

    Shows movement of the current state through the risk landscape.
    """

    def __init__(self, graph, regimes):
        self.graph = graph
        self.regimes = regimes

    def build_networkx_graph(self):
        """
        Convert StateGraph to NetworkX directed graph.
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
        Assign node color by regime.
        """
        if node in self.regimes.get("stable", []):
            return "green"

        if node in self.regimes.get("stress", []):
            return "orange"

        if node in self.regimes.get("failure", []):
            return "red"

        return "gray"

    def animate(self, path, interval=1000):
        """
        Animate system trajectory along the graph.
        """
        G = self.build_networkx_graph()
        pos = nx.spring_layout(G, seed=42)

        fig, ax = plt.subplots(figsize=(10, 7))

        base_colors = [self.regime_color(node) for node in G.nodes]

        def update(frame):
            ax.clear()

            # draw all nodes and edges
            nx.draw(
                G,
                pos,
                ax=ax,
                with_labels=True,
                node_color=base_colors,
                node_size=2000,
                font_size=10,
                font_weight="bold",
                arrows=True,
            )

            # highlight visited path edges
            if frame > 0:
                edge_path = list(zip(path[:frame], path[1:frame + 1]))
                nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=edge_path,
                    edge_color="blue",
                    width=3,
                    ax=ax,
                )

            # highlight current node
            current = path[frame]
            nx.draw_networkx_nodes(
                G,
                pos,
                nodelist=[current],
                node_color="cyan",
                node_size=2400,
                ax=ax,
            )

            ax.set_title(f"NEXAH Dynamic Risk Landscape\nCurrent State: {current}")

        ani = animation.FuncAnimation(
            fig,
            update,
            frames=len(path),
            interval=interval,
            repeat=False,
        )

        plt.show()
        return ani
