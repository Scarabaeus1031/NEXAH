import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
# -----------------------------

K = 1.5
dt = 0.05
T = 20

# -----------------------------
# Order parameter
# -----------------------------

def order_parameter(theta):
    return np.abs(np.mean(np.exp(1j * theta)))

# -----------------------------
# Kuramoto simulation
# -----------------------------

def simulate_kuramoto(G):

    nodes = list(G.nodes)
    N = len(nodes)

    theta = np.random.uniform(0, 2*np.pi, N)

    steps = int(T/dt)

    R_values = []

    for step in range(steps):

        dtheta = np.zeros(N)

        for i, ni in enumerate(nodes):
            for j, nj in enumerate(nodes):

                if G.has_edge(ni, nj):
                    dtheta[i] += np.sin(theta[j] - theta[i])

        theta += dt * K * dtheta

        R_values.append(order_parameter(theta))

    return R_values

# -----------------------------
# Graph definitions
# -----------------------------

def ring_graph():
    return nx.cycle_graph(18)

def random_graph():
    return nx.gnm_random_graph(18, 30)

def star_graph():
    G = nx.Graph()
    center = 0
    G.add_node(center)

    for i in range(1,18):
        G.add_edge(center,i)

    return G

def symmetry_graph():

    G = nx.Graph()
    center = 0
    G.add_node(center)

    spokes = list(range(1,18))

    for s in spokes:
        G.add_edge(center,s)

    pent = spokes[0:5]
    for i in range(5):
        G.add_edge(pent[i], pent[(i+1)%5])

    hex1 = spokes[5:11]
    for i in range(6):
        G.add_edge(hex1[i], hex1[(i+1)%6])

    hex2 = spokes[11:17]
    for i in range(6):
        G.add_edge(hex2[i], hex2[(i+1)%6])

    return G

# -----------------------------
# Run simulations
# -----------------------------

graphs = {
    "Ring": ring_graph(),
    "Random": random_graph(),
    "Star": star_graph(),
    "Symmetry (5+6+6)": symmetry_graph()
}

plt.figure(figsize=(8,5))

for name,G in graphs.items():

    R = simulate_kuramoto(G)

    t = np.arange(len(R))*dt

    plt.plot(t,R,label=name)

# -----------------------------
# Plot
# -----------------------------

plt.xlabel("Time")
plt.ylabel("Order Parameter R(t)")
plt.title("Kuramoto Synchronization Evolution")

plt.legend()

plt.tight_layout()

plt.savefig("phase_lock_evolution.png",dpi=300)

print("Saved: phase_lock_evolution.png")

plt.show()
