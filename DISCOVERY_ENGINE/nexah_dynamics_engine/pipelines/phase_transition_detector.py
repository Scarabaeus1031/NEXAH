# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/phase_transition_detector.py

import numpy as np


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

CONFIDENCE_JUMP_THRESHOLD = 0.20
SIGNATURE_DISTANCE_THRESHOLD = 0.15
MIN_TRANSITION_GAP = 1


# --------------------------------------------------
# SIGNATURE → VECTOR
# --------------------------------------------------

def signature_to_vector(signature):
    vec = []

    # degree distribution
    degree_dist = signature.get("degree_dist", {})
    for k in sorted(degree_dist.keys()):
        vec.append(float(degree_dist[k]))

    # scalar metrics
    vec.append(float(signature.get("avg_loop", 0.0)))
    vec.append(float(signature.get("std_loop", 0.0)))
    vec.append(float(signature.get("avg_channel", 0.0)))
    vec.append(float(signature.get("std_channel", 0.0)))

    # angle profile
    angle_profile = signature.get("angle_profile", {})
    for k in sorted(angle_profile.keys()):
        vec.append(float(angle_profile[k]))

    return np.array(vec)


# --------------------------------------------------
# DISTANCE
# --------------------------------------------------

def signature_distance(sig1, sig2):
    v1 = signature_to_vector(sig1)
    v2 = signature_to_vector(sig2)

    # gleiche Länge erzwingen
    max_len = max(len(v1), len(v2))

    v1 = np.pad(v1, (0, max_len - len(v1)))
    v2 = np.pad(v2, (0, max_len - len(v2)))

    return np.linalg.norm(v1 - v2)


# --------------------------------------------------
# MAIN DETECTOR
# --------------------------------------------------

def detect_phase_transitions(results_grid):
    """
    results_grid: 2D array of pipeline results
    """

    transitions = []

    rows = len(results_grid)
    cols = len(results_grid[0])

    for i in range(rows):
        for j in range(cols):

            current = results_grid[i][j]
            sig_current = current["signature"]

            # RIGHT neighbor
            if j < cols - 1:
                neighbor = results_grid[i][j + 1]
                dist = signature_distance(sig_current, neighbor["signature"])

                if dist > SIGNATURE_DISTANCE_THRESHOLD:
                    transitions.append({
                        "from": (i, j),
                        "to": (i, j + 1),
                        "distance": float(dist),
                        "type": "horizontal"
                    })

            # DOWN neighbor
            if i < rows - 1:
                neighbor = results_grid[i + 1][j]
                dist = signature_distance(sig_current, neighbor["signature"])

                if dist > SIGNATURE_DISTANCE_THRESHOLD:
                    transitions.append({
                        "from": (i, j),
                        "to": (i + 1, j),
                        "distance": float(dist),
                        "type": "vertical"
                    })

    return transitions


# --------------------------------------------------
# INTERPRETATION
# --------------------------------------------------

def interpret_transitions(transitions):

    print("\n--- PHASE TRANSITIONS ---")

    if len(transitions) == 0:
        print("No strong transitions detected.")
        return

    for t in transitions:
        print(
            f"{t['type'].upper()} | {t['from']} → {t['to']} | Δ = {t['distance']:.3f}"
        )
