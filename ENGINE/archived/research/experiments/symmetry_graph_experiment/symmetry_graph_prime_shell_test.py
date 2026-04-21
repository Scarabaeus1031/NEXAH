import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# -------------------------------------------------
# build hub shell graph
# -------------------------------------------------

def build_graph(n):

    G = nx.Graph()

    center = "center"
    G.add_node(center)

    nodes = [f"s{i}" for i in range(n)]

    for s in nodes:
        G.add_edge(center, s)

    # ring connections
    for i in range(n):
        G.add_edge(nodes[i], nodes[(i+1) % n])

    return G


# -------------------------------------------------
# kuramoto simulation
# -------------------------------------------------

def run_kuramoto(G, steps=400, dt=0.05, K=2.5):

    nodes = list(G.nodes())
    N = len(nodes)

    index = {n:i for i,n in enumerate(nodes)}

    A = nx.to_numpy_array(G, nodelist=nodes)

    theta = np.random.uniform(0,2*np.pi,N)

    omega = np.random.normal(0,0.1,N)

    R_series = []

    for t in range(steps):

        diff = theta.reshape((N,1)) - theta.reshape((1,N))

        coupling = np.sum(A*np.sin(-diff), axis=1)

        dtheta = omega + K*coupling

        theta += dt*dtheta

        r = np.abs(np.mean(np.exp(1j*theta)))

        R_series.append(r)

    return theta, R_series


# -------------------------------------------------
# cluster detection
# -------------------------------------------------

def cluster_count(theta, tol=0.3):

    clusters = []

    for angle in theta:

        placed = False

        for c in clusters:

            if abs(np.angle(np.exp(1j*(angle-c)))) < tol:
                placed = True
                break

        if not placed:
            clusters.append(angle)

    return len(clusters)


# -------------------------------------------------
# run experiment
# -------------------------------------------------

sizes = [16,17,18]

results = {}

for n in sizes:

    G = build_graph(n)

    theta, R = run_kuramoto(G)

    clusters = cluster_count(theta)

    sync_time = next((i for i,v in enumerate(R) if v>0.95), None)

    results[n] = (sync_time, clusters, R)

    print("\nNodes:",n)
    print("Sync time:",sync_time)
    print("Cluster count:",clusters)


# -------------------------------------------------
# plot
# -------------------------------------------------

plt.figure()

for n in sizes:

    plt.plot(results[n][2], label=f"{n} nodes")

plt.xlabel("time step")
plt.ylabel("global sync R")
plt.legend()
plt.title("Hub Shell Synchronization Comparison")

plt.show()
