# ==========================================================
# NEXAH PLANETARY ENGINE (Level-2)
# Multi-layer global cascade simulation with dependencies
# ==========================================================

import os
import json
import argparse
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

import networkx as nx


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DEFAULT_DATA = os.path.join(DATA_DIR, "planetary_network.json")


@dataclass
class NodeInfo:
    id: str
    label: str
    layer: str
    lat: float
    lon: float
    criticality: float


def load_network(path: str):
    with open(path, "r") as f:
        data = json.load(f)

    nodes: Dict[str, NodeInfo] = {}
    for n in data["nodes"]:
        nodes[n["id"]] = NodeInfo(
            id=n["id"],
            label=n.get("label", n["id"]),
            layer=n["layer"],
            lat=float(n.get("lat", 0.0)),
            lon=float(n.get("lon", 0.0)),
            criticality=float(n.get("criticality", 0.5)),
        )

    edges = data["edges"]
    return data.get("layers", []), nodes, edges


def build_graph(nodes: Dict[str, NodeInfo], edges: List[dict]) -> nx.DiGraph:
    G = nx.DiGraph()
    for node_id, info in nodes.items():
        G.add_node(node_id, label=info.label, layer=info.layer, lat=info.lat, lon=info.lon, criticality=info.criticality)

    for e in edges:
        G.add_edge(
            e["src"], e["tgt"],
            kind=e.get("kind", "intra"),
            layer=e.get("layer", ""),
            weight=float(e.get("weight", 0.5))
        )
    return G


def cascade_simulation(
    G: nx.DiGraph,
    start_failed: Set[str],
    steps: int = 8,
    dep_threshold: float = 0.75,
    stress_threshold: float = 0.90,
) -> List[Set[str]]:
    """
    Rule-set (simple but meaningful):
    - A dependency edge ("dep") can force failure if the source has failed and weight >= dep_threshold.
    - Intra-layer edges propagate as "stress" accumulation (risk). If accumulated risk >= stress_threshold => failure.
    """
    failed: Set[str] = set(start_failed)
    risk: Dict[str, float] = {n: 0.0 for n in G.nodes()}
    history: List[Set[str]] = [set(failed)]

    for _ in range(steps):
        newly_failed: Set[str] = set()

        # 1) hard dependencies
        for u, v, attrs in G.edges(data=True):
            if attrs.get("kind") != "dep":
                continue
            if u in failed and v not in failed:
                w = float(attrs.get("weight", 0.5))
                if w >= dep_threshold:
                    newly_failed.add(v)

        # 2) stress propagation on intra links
        for u, v, attrs in G.edges(data=True):
            if attrs.get("kind") != "intra":
                continue
            if u in failed and v not in failed:
                w = float(attrs.get("weight", 0.3))
                crit = float(G.nodes[v].get("criticality", 0.5))
                # critical nodes accumulate faster
                risk[v] += w * (0.6 + 0.8 * crit)

        # decide stress failures
        for n in G.nodes():
            if n in failed:
                continue
            if risk[n] >= stress_threshold:
                newly_failed.add(n)

        if not newly_failed:
            history.append(set(failed))
            break

        failed |= newly_failed
        history.append(set(failed))

    return history


def summarize(history: List[Set[str]]):
    for i, failed in enumerate(history):
        print(f"\nSTEP {i}")
        print("FAILED:", sorted(failed))


def main():
    parser = argparse.ArgumentParser(description="NEXAH Planetary Engine (Level-2)")
    parser.add_argument("--data", default=DEFAULT_DATA, help="Path to network JSON")
    parser.add_argument("--start", nargs="+", required=True, help="Initial failed node ids")
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--dep_threshold", type=float, default=0.75)
    parser.add_argument("--stress_threshold", type=float, default=0.90)

    args = parser.parse_args()

    _, nodes, edges = load_network(args.data)
    G = build_graph(nodes, edges)

    unknown = [x for x in args.start if x not in G.nodes()]
    if unknown:
        raise SystemExit(f"Unknown start node(s): {unknown}")

    history = cascade_simulation(
        G,
        start_failed=set(args.start),
        steps=args.steps,
        dep_threshold=args.dep_threshold,
        stress_threshold=args.stress_threshold,
    )
    summarize(history)


if __name__ == "__main__":
    main()
