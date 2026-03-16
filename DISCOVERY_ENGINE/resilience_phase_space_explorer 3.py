# tools/resilience_phase_space_explorer.py

import sys
import os
import json
import copy
import random
import tempfile
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_analyzer import analyze_system


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


# --------------------------------------------------
# IO
# --------------------------------------------------

def load_json(path):
    with open(path,"r") as f:
        return json.load(f)


def write_temp_system(data):

    tmp = tempfile.NamedTemporaryFile(mode="w",suffix=".json",delete=False)

    json.dump(data,tmp,indent=2)

    tmp.close()

    return tmp.name


# --------------------------------------------------
# scoring
# --------------------------------------------------

def score_system(data):

    temp = write_temp_system(data)

    try:

        report = analyze_system(temp)

        return report["resilience_score"]

    finally:

        os.remove(temp)


# --------------------------------------------------
# graph helpers
# --------------------------------------------------

def rebuild_edges(data):

    edges=[]

    for s,targets in data["transitions"].items():

        if isinstance(targets,list):

            for t in targets:
                edges.append([s,t])

        else:

            edges.append([s,targets])

    data["edges"]=edges

    return data


# --------------------------------------------------
# mutations
# --------------------------------------------------

def random_mutation(data):

    nodes=data["nodes"]

    m=random.choice(["add","remove","redirect"])

    if m=="add":

        s=random.choice(nodes)
        t=random.choice(nodes)

        if s!=t:

            data["transitions"].setdefault(s,[])

            if t not in data["transitions"][s]:
                data["transitions"][s].append(t)

    elif m=="remove":

        edges=[]

        for s,targets in data["transitions"].items():
            for t in targets:
                edges.append((s,t))

        if edges:

            s,t=random.choice(edges)

            if len(data["transitions"][s])>1:

                data["transitions"][s]=[
                    x for x in data["transitions"][s] if x!=t
                ]

    elif m=="redirect":

        edges=[]

        for s,targets in data["transitions"].items():
            for t in targets:
                edges.append((s,t))

        if edges:

            s,t=random.choice(edges)

            new=random.choice(nodes)

            if new!=s:

                data["transitions"][s]=[
                    x for x in data["transitions"][s] if x!=t
                ]

                data["transitions"][s].append(new)

    return rebuild_edges(data)


def mutate_system(data, intensity):

    data=copy.deepcopy(data)

    steps=int(1+intensity*10)

    for _ in range(steps):

        data=random_mutation(data)

    return data


# --------------------------------------------------
# density control
# --------------------------------------------------

def compute_density(data):

    nodes=len(data["nodes"])

    edges=len(data["edges"])

    max_edges=nodes*nodes

    return edges/max_edges


# --------------------------------------------------
# phase exploration
# --------------------------------------------------

def explore_phase_space(system_path):

    base=load_json(system_path)

    densities=np.linspace(0.1,0.9,12)

    mutation_levels=np.linspace(0,1,12)

    landscape=np.zeros((len(mutation_levels),len(densities)))

    for i,mut in enumerate(mutation_levels):

        print("\nMutation level:",round(mut,2))

        for j,target_density in enumerate(densities):

            candidate=copy.deepcopy(base)

            candidate=mutate_system(candidate,mut)

            try:

                score=score_system(candidate)

            except Exception:

                score=0

            landscape[i,j]=score

            print(
                f"density={target_density:.2f} mutation={mut:.2f} score={score:.3f}"
            )

    return densities,mutation_levels,landscape


# --------------------------------------------------
# visualization
# --------------------------------------------------

def visualize(densities,mutations,landscape):

    plt.figure(figsize=(8,6))

    plt.imshow(
        landscape,
        origin="lower",
        aspect="auto",
        extent=[
            densities[0],
            densities[-1],
            mutations[0],
            mutations[-1]
        ]
    )

    plt.colorbar(label="Resilience Score")

    plt.xlabel("Edge Density")

    plt.ylabel("Mutation Intensity")

    plt.title("Resilience Phase Space")

    plt.show()


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__=="__main__":

    d,m,l=explore_phase_space(SYSTEM_PATH)

    visualize(d,m,l)
