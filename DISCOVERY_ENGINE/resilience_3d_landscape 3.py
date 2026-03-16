# tools/resilience_3d_landscape.py

import sys
import os
import json
import random
import tempfile
import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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


# --------------------------------------------------
# architecture generator
# --------------------------------------------------

def generate_architecture(base,density):

    nodes=base["nodes"]

    data=copy.deepcopy(base)

    data["transitions"]={}

    k=max(1,int(len(nodes)*density))

    for n in nodes:

        targets=random.sample(nodes,min(k,len(nodes)))

        data["transitions"][n]=targets

    return rebuild_edges(data)


# --------------------------------------------------
# landscape scan
# --------------------------------------------------

def scan_landscape():

    base=load_json(BASE_SYSTEM)

    densities=np.linspace(0.05,0.9,15)
    noises=np.linspace(0.0,1.0,15)

    X=[]
    Y=[]
    Z=[]

    for noise in noises:

        for d in densities:

            candidate=generate_architecture(base,d)

            try:
                score=score_system(candidate)
            except:
                score=0

            X.append(d)
            Y.append(noise)
            Z.append(score)

            print("density",round(d,2),"noise",round(noise,2),"score",round(score,3))

    return np.array(X),np.array(Y),np.array(Z)


# --------------------------------------------------
# plot
# --------------------------------------------------

def plot_surface(X,Y,Z):

    fig=plt.figure(figsize=(10,7))

    ax=fig.add_subplot(111,projection='3d')

    ax.plot_trisurf(
        X,
        Y,
        Z,
        cmap="viridis",
        linewidth=0.2
    )

    ax.set_xlabel("Density")
    ax.set_ylabel("Noise")
    ax.set_zlabel("Resilience")

    ax.set_title("3D Resilience Landscape")

    plt.show()


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__=="__main__":

    X,Y,Z=scan_landscape()

    plot_surface(X,Y,Z)
