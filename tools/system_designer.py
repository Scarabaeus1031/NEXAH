# tools/system_designer.py

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import networkx as nx
import copy

from tools.resilience_analyzer import analyze_system
from FRAMEWORK.core.system_loader import load_system
from ENGINE.runtime.system_runner import build_regime_map


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


def suggest_improvements():

    system = load_system(SYSTEM_PATH)

    regime_map = build_regime_map(system)

    graph = regime_map["graph"]

    collapse_states = set(regime_map["collapse_states"])

    suggestions = []

    for u, v in graph.edges():

        if v in collapse_states:

            suggestions.append(
                f"Consider removing transition: {u} -> {v}"
            )

    for node in graph.nodes():

        successors = list(graph.successors(node))

        if len(successors) == 1:

            suggestions.append(
                f"Add alternative recovery path from: {node}"
            )

    return suggestions


def print_suggestions():

    print("\nNEXAH System Design Suggestions")
    print("--------------------------------")

    suggestions = suggest_improvements()

    if not suggestions:
        print("System already robust.")
        return

    for s in suggestions:
        print("-", s)


if __name__ == "__main__":

    report = analyze_system(SYSTEM_PATH)

    print_suggestions()

    print("\nCurrent Resilience Score:", report["resilience_score"])
