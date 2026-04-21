"""
NEXAH Resilience Phase Transition Detector

Detects critical phase transitions in architecture space by
analyzing large resilience gradients.

A phase transition occurs when a small change in architecture
(nodes or degree) causes a large change in resilience.

Axes
X = nodes
Y = degree
Z = resilience
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

            if "nodes" not in r:
                continue

            nodes = r["nodes"]
            edges = r["edges"]
            resilience = r["resilience_score"]

            if nodes == 0:
                continue

            degree = edges / nodes

            data.append((nodes, degree, resilience))

        except Exception:
            continue

    return data


def compute_gradient(p1, p2):

    n1, d1, r1 = p1
    n2, d2, r2 = p2

    dn = n2 - n1
    dd = d2 - d1

    distance = math.sqrt(dn * dn + dd * dd)

    if distance == 0:
        return 0

    dr = r2 - r1

    gradient = abs(dr) / distance

    return gradient


def detect_transitions(data):

    transitions = []

    for i in range(len(data)):

        for j in range(i + 1, len(data)):

            p1 = data[i]
            p2 = data[j]

            g = compute_gradient(p1, p2)

            if g > 0.25:  # threshold for phase transition

                transitions.append((p1, p2, g))

    return transitions


def summarize(transitions):

    if not transitions:

        print("\nNo strong phase transitions detected.")
        return

    print("\nDetected Phase Transitions")
    print("---------------------------")

    transitions.sort(key=lambda x: -x[2])

    for t in transitions[:10]:

        p1, p2, g = t

        n1, d1, r1 = p1
        n2, d2, r2 = p2

        print(
            f"({n1:.1f},{d1:.2f},{r1:.3f})  →  "
            f"({n2:.1f},{d2:.2f},{r2:.3f})  "
            f"| gradient ≈ {g:.3f}"
        )


def run():

    print("\nNEXAH Resilience Phase Transition Detector")
    print("-------------------------------------------")

    data = load_results()

    if len(data) < 6:

        print("Not enough data.")
        return

    transitions = detect_transitions(data)

    summarize(transitions)


if __name__ == "__main__":

    run()
