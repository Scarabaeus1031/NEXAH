import sys
import os
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_architecture_attractor_detector import (
    load_json,
    random_architecture,
    edge_density,
    cycle_ratio,
    score_system
)

BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"


def find_critical_point(samples=1000):

    base = load_json(BASE_SYSTEM)

    best_score = -1
    best_density = None
    best_cycle = None

    densities = []
    cycles = []
    scores = []

    print("\nSearching Critical Point\n")

    for i in range(samples):

        arch = random_architecture(base)

        d = edge_density(arch)
        c = cycle_ratio(arch)

        try:
            s = score_system(arch)
        except:
            s = 0

        densities.append(d)
        cycles.append(c)
        scores.append(s)

        if s > best_score:

            best_score = s
            best_density = d
            best_cycle = c

        if i % 50 == 0:
            print("sample", i, "score", s)

    print("\nCritical Point")
    print("--------------")

    print("max resilience:", best_score)
    print("density*:", best_density)
    print("cycle*:", best_cycle)

    print("\nDataset statistics")

    print("mean density:", np.mean(densities))
    print("mean cycle:", np.mean(cycles))
    print("mean score:", np.mean(scores))


if __name__ == "__main__":

    find_critical_point()
