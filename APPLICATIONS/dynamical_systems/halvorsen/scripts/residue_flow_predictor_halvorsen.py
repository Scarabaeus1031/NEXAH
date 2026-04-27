# ============================================================
# NEXAH — Residue Flow Predictor (Halvorsen)
# ============================================================
#
# Purpose:
# Test whether modular residue structure carries predictive
# information about Halvorsen flow transitions.
#
# Core Question:
# Can we predict next cluster using only residue-space structure?
#
# Input:
# - latest gate_aware_policy_matrix_*.npy
# - fallback: adaptive / connected / coarse matrix
#
# Outputs:
# - residue_flow_predictor_*.txt
# - residue_flow_prediction_matrix_mod7_*.png
# - residue_flow_prediction_matrix_mod17_*.png
# - residue_flow_accuracy_*.png
# - residue_flow_comparison_*.png
#
# ============================================================

import os
import glob
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# LOAD MATRIX
# ============================================================

def load_latest_matrix():
    import glob
    import os
    import numpy as np

    # 🔥 dynamischer Pfad (wichtig!)
    base_path = os.path.dirname(__file__)
    outputs_path = os.path.join(base_path, "..", "outputs")

    # 🔍 alle möglichen Matrix-Typen
    patterns = [
        "gate_aware_policy_matrix_*.npy",
        "policy_gradient_matrix_*.npy",
        "adaptive_matrix_*.npy",
        "connected_matrix_*.npy",
        "coarse_matrix_*.npy",
    ]

    files = []
    for pattern in patterns:
        files.extend(glob.glob(os.path.join(outputs_path, pattern)))

    if not files:
        raise RuntimeError("❌ No transition / policy matrix found.")

    files = sorted(files)
    latest = files[-1]

    print(f"→ loading matrix: {latest}")

    M = np.load(latest)

    return M, latest

# ============================================================
# EXTRACT OBSERVED TRANSITIONS
# ============================================================

def extract_observed_transitions(M, threshold=0.02):
    transitions = []

    n = M.shape[0]

    for i in range(n):
        row = M[i].copy()
        row[i] = 0.0

        for j in range(n):
            if i == j:
                continue

            p = row[j]

            if p >= threshold:
                transitions.append((i, j, float(p)))

    return transitions


# ============================================================
# BUILD RESIDUE JUMP MODEL
# ============================================================

def build_residue_jump_model(transitions, mod):
    """
    Learns dominant jump distribution:
    P(jump | residue_from)
    """

    counts = np.zeros((mod, mod))

    for i, j, p in transitions:
        r_from = i % mod
        jump = (j - i) % mod
        counts[r_from, jump] += p

    model = counts.copy()

    for r in range(mod):
        s = model[r].sum()
        if s > 0:
            model[r] /= s

    return model, counts


# ============================================================
# PREDICT NEXT CLUSTER
# ============================================================

def predict_next_cluster(i, n_clusters, model, mod):
    r = i % mod

    if model[r].sum() <= 0:
        return None, None

    best_jump = int(np.argmax(model[r]))
    confidence = float(model[r, best_jump])

    pred = (i + best_jump) % n_clusters

    return pred, confidence


# ============================================================
# EVALUATE MODEL
# ============================================================

def evaluate_model(M, model, mod, threshold=0.02):
    n = M.shape[0]

    exact_hits = 0
    top_observed_hits = 0
    tested = 0

    predictions = {}
    details = []

    for i in range(n):
        row = M[i].copy()
        row[i] = 0.0

        observed_targets = np.where(row >= threshold)[0]

        if len(observed_targets) == 0:
            predictions[i] = None
            continue

        true_top = int(np.argmax(row))

        pred, confidence = predict_next_cluster(i, n, model, mod)

        predictions[i] = pred

        if pred is None:
            continue

        tested += 1

        exact = pred == true_top
        observed = pred in observed_targets

        if exact:
            exact_hits += 1

        if observed:
            top_observed_hits += 1

        details.append({
            "state": i,
            "pred": pred,
            "confidence": confidence,
            "true_top": true_top,
            "observed_targets": observed_targets.tolist(),
            "exact": exact,
            "observed": observed,
        })

    exact_accuracy = exact_hits / tested if tested > 0 else 0.0
    observed_accuracy = top_observed_hits / tested if tested > 0 else 0.0

    return {
        "predictions": predictions,
        "details": details,
        "tested": tested,
        "exact_accuracy": exact_accuracy,
        "observed_accuracy": observed_accuracy,
    }


# ============================================================
# BUILD PREDICTION MATRIX
# ============================================================

