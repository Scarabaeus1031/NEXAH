# tools/system_designer.py

import sys
import os
import random

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import networkx as nx

from tools.resilience_analyzer import analyze_system
from FRAMEWORK.core.system_loader import load_system
from ENGINE.runtime.system_runner import build_regime_map

# optional random generator
try:
    from tools.random_architecture_generator import generate_random_architecture
    RANDOM_GENERATOR_AVAILABLE = True
except ImportError:
    RANDOM_GENERATOR_AVAILABLE = False


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


# ------------------------------------------------
# NEXAH ENGINE INTERFACE
# ------------------------------------------------

def generate_architecture(mode="auto"):
    """
    Generate an architecture for the NEXAH engine.

    Modes:
        "reference" → load reference system
        "random" → generate random topology
        "auto" → randomly choose
    """

    if mode == "reference":
        return generate_reference_architecture()

    if mode == "random" and RANDOM_GENERATOR_AVAILABLE:
        return generate_random_architecture()

    if mode == "auto":

        if RANDOM_GENERATOR_AVAILABLE and random.random() < 0.7:
            return generate_random_architecture()

        return generate_reference_architecture()

    # fallback
    return generate_reference_architecture()


def generate_reference_architecture():
    """
    Load the reference energy grid example.
    """

    system = load_system(SYSTEM_PATH)

    regime_map = build_regime_map(system)

    graph = regime_map["graph"]

    architecture = {
        "system": system,
        "graph": graph,
        "regime_map": regime_map,
        "type": "reference_system"
    }

    return architecture


# ------------------------------------------------
# DESIGN IMPROVEMENT LOGIC
# ------------------------------------------------

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


# ------------------------------------------------
# CLI ENTRYPOINT
# ------------------------------------------------

if __name__ == "__main__":

    report = analyze_system(SYSTEM_PATH)

    print_suggestions()

    print("\nCurrent Resilience Score:", report["resilience_score"])
