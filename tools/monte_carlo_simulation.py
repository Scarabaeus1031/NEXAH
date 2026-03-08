import sys
import os
import random

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import matplotlib.pyplot as plt

from FRAMEWORK.core.system_loader import load_system
from ENGINE.runtime.system_runner import build_regime_map
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry
from FRAMEWORK.NEXAH.navigation_policy import select_safest_transition


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


def random_walk(system, graph, start_state, collapse_states, steps=20):

    state = start_state

    for _ in range(steps):

        successors = list(graph.successors(state))

        if not successors:
            return state

        probs = None
        if hasattr(system, "probabilities"):
            probs = system.probabilities.get(state)

        if probs:
            state = random.choices(successors, probs)[0]
        else:
            state = random.choice(successors)

        if state in collapse_states:
            return state

    return state


def policy_walk(graph, regime_map, risk_geometry, start_state, collapse_states, steps=20):

    state = start_state

    for _ in range(steps):

        state = select_safest_transition(
            state,
            regime_map,
            risk_geometry
        )

        if state in collapse_states:
            return state

    return state


def run_experiment(num_agents=500):

    system = load_system(SYSTEM_PATH)

    regime_map = build_regime_map(system)

    risk_geometry = compute_risk_geometry(regime_map)

    graph = regime_map["graph"]

    collapse_states = regime_map["collapse_states"]

    start_state = system.nodes[0]

    collapse_random = 0
    collapse_policy = 0

    for _ in range(num_agents):

        end_state = random_walk(
            system,
            graph,
            start_state,
            collapse_states
        )

        if end_state in collapse_states:
            collapse_random += 1

    for _ in range(num_agents):

        end_state = policy_walk(
            graph,
            regime_map,
            risk_geometry,
            start_state,
            collapse_states
        )

        if end_state in collapse_states:
            collapse_policy += 1

    return collapse_random, collapse_policy, num_agents


def visualize(random_collapse, policy_collapse, total):

    labels = ["Random Navigation", "NEXAH Policy"]

    collapse_rates = [
        random_collapse / total,
        policy_collapse / total
    ]

    plt.figure(figsize=(6,5))

    plt.bar(labels, collapse_rates)

    plt.ylabel("Collapse Probability")

    plt.title("Monte Carlo Collapse Simulation")

    plt.ylim(0,1)

    for i, v in enumerate(collapse_rates):
        plt.text(i, v + 0.02, f"{v:.2f}", ha="center")

    plt.show()


if __name__ == "__main__":

    random_collapse, policy_collapse, total = run_experiment(1000)

    print("Random collapse:", random_collapse / total)
    print("Policy collapse:", policy_collapse / total)

    visualize(random_collapse, policy_collapse, total)
