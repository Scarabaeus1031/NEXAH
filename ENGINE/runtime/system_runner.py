# ENGINE/runtime/system_runner.py

import networkx as nx

from FRAMEWORK.core.system_loader import load_system
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry
from FRAMEWORK.NEXAH.navigation_policy import select_safest_transition
from FRAMEWORK.MEVA.execution_engine import ExecutionEngine


def build_regime_map(system):

    graph = nx.DiGraph()

    # -------------------------------------------------
    # ADD NODES
    # -------------------------------------------------

    for node in system.nodes:
        graph.add_node(node)

    # -------------------------------------------------
    # ADD TRANSITIONS
    # -------------------------------------------------

    for s, t in system.transitions.items():

        if isinstance(t, list):
            for target in t:
                graph.add_edge(s, target)
        else:
            graph.add_edge(s, t)

    # -------------------------------------------------
    # DETECT COLLAPSE STATES
    # -------------------------------------------------

    collapse_states = set()

    for state, regime in system.regimes.items():

        r = str(regime).lower()

        if r in ["collapse", "critical", "failure", "blackout"]:
            collapse_states.add(state)

    return {
        "graph": graph,
        "collapse_states": collapse_states
    }


def run_system(system_path, start_state, steps=20):

    system = load_system(system_path)

    regime_map = build_regime_map(system)

    risk_geometry = compute_risk_geometry(regime_map)

    engine = ExecutionEngine(regime_map, risk_geometry)

    engine.set_initial_state(start_state)

    def policy(state):

        return select_safest_transition(
            state,
            regime_map,
            risk_geometry
        )

    trajectory = engine.run(policy, max_steps=steps)

    return trajectory
