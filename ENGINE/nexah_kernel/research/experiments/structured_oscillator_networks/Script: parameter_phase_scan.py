"""
NEXAH Experiment Tool
Parameter Phase Scan

Purpose
-------
Scan parameter space to see where the system becomes

• synchronized
• domain-forming
• shear dominated
• chaotic

Parameters scanned
------------------
Coupling strength K
Drift magnitude ω

Outputs
-------
output/phase_diagram_R.png
output/phase_diagram_variance.png
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


# ------------------------------------------------
# Utilities
# ------------------------------------------------
def wrap_angle(x):
    return (x + np.pi) % (2*np.pi) - np.pi


def order_parameter(theta):
    return np.abs(np.mean(np.exp(1j*theta)))


# ------------------------------------------------
# Graph
# ------------------------------------------------
def build_graph(n_inner=16,n_middle=32,n_outer=16):

    G = nx.Graph()

    off_inner = 0
    off_middle = n_inner
    off_outer = n_inner + n_middle

    inner = list(range(off_inner,off_inner+n_inner))
    middle = list(range(off_middle,off_middle+n_middle))
    outer = list(range(off_outer,off_outer+n_outer))

    for nodes in [inner,middle,outer]:
        m=len(nodes)
        for i in range(m):
            G.add_edge(nodes[i],nodes[(i+1)%m])

    for i,u in enumerate(inner):
        j=int(round(i*n_middle/n_inner))%n_middle
        G.add_edge(u,middle[j])

    for i,u in enumerate(outer):
        j=int(round(i*n_middle/n_outer))%n_middle
        G.add_edge(u,middle[j])

    return nx.to_numpy_array(G),inner,middle,outer


# ------------------------------------------------
# Dynamics
# ------------------------------------------------
def kuramoto_step(theta,omega,A,K,dt):

    phase_diff = theta[:,None]-theta[None,:]
    coupling = np.sum(A*np.sin(-phase_diff),axis=1)

    return theta + dt*(omega + K/len(theta)*coupling)


# ------------------------------------------------
# Simulation
# ------------------------------------------------
def run_sim(K,drift,steps=2000,dt=0.02,seed=0):

    np.random.seed(seed)

    A,inner,middle,outer = build_graph()

    n=len(A)

    theta = np.random.uniform(0,2*np.pi,n)

    omega=np.zeros(n)

    omega[inner]  = +drift
    omega[middle] = 0
    omega[outer]  = -drift

    R_hist=[]

    for t in range(steps):

        theta = kuramoto_step(theta,omega,A,K,dt)

        if t>steps//2:
            R_hist.append(order_parameter(theta))

    return np.mean(R_hist), np.var(R_hist)


# ------------------------------------------------
# Scan
# ------------------------------------------------
def main():

    Path("output").mkdir(exist_ok=True)

    K_values = np.linspace(0.2,3.0,20)
    drift_values = np.linspace(0.05,0.3,20)

    R_map = np.zeros((len(K_values),len(drift_values)))
    V_map = np.zeros_like(R_map)

    for i,K in enumerate(K_values):
        for j,d in enumerate(drift_values):

            R,V = run_sim(K,d)

            R_map[i,j]=R
            V_map[i,j]=V

            print(f"K={K:.2f} drift={d:.2f} R={R:.3f}")

    plt.figure(figsize=(8,6))
    plt.imshow(R_map,origin="lower",aspect="auto",
               extent=[drift_values[0],drift_values[-1],
                       K_values[0],K_values[-1]])

    plt.colorbar(label="mean order parameter")
    plt.xlabel("drift")
    plt.ylabel("K")
    plt.title("Phase diagram: synchronization")

    plt.savefig("output/phase_diagram_R.png",dpi=300)
    plt.show()

    plt.figure(figsize=(8,6))
    plt.imshow(V_map,origin="lower",aspect="auto",
               extent=[drift_values[0],drift_values[-1],
                       K_values[0],K_values[-1]])

    plt.colorbar(label="R variance")
    plt.xlabel("drift")
    plt.ylabel("K")
    plt.title("Phase diagram: temporal variability")

    plt.savefig("output/phase_diagram_variance.png",dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
