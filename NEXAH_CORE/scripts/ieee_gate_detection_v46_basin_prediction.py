# ============================================================
# NEXAH — IEEE GATE DETECTION v46
# Basin Prediction Layer
# ============================================================
#
# PURPOSE:
# --------
# Predict the next basin from the current basin using the
# segment-based transition matrix from v45.
#
# Builds on:
# - v44: basin identity
# - v45: segment-based transition matrix
#
# CORE QUESTION:
# --------------
# Given current basin B_i:
#
#     what is the most likely next basin B_j?
#
# OUTPUTS:
# --------
# v46_basin_prediction_sequence.png
# v46_prediction_accuracy.txt
# v46_predicted_next_basins.npy
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v44_basin_identity import cluster_locked_basins
from ieee_gate_detection_v45_transition_matrix import compute_transition_matrix_from_segments
from ieee_gate_detection_v42_orbit_attractor_locking import compute_locking_score
from ieee_gate_detection_v41_ridge_aligned_control import ridge_aligned_control
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


# ------------------------------------------------------------
# Extract ordered basin segments
# ------------------------------------------------------------

def extract_basin_segments(basin_ids):
    """
    Extract ordered basin segments.

    Returns:
    --------
    segments:
        list of dictionaries:
        {
            "basin": basin_id,
            "start": start_index,
            "end": end_index
        }
    """

    segments = []
    current = None

    for t, b in enumerate(basin_ids):
        if b >= 0:
            if current is None:
                current = {
                    "basin": int(b),
                    "start": t,
                    "end": t
                }
            elif current["basin"] == int(b):
                current["end"] = t
            else:
                segments.append(current)
                current = {
                    "basin": int(b),
                    "start": t,
                    "end": t
                }
        else:
            if current is not None:
                segments.append(current)
                current = None

    if current is not None:
        segments.append(current)

    return segments


# ------------------------------------------------------------
# Predict next basin
# ------------------------------------------------------------

def predict_next_basin(current_basin, transition_probs, basin_list):
    """
    Predict next basin by maximum transition probability.
    """

    if current_basin not in basin_list:
        return -1, 0.0

    idx = basin_list.index(current_basin)
    row = transition_probs[idx]

    if np.sum(row) <= 0:
        return -1, 0.0

    pred_idx = int(np.argmax(row))
    pred_basin = basin_list[pred_idx]
    confidence = float(row[pred_idx])

    return pred_basin, confidence


# ------------------------------------------------------------
# Prediction evaluation
# ------------------------------------------------------------

def evaluate_predictions(segments, transition_probs, basin_list):
    """
    Predict next basin for every segment and compare with actual next segment.
    """

    predictions = []
    actuals = []
    confidences = []

    for i in range(len(segments) - 1):
        current_basin = segments[i]["basin"]
        actual_next = segments[i + 1]["basin"]

        pred_next, conf = predict_next_basin(
            current_basin,
            transition_probs,
            basin_list
        )

        predictions.append(pred_next)
        actuals.append(actual_next)
        confidences.append(conf)

    predictions = np.array(predictions)
    actuals = np.array(actuals)
    confidences = np.array(confidences)

    valid = predictions >= 0

    if np.sum(valid) == 0:
        accuracy = 0.0
    else:
        accuracy = np.mean(predictions[valid] == actuals[valid])

    return predictions, actuals, confidences, accuracy


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    # --------------------------------------------------------
    # Signal
    # --------------------------------------------------------

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    # --------------------------------------------------------
    # v38 base
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # v39 attractor memory
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # v41 ridge-aligned control
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # v42 locking score
    # --------------------------------------------------------

    A_interp = make_interpolator(A, r_grid, theta_grid)
    D_interp = make_interpolator(D, r_grid, theta_grid)
    P_interp = make_interpolator(P, r_grid, theta_grid)

    L, *_ = compute_locking_score(
        aligned,
        A_interp,
        D_interp,
        P_interp
    )

    # --------------------------------------------------------
    # v44 basin IDs
    # --------------------------------------------------------

    basin_ids, *_ = cluster_locked_basins(
        aligned,
        L,
        threshold=0.5,
        eps=0.18,
        min_samples=6
    )

    # --------------------------------------------------------
    # v45 transition matrix
    # --------------------------------------------------------

    counts, probs, basin_list, _ = compute_transition_matrix_from_segments(
        basin_ids
    )

    # --------------------------------------------------------
    # v46 prediction
    # --------------------------------------------------------

    segments = extract_basin_segments(basin_ids)

    predictions, actuals, confidences, accuracy = evaluate_predictions(
        segments,
        probs,
        basin_list
    )

    # --------------------------------------------------------
    # Plot prediction sequence
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
        label="predicted next basin"
    )

    plt.xlabel("segment index")
    plt.ylabel("basin id")
    plt.title("NEXAH v46 — Basin Prediction")
    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        "v46_basin_prediction_sequence.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Save outputs
    # --------------------------------------------------------

    np.save(
        os.path.join(OUT_DIR, "v46_predicted_next_basins.npy"),
        predictions
    )

    np.save(
        os.path.join(OUT_DIR, "v46_actual_next_basins.npy"),
        actuals
    )

    np.save(
        os.path.join(OUT_DIR, "v46_prediction_confidences.npy"),
        confidences
    )

    summary_path = os.path.join(
        OUT_DIR,
        "v46_prediction_accuracy.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v46 — Basin Prediction Summary\n")
        f.write("===================================\n\n")
        f.write(f"Basins: {basin_list}\n")
        f.write(f"Segments: {len(segments)}\n")
        f.write(f"Predictions: {len(predictions)}\n")
        f.write(f"Accuracy: {accuracy:.4f}\n")
        f.write(f"Mean confidence: {np.mean(confidences):.4f}\n\n")
        f.write("Transition probability matrix:\n")
        f.write(str(probs))
        f.write("\n\n")

        for i in range(len(predictions)):
            f.write(
                f"Segment {i}: "
                f"actual={actuals[i]}, "
                f"predicted={predictions[i]}, "
                f"confidence={confidences[i]:.4f}\n"
            )

    # --------------------------------------------------------
    # Console output
    # --------------------------------------------------------

    print("NEXAH v46 complete")
    print(f"Basins: {basin_list}")
    print(f"Segments: {len(segments)}")
    print(f"Predictions: {len(predictions)}")
    print(f"Prediction accuracy: {accuracy:.4f}")
    print(f"Mean confidence: {np.mean(confidences):.4f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
