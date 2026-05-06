# tools/resilience_universal_constant_finder.py

import sys
import os
import json
import random
import tempfile
import copy
import numpy as np
import networkx as nx

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_analyzer import analyze_system


BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"


# --------------------------------------------------
# IO
# --------------------------------------------------

def load_json(path):
    with open(path,"r") as f:
        return json.load(f)


def write_temp(data):

    tmp = tempfile.NamedTemporaryFile(mode="w",suffix=".json",delete=False)

    json.dump(data,tmp,indent=2)

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

    edges=[]

    for s,targets in data["transitions"].items():

        if isinstance(targets,list):

            for t in targets:
                edges.append([s,t])

        else:

            edges.append([s,targets])

    data["edges"]=edges

    return data


def build_graph(data):

    G = nx.DiGraph()

    for s,targets in data["transitions"].items():

        if isinstance(targets,list):

            for t in targets:
                G.add_edge(s,t)

        else:

            G.add_edge(s,targets)

    return G


# --------------------------------------------------
# metrics
# --------------------------------------------------

def edge_density(data):

    nodes=len(data["nodes"])
    edges=len(data["edges"])

    return edges/(nodes*nodes)


def cycle_ratio(data):

    G=build_graph(data)

    cycles=list(nx.simple_cycles(G))

    nodes_in_cycles=set()

    for c in cycles:
        for n in c:
            nodes_in_cycles.add(n)

    if len(G.nodes())==0:
        return 0

    return len(nodes_in_cycles)/len(G.nodes())


# --------------------------------------------------
# random architecture
# --------------------------------------------------

def random_architecture(base):

    nodes=base["nodes"]

    data=copy.deepcopy(base)

    data["transitions"]={}

    for n in nodes:

        k=random.randint(1,len(nodes))

        targets=random.sample(nodes,k)

        data["transitions"][n]=targets

    return rebuild_edges(data)


# --------------------------------------------------
# constant search
# --------------------------------------------------

def search_constant(samples=1500):

    base=load_json(BASE_SYSTEM)

    constants=[]

    for i in range(samples):

        candidate=random_architecture(base)

        try:
            score=score_system(candidate)
        except:
            score=0

        if score < 0.4:
            continue

        d=edge_density(candidate)
        c=cycle_ratio(candidate)

        if c == 0:
            continue

        # candidate constants

        k1 = d * c
        k2 = d / c
        k3 = (d + c) / 2

        constants.append([k1,k2,k3])

        if i % 50 == 0:
            print("sample",i,"score",score)

    constants=np.array(constants)

    means=np.mean(constants,axis=0)
    stds=np.std(constants,axis=0)

    print("\nResilience Constant Candidates")
    print("--------------------------------")

    print("K1 = density * cycle")
    print("mean:",means[0],"std:",stds[0])

    print("\nK2 = density / cycle")
    print("mean:",means[1],"std:",stds[1])

    print("\nK3 = (density + cycle)/2")
    print("mean:",means[2],"std:",stds[2])

    best_index=np.argmin(stds)

    labels=["density*cycle","density/cycle","(density+cycle)/2"]

    print("\nMost stable constant:")
    print(labels[best_index])
    print("≈",means[best_index])


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__=="__main__":

    search_constant()
