# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/topology_signature.py

import numpy as np


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def normalize_distribution(d):
    total = sum(d.values()) + 1e-8
    return {k: v / total for k, v in d.items()}


# --------------------------------------------------
# ORIGINAL SIGNATURE (DEIN SYSTEM)
# --------------------------------------------------

def compute_signature(
    degree_dist,
    loop_sizes,
    channel_lengths,
    angle_hits
):
    deg_norm = normalize_distribution(degree_dist)

    avg_loop = np.mean(loop_sizes) if len(loop_sizes) > 0 else 0
    std_loop = np.std(loop_sizes) if len(loop_sizes) > 0 else 0

    avg_channel = np.mean(channel_lengths) if len(channel_lengths) > 0 else 0
    std_channel = np.std(channel_lengths) if len(channel_lengths) > 0 else 0

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
# 🔥 PIPELINE WRAPPER (NEU)
# --------------------------------------------------

def compute_topology_signature(metrics):
    """
    Adapter: converts pipeline metrics → full signature
    """

    degree_dist = metrics.get("degree_distribution", {})

    # placeholders for now (werden später verbessert)
    loop_sizes = metrics.get("loop_sizes", [])
    channel_lengths = metrics.get("channel_lengths", [])
    angle_hits = metrics.get("angle_hits", {})

    return compute_signature(
        degree_dist,
        loop_sizes,
        channel_lengths,
        angle_hits
    )


# --------------------------------------------------
# VECTORIZE
# --------------------------------------------------

def signature_to_vector(signature):

    vec = []

    for k in sorted(signature["degree_dist"].keys()):
        vec.append(signature["degree_dist"][k])

    vec.append(signature["avg_loop"])
    vec.append(signature["std_loop"])

    vec.append(signature["avg_channel"])
    vec.append(signature["std_channel"])

    for k in sorted(signature["angle_profile"].keys()):
        vec.append(signature["angle_profile"][k])

    return np.array(vec)


# --------------------------------------------------
# COMPARISON
# --------------------------------------------------

def compare_signatures(sig1, sig2):

    v1 = signature_to_vector(sig1)
    v2 = signature_to_vector(sig2)

    v1 = v1 / (np.linalg.norm(v1) + 1e-8)
    v2 = v2 / (np.linalg.norm(v2) + 1e-8)

    return np.dot(v1, v2)


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":
    print("Topology Signature Module Ready")
