# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/topology_classifier.py

import numpy as np


# --------------------------------------------------
# CLASSIFICATION RULES
# --------------------------------------------------

def classify_topology(signature):
    """
    Classify topology based on signature patterns
    """

    deg = signature["degree_dist"]
    angles = signature["angle_profile"]

    avg_loop = signature["avg_loop"]
    avg_channel = signature["avg_channel"]

    num_hubs = sum(1 for k, v in deg.items() if k >= 5 and v > 0)

    # --------------------------------------------------
    # RULE SET
    # --------------------------------------------------

    # 1. LOOP DOMINANT (Shell / Spiral Systems)
    if avg_loop > avg_channel and angles.get(120, 0) > 0.2:
        return "Loop-Dominant (Shell / Orbital System)"

    # 2. SPIRAL SYSTEM (asymmetric + φ / golden angle hint)
    if angles.get(137.5, 0) > 0.15:
        return "Spiral / Phi-Driven System"

    # 3. NETWORK SYSTEM (many hubs)
    if num_hubs >= 2:
        return "Network System (Hub-Based Topology)"

    # 4. CHANNEL DOMINANT (transport structure)
    if avg_channel > avg_loop * 1.2:
        return "Channel-Dominant System (Transport Topology)"

    # 5. TRIANGULAR / HEXAGONAL STRUCTURE
    if angles.get(120, 0) > 0.25:
        return "Triangular / Hexagonal Structure"

    # 6. PENTAGONAL STRUCTURE
    if angles.get(72, 0) > 0.2:
        return "Pentagonal Structure"

    # 7. CHAOTIC SYSTEM
    if len(deg) > 6 and max(deg.values()) < 0.3:
        return "Chaotic / Diffuse System"

    return "Hybrid / Unclassified"


# --------------------------------------------------
# CONFIDENCE ESTIMATION
# --------------------------------------------------

def classification_confidence(signature):
    """
    Estimate how strong the structure is
    """

    deg = signature["degree_dist"]
    angles = signature["angle_profile"]

    # concentration of structure
    deg_entropy = -sum(v * np.log(v + 1e-8) for v in deg.values())
    angle_strength = sum(angles.values())

    confidence = np.exp(-deg_entropy) * angle_strength

    return confidence


# --------------------------------------------------
# FULL CLASSIFICATION PIPELINE
# --------------------------------------------------

def analyze_topology(signature):
    """
    Full classification + interpretation
    """

    classification = classify_topology(signature)
    confidence = classification_confidence(signature)

    result = {
        "type": classification,
        "confidence": float(confidence)
    }

    return result


# --------------------------------------------------
# PRINT HELPER
# --------------------------------------------------

def print_classification(result):
    print("\n--- TOPOLOGY CLASSIFICATION ---")
    print(f"Type: {result['type']}")
    print(f"Confidence: {result['confidence']:.4f}")


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":
    print("Topology Classifier Ready")
