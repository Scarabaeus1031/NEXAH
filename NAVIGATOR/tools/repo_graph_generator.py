import os
import networkx as nx
import matplotlib.pyplot as plt

ROOT_DIR = "../../"

IGNORE = {".git", "__pycache__", ".mypy_cache"}

def build_graph(root):
    G = nx.DiGraph()

    for dirpath, dirnames, filenames in os.walk(root):

        # ignore unwanted folders
        dirnames[:] = [d for d in dirnames if d not in IGNORE]

        parent = os.path.relpath(dirpath, root)

        for d in dirnames:
            child = os.path.join(parent, d)
            G.add_edge(parent, child)

    return G


def draw_graph(G):

    plt.figure(figsize=(14,10))

    pos = nx.spring_layout(G, k=0.8)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=3000,
        node_color="#2b6cb0",
        font_size=9,
        font_color="white",
        edge_color="#888"
    )

    plt.title("NEXAH Repository Structure", fontsize=18)

    output = "../generated/NEXAH_REPOSITORY_GRAPH.png"
    plt.savefig(output, bbox_inches="tight")
    print("Graph saved to:", output)


if __name__ == "__main__":

    G = build_graph(ROOT_DIR)

    draw_graph(G)
