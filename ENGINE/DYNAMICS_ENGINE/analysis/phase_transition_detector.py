# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/phase_transition_detector.py

import numpy as np


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

CONFIDENCE_JUMP_THRESHOLD = 0.20
SIGNATURE_DISTANCE_THRESHOLD = 0.15
MIN_TRANSITION_GAP = 1


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def signature_to_vector(signature):
    """
    Convert signature dict into a numeric vector.
    """
    vec = []

    degree_dist = signature.get("degree_dist", {})
    angle_profile = signature.get("angle_profile", {})

    # degree distribution
    for k in sorted(degree_dist.keys()):
        vec.append(float(degree_dist[k]))

    # scalar metrics
    vec.append(float(signature.get("avg_loop", 0.0)))
    vec.append(float(signature.get("std_loop", 0.0)))
    vec.append(float(signature.get("avg_channel", 0.0)))
    vec.append(float(signature.get("std_channel", 0.0)))

    # angle profile
    for k in sorted(angle_profile.keys()):
        vec.append(float(angle_profile[k]))

    return np.array(vec, dtype=float)


def compute_signature_distance(sig1, sig2):
    """
    Euclidean distance between two signatures
    """
    v1 = signature_to_vector(sig1)
    v2 = signature_to_vector(sig2)

    # align length (important!)
    min_len = min(len(v1), len(v2))
    v1 = v1[:min_len]
    v2 = v2[:min_len]

    return np.linalg.norm(v1 - v2)


# --------------------------------------------------
# TRANSITION DETECTION
# --------------------------------------------------

def detect_phase_transitions(results):
    """
    results: list of dicts:
        {
            "params": {...},
            "classification": "...",
            "signature": {...}
        }
    """

    transitions = []

    last_transition_idx = -MIN_TRANSITION_GAP - 1

    for i in range(1, len(results)):

        prev = results[i - 1]
        curr = results[i]

        prev_class = prev.get("classification")
        curr_class = curr.get("classification")

        prev_sig = prev.get("signature", {})
        curr_sig = curr.get("signature", {})

        # --------------------------------------------------
        # 1. CLASS CHANGE
        # --------------------------------------------------

        class_changed = prev_class != curr_class

        # --------------------------------------------------
        # 2. SIGNATURE DISTANCE
        # --------------------------------------------------

        distance = compute_signature_distance(prev_sig, curr_sig)
        strong_shift = distance > SIGNATURE_DISTANCE_THRESHOLD

        # --------------------------------------------------
        # 3. OPTIONAL CONFIDENCE CHECK
        # --------------------------------------------------

        prev_conf = prev.get("confidence", 0.0)
        curr_conf = curr.get("confidence", 0.0)

        confidence_jump = abs(curr_conf - prev_conf) > CONFIDENCE_JUMP_THRESHOLD

        # --------------------------------------------------
        # DECISION
        # --------------------------------------------------

        if (class_changed or strong_shift or confidence_jump):

            # avoid too dense transitions
            if i - last_transition_idx < MIN_TRANSITION_GAP:
                continue

            transition = {
                "index": i,
                "from": prev_class,
                "to": curr_class,
                "signature_distance": float(distance),
                "confidence_jump": float(abs(curr_conf - prev_conf)),
                "params_before": prev.get("params", {}),
                "params_after": curr.get("params", {})
            }

            transitions.append(transition)
            last_transition_idx = i

    return transitions


# --------------------------------------------------
# ANALYSIS WRAPPER
# --------------------------------------------------

def analyze_phase_space(results):

    transitions = detect_phase_transitions(results)

    print("\n--- PHASE TRANSITIONS ---")

    if len(transitions) == 0:
        print("No transitions detected.")
        return transitions

    for t in transitions:
        print("\nTransition @ index", t["index"])
        print("  From:", t["from"])
        print("  To  :", t["to"])
        print("  Signature Δ:", round(t["signature_distance"], 4))
        print("  Confidence Δ:", round(t["confidence_jump"], 4))
        print("  Params before:", t["params_before"])
        print("  Params after :", t["params_after"])

    return transitions


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    print("Phase Transition Detector Ready")
