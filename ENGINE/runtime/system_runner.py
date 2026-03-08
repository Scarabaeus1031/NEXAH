# ENGINE/runtime/system_runner.py

import networkx as nx

from FRAMEWORK.core.system_loader import load_system
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry
from FRAMEWORK.NEXAH.navigation_policy import select_safest_transition
from FRAMEWORK.MEVA.execution_engine import ExecutionEngine


def build_regime_map(system):

    graph = nx.DiGraph()

    for s, targets in system.transitions.items():

        if isinstance(targets, list):

            for t in targets:
                graph.add_edge(s, t)

        else:
            graph.add_edge(s, targets)

    collapse_states = {
        s for s, r in system.regimes.items()
        if r.lower() in ["collapse", "failure", "blackout"]
    }

    if not collapse_states and system.risk_target:
        collapse_states = {system.risk_target}

    if not collapse_states:
        raise ValueError(
            f"No collapse states detected in regimes: {system.regimes}"
        )

    return {
        "graph": graph,
        "collapse_states": collapse_states
    }


def run_system(system_path, start_state=None, steps=20):

    system = load_system(system_path)

    regime_map = build_regime_map(system)

    graph = regime_map["graph"]

    if start_state is None:
        start_state = list(graph.nodes)[0]

    if start_state not in graph:
        raise ValueError(
            f"Start state '{start_state}' not found.\n"
            f"Available states: {list(graph.nodes)}"
        )

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
