"""
NEXAH Symmetry Graph – Regime Landscape 2D
------------------------------------------

Scans two parameters:

K      = coupling strength
sigma  = oscillator frequency variance

For each point we run Kuramoto simulations and classify the resulting
domain type.

Domains:

0 = GLOBAL_LOCK
1 = BIPOLAR
2 = MULTI_CLUSTER
3 = FRAGMENTED_PHASE

Output:
- 2D regime landscape plot
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import networkx as nx


# --------------------------------------------------
# Build symmetry graph
# --------------------------------------------------

def build_symmetry_graph():

    G = nx.Graph()

    G.add_node("hub_A")
    G.add_node("hub_B")
    G.add_edge("hub_A","hub_B")

    C5 = [f"C5_{i}" for i in range(5)]
    for i in range(5):
        G.add_edge(C5[i],C5[(i+1)%5])

    C6A = [f"C6A_{i}" for i in range(6)]
    for i in range(6):
        G.add_edge(C6A[i],C6A[(i+1)%6])

    C6B = [f"C6B_{i}" for i in range(6)]
    for i in range(6):
        G.add_edge(C6B[i],C6B[(i+1)%6])

    for n in C5:
        G.add_edge("hub_A",n)

    for n in C6A:
        G.add_edge("hub_A",n)

    for n in C6B:
        G.add_edge("hub_B",n)

    return G


# --------------------------------------------------
# Kuramoto simulation
# --------------------------------------------------

def run_kuramoto(G,K,sigma,steps=2000,dt=0.05):

    nodes=list(G.nodes())
    N=len(nodes)

    theta=np.random.uniform(0,2*np.pi,N)
    omega=np.random.normal(1.0,sigma,N)

    adjacency=nx.to_numpy_array(G,nodelist=nodes)

    for step in range(steps):

        dtheta=np.zeros(N)

        for i in range(N):

            coupling_sum=0

            for j in range(N):

                if adjacency[i,j]>0:
                    coupling_sum+=math.sin(theta[j]-theta[i])

            dtheta[i]=omega[i]+K*coupling_sum

        theta+=dtheta*dt
        theta=np.mod(theta,2*np.pi)

    return theta


# --------------------------------------------------
# Cluster detection
# --------------------------------------------------

def detect_clusters(theta,threshold=0.25):

    clusters=[]
    used=set()

    N=len(theta)

    for i in range(N):

        if i in used:
            continue

        cluster=[i]

        for j in range(N):

            if i==j:
                continue

            d=abs(np.angle(np.exp(1j*(theta[i]-theta[j]))))

            if d<threshold:
                cluster.append(j)

        for c in cluster:
            used.add(c)

        clusters.append(cluster)

    return clusters


# --------------------------------------------------
# Domain classification
# --------------------------------------------------

def classify_domain(clusters):

    n=len(clusters)

    if n==1:
        return 0  # GLOBAL_LOCK

    if n==2:
        return 1  # BIPOLAR

    if 3<=n<=4:
        return 2  # MULTI_CLUSTER

    return 3     # FRAGMENTED_PHASE


# --------------------------------------------------
# Parameter scan
# --------------------------------------------------

def scan_regime_landscape(K_values,sigma_values,runs=10):

    G=build_symmetry_graph()

    landscape=np.zeros((len(sigma_values),len(K_values)))

    for i,sigma in enumerate(sigma_values):

        for j,K in enumerate(K_values):

            domains=[]

            for r in range(runs):

                theta=run_kuramoto(G,K,sigma)

                clusters=detect_clusters(theta)

                domain=classify_domain(clusters)

                domains.append(domain)

            landscape[i,j]=np.mean(domains)

    return landscape


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_landscape(landscape,K_values,sigma_values):

    plt.figure(figsize=(8,6))

    plt.imshow(
        landscape,
        origin="lower",
        aspect="auto",
        extent=[K_values[0],K_values[-1],sigma_values[0],sigma_values[-1]],
        cmap="viridis"
    )

    cbar=plt.colorbar()
    cbar.set_label("Domain Regime")

    plt.xlabel("Coupling K")
    plt.ylabel("Frequency variance σ")
    plt.title("Symmetry Graph Regime Landscape")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__=="__main__":

    print("\nRunning 2D Regime Landscape Scan...\n")

    K_values=np.linspace(0.02,0.35,20)
    sigma_values=np.linspace(0.02,0.20,20)

    landscape=scan_regime_landscape(K_values,sigma_values)

    plot_landscape(landscape,K_values,sigma_values)
