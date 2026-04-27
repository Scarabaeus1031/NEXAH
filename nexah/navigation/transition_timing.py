# ============================================================
# 🧭 NEXAH v18 — Transition Timing Model
# Predict WHEN system leaves a basin
# ============================================================

import numpy as np

from nexah.navigation.state_space_control import (
    generate_signal,
    compute_risk,
    compute_adaptive_levels,
    assign_basins,
)


# ------------------------------------------------------------
# BUILD DATASET
# ------------------------------------------------------------

def build_transition_dataset(n=500, n_basins=10):
    x = generate_signal(n=n)
    risk = compute_risk(x)

    levels = compute_adaptive_levels(x, n_basins=n_basins)
    basins = assign_basins(x, levels)

    X = []
    y = []

    for t in range(len(basins) - 1):
        current = int(basins[t])
        next_state = int(basins[t + 1])

        jump = int(next_state != current)

        X.append([current, risk[t]])
        y.append(jump)

    return np.array(X), np.array(y)


# ------------------------------------------------------------
# SIMPLE MODEL (logistic-like thresholding)
# ------------------------------------------------------------

def compute_jump_probability(risk, threshold=0.65, sharpness=10):
    """
    Sigmoid-like jump probability based on risk.
    """
    return 1 / (1 + np.exp(-sharpness * (risk - threshold)))


# ------------------------------------------------------------
# EVALUATION
# ------------------------------------------------------------

def evaluate_model(X, y):
    correct = 0
    total = len(y)

    records = []

    for i in range(total):
        basin, r = X[i]
        actual = y[i]

        prob = compute_jump_probability(r)
        predicted = int(prob > 0.5)

        if predicted == actual:
            correct += 1

        records.append({
            "basin": int(basin),
            "risk": float(r),
            "predicted_jump": predicted,
            "actual_jump": int(actual),
            "probability": float(prob),
        })

    accuracy = correct / total

    return accuracy, records


# ------------------------------------------------------------
# ANALYSIS
# ------------------------------------------------------------

def analyze_jump_distribution(X, y):
    """
    How jump probability relates to risk.
    """

    risk_vals = X[:, 1]

    bins = np.linspace(0, 1, 10)
    counts = np.zeros(len(bins) - 1)
    jumps = np.zeros(len(bins) - 1)

    for r, jump in zip(risk_vals, y):
        for i in range(len(bins) - 1):
            if bins[i] <= r < bins[i + 1]:
                counts[i] += 1
                jumps[i] += jump

    print("\n--- Jump Probability by Risk Bin ---")

    for i in range(len(counts)):
        if counts[i] == 0:
            continue

        p = jumps[i] / counts[i]

        print(
            f"risk[{bins[i]:.2f}-{bins[i+1]:.2f}] "
            f"→ jump_prob={p:.3f} "
            f"(n={int(counts[i])})"
        )


# ------------------------------------------------------------
# DEMO
# ------------------------------------------------------------

def demo():
    X, y = build_transition_dataset()

    acc, records = evaluate_model(X, y)

    print("\n--- Jump Prediction Accuracy ---")
    print(f"{acc:.3f}")

    print("\n--- Sample Records ---")
    for r in records[:30]:
        print(r)

    analyze_jump_distribution(X, y)


if __name__ == "__main__":
    demo()