def build_prediction_matrix(predictions, n):
    P = np.zeros((n, n))

    for i, pred in predictions.items():
        if pred is not None:
            P[i, pred] = 1.0

    return P


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(source, result7, result17, model7, model17, timestamp, base):
    txt_path = f"{base}/residue_flow_predictor_{timestamp}.txt"

    with open(txt_path, "w") as f:
        f.write("NEXAH — Residue Flow Predictor\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Source matrix: {source}\n\n")

        f.write("SUMMARY\n")
        f.write("-" * 70 + "\n")
        f.write(f"mod 7 tested states: {result7['tested']}\n")
        f.write(f"mod 7 exact top-target accuracy: {result7['exact_accuracy']:.4f}\n")
        f.write(f"mod 7 observed-target accuracy: {result7['observed_accuracy']:.4f}\n\n")

        f.write(f"mod 17 tested states: {result17['tested']}\n")
        f.write(f"mod 17 exact top-target accuracy: {result17['exact_accuracy']:.4f}\n")
        f.write(f"mod 17 observed-target accuracy: {result17['observed_accuracy']:.4f}\n\n")

        f.write("DETAILS MOD 7\n")
        f.write("-" * 70 + "\n")
        for d in result7["details"]:
            f.write(
                f"{d['state']} -> pred {d['pred']} "
                f"| conf={d['confidence']:.3f} "
                f"| true_top={d['true_top']} "
                f"| observed={d['observed_targets']} "
                f"| exact={d['exact']} "
                f"| hit_observed={d['observed']}\n"
            )

        f.write("\nDETAILS MOD 17\n")
        f.write("-" * 70 + "\n")
        for d in result17["details"]:
            f.write(
                f"{d['state']} -> pred {d['pred']} "
                f"| conf={d['confidence']:.3f} "
                f"| true_top={d['true_top']} "
                f"| observed={d['observed_targets']} "
                f"| exact={d['exact']} "
                f"| hit_observed={d['observed']}\n"
            )

        f.write("\nRESIDUE MODEL MOD 7\n")
        f.write("-" * 70 + "\n")
        for r in range(model7.shape[0]):
            f.write(f"residue {r}: {model7[r].round(4).tolist()}\n")

        f.write("\nRESIDUE MODEL MOD 17\n")
        f.write("-" * 70 + "\n")
        for r in range(model17.shape[0]):
            f.write(f"residue {r}: {model17[r].round(4).tolist()}\n")

    print(f"[✓] Report saved: {txt_path}")


# ============================================================
# VISUALS
# ============================================================

def plot_prediction_matrix(P, mod, timestamp, base):
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(P)

    ax.set_title(f"Residue Flow Prediction Matrix — mod {mod}")
    ax.set_xlabel("predicted next cluster")
    ax.set_ylabel("current cluster")
    plt.colorbar(im)

    plt.tight_layout()
    path = f"{base}/residue_flow_prediction_matrix_mod{mod}_{timestamp}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"[✓] Prediction matrix mod {mod} saved: {path}")


def plot_accuracy(result7, result17, timestamp, base):
    labels = [
        "mod7 exact",
        "mod7 observed",
        "mod17 exact",
        "mod17 observed",
    ]

    values = [
        result7["exact_accuracy"],
        result7["observed_accuracy"],
        result17["exact_accuracy"],
        result17["observed_accuracy"],
    ]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values)
    ax.set_ylim(0, 1)
    ax.set_title("Residue Flow Predictor Accuracy")
    ax.set_ylabel("accuracy")
    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    path = f"{base}/residue_flow_accuracy_{timestamp}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"[✓] Accuracy plot saved: {path}")


def plot_comparison(M, P7, P17, timestamp, base):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    im0 = axes[0].imshow(M)
    axes[0].set_title("Observed Flow / Policy")
    plt.colorbar(im0, ax=axes[0])

    im1 = axes[1].imshow(P7)
    axes[1].set_title("Residue Predictor mod 7")
    plt.colorbar(im1, ax=axes[1])

    im2 = axes[2].imshow(P17)
    axes[2].set_title("Residue Predictor mod 17")
    plt.colorbar(im2, ax=axes[2])

    for ax in axes:
        ax.set_xlabel("to cluster")
        ax.set_ylabel("from cluster")

    plt.tight_layout()
    path = f"{base}/residue_flow_comparison_{timestamp}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"[✓] Comparison plot saved: {path}")


def plot_residue_models(model7, model17, timestamp, base):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    im0 = axes[0].imshow(model7)
    axes[0].set_title("Learned Residue Jump Model — mod 7")
    axes[0].set_xlabel("jump")
    axes[0].set_ylabel("from residue")
    plt.colorbar(im0, ax=axes[0])

    im1 = axes[1].imshow(model17)
    axes[1].set_title("Learned Residue Jump Model — mod 17")
    axes[1].set_xlabel("jump")
    axes[1].set_ylabel("from residue")
    plt.colorbar(im1, ax=axes[1])

    plt.tight_layout()
    path = f"{base}/residue_flow_models_{timestamp}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"[✓] Residue models saved: {path}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("→ load matrix")
    M, source = load_latest_matrix()

    print("→ extract observed transitions")
    transitions = extract_observed_transitions(M, threshold=0.02)
    print(f"observed transitions: {len(transitions)}")

    print("→ build residue models")
    model7, counts7 = build_residue_jump_model(transitions, mod=7)
    model17, counts17 = build_residue_jump_model(transitions, mod=17)

    print("→ evaluate predictors")
    result7 = evaluate_model(M, model7, mod=7, threshold=0.02)
    result17 = evaluate_model(M, model17, mod=17, threshold=0.02)

    print(f"mod 7 exact accuracy: {result7['exact_accuracy']:.4f}")
    print(f"mod 7 observed accuracy: {result7['observed_accuracy']:.4f}")
    print(f"mod 17 exact accuracy: {result17['exact_accuracy']:.4f}")
    print(f"mod 17 observed accuracy: {result17['observed_accuracy']:.4f}")

    print("→ build prediction matrices")
    P7 = build_prediction_matrix(result7["predictions"], M.shape[0])
    P17 = build_prediction_matrix(result17["predictions"], M.shape[0])

    print("→ save report")
    save_report(source, result7, result17, model7, model17, timestamp, base)

    print("→ create visuals")
    plot_prediction_matrix(P7, 7, timestamp, base)
    plot_prediction_matrix(P17, 17, timestamp, base)
    plot_accuracy(result7, result17, timestamp, base)
    plot_comparison(M, P7, P17, timestamp, base)
    plot_residue_models(model7, model17, timestamp, base)

    print("✔ DONE")
