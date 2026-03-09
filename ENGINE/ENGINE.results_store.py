"""
NEXAH Results Store

Stores experiment results produced by the NEXAH discovery engine.
"""

import os
import json
from datetime import datetime


RESULT_DIR = "results"


def ensure_results_dir():

    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)


def _serialize(obj):

    """
    Convert objects into JSON serializable structures.
    """

    try:
        import networkx as nx
    except ImportError:
        nx = None

    # Graphs
    if nx and isinstance(obj, (nx.Graph, nx.DiGraph)):
        return {
            "nodes": list(obj.nodes()),
            "edges": list(obj.edges())
        }

    # Sets
    if isinstance(obj, set):
        return list(obj)

    # Dict
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}

    # List
    if isinstance(obj, list):
        return [_serialize(v) for v in obj]

    # Primitive JSON types
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj

    # Fallback for custom objects (like NexahSystem)
    return str(obj)


def store_result(result, experiment_id=None):

    ensure_results_dir()

    if experiment_id is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"experiment_{timestamp}.json"
    else:
        filename = f"experiment_{experiment_id:04d}.json"

    path = os.path.join(RESULT_DIR, filename)

    result_serialized = _serialize(result)

    with open(path, "w") as f:
        json.dump(result_serialized, f, indent=2)

    print(f"Result stored: {path}")

    return path


def load_all_results():

    ensure_results_dir()

    results = []

    for file in sorted(os.listdir(RESULT_DIR)):

        if not file.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, file)

        with open(path, "r") as f:
            results.append(json.load(f))

    return results
def load_all_results():

    ensure_results_dir()

    results = []

    for file in sorted(os.listdir(RESULT_DIR)):

        if not file.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, file)

        with open(path, "r") as f:
            results.append(json.load(f))

    return results
