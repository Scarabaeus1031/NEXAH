import sys
import os
import json
import random
import tempfile
import copy
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_architecture_attractor_detector import (
    load_json,
    rebuild_edges,
    edge_density,
    cycle_ratio,
    score_system
)

BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"


# --------------------------------------------------
# mutation
# --------------------------------------------------

def mutate_architecture(base):

    nodes = base["nodes"]

    data = copy.deepcopy(base)
    data["transitions"] = {}

    for n in nodes:

        k = random.randint(1, min(4, len(nodes)))
        targets = random.sample(nodes, k)

        data["transitions"][n] = targets

    return rebuild_edges(data)


# --------------------------------------------------
# evolution
# --------------------------------------------------

def evolve_architectures(system_path,
                         generations=40,
                         population=40,
                         elite=10):

    base = load_json(system_path)

    pop = [mutate_architecture(base) for _ in range(population)]

    best_global = None
    best_score = -1

    for g in range(generations):

        scored = []

        for p in pop:

            try:
                s = score_system(p)
            except:
                s = 0

            scored.append((s, p))

            if s > best_score:
                best_score = s
                best_global = p

        scored.sort(reverse=True, key=lambda x: x[0])

        elites = [p for (_, p) in scored[:elite]]

        print(
            f"generation {g} best={scored[0][0]:.3f} "
            f"avg={np.mean([s for s,_ in scored]):.3f}"
        )

        new_pop = []

        while len(new_pop) < population:

            parent = random.choice(elites)

            child = mutate_architecture(parent)

            new_pop.append(child)

        pop = new_pop

    print("\nBest Architecture Found")
    print("----------------------")

    d = edge_density(best_global)
    c = cycle_ratio(best_global)

    print("score:", best_score)
    print("density:", d)
    print("cycle:", c)

    return best_global


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    evolve_architectures(BASE_SYSTEM)
