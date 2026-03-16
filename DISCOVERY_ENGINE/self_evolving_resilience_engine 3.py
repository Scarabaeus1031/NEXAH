# tools/self_evolving_resilience_engine.py

import sys
import os
import json
import copy
import random
import tempfile

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_analyzer import analyze_system


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"
OUTPUT_PATH = "APPLICATIONS/examples/energy_grid_evolved.json"


# --------------------------------------------------
# IO
# --------------------------------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# --------------------------------------------------
# scoring
# --------------------------------------------------

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


# --------------------------------------------------
# graph helpers
# --------------------------------------------------

def rebuild_edges(data):

    edges = []

    for s, targets in data["transitions"].items():
        for t in targets:
            edges.append([s, t])

    data["edges"] = edges

    return data


# --------------------------------------------------
# mutations
# --------------------------------------------------

def add_random_edge(data):

    nodes = data["nodes"]

    s = random.choice(nodes)
    t = random.choice(nodes)

    if s != t and t not in data["transitions"].get(s, []):

        data["transitions"].setdefault(s, []).append(t)

    return rebuild_edges(data)


def remove_random_edge(data):

    edges = []

    for s, targets in data["transitions"].items():
        for t in targets:
            edges.append((s, t))

    if not edges:
        return data

    s, t = random.choice(edges)

    if len(data["transitions"][s]) <= 1:
        return data

    data["transitions"][s] = [x for x in data["transitions"][s] if x != t]

    return rebuild_edges(data)


def redirect_edge(data):

    edges = []

    for s, targets in data["transitions"].items():
        for t in targets:
            edges.append((s, t))

    if not edges:
        return data

    s, t = random.choice(edges)

    nodes = data["nodes"]

    new_target = random.choice(nodes)

    if new_target == s:
        return data

    data["transitions"][s] = [x for x in data["transitions"][s] if x != t]
    data["transitions"][s].append(new_target)

    return rebuild_edges(data)


def mutate_system(data):

    data = copy.deepcopy(data)

    mutation = random.choice(["add", "remove", "redirect"])

    if mutation == "add":
        return add_random_edge(data)

    if mutation == "remove":
        return remove_random_edge(data)

    if mutation == "redirect":
        return redirect_edge(data)

    return data


# --------------------------------------------------
# evolution engine
# --------------------------------------------------

def evolve_system(system_path, generations=30, population_size=20):

    base = load_json(system_path)

    population = [copy.deepcopy(base) for _ in range(population_size)]

    best_system = copy.deepcopy(base)
    best_score = score_system(best_system)

    print("\nInitial score:", best_score)

    for g in range(generations):

        print(f"\nGeneration {g}")

        scored_population = []

        for system in population:

            mutated = mutate_system(system)

            try:

                score = score_system(mutated)

            except Exception:

                continue

            scored_population.append((score, mutated))

            if score > best_score:

                best_score = score
                best_system = copy.deepcopy(mutated)

                print("New best score:", best_score)

        # select best half
        scored_population.sort(key=lambda x: x[0], reverse=True)

        survivors = [x[1] for x in scored_population[: population_size // 2]]

        # reproduce
        new_population = []

        while len(new_population) < population_size:

            parent = random.choice(survivors)

            child = mutate_system(parent)

            new_population.append(child)

        population = new_population

    return best_system, best_score


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    best, score = evolve_system(SYSTEM_PATH)

    print("\nFinal best score:", score)

    save_json(OUTPUT_PATH, best)

    print("\nSaved evolved system to:")
    print(OUTPUT_PATH)
