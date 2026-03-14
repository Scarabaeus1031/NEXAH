# tools/resilience_architecture_evolver_v2.py

import sys
import os
import json
import random
import copy
import tempfile

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from tools.resilience_analyzer import analyze_system


BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"
OUTPUT_SYSTEM = "APPLICATIONS/examples/energy_grid_architecture_evolved_v2.json"


# --------------------------------------------------
# IO
# --------------------------------------------------

def load_json(path):
    with open(path,"r") as f:
        return json.load(f)


def save_json(path,data):
    with open(path,"w") as f:
        json.dump(data,f,indent=2)


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
# helpers
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

def add_edge(data):

    nodes=data["nodes"]

    s=random.choice(nodes)
    t=random.choice(nodes)

    if s==t:
        return data

    targets=data["transitions"].get(s,[])

    if not isinstance(targets,list):
        targets=[targets]

    if t not in targets:
        targets.append(t)

    data["transitions"][s]=targets

    return rebuild_edges(data)


def remove_edge(data):

    edges=data["edges"]

    if not edges:
        return data

    s,t=random.choice(edges)

    targets=data["transitions"][s]

    if isinstance(targets,list) and len(targets)>1:

        targets=[x for x in targets if x!=t]

        data["transitions"][s]=targets

    return rebuild_edges(data)


def redirect_edge(data):

    edges=data["edges"]
    nodes=data["nodes"]

    if not edges:
        return data

    s,t=random.choice(edges)

    new=random.choice(nodes)

    targets=data["transitions"][s]

    if isinstance(targets,list):

        targets=[new if x==t else x for x in targets]

        data["transitions"][s]=targets

    return rebuild_edges(data)


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
# mutation controller
# --------------------------------------------------

def mutate(data):

    candidate=copy.deepcopy(data)

    ops=[add_edge,remove_edge,redirect_edge]

    op=random.choice(ops)

    return op(candidate)


# --------------------------------------------------
# evolution
# --------------------------------------------------

def evolve(system_path,generations=80,pop_size=40):

    base=load_json(system_path)

    population=[random_architecture(base) for _ in range(pop_size)]

    best_system=base
    best_score=score_system(base)

    mutation_rate=0.4
    stagnation=0

    history=[best_score]

    print("\nResilience Evolver v2")
    print("-----------------------")

    print("initial score:",best_score)

    for g in range(generations):

        scored=[]

        for sys in population:

            try:

                s=score_system(sys)

            except:

                s=0

            scored.append((s,sys))

            if s>best_score:

                best_score=s
                best_system=sys
                stagnation=0

                print("generation",g,"new best",s)

        scored.sort(reverse=True,key=lambda x:x[0])

        elites=[x[1] for x in scored[:10]]

        if scored[0][0]<=best_score:

            stagnation+=1

        # adaptive mutation
        if stagnation>10:

            mutation_rate=0.8

        else:

            mutation_rate=0.4

        next_pop=elites.copy()

        while len(next_pop)<pop_size:

            parent=random.choice(elites)

            child=copy.deepcopy(parent)

            if random.random()<mutation_rate:

                child=mutate(child)

            # exploration boost
            if random.random()<0.1:

                child=random_architecture(base)

            next_pop.append(child)

        population=next_pop

        history.append(best_score)

        print("generation",g,"best",best_score)

    save_json(OUTPUT_SYSTEM,best_system)

    print("\nfinal best score:",best_score)

    print("saved to",OUTPUT_SYSTEM)

    return history


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__=="__main__":

    evolve(BASE_SYSTEM)
