# tools/system_evolver_population.py

import sys
import os
import json
import random
import copy
import tempfile

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_analyzer import analyze_system


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


# ------------------------------
# utilities
# ------------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_temp_system(data):
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(data, tmp, indent=2)
    tmp.close()
    return tmp.name


def score_system(data):
    temp_path = write_temp_system(data)

    try:
        report = analyze_system(temp_path)
        return report["resilience_score"]
    finally:
        os.remove(temp_path)


def normalize_transitions(data):

    transitions = data.get("transitions", {})
    normalized = {}

    for state, targets in transitions.items():

        if isinstance(targets, list):
            normalized[state] = list(targets)
        else:
            normalized[state] = [targets]

    data["transitions"] = normalized
    return data


def rebuild_edges(data):

    edges = []

    for s, targets in data["transitions"].items():
        for t in targets:
            edges.append([s, t])

    data["edges"] = edges

    return data


# ------------------------------
# mutation operators
# ------------------------------

def mutate_add_edge(data):

    nodes = data["nodes"]

    s = random.choice(nodes)
    t = random.choice(nodes)

    if s == t:
        return data

    if t not in data["transitions"].get(s, []):
        data["transitions"].setdefault(s, []).append(t)

    return rebuild_edges(data)


def mutate_remove_edge(data):

    all_edges = []

    for s, targets in data["transitions"].items():
        for t in targets:
            all_edges.append((s, t))

    if not all_edges:
        return data

    s, t = random.choice(all_edges)

    if len(data["transitions"].get(s, [])) <= 1:
        return data

    data["transitions"][s] = [
        x for x in data["transitions"][s] if x != t
    ]

    return rebuild_edges(data)


def mutate_redirect_edge(data):

    nodes = data["nodes"]

    s = random.choice(nodes)

    if s not in data["transitions"]:
        return data

    if not data["transitions"][s]:
        return data

    old = random.choice(data["transitions"][s])
    new = random.choice(nodes)

    if new == s:
        return data

    data["transitions"][s] = [
        new if x == old else x for x in data["transitions"][s]
    ]

    return rebuild_edges(data)


def mutate(data):

    op = random.choice([
        mutate_add_edge,
        mutate_remove_edge,
        mutate_redirect_edge
    ])

    return op(copy.deepcopy(data))


# ------------------------------
# evolutionary algorithm
# ------------------------------

def evolve_population(
    system_path,
    population_size=30,
    generations=200,
    elite_size=5
):

    base = load_json(system_path)
    base = normalize_transitions(base)
    base = rebuild_edges(base)

    population = [copy.deepcopy(base) for _ in range(population_size)]

    best_score = -1
    best_system = None

    for g in range(generations):

        scored = []

        for system in population:

            try:
                score = score_system(system)
            except Exception:
                score = 0

            scored.append((score, system))

            if score > best_score:
                best_score = score
                best_system = copy.deepcopy(system)

        scored.sort(key=lambda x: x[0], reverse=True)

        elites = [copy.deepcopy(s) for _, s in scored[:elite_size]]

        print(f"generation={g} best_score={best_score:.3f}")

        new_population = elites.copy()

        while len(new_population) < population_size:

            parent = random.choice(elites)
            child = mutate(parent)

            new_population.append(child)

        population = new_population

    return best_system, best_score


# ------------------------------
# main
# ------------------------------

if __name__ == "__main__":

    best_system, best_score = evolve_population(
        SYSTEM_PATH,
        population_size=30,
        generations=300,
        elite_size=5
    )

    print("\nBest system score:", round(best_score, 3))

    output = "APPLICATIONS/examples/energy_grid_population_evolved.json"

    with open(output, "w") as f:
        json.dump(best_system, f, indent=2)

    print("Saved best system to:")
    print(output)
