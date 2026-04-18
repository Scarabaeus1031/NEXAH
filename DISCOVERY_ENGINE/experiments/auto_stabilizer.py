# tools/auto_stabilizer.py

import sys
import os
import copy

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import networkx as nx

from FRAMEWORK.core.system_loader import load_system
from ENGINE.runtime.system_runner import build_regime_map
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry
from tools.resilience_analyzer import compute_resilience_score


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


def compute_score(graph, collapse_states):

    regime_map = {
        "graph": graph,
        "collapse_states": collapse_states
    }

    risk_geometry = compute_risk_geometry(regime_map)

    catastrophe_info = {
        "collapse_states": set(collapse_states),
        "critical_states": set(),
        "safe_states": set(graph.nodes())
    }

    score = compute_resilience_score(
        graph,
        risk_geometry,
        catastrophe_info
    )

    return score


def test_edge_removals(graph, collapse_states):

    best_score = -1
    best_change = None

    base_score = compute_score(graph, collapse_states)

    for u, v in list(graph.edges()):

        if v in collapse_states:

            g2 = copy.deepcopy(graph)
            g2.remove_edge(u, v)

            score = compute_score(g2, collapse_states)

            if score > best_score:

                best_score = score
                best_change = f"Remove edge {u} -> {v}"

    return base_score, best_score, best_change


def test_edge_additions(graph, collapse_states):

    best_score = -1
    best_change = None

    nodes = list(graph.nodes())

    base_score = compute_score(graph, collapse_states)

    for u in nodes:
        for v in nodes:

            if u == v:
                continue

            if graph.has_edge(u, v):
                continue

            if v in collapse_states:
                continue

            g2 = copy.deepcopy(graph)
            g2.add_edge(u, v)

            score = compute_score(g2, collapse_states)

            if score > best_score:

                best_score = score
                best_change = f"Add edge {u} -> {v}"

    return base_score, best_score, best_change


def auto_stabilize():

    system = load_system(SYSTEM_PATH)

    regime_map = build_regime_map(system)

    graph = regime_map["graph"]

    collapse_states = regime_map["collapse_states"]

    print("\nNEXAH Auto Stabilizer")
    print("----------------------")

    base_score, remove_score, remove_change = test_edge_removals(graph, collapse_states)

    _, add_score, add_change = test_edge_additions(graph, collapse_states)

    print("\nCurrent resilience score:", round(base_score, 3))

    if remove_change:
        print("\nBest edge removal:")
        print(remove_change)
        print("New score:", round(remove_score, 3))

    if add_change:
        print("\nBest edge addition:")
        print(add_change)
        print("New score:", round(add_score, 3))

    if remove_score > add_score:
        print("\nRecommended modification:")
        print(remove_change)
    else:
        print("\nRecommended modification:")
        print(add_change)


if __name__ == "__main__":

    auto_stabilize()
