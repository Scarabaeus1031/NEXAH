import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def kuramoto_step(theta, omega, A, K, dt):

    phase_diff = theta[:, None] - theta[None, :]
    coupling = np.sum(A * np.sin(-phase_diff), axis=1)

    dtheta = omega + (K / len(theta)) * coupling

    return theta + dt * dtheta


def build_hub_ring(N):

    G = nx.Graph()

    center = 0

    for i in range(1, N+1):
        G.add_edge(center, i)

    for i in range(1, N+1):
        G.add_edge(i, 1 + (i % N))

    return G


def simulate(N, steps=4000, dt=0.02, K=1.0):

    G = build_hub_ring(N)
    A = nx.to_numpy_array(G)

    nodes = len(A)

    theta = np.random.uniform(0, 2*np.pi, nodes)
    omega = np.random.normal(0, 0.1, nodes)

    for t in range(steps):

        theta = kuramoto_step(theta, omega, A, K, dt)

    return theta


def plot_ring(theta):

    ring_theta = theta[1:]
    N = len(ring_theta)

    angles = np.linspace(0, 2*np.pi, N, endpoint=False)

    x = np.cos(angles)
    y = np.sin(angles)

    colors = (ring_theta % (2*np.pi)) / (2*np.pi)

    plt.figure(figsize=(6,6))

    plt.scatter(x, y, c=colors, cmap="hsv", s=120)

    for i in range(N):

        plt.text(x[i]*1.1, y[i]*1.1, str(i+1))

    plt.gca().set_aspect('equal')
    plt.title("Ring Phase Configuration")

    plt.show()


def main():

    N = 60

    theta = simulate(N)

    plot_ring(theta)


if __name__ == "__main__":
    main()
