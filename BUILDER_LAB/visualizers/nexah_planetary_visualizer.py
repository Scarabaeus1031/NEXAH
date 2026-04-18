# ==========================================================
# NEXAH PLANETARY VISUALIZER
# Map + Network plot + cascade frames (optional)
# ==========================================================

import os
import json
import argparse

import networkx as nx
import matplotlib.pyplot as plt

from nexah_planetary_engine import load_network, build_graph, cascade_simulation


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
VIS_DIR = os.path.join(BASE_DIR, "visuals")
DEFAULT_DATA = os.path.join(DATA_DIR, "planetary_network.json")

os.makedirs(VIS_DIR, exist_ok=True)


def draw_network(G: nx.DiGraph, failed: set, title: str, outpath: str = None):
    plt.figure(figsize=(12, 6))
    pos = nx.spring_layout(G, seed=42)

    colors = []
    for n in G.nodes():
        colors.append("red" if n in failed else "lightblue")

    nx.draw(
        G, pos,
        with_labels=True,
        labels={n: G.nodes[n].get("label", n) for n in G.nodes()},
        node_color=colors,
        node_size=2200,
        arrows=True
    )
    plt.title(title)

    if outpath:
        plt.savefig(outpath, dpi=160, bbox_inches="tight")
        print("Saved:", outpath)
        plt.close()
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="NEXAH Planetary Visualizer")
    parser.add_argument("--data", default=DEFAULT_DATA)
    parser.add_argument("--start", nargs="+", required=True)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--save_frames", action="store_true", help="Save step-by-step PNG frames")

    args = parser.parse_args()

    _, nodes, edges = load_network(args.data)
    G = build_graph(nodes, edges)

    history = cascade_simulation(G, set(args.start), steps=args.steps)

    for i, failed in enumerate(history):
        title = f"NEXAH Planetary Cascade — step {i} (failed={len(failed)})"
        out = None
        if args.save_frames:
            out = os.path.join(VIS_DIR, f"planetary_frame_{i}.png")
        draw_network(G, failed, title, outpath=out)


if __name__ == "__main__":
    main()
