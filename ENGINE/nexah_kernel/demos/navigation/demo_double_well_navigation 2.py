"""
NEXAH Demo — Double Well Regime Navigation

This demo illustrates navigation between attractor basins
in a double-well energy landscape.

The system evolves according to a stochastic differential equation
in a double-well potential:

    V(x) = x^4 - x^2

The two wells correspond to two stable regimes.

The NEXAH kernel detects the regime, analyzes reachable regimes,
and proposes possible interventions.
"""

import numpy as np

from ENGINE.nexah_kernel.regime.regime_detector import RegimeDetector
from ENGINE.nexah_kernel.regime.regime_graph import RegimeGraph
from ENGINE.nexah_kernel.regime.transition_detector import TransitionDetector

from ENGINE.nexah_kernel.navigation.navigator import Navigator
from ENGINE.nexah_kernel.navigation.intervention_planner import InterventionPlanner


# ---------------------------------------------------------
# double well dynamics
# ---------------------------------------------------------

def simulate_double_well(steps=200, dt=0.05):

    x = 0.5
    series = []

    for _ in range(steps):

        # gradient of potential
        grad = 4 * x**3 - 2 * x

        noise = np.random.normal(0, 0.3)

        x = x - grad * dt + noise * np.sqrt(dt)

        series.append(x)

    return series


# ---------------------------------------------------------
# run system
# ---------------------------------------------------------

series = simulate_double_well()


# ---------------------------------------------------------
# regime detection
# ---------------------------------------------------------

detector = RegimeDetector()

regime = detector.detect(series)

print("\nDetected regime:", regime)


# ---------------------------------------------------------
# transition detection
# ---------------------------------------------------------

transition_detector = TransitionDetector()

transition = transition_detector.detect(series)

print("Transition detected:", transition)


# ---------------------------------------------------------
# regime graph
# ---------------------------------------------------------

graph = RegimeGraph()

graph.add_regime("LEFT_WELL")
graph.add_regime("RIGHT_WELL")
graph.add_regime("BARRIER")

graph.add_transition("LEFT_WELL", "BARRIER")
graph.add_transition("BARRIER", "RIGHT_WELL")
graph.add_transition("RIGHT_WELL", "BARRIER")
graph.add_transition("BARRIER", "LEFT_WELL")


# ---------------------------------------------------------
# navigation
# ---------------------------------------------------------

navigator = Navigator(graph)

reachable = navigator.reachable_regimes(regime)

print("\nReachable regimes:", reachable)


# ---------------------------------------------------------
# intervention planning
# ---------------------------------------------------------

actions = [

    {"name": "push_right", "from": "LEFT_WELL", "to": "BARRIER"},
    {"name": "push_left", "from": "RIGHT_WELL", "to": "BARRIER"},
    {"name": "stabilize_left", "from": "BARRIER", "to": "LEFT_WELL"},
    {"name": "stabilize_right", "from": "BARRIER", "to": "RIGHT_WELL"}

]

planner = InterventionPlanner(actions)

target = "LEFT_WELL"

action = planner.plan(regime, target)

print("\nSuggested intervention:", action)
