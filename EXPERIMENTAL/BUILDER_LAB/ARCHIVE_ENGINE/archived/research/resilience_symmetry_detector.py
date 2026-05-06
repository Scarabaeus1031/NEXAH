"""
NEXAH Resilience Symmetry Detector

Detects symmetry structures in the resilience landscape.

Searches for:

1. Gradient symmetry
2. Transition pairs
3. Resonance triangles
"""

import os
import json
import math


RESULT_DIR = "results"


def load_results():

    data = []

    if not os.path.exists(RESULT_DIR):
        return data

    for f in os.listdir(RESULT_DIR):

        if not f.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, f)

        try:

            with open(path) as file:
                r = json.load(file)

            nodes = r["nodes"]
            edges = r["edges"]
            res = r["resilience_score"]

            if nodes == 0:
                continue

            degree = edges / nodes

            data.append((nodes, degree, res))

        except Exception:
            continue

    return data


def gradient(p1, p2):

    n1, d1, r1 = p1
    n2, d2, r2 = p2

    dn = n2 - n1
    dd = d2 - d1

    dist = math.sqrt(dn * dn + dd * dd)

    if dist == 0:
        return 0

    return abs(r2 - r1) / dist


def detect_gradient_symmetry(data):

    grads = []

    for i in range(len(data)):

        for j in range(i + 1, len(data)):

            g = gradient(data[i], data[j])

            grads.append((data[i], data[j], g))

    pairs = []

    for i in range(len(grads)):

        for j in range(i + 1, len(grads)):

            g1 = grads[i][2]
            g2 = grads[j][2]

            if abs(g1 - g2) < 0.02:

                pairs.append((grads[i], grads[j]))

    return pairs


def detect_triangles(data):

    triangles = []

    for i in range(len(data)):

        for j in range(i + 1, len(data)):

            for k in range(j + 1, len(data)):

                g1 = gradient(data[i], data[j])
                g2 = gradient(data[j], data[k])
                g3 = gradient(data[i], data[k])

                if (
                    abs(g1 - g2) < 0.05
                    and abs(g2 - g3) < 0.05
                ):
                    triangles.append((data[i], data[j], data[k], g1))

    return triangles


def run():

    print("\nNEXAH Resilience Symmetry Detector")
    print("----------------------------------")

    data = load_results()

    if len(data) < 5:
        print("Not enough data.")
        return

    pairs = detect_gradient_symmetry(data)
    triangles = detect_triangles(data)

    print("\nGradient Symmetry Pairs")
    print("-----------------------")

    for p in pairs[:5]:

        (a, b, g1), (c, d, g2) = p

        print(
            f"{a} ↔ {b}  gradient={round(g1,3)}"
            f"   ||   "
            f"{c} ↔ {d}  gradient={round(g2,3)}"
        )

    print("\nResonance Triangles")
    print("-------------------")

    for t in triangles[:5]:

        a, b, c, g = t

        print(
            f"{a}  {b}  {c}  gradient≈{round(g,3)}"
        )


if __name__ == "__main__":

    run()
