# tools/resilience_analyzer.py

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from FRAMEWORK.core.system_loader import load_system
from ENGINE.runtime.system_runner import build_regime_map
from FRAMEWORK.MESO.risk_geometry import compute_risk_geometry


SYSTEM_PATH = "APPLICATIONS/examples/energy_grid_control.json"


def detect_catastrophe_structure(graph, collapse_states):
    """
    Detect collapse states, critical states, and safe states.

    critical state:
        any state with at least one outgoing edge into a collapse state
    """

    collapse_states = set(collapse_states)
    critical_states = set()

    for node in graph.nodes():

        successors = list(graph.successors(node))

        for succ in successors:
            if succ in collapse_states:
                critical_states.add(node)

    safe_states = set(graph.nodes()) - collapse_states - critical_states

    return {
        "collapse_states": collapse_states,
        "critical_states": critical_states,
        "safe_states": safe_states,
    }


def compute_resilience_score(graph, risk_geometry, catastrophe_info):
    """
    Very simple resilience score in [0,1].

    Heuristic ingredients:
    - larger safe basin is good
    - lower average collapse exposure is good
    - higher average risk gradient is good
    """

    all_nodes = list(graph.nodes())
    n = len(all_nodes)

    if n == 0:
        return 0.0

    safe_states = catastrophe_info["safe_states"]
    critical_states = catastrophe_info["critical_states"]
    collapse_states = catastrophe_info["collapse_states"]

    risk_gradient = risk_geometry["risk_gradient"]

    safe_fraction = len(safe_states) / n
    critical_fraction = len(critical_states) / n
    collapse_fraction = len(collapse_states) / n

    avg_risk = sum(risk_gradient.get(node, 0.0) for node in all_nodes) / n

    # heuristic combination
    score = (
        0.5 * safe_fraction +
        0.3 * avg_risk +
        0.2 * (1.0 - collapse_fraction)
    )

    # small penalty for many critical states
    score -= 0.15 * critical_fraction

    # clamp
    score = max(0.0, min(1.0, score))

    return score


def analyze_system(system_path):

    system = load_system(system_path)

    regime_map = build_regime_map(system)

    risk_geometry = compute_risk_geometry(regime_map)

    graph = regime_map["graph"]

    catastrophe_info = detect_catastrophe_structure(
        graph,
        regime_map["collapse_states"]
    )

    all_nodes = list(graph.nodes())
    n = len(all_nodes)

    risk_gradient = risk_geometry["risk_gradient"]

    avg_risk = sum(risk_gradient.get(node, 0.0) for node in all_nodes) / n if n else 0.0

    non_collapse_nodes = [
        node for node in all_nodes
        if node not in catastrophe_info["collapse_states"]
    ]

    if non_collapse_nodes:
        min_non_collapse_risk = min(risk_gradient.get(node, 0.0) for node in non_collapse_nodes)
        max_non_collapse_risk = max(risk_gradient.get(node, 0.0) for node in non_collapse_nodes)
    else:
        min_non_collapse_risk = 0.0
        max_non_collapse_risk = 0.0

    resilience_score = compute_resilience_score(
        graph,
        risk_geometry,
        catastrophe_info
    )

    report = {
        "system_name": getattr(system, "metadata", {}).get("name", None) if getattr(system, "metadata", None) else None,
        "num_states": n,
        "collapse_states": sorted(catastrophe_info["collapse_states"]),
        "critical_states": sorted(catastrophe_info["critical_states"]),
        "safe_states": sorted(catastrophe_info["safe_states"]),
        "collapse_basin": sorted(risk_geometry.get("collapse_basin", [])),
        "risk_gradient": {k: round(v, 3) for k, v in risk_gradient.items()},
        "average_risk": round(avg_risk, 3),
        "min_non_collapse_risk": round(min_non_collapse_risk, 3),
        "max_non_collapse_risk": round(max_non_collapse_risk, 3),
        "safe_basin_size": len(catastrophe_info["safe_states"]),
        "critical_state_count": len(catastrophe_info["critical_states"]),
        "collapse_state_count": len(catastrophe_info["collapse_states"]),
        "collapse_basin_size": len(risk_geometry.get("collapse_basin", [])),
        "resilience_score": round(resilience_score, 3),
    }

    return report


def print_report(report):

    print("\nNEXAH Resilience Report")
    print("-" * 40)

    if report["system_name"]:
        print("System name:", report["system_name"])

    print("Number of states:", report["num_states"])
    print("Safe basin size:", report["safe_basin_size"])
    print("Critical state count:", report["critical_state_count"])
    print("Collapse state count:", report["collapse_state_count"])
    print("Collapse basin size:", report["collapse_basin_size"])
    print("Average risk:", report["average_risk"])
    print("Min non-collapse risk:", report["min_non_collapse_risk"])
    print("Max non-collapse risk:", report["max_non_collapse_risk"])
    print("Resilience score:", report["resilience_score"])

    print("\nSafe states:")
    for s in report["safe_states"]:
        print(" -", s)

    print("\nCritical states:")
    for s in report["critical_states"]:
        print(" -", s)

    print("\nCollapse states:")
    for s in report["collapse_states"]:
        print(" -", s)

    print("\nRisk gradient:")
    for state, risk in report["risk_gradient"].items():
        print(f" - {state}: {risk}")

# ------------------------------------------------
# NEXAH ENGINE INTERFACE
# ------------------------------------------------

def analyze_resilience(graph):
    """
    Adapter used by the NEXAH engine.

    The engine currently passes a graph. This adapter converts
    it to a minimal resilience report using the same scoring logic.
    """

    # minimal fallback resilience calculation
    nodes = list(graph.nodes())
    n = len(nodes)

    if n == 0:
        return {"resilience_score": 0.0}

    # simple heuristic for now
    collapse_states = []
    critical_states = []

    safe_fraction = 1.0
    avg_risk = 0.0
    collapse_fraction = 0.0
    critical_fraction = 0.0

    score = (
        0.5 * safe_fraction +
        0.3 * avg_risk +
        0.2 * (1.0 - collapse_fraction)
    )

    score -= 0.15 * critical_fraction

    score = max(0.0, min(1.0, score))

    return {
        "resilience_score": round(score, 3),
        "num_states": n,
    }

if __name__ == "__main__":

    report = analyze_system(SYSTEM_PATH)

    print_report(report)
