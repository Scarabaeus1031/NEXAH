# ============================================================
# NEXAH — Gate Detection (Halvorsen System)
# ============================================================
#
# Purpose:
# Detect transition gates between coarse-grained basins
# based on relative transition strength.
#
# Input:
# - coarse_matrix_*.npy (auto-loaded latest)
#
# Output:
# - gate list (txt)
# - visualization (png)
#
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from datetime import datetime

# ============================================================
# 🔹 LOAD MATRIX
# ============================================================

def load_latest_matrix():
    files = sorted(glob.glob(
        "APPLICATIONS/dynamical_systems/halvorsen/outputs/coarse_matrix_*.npy"
    ))

    if len(files) == 0:
        raise RuntimeError("❌ No coarse_matrix_*.npy found. Run coarse_grain first.")

    latest = files[-1]
    print(f"→ loading matrix: {latest}")

    M = np.load(latest)
    print("matrix shape:", M.shape)

    return M

# ============================================================
# 🔹 DETECT GATES (RELATIVE RULE)
# ============================================================

def detect_gates(M, alpha=0.2):
    gates = []

    n = M.shape[0]

    for i in range(n):
        diag = M[i, i]

        for j in range(n):
            if i == j:
                continue

            p = M[i, j]

            # relative transition strength
            if diag > 0 and (p / diag) > alpha:
                gates.append((i, j, p, p / diag))

    return gates

# ============================================================
# 🔹 VISUALIZE
# ============================================================

def plot_gates(M, gates):
    fig = plt.figure(figsize=(7,6))

    plt.imshow(M)
    plt.colorbar()

    # mark gates
    for (i, j, p, rel) in gates:
        plt.scatter(j, i, s=120, facecolors='none',
                    edgecolors='red', linewidths=2)

    plt.title("NEXAH — Gate Detection (Coarse System)")
    plt.xlabel("to cluster j")
    plt.ylabel("from cluster i")

    return fig

# ============================================================
# 🔹 SAVE OUTPUT
# ============================================================

def save(gates, fig):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base, exist_ok=True)

    # TXT
    txt_path = f"{base}/gates_{timestamp}.txt"
    with open(txt_path, "w") as f:
        f.write("NEXAH Gate Detection\n")
        f.write("="*40 + "\n\n")

        for (i, j, p, rel) in gates:
            f.write(f"{i} -> {j} : p={p:.4f}, rel={rel:.3f}\n")

    # PNG
    png_path = f"{base}/gates_{timestamp}.png"
    fig.savefig(png_path)
    plt.close()

    print(f"[✓] Gates saved: {txt_path}")
    print(f"[✓] Plot saved: {png_path}")

# ============================================================
# 🔹 MAIN
# ============================================================

if __name__ == "__main__":

    print("→ load matrix")
    M = load_latest_matrix()

    print("→ detect gates")
    gates = detect_gates(M, alpha=0.2)

    print(f"found gates: {len(gates)}")

    for g in gates:
        print(f"{g[0]} -> {g[1]} | p={g[2]:.4f} | rel={g[3]:.3f}")

    print("→ visualize")
    fig = plot_gates(M, gates)

    print("→ save")
    save(gates, fig)

    print("✔ DONE")
