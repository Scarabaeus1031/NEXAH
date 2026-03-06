import os
import networkx as nx
import matplotlib.pyplot as plt

ROOT_DIR = "../../"

# folders that should not appear in the architecture map
IGNORE = {
".git",
".github",
".pytest_cache",
"__pycache__",
".mypy_cache",
"visuals",
"generated",
"tools",
"tests"
}

# main architecture layers
CORE_LAYERS = {
"ENGINE": "#2b6cb0",
"FRAMEWORK": "#6b46c1",
"RESEARCH": "#2f855a",
"APPLICATIONS": "#dd6b20",
"BUILDER_LAB": "#d69e2e",
"NAVIGATOR": "#4a5568"
}


def build_graph(root):

    G = nx.DiGraph()

    for dirpath, dirnames, filenames in os.walk(root):

        dirnames[:] = [d for d in dirnames if d not in IGNORE]

        parent = os.path.relpath(dirpath, root)

        for d in dirnames:

            child = os.path.join(parent, d)

            G.add_edge(parent, child)

    return G


def node_color(node):

    parts = node.split("/")

    for layer in CORE_LAYERS:

        if layer in parts:
            return CORE_LAYERS[layer]

    return "#718096"


def draw_graph(G):

    plt.figure(figsize=(14,10))

    pos = nx.spring_layout(G, k=0.9, seed=42)

    colors = [node_color(n) for n in G.nodes()]

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2800,
        node_color=colors,
        font_size=9,
        font_color="white",
        edge_color="#a0aec0"
    )

    plt.title("NEXAH Repository Architecture", fontsize=18)

    os.makedirs("../generated", exist_ok=True)

    output = "../generated/NEXAH_REPOSITORY_GRAPH.png"

    plt.savefig(output, bbox_inches="tight")

    print("Graph saved to:", output)


if __name__ == "__main__":

    G = build_graph(ROOT_DIR)

    draw_graph(G)
