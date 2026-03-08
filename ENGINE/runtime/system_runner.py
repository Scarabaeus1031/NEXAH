# ENGINE/runtime/system_runner.py

import networkx as nx

from FRAMEWORK.core.system_loader import load_system
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry
from FRAMEWORK.NEXAH.navigation_policy import select_safest_transition
from FRAMEWORK.MEVA.execution_engine import ExecutionEngine


# ---------------------------------------------------------
# BUILD REGIME MAP
# ---------------------------------------------------------

def build_regime_map(system):

    graph = nx.DiGraph()

    # Build transition graph
    for s, t in system.transitions.items():
        graph.add_edge(s, t)

    # Detect collapse states robustly
    collapse_states = {
        s for s, r in system.regimes.items()
        if r.lower() in ["collapse", "failure", "blackout", "terminal"]
    }

    # Fallback: use risk_target if no collapse states detected
    if not collapse_states and system.risk_target:

        if system.risk_target not in graph:
            raise ValueError(
                f"Risk target '{system.risk_target}' not present in system states"
            )

        collapse_states = {system.risk_target}

    # Final safety check
    if not collapse_states:
        raise ValueError(
            f"No collapse states detected.\n"
            f"Regimes found: {system.regimes}"
        )

    return {
        "graph": graph,
        "collapse_states": collapse_states
    }


# ---------------------------------------------------------
# RUN SYSTEM SIMULATION
# ---------------------------------------------------------

def run_system(system_path, start_state, steps=20):

    # Load system definition
    system = load_system(system_path)

    # Build regime map
    regime_map = build_regime_map(system)

    # Compute MESO risk geometry
    risk_geometry = compute_risk_geometry(regime_map)

    # Initialize execution engine
    engine = ExecutionEngine(regime_map, risk_geometry)

    engine.set_initial_state(start_state)

    # Navigation policy wrapper
    def policy(state):

        return select_safest_transition(
            state,
            regime_map,
            risk_geometry
        )

    # Run simulation
    trajectory = engine.run(policy, max_steps=steps)

    return trajectory
