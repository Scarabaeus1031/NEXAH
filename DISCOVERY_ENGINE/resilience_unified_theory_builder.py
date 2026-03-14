# tools/resilience_unified_theory_builder.py

import sys
import os
import json
import random
import tempfile
import copy
import numpy as np
import networkx as nx
from sklearn.linear_model import LinearRegression

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
    tmp=tempfile.NamedTemporaryFile(mode="w",suffix=".json",delete=False)
    json.dump(data,tmp,indent=2)
    tmp.close()
    return tmp.name


# --------------------------------------------------
# scoring
# --------------------------------------------------

def score_system(data):

    temp=write_temp(data)

    try:
        report=analyze_system(temp)
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
# architecture generator
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
# theory discovery
# --------------------------------------------------

def discover_unified_law(samples=2000):

    base=load_json(BASE_SYSTEM)

    X=[]
    y=[]

    for i in range(samples):

        candidate=random_architecture(base)

        try:
            score=score_system(candidate)
        except:
            score=0

        d=edge_density(candidate)
        c=cycle_ratio(candidate)

        if c==0:
            continue

        # feature space
        features=[
            d,
            c,
            d*c,
            d/c,
            (d+c)/2
        ]

        X.append(features)
        y.append(score)

        if i%100==0:
            print("sample",i,"score",score)

    X=np.array(X)
    y=np.array(y)

    model=LinearRegression()
    model.fit(X,y)

    coefs=model.coef_
    intercept=model.intercept_

    r2=model.score(X,y)

    labels=[
        "density",
        "cycle",
        "density*cycle",
        "density/cycle",
        "(density+cycle)/2"
    ]

    print("\nUnified Resilience Equation")
    print("----------------------------")

    for i,label in enumerate(labels):

        print(f"{coefs[i]:.3f} * {label}")

    print(f"+ {intercept:.3f}")

    print("\nModel fit R²:",r2)


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__=="__main__":

    discover_unified_law()
