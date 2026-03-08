# tools/resilience_universe_search.py

import sys
import os
import json
import random
import tempfile
import copy

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_analyzer import analyze_system


BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"
OUTPUT_PATH = "APPLICATIONS/examples/universe_best_system.json"


# --------------------------------------------------
# IO
# --------------------------------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def write_temp(data):

    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)

    json.dump(data, tmp, indent=2)

    tmp.close()

    return tmp.name


# --------------------------------------------------
# scoring
# --------------------------------------------------

def score_system(data):

    temp = write_temp(data)

    try:

        report = analyze_system(temp)

        return report["resilience_score"]

    finally:

        os.remove(temp)


# --------------------------------------------------
# graph helpers
# --------------------------------------------------

def rebuild_edges(data):

    edges = []

    for s, targets in data["transitions"].items():

        if isinstance(targets, list):

            for t in targets:
                edges.append([s, t])

        else:

            edges.append([s, targets])

    data["edges"] = edges

    return data


# --------------------------------------------------
# random architecture generator
# --------------------------------------------------

def random_architecture(base):

    nodes = base["nodes"]

    data = copy.deepcopy(base)

    data["transitions"] = {}

    for n in nodes:

        targets = []

        # random number of edges
        k = random.randint(1, len(nodes))

        for _ in range(k):

            t = random.choice(nodes)

            if t != n and t not in targets:
                targets.append(t)

        data["transitions"][n] = targets

    return rebuild_edges(data)


# --------------------------------------------------
# universe search
# --------------------------------------------------

def universe_search(base_system, trials=2000):

    base = load_json(base_system)

    best_score = -1
    best_system = None

    for i in range(trials):

        candidate = random_architecture(base)

        try:

            score = score_system(candidate)

        except Exception:

            score = 0

        if score > best_score:

            best_score = score
            best_system = candidate

            print(f"new best system at trial {i}: score={score:.3f}")

    return best_system, best_score


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    best, score = universe_search(BASE_SYSTEM, trials=2000)

    print("\nBest system score:", score)

    save_json(OUTPUT_PATH, best)

    print("\nSaved to:")
    print(OUTPUT_PATH)
