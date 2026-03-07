"""
NEXAH MESO Layer

cascade_simulator.py

Simulate multiple cascade scenarios in the system graph.
"""

import random


def simulate_cascade(regime_map, start_state, max_steps=20):
    """
    Simulate a single cascade trajectory.

    Parameters
    ----------
    regime_map : dict
        regime graph structure

    start_state : str
        initial state

    max_steps : int
        maximum cascade length
    """

    graph = regime_map["graph"]

    current = start_state

    path = [current]

    for _ in range(max_steps):

        neighbors = list(graph.successors(current))

        if not neighbors:
            break

        next_state = random.choice(neighbors)

        path.append(next_state)

        current = next_state

    return path


def cascade_simulator(regime_map, start_state, runs=100):
    """
    Run multiple cascade simulations.

    Parameters
    ----------
    regime_map : dict
        regime graph

    start_state : str

    runs : int
        number of simulations
    """

    cascades = []

    for _ in range(runs):

        path = simulate_cascade(regime_map, start_state)

        cascades.append(path)

    return {
        "start_state": start_state,
        "runs": runs,
        "cascades": cascades
    }
