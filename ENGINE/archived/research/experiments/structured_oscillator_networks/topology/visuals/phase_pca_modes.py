import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

N_MODES = 10


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

phase_history = np.load(PHASE_FILE)

steps, nodes = phase_history.shape

# unwrap phase so PCA doesn't see discontinuities
phase_unwrapped = np.unwrap(phase_history, axis=0)

# subtract mean
phase_centered = phase_unwrapped - np.mean(phase_unwrapped, axis=0)

# ---------------------------------------------------------
# PCA
# ---------------------------------------------------------

pca = PCA()
pca.fit(phase_centered)

explained = pca.explained_variance_ratio_
components = pca.components_

# ---------------------------------------------------------
# PLOT EXPLAINED VARIANCE
# ---------------------------------------------------------

plt.figure(figsize=(8,5))

plt.plot(explained[:20], marker="o")
plt.title("PCA explained variance")
plt.xlabel("mode")
plt.ylabel("variance ratio")

plt.grid()

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pca_variance.png")
plt.close()

# ---------------------------------------------------------
# PLOT FIRST MODES
# ---------------------------------------------------------

plt.figure(figsize=(10,6))

for i in range(N_MODES):
    plt.plot(components[i], label=f"mode {i+1}")

plt.title("PCA spatial modes")
plt.xlabel("node")
plt.ylabel("amplitude")

plt.legend()
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "pca_modes.png")
plt.close()

# ---------------------------------------------------------
# TEMPORAL PROJECTION
# ---------------------------------------------------------

projection = pca.transform(phase_centered)

plt.figure(figsize=(10,6))

plt.plot(projection[:,0], label="mode1")
plt.plot(projection[:,1], label="mode2")
plt.plot(projection[:,2], label="mode3")

plt.title("Temporal evolution of main modes")
plt.xlabel("time")
plt.ylabel("mode amplitude")

plt.legend()

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "pca_temporal_modes.png")
plt.close()

# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

with open(OUTPUT_DIR / "pca_report.txt","w") as f:

    f.write("PCA Analysis Report\n")
    f.write("===================\n\n")

    f.write(f"nodes: {nodes}\n")
    f.write(f"timesteps: {steps}\n\n")

    f.write("Explained variance (first 10 modes)\n\n")

    for i in range(10):
        f.write(f"mode {i+1}: {explained[i]:.4f}\n")

print("PCA analysis complete.")
print("Results written to /output")
