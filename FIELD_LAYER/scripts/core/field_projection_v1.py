# FIELD_LAYER/scripts/core/field_projection_v1.py

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# 1. GENERATE LORENZ DATA
# =========================

def generate_lorenz(n_steps=5000, dt=0.01):
    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0

    X = np.zeros((n_steps, 3))
    x, y, z = 1.0, 1.0, 1.0

    for i in range(n_steps):
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z

        x += dx * dt
        y += dy * dt
        z += dz * dt

        X[i] = [x, y, z]

    return X


# =========================
# 2. PCA FIELD AXIS
# =========================

def compute_field_basis(X):
    pca = PCA(n_components=3)
    pca.fit(X)

    components = pca.components_

    e1 = components[0]  # dominant flow
    e2 = components[1]
    e3 = components[2]

    return e1, e2, e3


# =========================
# 3. PROJECTION
# =========================

def project_field(X, e1, e2, e3):
    alpha = X @ e1
    beta = X @ e2
    gamma = X @ e3

    return alpha, beta, gamma


# =========================
# 4. DEVIATION
# =========================

def compute_deviation(beta, gamma):
    return np.sqrt(beta**2 + gamma**2)


# =========================
# 5. MAIN
# =========================

def main():
    print("Running Field Projection V1...")

    X = generate_lorenz()

    # center data
    X = X - np.mean(X, axis=0)

    e1, e2, e3 = compute_field_basis(X)

    alpha, beta, gamma = project_field(X, e1, e2, e3)
    D = compute_deviation(beta, gamma)

    # =========================
    # PLOT 1: α vs β
    # =========================
    plt.figure(figsize=(6,6))
    plt.scatter(alpha, beta, s=1, alpha=0.5)
    plt.title("Field Projection (α vs β)")
    plt.xlabel("α (flow)")
    plt.ylabel("β (deviation)")

    out1 = os.path.join(OUTPUT_DIR, "field_projection_alpha_beta.png")
    plt.savefig(out1, dpi=150)
    plt.close()

    # =========================
    # PLOT 2: Deviation over time
    # =========================
    plt.figure(figsize=(10,4))
    plt.plot(D)
    plt.title("Deviation D(t)")
    plt.xlabel("time")
    plt.ylabel("D")

    out2 = os.path.join(OUTPUT_DIR, "field_deviation.png")
    plt.savefig(out2, dpi=150)
    plt.close()

    print(f"Saved: {out1}")
    print(f"Saved: {out2}")


if __name__ == "__main__":
    main()
