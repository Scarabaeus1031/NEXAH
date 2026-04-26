# ============================================================
# NEXAH — IEEE GATE DETECTION v46.2
# Memory-Based Basin Prediction
# ============================================================
#
# PURPOSE:
# --------
# Improve basin prediction by adding discrete transition memory.
#
# v46 used:
#     P(next | current basin)
#
# v46.2 uses:
#     P(next | previous basin, current basin)
#
# CORE IDEA:
# ----------
# The next basin may depend not only on where the system is now,
# but where it came from.
#
# This is a second-order Markov prediction layer.
#
# OUTPUTS:
# --------
# v46_2_memory_prediction_sequence.png
# v46_2_memory_prediction_accuracy.txt
# v46_2_predicted_next_basins.npy
# v46_2_actual_next_basins.npy
# v46_2_prediction_confidences.npy
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import (
    run_v38_control,
    gradient_field,
    make_interpolator
)

from ieee_gate_detection_v39_attractor_memory import (
    stability_score,
    detect_stable_attractors,
    attractor_memory_field
)

from ieee_gate_detection_v41_ridge_aligned_control import ridge_aligned_control

from ieee_gate_detection_v42_orbit_attractor_locking import compute_locking_score

from ieee_gate_detection_v44_basin_identity import cluster_locked_basins

from ieee_gate_detection_v46_basin_prediction import extract_basin_segments


# ------------------------------------------------------------
# Memory transition tensor
# ------------------------------------------------------------

def compute_memory_transition_tensor(segments, basin_list):
    """
    Compute second-order transition counts:

        P(B_next | B_prev, B_current)

    Returns:
    --------
    counts : shape (N, N, N)
        counts[prev, current, next]

    probs : shape (N, N, N)
        normalized probabilities over next basin.
    """

    n = len(basin_list)
    id_map = {b: i for i, b in enumerate(basin_list)}

    counts = np.zeros((n, n, n))

    for i in range(1, len(segments) - 1):
        b_prev = segments[i - 1]["basin"]
        b_curr = segments[i]["basin"]
        b_next = segments[i + 1]["basin"]

        if b_prev in id_map and b_curr in id_map and b_next in id_map:
            counts[
                id_map[b_prev],
                id_map[b_curr],
                id_map[b_next]
            ] += 1

    probs = np.zeros_like(counts)

    for i in range(n):
        for j in range(n):
            s = counts[i, j].sum()
            if s > 0:
                probs[i, j] = counts[i, j] / s

    return counts, probs


# ------------------------------------------------------------
# First-order fallback matrix
# ------------------------------------------------------------

def compute_first_order_probs(segments, basin_list):
    """
    Compute first-order fallback:

        P(B_next | B_current)

    Used when memory pair has no observations.
    """

    n = len(basin_list)
    id_map = {b: i for i, b in enumerate(basin_list)}

    counts = np.zeros((n, n))

    for i in range(len(segments) - 1):
        b_curr = segments[i]["basin"]
        b_next = segments[i + 1]["basin"]

        if b_curr in id_map and b_next in id_map and b_curr != b_next:
            counts[id_map[b_curr], id_map[b_next]] += 1

    probs = np.zeros_like(counts)

    for i in range(n):
        s = counts[i].sum()
        if s > 0:
            probs[i] = counts[i] / s

    return counts, probs


# ------------------------------------------------------------
# Prediction
# ------------------------------------------------------------

def predict_next_with_memory(
    previous_basin,
    current_basin,
    memory_probs,
    fallback_probs,
    basin_list
):
    """
    Predict next basin using memory if available,
    otherwise fallback to first-order transition.
    """

    if previous_basin not in basin_list or current_basin not in basin_list:
        return -1, 0.0, "invalid"

    id_map = {b: i for i, b in enumerate(basin_list)}

    i = id_map[previous_basin]
    j = id_map[current_basin]

    row = memory_probs[i, j]

    if row.sum() > 0:
        pred_idx = int(np.argmax(row))
        return basin_list[pred_idx], float(row[pred_idx]), "memory"

    # fallback
    row = fallback_probs[j]

    if row.sum() > 0:
        pred_idx = int(np.argmax(row))
        return basin_list[pred_idx], float(row[pred_idx]), "fallback"

    return -1, 0.0, "none"


def evaluate_memory_predictions(
    segments,
    memory_probs,
    fallback_probs,
    basin_list
):
    """
    Evaluate predictions for all segment triples.
    """

    predictions = []
    actuals = []
    confidences = []
    modes = []

    for i in range(1, len(segments) - 1):
        previous_basin = segments[i - 1]["basin"]
        current_basin = segments[i]["basin"]
        actual_next = segments[i + 1]["basin"]

        pred_next, conf, mode = predict_next_with_memory(
            previous_basin,
            current_basin,
            memory_probs,
            fallback_probs,
            basin_list
        )

        predictions.append(pred_next)
        actuals.append(actual_next)
        confidences.append(conf)
        modes.append(mode)

    predictions = np.array(predictions)
    actuals = np.array(actuals)
    confidences = np.array(confidences)

    valid = predictions >= 0

    if np.sum(valid) == 0:
        accuracy = 0.0
    else:
        accuracy = float(np.mean(predictions[valid] == actuals[valid]))

    return predictions, actuals, confidences, modes, accuracy


