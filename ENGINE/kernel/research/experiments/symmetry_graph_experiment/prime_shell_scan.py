import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def build_graph(n):

    G = nx.Graph()

    center = "center"
    G.add_node(center)

    nodes = [f"s{i}" for i in range(n)]

    for s in nodes:
        G.add_edge(center, s)

    for i in range(n):
        G.add_edge(nodes[i], nodes[(i+1)%n])

    return G


def run_kuramoto(G,steps=400,dt=0.05,K=2.5):

    nodes=list(G.nodes())
    N=len(nodes)

    A=nx.to_numpy_array(G,nodelist=nodes)

    theta=np.random.uniform(0,2*np.pi,N)
    omega=np.random.normal(0,0.1,N)

    R=[]

    for _ in range(steps):

        diff=theta.reshape((N,1))-theta.reshape((1,N))
        coupling=np.sum(A*np.sin(-diff),axis=1)

        theta+=dt*(omega+K*coupling)

        r=np.abs(np.mean(np.exp(1j*theta)))
        R.append(r)

    return theta,R


sizes=range(8,41)

sync_times=[]

for n in sizes:

    G=build_graph(n)

    theta,R=run_kuramoto(G)

    t=next((i for i,v in enumerate(R) if v>0.95),None)

    if t is None:
        t=400

    sync_times.append(t)

    print(n,t)


plt.figure()

plt.scatter(sizes,sync_times)

plt.xlabel("Shell size")
plt.ylabel("Sync time")

plt.title("Prime Shell Synchronization Scan")

plt.show()
