import numpy as np

# FIELD
from nexah.field_layer.core.field import compute_field
from nexah.field_layer.core.metrics import (
    compute_flow_strength,
    compute_curvature,
)

# BASIN
from nexah.core.system.basin import assign_basins_by_threshold

# TRANSITIONS
from nexah.transitions.transition_matrix import compute_transition_matrix


# ----------------------------
# 1. Generate simple dynamics
# ----------------------------

def generate_signal(n=500):
    t = np.linspace(0, 20, n)
    x = np.sin(t) + 0.3 * np.sin(5 * t)
    return x


# ----------------------------
# 2. Pipeline
# ----------------------------

def run_pipeline():
    # --- state ---
    x = generate_signal()

    # reshape to (T, 1)
    X = x.reshape(-1, 1)

    # --- FIELD ---
    F = compute_field(X)

    flow = compute_flow_strength(F)
    curvature = compute_curvature(F)

    # align lengths (safety)
    min_len = min(len(flow), len(curvature))
    flow = flow[:min_len]
    curvature = curvature[:min_len]

    # --- SIGNAL (risk) ---
    risk = flow * curvature

    # normalize
    risk = (risk - np.min(risk)) / (np.max(risk) + 1e-8)

    # --- BASIN ---
    basins = assign_basins_by_threshold(
        risk,
        thresholds=[0.2, 0.5, 0.8]
    )

    # --- TRANSITIONS ---
    P, unique_basins = compute_transition_matrix(basins)

    return {
        "x": x,
        "flow": flow,
        "curvature": curvature,
        "risk": risk,
        "basins": basins,
        "P": P,
        "unique_basins": unique_basins,
    }


# ----------------------------
# 3. Run + print
# ----------------------------

if __name__ == "__main__":
    result = run_pipeline()

    print("\n--- NEXAH PIPELINE RESULT ---\n")

    print("Unique basins:", result["unique_basins"])
    print("\nTransition matrix:\n", result["P"])

    print("\nSample risk values:")
    print(result["risk"][:20])

    print("\nSample basin assignments:")
    print(result["basins"][:20])