# ------------------------------------------------------------
# Main pipeline helper
# ------------------------------------------------------------

def build_basin_sequence():
    """
    Rebuild the v38-v44 pipeline and return basin segments.
    """

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    states = np.column_stack([
        result["r"],
        result["theta"]
    ])

    raw_controls = result["controls"]

    rho = result["rho"]
    P = result["P_IOTA"]
    D = result["D"]
    r_grid = result["r_grid"]
    theta_grid = result["theta_grid"]

    S = stability_score(rho, P, D)

    attractors = detect_stable_attractors(
        S,
        r_grid,
        theta_grid,
        percentile=98
    )

    A = attractor_memory_field(
        attractors,
        r_grid,
        theta_grid
    )

    grad_rho = gradient_field(rho, r_grid, theta_grid)

    grad_rho_interp = (
        make_interpolator(grad_rho[0], r_grid, theta_grid),
        make_interpolator(grad_rho[1], r_grid, theta_grid),
    )

    aligned = ridge_aligned_control(
        states,
        raw_controls,
        grad_rho_interp,
        eta=0.02,
        max_step=0.04,
        tangential_gain=1.0,
        damping=0.15
    )

    A_interp = make_interpolator(A, r_grid, theta_grid)
    D_interp = make_interpolator(D, r_grid, theta_grid)
    P_interp = make_interpolator(P, r_grid, theta_grid)

    L, *_ = compute_locking_score(
        aligned,
        A_interp,
        D_interp,
        P_interp
    )

    basin_ids, *_ = cluster_locked_basins(
        aligned,
        L,
        threshold=0.5,
        eps=0.18,
        min_samples=6
    )

    segments = extract_basin_segments(basin_ids)
    basin_list = sorted([int(b) for b in np.unique(basin_ids) if b >= 0])

    return t, segments, basin_ids, basin_list


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    t, segments, basin_ids, basin_list = build_basin_sequence()

    memory_counts, memory_probs = compute_memory_transition_tensor(
        segments,
        basin_list
    )

    fallback_counts, fallback_probs = compute_first_order_probs(
        segments,
        basin_list
    )

    predictions, actuals, confidences, modes, accuracy = evaluate_memory_predictions(
        segments,
        memory_probs,
        fallback_probs,
        basin_list
    )

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    x_axis = np.arange(len(predictions))

    plt.figure(figsize=(10, 4))

    plt.plot(
        x_axis,
        actuals,
        marker="o",
        linewidth=1.5,
        label="actual next basin"
    )

    plt.plot(
        x_axis,
        predictions,
        marker="x",
        linewidth=1.5,
        label="memory predicted next basin"
    )

    plt.xlabel("segment index")
    plt.ylabel("basin id")
    plt.title("NEXAH v46.2 — Memory-Based Basin Prediction")
    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        "v46_2_memory_prediction_sequence.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Save arrays
    # --------------------------------------------------------

    np.save(
        os.path.join(OUT_DIR, "v46_2_memory_transition_counts.npy"),
        memory_counts
    )

    np.save(
        os.path.join(OUT_DIR, "v46_2_memory_transition_probs.npy"),
        memory_probs
    )

    np.save(
        os.path.join(OUT_DIR, "v46_2_fallback_transition_probs.npy"),
        fallback_probs
    )

    np.save(
        os.path.join(OUT_DIR, "v46_2_predicted_next_basins.npy"),
        predictions
    )

    np.save(
        os.path.join(OUT_DIR, "v46_2_actual_next_basins.npy"),
        actuals
    )

    np.save(
        os.path.join(OUT_DIR, "v46_2_prediction_confidences.npy"),
        confidences
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    memory_used = sum(1 for m in modes if m == "memory")
    fallback_used = sum(1 for m in modes if m == "fallback")
    none_used = sum(1 for m in modes if m == "none")

    summary_path = os.path.join(
        OUT_DIR,
        "v46_2_memory_prediction_accuracy.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v46.2 — Memory-Based Basin Prediction Summary\n")
        f.write("=================================================\n\n")
        f.write(f"Basins: {basin_list}\n")
        f.write(f"Segments: {len(segments)}\n")
        f.write(f"Predictions: {len(predictions)}\n")
        f.write(f"Accuracy: {accuracy:.4f}\n")
        f.write(f"Mean confidence: {np.mean(confidences):.4f}\n")
        f.write(f"Memory used: {memory_used}\n")
        f.write(f"Fallback used: {fallback_used}\n")
        f.write(f"No prediction: {none_used}\n\n")

        for i in range(len(predictions)):
            f.write(
                f"Segment {i}: "
                f"actual={actuals[i]}, "
                f"predicted={predictions[i]}, "
                f"confidence={confidences[i]:.4f}, "
                f"mode={modes[i]}\n"
            )

    print("NEXAH v46.2 complete")
    print(f"Basins: {basin_list}")
    print(f"Segments: {len(segments)}")
    print(f"Predictions: {len(predictions)}")
    print(f"Prediction accuracy: {accuracy:.4f}")
    print(f"Mean confidence: {np.mean(confidences):.4f}")
    print(f"Memory used: {memory_used}")
    print(f"Fallback used: {fallback_used}")
    print(f"No prediction: {none_used}")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
