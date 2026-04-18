# tools/resilience_renormalization_detector.py

import sys
import os
import json
import random
import tempfile
import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_analyzer import analyze_system

BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"


# --------------------------------------------------
# IO
# --------------------------------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


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
# architecture generator
# --------------------------------------------------

def random_architecture(base):

    nodes = base["nodes"]

    data = copy.deepcopy(base)

    data["transitions"] = {}

    for n in nodes:

        k = random.randint(1, min(4, len(nodes)))

        targets = random.sample(nodes, k)

        data["transitions"][n] = targets

    return data


# --------------------------------------------------
# renormalization
# --------------------------------------------------

def coarse_grain(data):

    nodes = data["nodes"]

    if len(nodes) < 4:
        return data

    grouped = {}

    new_nodes = []

    for i in range(0, len(nodes), 2):

        group = nodes[i:i+2]

        name = "_".join(group)

        new_nodes.append(name)

        for g in group:
            grouped[g] = name

    new_trans = {}

    for old_s, targets in data["transitions"].items():

        s = grouped[old_s]

        if s not in new_trans:
            new_trans[s] = []

        if isinstance(targets, list):

            for t in targets:

                t2 = grouped[t]

                if t2 != s:
                    new_trans[s].append(t2)

        else:

            t2 = grouped[targets]

            if t2 != s:
                new_trans[s].append(t2)

    new_data = {
        "nodes": list(set(new_nodes)),
        "transitions": new_trans
    }

    return new_data


# --------------------------------------------------
# test renormalization
# --------------------------------------------------

def test_scaling(system_path, samples=500):

    base = load_json(system_path)

    original_scores = []
    coarse_scores = []

    for i in range(samples):

        arch = random_architecture(base)

        try:
            s1 = score_system(arch)
        except:
            s1 = 0

        coarse = coarse_grain(arch)

        try:
            s2 = score_system(coarse)
        except:
            s2 = 0

        original_scores.append(s1)
        coarse_scores.append(s2)

        if i % 50 == 0:
            print("sample", i)

    return np.array(original_scores), np.array(coarse_scores)


# --------------------------------------------------
# plot
# --------------------------------------------------

def plot_scaling(original, coarse):

    plt.figure(figsize=(6,6))

    plt.scatter(original, coarse, alpha=0.5)

    plt.xlabel("Original Resilience")
    plt.ylabel("Coarse Grained Resilience")

    plt.title("Renormalization Scaling")

    plt.plot([0,1],[0,1], linestyle="--")

    plt.show()


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    original, coarse = test_scaling(BASE_SYSTEM, samples=500)

    corr = np.corrcoef(original, coarse)[0,1]

    print("\nRenormalization correlation:", corr)

    plot_scaling(original, coarse)
