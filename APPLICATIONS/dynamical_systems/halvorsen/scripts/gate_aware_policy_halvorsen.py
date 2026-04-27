# ============================================================
# NEXAH — Gate-Aware Policy (Halvorsen)
# ============================================================
#
# Purpose:
# Build a policy that explicitly prefers detected gates while
# preserving mass conservation.
#
# Concept:
# - gates = strong off-diagonal transitions
# - gate-aware policy boosts gate edges
# - rows are renormalized so ΣP = 1
#
# Input:
# - latest adaptive_matrix_*.npy
#   fallback: latest connected_matrix_*.npy
#   fallback: latest coarse_matrix_*.npy
#
# Output:
# - gate_aware_policy_*.txt
# - gate_aware_policy_matrix_*.png
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
    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"

    patterns = [
        "adaptive_matrix_*.npy",
        "connected_matrix_*.npy",
        "coarse_matrix_*.npy",
    ]

    for pattern in patterns:
        files = sorted(glob.glob(os.path.join(base, pattern)))
        if files:
            path = files[-1]
            print(f"→ loading matrix: {path}")
            return np.load(path), path

    raise RuntimeError("No matrix found.")


# ============================================================
# DETECT GATES
# ============================================================

def detect_gates(M, alpha=0.2):
    gates = []

    for i in range(M.shape[0]):
        diag = M[i, i]

        for j in range(M.shape[1]):
            if i == j:
                continue

            p = M[i, j]

            if diag > 0 and (p / diag) > alpha:
                gates.append((i, j, float(p), float(p / diag)))

    return gates


# ============================================================
# BUILD GATE-AWARE POLICY
# ============================================================

def build_gate_aware_policy(M, gates, boost=2.0, diagonal_damping=0.85):
    policy = M.copy()

    # Slightly reduce self-locking on diagonal.
    for i in range(policy.shape[0]):
        policy[i, i] *= diagonal_damping

    # Boost detected gate edges.
    for i, j, p, rel in gates:
        policy[i, j] *= boost

    # Renormalize rows: mass conservation.
    for i in range(policy.shape[0]):
        s = policy[i].sum()
        if s > 0:
            policy[i] /= s

    return policy


# ============================================================
# GREEDY POLICY
# ============================================================

def greedy_policy(policy):
    result = {}

    for i in range(policy.shape[0]):
        row = policy[i].copy()
        row[i] = 0.0

        if row.sum() <= 0:
            result[i] = None
        else:
            result[i] = int(np.argmax(row))

    return result


# ============================================================
# SAVE OUTPUTS
# ============================================================

def save_outputs(M, policy, gates, greedy, source_matrix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base, exist_ok=True)

    txt_path = f"{base}/gate_aware_policy_{timestamp}.txt"
    with open(txt_path, "w") as f:
        f.write("NEXAH — Gate-Aware Policy\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Source matrix: {source_matrix}\n\n")

        f.write("GATES\n")
        f.write("-" * 60 + "\n")
        for i, j, p, rel in gates:
            f.write(f"{i} -> {j} | p={p:.4f} | rel={rel:.3f}\n")

        f.write("\nGREEDY GATE-AWARE POLICY\n")
        f.write("-" * 60 + "\n")
        for i in sorted(greedy):
            f.write(f"{i} -> {greedy[i]}\n")

        f.write("\nROW SUM CHECK\n")
        f.write("-" * 60 + "\n")
        for i in range(policy.shape[0]):
            f.write(f"{i}: {policy[i].sum():.6f}\n")

    png_path = f"{base}/gate_aware_policy_matrix_{timestamp}.png"
    plt.figure(figsize=(6, 5))
    plt.imshow(policy)
    plt.colorbar()
    plt.title("Gate-Aware Policy Matrix")
    plt.xlabel("to cluster")
    plt.ylabel("from cluster")

    for i, j, _, _ in gates:
        plt.scatter(j, i, s=120, facecolors="none", edgecolors="red", linewidths=2)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300)
    plt.close()

    diff_path = f"{base}/gate_aware_policy_delta_{timestamp}.png"
    plt.figure(figsize=(6, 5))
    plt.imshow(policy - M)
    plt.colorbar()
    plt.title("Gate-Aware Policy Delta")
    plt.xlabel("to cluster")
    plt.ylabel("from cluster")
    plt.tight_layout()
    plt.savefig(diff_path, dpi=300)
    plt.close()

    npy_path = f"{base}/gate_aware_policy_matrix_{timestamp}.npy"
    np.save(npy_path, policy)

    print(f"[✓] TXT saved: {txt_path}")
    print(f"[✓] Policy PNG saved: {png_path}")
    print(f"[✓] Delta PNG saved: {diff_path}")
    print(f"[✓] NPY saved: {npy_path}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("→ load matrix")
    M, source_matrix = load_latest_matrix()

    print("→ detect gates")
    gates = detect_gates(M, alpha=0.2)
    print(f"gates found: {len(gates)}")

    for g in gates:
        print(f"{g[0]} -> {g[1]} | p={g[2]:.4f} | rel={g[3]:.3f}")

    print("→ build gate-aware policy")
    policy = build_gate_aware_policy(
        M,
        gates,
        boost=2.0,
        diagonal_damping=0.85
    )

    print("→ greedy policy")
    greedy = greedy_policy(policy)

    for k in sorted(greedy):
        print(f"{k} -> {greedy[k]}")

    print("→ save")
    save_outputs(M, policy, gates, greedy, source_matrix)

    print("✔ DONE")
