# tools/architecture_diff.py

import json
import sys


BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"
NEW_SYSTEM = "APPLICATIONS/examples/energy_grid_evolved.json"


# --------------------------------------------------
# IO
# --------------------------------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


# --------------------------------------------------
# edge extraction
# --------------------------------------------------

def extract_edges(data):

    edges = set()

    transitions = data.get("transitions", {})

    for source, targets in transitions.items():

        if isinstance(targets, list):

            for target in targets:
                edges.add((source, target))

        else:

            edges.add((source, targets))

    return edges


# --------------------------------------------------
# diff
# --------------------------------------------------

def compute_diff(base_edges, new_edges):

    added = new_edges - base_edges
    removed = base_edges - new_edges

    return added, removed


# --------------------------------------------------
# pretty print
# --------------------------------------------------

def print_edges(label, edges):

    print(f"\n{label}")

    if not edges:
        print("  none")
        return

    for s, t in sorted(edges):
        print(f"  {s} -> {t}")


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    base = load_json(BASE_SYSTEM)
    new = load_json(NEW_SYSTEM)

    base_edges = extract_edges(base)
    new_edges = extract_edges(new)

    added, removed = compute_diff(base_edges, new_edges)

    print("\nArchitecture Difference Report")
    print("--------------------------------")

    print_edges("Added edges:", added)
    print_edges("Removed edges:", removed)

    print("\nTotal base edges:", len(base_edges))
    print("Total new edges:", len(new_edges))
