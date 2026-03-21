import numpy as np
import json
import os
from datetime import datetime

# --------------------------------------------------
# METRICS
# --------------------------------------------------

def compute_entropy(field):
    """Shannon entropy"""
    p = field / (np.sum(field) + 1e-12)
    p = p + 1e-12
    return -np.sum(p * np.log(p))


def compute_spread(field):
    """Wie breit ist das Feld verteilt"""
    return np.std(field)


def compute_peak(field):
    """Max intensity"""
    return np.max(field)


def compute_center_of_mass(field):
    """Schwerpunkt"""
    size = field.shape[0]

    xs, ys = np.meshgrid(np.arange(size), np.arange(size), indexing='ij')
    total = np.sum(field) + 1e-12

    cx = np.sum(xs * field) / total
    cy = np.sum(ys * field) / total

    return np.array([cx, cy])


def compute_path_length(paths):
    """Durchschnittliche Weglänge"""
    lengths = []

    for path in paths:
        d = 0
        for i in range(1, len(path)):
            d += np.linalg.norm(path[i] - path[i-1])
        lengths.append(d)

    return float(np.mean(lengths))


def compute_switch_rate(paths_targets):
    """Wie oft Agenten Ziel wechseln"""

    switches = 0
    total = 0

    for targets in paths_targets:
        for i in range(1, len(targets)):
            if not np.array_equal(targets[i], targets[i-1]):
                switches += 1
            total += 1

    return switches / (total + 1e-6)


# --------------------------------------------------
# LOGGER
# --------------------------------------------------

def log_run(config, metrics, save_dir="ENGINE/logs"):

    os.makedirs(save_dir, exist_ok=True)

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    data = {
        "run_id": run_id,
        "config": config,
        "metrics": metrics
    }

    path = os.path.join(save_dir, f"{run_id}.json")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nSaved log → {path}")

    return path
