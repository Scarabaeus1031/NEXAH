# ==========================================================
# NEXAH GLOBAL CASCADE SIMULATOR
# Simulate cascading failures across global systems
# ==========================================================

import os
import json
import networkx as nx
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_FILE = os.path.join(BASE_DIR, "global_systems", "global_system_map.json")


# ----------------------------------------------------------
# LOAD MAP
# ----------------------------------------------------------

def load_map():

    with open(MAP_FILE) as f:
        return json.load(f)


# ----------------------------------------------------------
# BUILD GRAPH
# ----------------------------------------------------------

def build_graph(data):

    G = nx.DiGraph()

    for s in data["systems"]:
        G.add_node(s)

    for src, tgt in data["couplings"]:
        G.add_edge(src, tgt)

    return G


# ----------------------------------------------------------
# CASCADE SIMULATION
# ----------------------------------------------------------

def simulate_cascade(G, start_system):

    failed = set([start_system])

    step = 0

    print("\n====================================")
    print("NEXAH GLOBAL CASCADE SIMULATION")
    print("====================================\n")

    while True:

        new_failures = set()

        for system in failed:

            for neighbor in G.successors(system):

                if neighbor not in failed:
                    new_failures.add(neighbor)

        if not new_failures:
            break

        step += 1

        print(f"STEP {step}")

        for s in new_failures:
            print(" →", s, "fails")

        print()

        failed.update(new_failures)

    print("FINAL FAILED SYSTEMS:\n")

    for s in failed:
        print(" •", s)


# ----------------------------------------------------------
# CLI
# ----------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="NEXAH Global Cascade Simulator"
    )

    parser.add_argument(
        "--start",
        help="System that initially fails"
    )

    args = parser.parse_args()

    data = load_map()

    G = build_graph(data)

    simulate_cascade(G, args.start)
