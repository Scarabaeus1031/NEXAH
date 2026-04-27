# ============================================================
# 🧭 NEXAH v17 — Next State Prediction
# Predict next basin using transition graph
# ============================================================

import numpy as np

from nexah.navigation.state_space_control import (
    generate_signal,
    compute_risk,
    compute_adaptive_levels,
    assign_basins,
)

from nexah.navigation.transition_graph import build_transition_graph


# ------------------------------------------------------------
# PREDICT NEXT STATE
# ------------------------------------------------------------

def predict_next_state(graph, current_state):
    """
    Predict next basin based on highest probability transition.
    """
    if current_state not in graph:
        return current_state

    transitions = graph[current_state]

    # pick max probability transition
    best_target = max(
        transitions.items(),
        key=lambda item: (item[1]["probability"], item[1]["count"])
    )[0]

    return int(best_target)


# ------------------------------------------------------------
# RUN PREDICTION
# ------------------------------------------------------------

def run_prediction(n=500, n_basins=10):
    # ----------------------------
    # Generate system
    # ----------------------------
    x = generate_signal(n=n)
    risk = compute_risk(x)

    levels = compute_adaptive_levels(x, n_basins=n_basins)
    basins = assign_basins(x, levels)

    # ----------------------------
    # Build graph
    # ----------------------------
    graph = build_transition_graph(basins)

    # ----------------------------
    # Predict sequence
    # ----------------------------
    predictions = []

    for t in range(len(basins) - 1):
        current = int(basins[t])
        predicted = predict_next_state(graph, current)
        actual = int(basins[t + 1])

        predictions.append({
            "t": t,
            "current": current,
            "predicted": predicted,
            "actual": actual,
            "correct": predicted == actual,
        })

    # ----------------------------
    # Stats
    # ----------------------------
    correct = sum(p["correct"] for p in predictions)
    accuracy = correct / len(predictions)

    print("\n--- Prediction Accuracy ---")
    print(f"{accuracy:.3f}")

    print("\n--- Sample Predictions ---")
    for p in predictions[:30]:
        print(p)

    return predictions, graph


# ------------------------------------------------------------
# ENTRY
# ------------------------------------------------------------

if __name__ == "__main__":
    run_prediction()
