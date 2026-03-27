import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# LOAD
# ----------------------------
df = pd.read_csv("v34_physical_coupling.csv")
df["theta"] = 2 * np.pi * df["t"] / 24.0

# Polar → Cartesian
df["x"] = df["C"] * np.cos(df["theta"])
df["y"] = df["C"] * np.sin(df["theta"])

# Optional: nur GH nehmen
gh = df[df["phase"] == "GH"]

X = gh[["x", "y"]].values

# ----------------------------
# PCA (Hauptachse)
# ----------------------------
X_mean = X.mean(axis=0)
X_centered = X - X_mean

cov = np.cov(X_centered.T)
eigvals, eigvecs = np.linalg.eig(cov)

# größte Eigenrichtung = Hauptachse
main_axis = eigvecs[:, np.argmax(eigvals)]

angle = np.arctan2(main_axis[1], main_axis[0])

print("\n--- KNICK AXIS FIT ---")
print(f"Axis angle: {angle:.3f} rad ({np.degrees(angle):.1f}°)")

# ----------------------------
# PLOT
# ----------------------------
plt.figure(figsize=(6,6))
plt.scatter(gh["x"], gh["y"], alpha=0.5)

# Achse zeichnen
line = np.linspace(-0.1, 0.1, 100)
plt.plot(
    X_mean[0] + line * main_axis[0],
    X_mean[1] + line * main_axis[1],
    linewidth=3
)

plt.axhline(0)
plt.axvline(0)
plt.gca().set_aspect('equal', adjustable='box')

plt.title("Fitted Knick Axis (PCA)")
plt.show()
