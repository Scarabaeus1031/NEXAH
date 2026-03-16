import os
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt

# Repository root relative to this script
ROOT_DIR = os.path.abspath("../../")

# Folders to ignore
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

# Architecture layer colors
CORE_LAYERS = {
    "ENGINE": "#3b82f6",
    "FRAMEWORK": "#a855f7",
    "RESEARCH": "#22c55e",
    "APPLICATIONS": "#f97316",
    "BUILDER_LAB": "#eab308",
    "NAVIGATOR": "#64748b"
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

    return "#94a3b8"


def draw_graph(G):

    plt.figure(figsize=(14, 10), facecolor="#0f172a")

    pos = nx.spring_layout(G, k=0.9, seed=42)

    colors = [node_color(n) for n in G.nodes()]

    ax = plt.gca()
    ax.set_facecolor("#0f172a")

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=3200,
        node_color=colors,
        font_size=9,
        font_color="white",
        edge_color="#94a3b8",
        linewidths=1.5
    )

    plt.title(
        "NEXAH Repository Architecture",
        fontsize=20,
        color="white",
        pad=20
    )

    plt.axis("off")

    output_dir = os.path.abspath("../generated")
    os.makedirs(output_dir, exist_ok=True)

    main_output = os.path.join(
        output_dir,
        "NEXAH_REPOSITORY_GRAPH.png"
    )

    timestamp = datetime.now().strftime("%Y%m%d")

    archive_output = os.path.join(
        output_dir,
        f"NEXAH_REPOSITORY_GRAPH_{timestamp}.png"
    )

    plt.savefig(main_output, bbox_inches="tight", facecolor="#0f172a")
    plt.savefig(archive_output, bbox_inches="tight", facecolor="#0f172a")

    plt.close()

    print("Graph updated:", main_output)
    print("Archive saved:", archive_output)


if __name__ == "__main__":

    G = build_graph(ROOT_DIR)

    draw_graph(G)
