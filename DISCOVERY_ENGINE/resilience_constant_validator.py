# tools/resilience_constant_validator.py

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
    score_system,
)

BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"


def validate_constant(samples=500):

    base = load_json(BASE_SYSTEM)

    constants = []
    scores = []

    print("\nTesting Resilience Constant\n")
    print("---------------------------")

    for i in range(samples):

        candidate = random_architecture(base)

        d = edge_density(candidate)
        c = cycle_ratio(candidate)

        if c == 0:
            continue

        try:
            s = score_system(candidate)
        except:
            s = 0

        k = d / c

        constants.append(k)
        scores.append(s)

        if i % 50 == 0:
            print(
                f"sample {i} | density={d:.3f} cycle={c:.3f} k={k:.3f} score={s:.3f}"
            )

    constants = np.array(constants)
    scores = np.array(scores)

    print("\nResults")
    print("-------")

    print("mean constant:", np.mean(constants))
    print("std constant:", np.std(constants))

    corr = np.corrcoef(constants, scores)[0,1]

    print("correlation(constant, score):", corr)

    print("\nInterpretation")

    if abs(corr) > 0.5:
        print("Strong relationship detected → possible resilience constant")
    elif abs(corr) > 0.2:
        print("Weak relationship detected")
    else:
        print("No clear constant behaviour")


if __name__ == "__main__":

    validate_constant(samples=600)
