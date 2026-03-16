# tools/resilience_architecture_map.py

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

    G=nx.DiGraph()

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
# map builder
# --------------------------------------------------

def build_map(system_path,samples=600):

    base=load_json(system_path)

    densities=[]
    cycles=[]
    scores=[]

    for i in range(samples):

        candidate=random_architecture(base)

        try:

            score=score_system(candidate)

        except:

            score=0

        d=edge_density(candidate)
        c=cycle_ratio(candidate)

        densities.append(d)
        cycles.append(c)
        scores.append(score)

        if i%50==0:
            print("sample",i,"score",score)

    return densities,cycles,scores


# --------------------------------------------------
# plot
# --------------------------------------------------

def plot_map(densities,cycles,scores):

    plt.figure(figsize=(8,6))

    sc=plt.scatter(
        densities,
        cycles,
        c=scores,
        cmap="viridis",
        s=60
    )

    plt.xlabel("Edge Density")
    plt.ylabel("Cycle Ratio")

    plt.title("Resilience Architecture Map")

    plt.colorbar(sc,label="Resilience Score")

    plt.grid(True)

    plt.show()


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__=="__main__":

    d,c,s=build_map(BASE_SYSTEM, samples=700)

    plot_map(d,c,s)
