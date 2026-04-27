# ============================================================
# NEXAH — Gate Detection (Halvorsen Coarse System)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ------------------------------------------------------------
# 🔹 LOAD MATRIX
# ------------------------------------------------------------

# 👉 Hier: einfach deine letzte Matrix manuell einfügen
# (oder später aus Datei laden)

# Beispiel (ERSETZEN mit deiner echten Matrix!)
M = np.array([
    # copy deine coarse matrix hier rein
])

# ------------------------------------------------------------
# 🔹 DETECT GATES
# ------------------------------------------------------------

def detect_gates(M, threshold=0.15):
    gates = []

    n = M.shape[0]

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            p = M[i, j]

            if p > threshold:
                gates.append((i, j, p))

    return gates

# ------------------------------------------------------------
# 🔹 VISUALIZE GATES
# ------------------------------------------------------------

def plot_gates(M, gates):
    fig = plt.figure(figsize=(6,5))

    plt.imshow(M)
    plt.colorbar()

    # mark gates
    for (i, j, p) in gates:
        plt.scatter(j, i, s=100, facecolors='none', edgecolors='red', linewidths=2)

    plt.title("Gate Detection (Coarse System)")
    plt.xlabel("to cluster j")
    plt.ylabel("from cluster i")

    return fig

# ------------------------------------------------------------
# 🔹 SAVE OUTPUT
# ------------------------------------------------------------

def save(gates, fig):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base, exist_ok=True)

    txt_path = f"{base}/gates_{timestamp}.txt"
    with open(txt_path, "w") as f:
        for (i, j, p) in gates:
            f.write(f"{i} -> {j} : {p:.4f}\n")

    png_path = f"{base}/gates_{timestamp}.png"
    fig.savefig(png_path)
    plt.close()

    print(f"[✓] Gates saved: {txt_path}")
    print(f"[✓] Plot saved: {png_path}")

# ------------------------------------------------------------
# 🔹 MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    print("→ detect gates")
    gates = detect_gates(M, threshold=0.15)

    print(f"found gates: {len(gates)}")

    for g in gates:
        print(g)

    print("→ visualize")
    fig = plot_gates(M, gates)

    print("→ save")
    save(gates, fig)

    print("✔ DONE")
