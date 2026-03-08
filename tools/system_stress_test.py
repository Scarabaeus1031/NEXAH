# tools/system_stress_test.py

import sys
import os
import random

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import matplotlib.pyplot as plt
import numpy as np

from FRAMEWORK.core.system_loader import load_system
from ENGINE.runtime.system_runner import build_regime_map
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry
from FRAMEWORK.NEXAH.navigation_policy import select_safest_transition


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


def noisy_policy(state, graph, regime_map, risk_geometry, noise):

    successors = list(graph.successors(state))

    if not successors:
        return state

    # with probability "noise" choose random action
    if random.random() < noise:
        return random.choice(successors)

    return select_safest_transition(
        state,
        regime_map,
        risk_geometry
    )


def run_trial(graph, regime_map, risk_geometry, start_state, collapse_states, noise, steps=20):

    state = start_state

    for _ in range(steps):

        state = noisy_policy(
            state,
            graph,
            regime_map,
            risk_geometry,
            noise
        )

        if state in collapse_states:
            return True

    return False


def stress_test(num_agents=500):

    system = load_system(SYSTEM_PATH)

    regime_map = build_regime_map(system)

    risk_geometry = compute_risk_geometry(regime_map)

    graph = regime_map["graph"]

    collapse_states = regime_map["collapse_states"]

    start_state = system.nodes[0]

    noise_levels = np.linspace(0, 1, 15)

    collapse_probabilities = []

    for noise in noise_levels:

        collapse_count = 0

        for _ in range(num_agents):

            if run_trial(
                graph,
                regime_map,
                risk_geometry,
                start_state,
                collapse_states,
                noise
            ):
                collapse_count += 1

        collapse_prob = collapse_count / num_agents

        collapse_probabilities.append(collapse_prob)

        print(f"noise={noise:.2f} collapse={collapse_prob:.3f}")

    return noise_levels, collapse_probabilities


def visualize(noise_levels, collapse_probabilities):

    plt.figure(figsize=(8,6))

    plt.plot(
        noise_levels,
        collapse_probabilities,
        marker="o"
    )

    plt.xlabel("Agent Noise Level")

    plt.ylabel("Collapse Probability")

    plt.title("NEXAH System Stress Test")

    plt.ylim(0,1)

    plt.grid(True)

    plt.show()


if __name__ == "__main__":

    noise_levels, collapse_probabilities = stress_test()

    visualize(noise_levels, collapse_probabilities)
