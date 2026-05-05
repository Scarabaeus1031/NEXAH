import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# --- LOAD DATA ---
# Erwartet CSV aus deinem vorherigen Script
data = np.genfromtxt(
    "RESEARCH/VALIDATION/fractal_tests/scripts/outputs/transition_probability_data.csv",
    delimiter=",",
    names=True
)

delta = data["delta"]
distance = data["distance"]
transition = data["transition"]

# --- FEATURE MATRIX ---
X = np.vstack([delta, distance]).T
y = transition

# --- SCALE FEATURES ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- LOGISTIC REGRESSION ---
model = LogisticRegression()
model.fit(X_scaled, y)

# --- GRID FOR FIELD ---
d_range = np.linspace(min(delta), max(delta), 200)
dist_range = np.linspace(min(distance), max(distance), 200)

D, DIST = np.meshgrid(d_range, dist_range)

grid = np.vstack([D.ravel(), DIST.ravel()]).T
grid_scaled = scaler.transform(grid)

P = model.predict_proba(grid_scaled)[:, 1]
P = P.reshape(D.shape)

# --- PLOT ---
plt.figure(figsize=(8,6))

# Heatmap (Field)
plt.contourf(D, DIST, P, levels=20, cmap="viridis", alpha=0.8)

# Decision Boundary (Zipper!)
plt.contour(D, DIST, P, levels=[0.5], colors="red", linewidths=2)

# Original Data
plt.scatter(delta, distance, c=transition, cmap="bwr", edgecolor="k", s=40)

plt.xlabel("Δ")
plt.ylabel("distance")
plt.title("Transition Field Fit (Δ vs distance)")
plt.colorbar(label="P(transition)")

plt.grid()
plt.tight_layout()

# --- SAVE ---
plt.savefig(
    "RESEARCH/VALIDATION/fractal_tests/scripts/outputs/transition_field_fit.png",
    dpi=300
)

plt.show()

print("Field fit complete.")
