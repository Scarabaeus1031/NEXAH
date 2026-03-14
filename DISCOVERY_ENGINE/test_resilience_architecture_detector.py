import sys
import os
import json
import random
import copy

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_architecture_attractor_detector import (
    load_json,
    random_architecture,
    edge_density,
    cycle_ratio,
    score_system,
)

BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"


def run_test(samples=50):

    base = load_json(BASE_SYSTEM)

    print("\nRunning Architecture Detector Test\n")
    print("-----------------------------------")

    densities = []
    cycles = []
    scores = []

    for i in range(samples):

        candidate = random_architecture(base)

        d = edge_density(candidate)
        c = cycle_ratio(candidate)

        try:
            s = score_system(candidate)
        except:
            s = 0

        densities.append(d)
        cycles.append(c)
        scores.append(s)

        print(
            f"sample {i} | density={d:.3f} cycle={c:.3f} score={s:.3f}"
        )

    print("\nSummary")
    print("-------")

    print("density range:", min(densities), "→", max(densities))
    print("cycle range:", min(cycles), "→", max(cycles))
    print("score range:", min(scores), "→", max(scores))

    print("\nTest completed ✔")


if __name__ == "__main__":

    run_test(samples=50)
