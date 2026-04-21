import numpy as np
import networkx as nx


def wrap_phase(angle):
    """
    Wrap phase difference to [-pi, pi]
    """
    return (angle + np.pi) % (2 * np.pi) - np.pi


def phase_winding(theta, cycle):
    """
    Compute winding number for a given cycle.

    Parameters
    ----------
    theta : array-like
        Phase values for each node
    cycle : list
        Node indices forming a loop

    Returns
    -------
    float
        Winding number
    """

    total = 0.0

    for i in range(len(cycle)):

        a = cycle[i]
        b = cycle[(i + 1) % len(cycle)]

        dtheta = wrap_phase(theta[b] - theta[a])
        total += dtheta

    return total / (2 * np.pi)


def find_triangle_vortices(G, theta, threshold=0.5):
    """
    Detect vortices on triangle cycles of the graph.

    Parameters
    ----------
    G : networkx.Graph
        Graph structure
    theta : array-like
        Phase values for nodes
    threshold : float
        Minimum winding magnitude to count as vortex

    Returns
    -------
    list
        List of detected vortices (triangle, winding)
    """

    vortices = []

    cycles = nx.cycle_basis(G)

    for cycle in cycles:

        if len(cycle) == 3:

            w = phase_winding(theta, cycle)

            if abs(w) > threshold:
                vortices.append((cycle, w))

    return vortices


def example_test():
    """
    Simple internal test for vortex detection
    """

    G = nx.Graph()

    G.add_edges_from([
        (0, 1),
        (1, 2),
        (2, 0)
    ])

    theta = np.array([
        0,
        2*np.pi/3,
        4*np.pi/3
    ])

    vortices = find_triangle_vortices(G, theta)

    print("Detected vortices:")
    for tri, w in vortices:
        print("triangle:", tri, "winding:", w)


if __name__ == "__main__":
    example_test()
