# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/topology_classifier.py

import numpy as np


# --------------------------------------------------
# CLASSIFICATION RULES (IMPROVED)
# --------------------------------------------------

def classify_topology(signature):
    """
    Improved topology classification based on signature patterns
    """

    deg = signature.get("degree_dist", {})
    angles = signature.get("angle_profile", {})

    avg_loop = signature.get("avg_loop", 0.0)
    avg_channel = signature.get("avg_channel", 0.0)

    # --------------------------------------------------
    # BASIC FEATURES
    # --------------------------------------------------

    num_hubs = sum(1 for k, v in deg.items() if k >= 5 and v > 0)
    degree_variation = len(deg)

    loop_strength = avg_loop
    channel_strength = avg_channel

    angle_120 = angles.get(120, 0)
    angle_phi = angles.get(137.5, 0)
    angle_72 = angles.get(72, 0)

    # --------------------------------------------------
    # PRIORITY RULES (IMPORTANT ORDER!)
    # --------------------------------------------------

    # 1. 🔵 STRONG LOOP SYSTEM
    if loop_strength > 0.05 and channel_strength < 0.02:
        return "Loop System"

    # 2. 🟢 STRONG CHANNEL SYSTEM
    if channel_strength > 0.05 and loop_strength < 0.02:
        return "Channel System"

    # 3. 🟣 HYBRID SYSTEM (both active)
    if loop_strength > 0.02 and channel_strength > 0.02:
        return "Hybrid System"

    # 4. 🔺 TRIANGULAR / HEX STRUCTURE
    if angle_120 > 0.25:
        return "Triangular / Hexagonal Structure"

    # 5. ⭐ PHI / SPIRAL SYSTEM
    if angle_phi > 0.15:
        return "Spiral / Phi-Driven System"

    # 6. 🔶 PENTAGONAL STRUCTURE
    if angle_72 > 0.2:
        return "Pentagonal Structure"

    # 7. 🟡 STRUCTURED NETWORK (ONLY if above didn't trigger!)
    if num_hubs >= 2 and degree_variation > 30:
        return "Structured Network"

    # 8. ⚫ CHAOTIC / DIFFUSE
    if degree_variation > 50 and max(deg.values(), default=0) < 0.3:
        return "Chaotic / Diffuse System"

    # --------------------------------------------------
    # FALLBACK
    # --------------------------------------------------

    return "Weak / Transitional System"


# --------------------------------------------------
# CONFIDENCE ESTIMATION (IMPROVED)
# --------------------------------------------------

def classification_confidence(signature):
    """
    Estimate how strong the structure is
    """

    deg = signature.get("degree_dist", {})
    angles = signature.get("angle_profile", {})

    if len(deg) == 0:
        return 0.0

    # entropy (structure randomness)
    deg_entropy = -sum(v * np.log(v + 1e-8) for v in deg.values())

    # angle concentration
    angle_strength = sum(angles.values())

    # normalize
    confidence = np.exp(-deg_entropy) * (1 + angle_strength)

    return float(confidence)


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
