# tools/resilience_symbolic_law_finder.py

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
# random architecture
# --------------------------------------------------

def random_architecture(base):

    nodes=base["nodes"]

    data=copy.deepcopy(base)

    data["transitions"]={}

    for n in nodes:

        targets=[]

        k=random.randint(1,len(nodes))

        for _ in range(k):

            t=random.choice(nodes)

            if t!=n and t not in targets:
                targets.append(t)

        data["transitions"][n]=targets

    return rebuild_edges(data)


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
# symbolic features
# --------------------------------------------------

def symbolic_features(d,c):

    return [
        d,
        c,
        d*d,
        c*c,
        d*c,
        np.sqrt(d),
        np.sqrt(c),
        np.log(d+1e-6),
        np.log(c+1e-6),
        1/(d+1e-3)
    ]


feature_names=[
"density",
"cycle_ratio",
"density^2",
"cycle_ratio^2",
"density*cycle",
"sqrt(density)",
"sqrt(cycle)",
"log(density)",
"log(cycle)",
"1/density"
]


# --------------------------------------------------
# symbolic law discovery
# --------------------------------------------------

def discover_symbolic_law(system_path,samples=800):

    base=load_json(system_path)

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

        X.append(symbolic_features(d,c))
        y.append(score)

        if i%50==0:
            print(f"sample {i} score={score:.3f}")

    X=np.array(X)
    y=np.array(y)

    model=LinearRegression()

    model.fit(X,y)

    print("\nSymbolic Resilience Law")
    print("---------------------------")

    for name,coef in zip(feature_names,model.coef_):

        if abs(coef)>0.02:
            print(f"{coef:+.3f} * {name}")

    print(f"{model.intercept_:+.3f} (intercept)")


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__=="__main__":

    discover_symbolic_law(BASE_SYSTEM, samples=800)
