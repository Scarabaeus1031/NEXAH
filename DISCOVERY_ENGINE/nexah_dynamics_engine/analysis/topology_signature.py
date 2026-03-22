# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/topology_signature.py

import numpy as np
from collections import Counter


# --------------------------------------------------
# SIGNATURE CORE
# --------------------------------------------------

def normalize_distribution(d):
    total = sum(d.values()) + 1e-8
    return {k: v / total for k, v in d.items()}


def compute_signature(
    degree_dist,
    loop_sizes,
    channel_lengths,
    angle_hits
):
    """
    Build compact signature vector from topology metrics
    """

    # Degree distribution (normalized)
    deg_norm = normalize_distribution(degree_dist)

    # Loop statistics
    avg_loop = np.mean(loop_sizes) if len(loop_sizes) > 0 else 0
    std_loop = np.std(loop_sizes) if len(loop_sizes) > 0 else 0

    # Channel statistics
    avg_channel = np.mean(channel_lengths) if len(channel_lengths) > 0 else 0
    std_channel = np.std(channel_lengths) if len(channel_lengths) > 0 else 0

    # Angle normalization
    angle_norm = normalize_distribution(angle_hits)

    signature = {
        "degree_dist": deg_norm,
        "avg_loop": avg_loop,
        "std_loop": std_loop,
        "avg_channel": avg_channel,
        "std_channel": std_channel,
        "angle_profile": angle_norm
    }

    return signature


# --------------------------------------------------
# VECTORIZE SIGNATURE
# --------------------------------------------------

def signature_to_vector(signature):
    """
    Convert signature dict into numeric vector
    """

    vec = []

    # degree distribution (sorted keys)
    for k in sorted(signature["degree_dist"].keys()):
        vec.append(signature["degree_dist"][k])

    # loop stats
    vec.append(signature["avg_loop"])
    vec.append(signature["std_loop"])

    # channel stats
    vec.append(signature["avg_channel"])
    vec.append(signature["std_channel"])

    # angle profile (sorted)
    for k in sorted(signature["angle_profile"].keys()):
        vec.append(signature["angle_profile"][k])

    return np.array(vec)


# --------------------------------------------------
# COMPARISON
# --------------------------------------------------

def compare_signatures(sig1, sig2):
    """
    Compare two signatures via cosine similarity
    """

    v1 = signature_to_vector(sig1)
    v2 = signature_to_vector(sig2)

    # normalize
    v1 = v1 / (np.linalg.norm(v1) + 1e-8)
    v2 = v2 / (np.linalg.norm(v2) + 1e-8)

    similarity = np.dot(v1, v2)

    return similarity


# --------------------------------------------------
# INTERPRETATION
# --------------------------------------------------

def interpret_signature(signature):
    """
    Human-readable interpretation
    """

    print("\n--- TOPOLOGY SIGNATURE ---")

    print("\nDegree Distribution:")
    for k, v in signature["degree_dist"].items():
        print(f"  Degree {k}: {v:.3f}")

    print("\nLoop Size:")
    print(f"  Avg: {signature['avg_loop']:.2f}")
    print(f"  Std: {signature['std_loop']:.2f}")

    print("\nChannel Length:")
    print(f"  Avg: {signature['avg_channel']:.2f}")
    print(f"  Std: {signature['std_channel']:.2f}")

    print("\nAngle Profile:")
    for k, v in signature["angle_profile"].items():
        if v > 0:
            print(f"  {k}°: {v:.3f}")


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":
    print("Topology Signature Module Ready")
