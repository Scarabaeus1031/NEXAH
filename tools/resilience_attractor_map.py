# tools/resilience_attractor_map.py

import json
import random


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_evolved.json"


def load_json(path):
    with open(path,"r") as f:
        return json.load(f)


def step(state, transitions):

    targets = transitions.get(state)

    if targets is None:
        return None

    if isinstance(targets, list):
        return random.choice(targets)

    return targets


def simulate(start_state, transitions, steps=20):

    state = start_state

    for _ in range(steps):

        nxt = step(state, transitions)

        if nxt is None:
            break

        state = nxt

    return state


def compute_attractors(data, runs=200):

    transitions = data["transitions"]
    nodes = data["nodes"]

    attractor_counts = {}

    for start in nodes:

        results = {}

        for _ in range(runs):

            final = simulate(start, transitions)

            results[final] = results.get(final,0) + 1

        attractor_counts[start] = results

    return attractor_counts


def print_attractors(attractors):

    print("\nResilience Attractor Map")
    print("----------------------------")

    for start, outcomes in attractors.items():

        print(f"\nStart state: {start}")

        for state, count in outcomes.items():

            print(f"  → {state}: {count}")


if __name__ == "__main__":

    data = load_json(SYSTEM_PATH)

    attractors = compute_attractors(data)

    print_attractors(attractors)
