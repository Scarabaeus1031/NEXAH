"""
NEXAH Demo — Regime Navigation

This demo illustrates the core idea of the NEXAH kernel:

    system → regimes → navigation → intervention

A simple stochastic dynamical system is simulated.
The system time series is analyzed to detect its regime.
Possible regime transitions are identified and the NEXAH
navigation layer computes reachable regimes and possible
interventions.

This demo serves as a minimal integration example for:

- regime detection
- transition detection
- regime graph construction
- navigation analysis
- intervention planning
"""

import numpy as np

from ENGINE.nexah_kernel.regime.regime_detector import RegimeDetector
from ENGINE.nexah_kernel.regime.regime_graph import RegimeGraph
from ENGINE.nexah_kernel.regime.transition_detector import TransitionDetector

from ENGINE.nexah_kernel.navigation.navigator import Navigator
from ENGINE.nexah_kernel.navigation.intervention_planner import InterventionPlanner


# ---------------------------------------------------------
# simple dynamical system
# ---------------------------------------------------------

def simulate_system(steps=50):

    x = 0.0
    series = []

    for t in range(steps):

        noise = np.random.normal(0, 0.1)
        x = x + noise

        # artificial instability
        if t > 30:
            x += np.random.normal(0, 0.8)

        series.append(x)

    return series


# ---------------------------------------------------------
# run system
# ---------------------------------------------------------

series = simulate_system()


# ---------------------------------------------------------
# regime detection
# ---------------------------------------------------------

detector = RegimeDetector()

regime = detector.detect(series)

print("\nCurrent regime:", regime)


# ---------------------------------------------------------
# transition detection
# ---------------------------------------------------------

transition_detector = TransitionDetector()

transition = transition_detector.detect(series)

print("Transition detected:", transition)


# ---------------------------------------------------------
# build regime graph
# ---------------------------------------------------------

graph = RegimeGraph()

graph.add_regime("STABLE")
graph.add_regime("OSCILLATORY")
graph.add_regime("CHAOTIC")

graph.add_transition("STABLE", "OSCILLATORY")
graph.add_transition("OSCILLATORY", "CHAOTIC")


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

    {"name": "damp_system", "from": "CHAOTIC", "to": "OSCILLATORY"},
    {"name": "stabilize", "from": "OSCILLATORY", "to": "STABLE"}

]

planner = InterventionPlanner(actions)

action = planner.plan(regime, "STABLE")

print("\nSuggested intervention:", action)
