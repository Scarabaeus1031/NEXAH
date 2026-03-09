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

    # networkx graphs
    if nx and isinstance(obj, (nx.Graph, nx.DiGraph)):
        return {
            "nodes": list(obj.nodes()),
            "edges": list(obj.edges())
        }

    # sets
    if isinstance(obj, set):
        return list(obj)

    # objects with __dict__
    if hasattr(obj, "__dict__"):
        return obj.__dict__

    # fallback
    return str(obj)


def store_result(result, experiment_id=None):

    ensure_results_dir()

    if experiment_id is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"experiment_{timestamp}.json"
    else:
        filename = f"experiment_{experiment_id:04d}.json"

    path = os.path.join(RESULT_DIR, filename)

    with open(path, "w") as f:
        json.dump(result, f, indent=2, default=_serialize)

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
