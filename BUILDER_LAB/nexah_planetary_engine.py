# ==========================================================
# NEXAH PLANETARY ENGINE
# Load planetary network + run cascade simulation
# ==========================================================

import os
import json
import argparse
import networkx as nx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------
# LOAD NETWORK (JSON)
# Expected format:
# {
#   "layers": {... optional ...},
#   "nodes": [{"id":"SAT_GNSS","label":"Satellites","layer":"SPACE"}, ...],
#   "edges": [{"source":"SAT_GNSS","target":"PORT_RTM","type":"dependency"}, ...]
# }
# ----------------------------------------------------------

def load_network(json_path: str):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Network JSON not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    layers = data.get("layers", {})
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    # allow shorthand formats
    # nodes could be dict: { "SAT_GNSS": {...}, ... }
    if isinstance(nodes, dict):
        nodes = [{"id": k, **v} for k, v in nodes.items()]

    return layers, nodes, edges


# ----------------------------------------------------------
# BUILD GRAPH
# ----------------------------------------------------------

def build_graph(nodes, edges):
    G = nx.DiGraph()

    for n in nodes:
        node_id = n.get("id") or n.get("name")
        if not node_id:
            continue
        G.add_node(
            node_id,
            label=n.get("label", node_id),
            layer=n.get("layer", "UNKNOWN"),
            meta={k: v for k, v in n.items() if k not in ("id", "name", "label", "layer")}
        )

    for e in edges:
        src = e.get("source") or e.get("src")
        tgt = e.get("target") or e.get("tgt")
        if not src or not tgt:
            continue
        G.add_edge(src, tgt, **{k: v for k, v in e.items() if k not in ("source", "target", "src", "tgt")})

    return G


# ----------------------------------------------------------
# CASCADE SIMULATION
# Rule: if a node fails, all outgoing dependents fail next step.
# (You can later add probabilities / weights / thresholds.)
# ----------------------------------------------------------

def cascade_simulation(G: nx.DiGraph, start_failed: set, steps: int = 8):
    failed = set(start_failed)
    history = [set(failed)]

    for _ in range(steps):
        next_failed = set(failed)
        # propagate along outgoing edges
        for f in failed:
            if f in G:
                for dep in G.successors(f):
                    next_failed.add(dep)

        failed = next_failed
        history.append(set(failed))

    return history


# ----------------------------------------------------------
# CLI
# ----------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="NEXAH Planetary Cascade Engine")
    parser.add_argument("--data", default=os.path.join(BASE_DIR, "data", "planetary_network.json"))
    parser.add_argument("--start", required=True, help="Start failed node id (e.g. SAT_GNSS)")
    parser.add_argument("--steps", type=int, default=8)

    args = parser.parse_args()

    _, nodes, edges = load_network(args.data)
    G = build_graph(nodes, edges)

    hist = cascade_simulation(G, start_failed={args.start}, steps=args.steps)

    for i, failed in enumerate(hist):
        print(f"\nSTEP {i}")
        print("FAILED:", sorted(list(failed)))


if __name__ == "__main__":
    main()
