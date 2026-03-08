import sys
import os
import numpy as np
import random

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


def detect_scaling(samples=800):

    base = load_json(BASE_SYSTEM)

    densities = []
    cycles = []
    scores = []

    print("\nCollecting scaling dataset\n")

    for i in range(samples):

        arch = random_architecture(base)

        d = edge_density(arch)
        c = cycle_ratio(arch)

        if d == 0 or c == 0:
            continue

        try:
            s = score_system(arch)
        except:
            s = 0

        densities.append(d)
        cycles.append(c)
        scores.append(s)

        if i % 50 == 0:
            print("sample", i, "score", s)

    densities = np.array(densities)
    cycles = np.array(cycles)
    scores = np.array(scores)

    # log transform
    X1 = np.log(densities)
    X2 = np.log(cycles)
    Y = np.log(scores + 1e-6)

    X = np.vstack([X1, X2, np.ones(len(X1))]).T

    coeffs, *_ = np.linalg.lstsq(X, Y, rcond=None)

    a = coeffs[0]
    b = coeffs[1]
    c0 = coeffs[2]

    print("\nScaling Law")
    print("-----------")

    print("Resilience ≈ exp(c) * density^a * cycle^b")
    print()

    print("a (density exponent):", a)
    print("b (cycle exponent):", b)
    print("constant:", np.exp(c0))

    pred = np.exp(c0) * densities**a * cycles**b

    r2 = 1 - np.sum((scores - pred)**2) / np.sum((scores - np.mean(scores))**2)

    print("\nModel fit R²:", r2)


if __name__ == "__main__":

    detect_scaling()
