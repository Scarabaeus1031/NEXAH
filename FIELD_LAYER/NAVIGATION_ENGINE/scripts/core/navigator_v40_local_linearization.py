# navigator_v40_local_linearization.py

import os
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 1. CLUSTERS
# ============================================================

clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),
    "C3": np.array([11.0, 28.5]),
}

# Fixpoint aus V39 (oder automatisch übernehmen)
x_star = np.array([13.494418, 25.994391])

# ============================================================
# 2. FIELD
# ============================================================

def gaussian(x, y, center, strength, sigma=1.2):
    return strength * np.exp(-((x - center[0])**2 + (y - center[1])**2) / (2 * sigma**2))

def scalar_field(x, y):
    return (
        gaussian(x, y, clusters["C0"], 1.5)
        + gaussian(x, y, clusters["C1"], 2.0)
        + gaussian(x, y, clusters["C2"], 3.0)
        - gaussian(x, y, clusters["C3"], 2.0)
    )

def grad_field(x, y, eps=1e-4):
    dx = (scalar_field(x + eps, y) - scalar_field(x - eps, y)) / (2 * eps)
    dy = (scalar_field(x, y + eps) - scalar_field(x, y - eps)) / (2 * eps)
    return np.array([dx, dy])

def rotational_field(x, y):
    p = np.array([x, y], dtype=float)
    v = np.zeros(2)

    r2 = p - clusters["C2"]
    d2 = np.linalg.norm(r2) + 1e-9
    v += 0.6 * np.array([r2[1], -r2[0]]) * np.exp(-(d2**2)/(2*1.6**2))

    r3 = p - clusters["C3"]
    d3 = np.linalg.norm(r3) + 1e-9
    v += 0.55 * np.array([-r3[1], r3[0]]) * np.exp(-(d3**2)/(2*1.3**2))

    return v

def combined_field(x, y):
    return grad_field(x, y) + rotational_field(x, y)

# ============================================================
# 3. JACOBIAN (numerisch)
# ============================================================

def jacobian(x, eps=1e-4):
    J = np.zeros((2,2))

    f0 = combined_field(x[0], x[1])

    for i in range(2):
        dx = np.zeros(2)
        dx[i] = eps

        f_plus = combined_field(x[0] + dx[0], x[1] + dx[1])
        f_minus = combined_field(x[0] - dx[0], x[1] - dx[1])

        J[:, i] = (f_plus - f_minus) / (2 * eps)

    return J

J = jacobian(x_star)

# ============================================================
# 4. EIGENSTRUCTURE
# ============================================================

eigvals, eigvecs = np.linalg.eig(J)

print("Fixpoint x*:", x_star)
print("\nJacobian:\n", J)
print("\nEigenvalues:")
for i, l in enumerate(eigvals):
    print(f"  λ{i}: {l:.6f}")

print("\nEigenvectors:")
print(eigvecs)

# ============================================================
# 5. LOCAL SAMPLING (zur Visualisierung)
# ============================================================

np.random.seed(42)

points = []
for _ in range(300):
    p = x_star + np.random.randn(2) * 0.08
    points.append(p)

points = np.array(points)

# ============================================================
# 6. ELLIPSE AUS EIGENSTRUKTUR
# ============================================================

# Kovarianz-artige Approximation
cov = eigvecs @ np.diag(np.abs(1 / (np.real(eigvals) + 1e-6))) @ eigvecs.T

# Eigenzerlegung für Ellipse
w, v = np.linalg.eigh(cov)

theta = np.linspace(0, 2*np.pi, 200)
ellipse = np.array([
    np.sqrt(w[0]) * np.cos(theta),
    np.sqrt(w[1]) * np.sin(theta)
])

ellipse = v @ ellipse
ellipse = ellipse.T + x_star

# ============================================================
# 7. BACKGROUND FIELD
# ============================================================

xv = np.linspace(12.5, 14.5, 200)
yv = np.linspace(25.0, 27.0, 200)
X, Y = np.meshgrid(xv, yv)
Z = scalar_field(X, Y)

# ============================================================
# 8. PLOT
# ============================================================

fig, axs = plt.subplots(1, 2, figsize=(12,5))

# Q1 — local field + eigenvectors
im = axs[0].contourf(X, Y, Z, levels=40, cmap="viridis")

axs[0].scatter(x_star[0], x_star[1], c="yellow", s=120, edgecolor="black")

# eigenvectors
for i in range(2):
    vec = np.real(eigvecs[:, i])
    axs[0].arrow(
        x_star[0], x_star[1],
        vec[0]*0.4, vec[1]*0.4,
        color="white", width=0.01
    )

axs[0].set_title("Q1 — Local Linearization (Eigenvectors)")
axs[0].set_xlabel("α")
axs[0].set_ylabel("β")

# Q2 — cloud + ellipse
axs[1].contourf(X, Y, Z, levels=40, cmap="viridis")
axs[1].scatter(points[:,0], points[:,1], s=20, c="cyan", alpha=0.5)
axs[1].plot(ellipse[:,0], ellipse[:,1], color="yellow", lw=2)

axs[1].scatter(x_star[0], x_star[1], c="white", s=120, edgecolor="black")

axs[1].set_title("Q2 — Local Geometry (Ellipse Approximation)")
axs[1].set_xlabel("α")
axs[1].set_ylabel("β")

plt.tight_layout()

out_path = os.path.join(OUTPUT_DIR, "v40_local_linearization.png")
plt.savefig(out_path, dpi=180)
plt.close()

print("\nSaved:", out_path)
