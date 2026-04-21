import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# -------------------------
# load data
# -------------------------

phase = np.load(PHASE_FILE)

steps, nodes = phase.shape

phase = np.unwrap(phase, axis=0)

# -------------------------
# remove global drift
# -------------------------

global_phase = np.mean(phase, axis=1)

phase_corot = phase - global_phase[:, None]

phase_corot -= np.mean(phase_corot, axis=0)

# -------------------------
# PCA
# -------------------------

pca = PCA()
pca.fit(phase_corot)

explained = pca.explained_variance_ratio_
components = pca.components_

projection = pca.transform(phase_corot)

# -------------------------
# variance plot
# -------------------------

plt.figure(figsize=(8,5))

plt.plot(explained[:20], marker="o")

plt.title("PCA variance (drift removed)")
plt.xlabel("mode")
plt.ylabel("variance")

plt.grid()

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "pca_variance_corot.png")
plt.close()

# -------------------------
# spatial modes
# -------------------------

plt.figure(figsize=(10,6))

for i in range(6):
    plt.plot(components[i], label=f"mode {i+1}")

plt.legend()

plt.title("Spatial PCA modes (drift removed)")
plt.xlabel("node")
plt.ylabel("amplitude")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "pca_modes_corot.png")
plt.close()

# -------------------------
# temporal evolution
# -------------------------

plt.figure(figsize=(10,6))

plt.plot(projection[:,0], label="mode1")
plt.plot(projection[:,1], label="mode2")
plt.plot(projection[:,2], label="mode3")

plt.legend()

plt.title("Temporal PCA modes (drift removed)")
plt.xlabel("time")
plt.ylabel("mode amplitude")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "pca_temporal_corot.png")
plt.close()

# -------------------------
# report
# -------------------------

with open(OUTPUT_DIR / "pca_corot_report.txt","w") as f:

    f.write("Drift Removed PCA\n")
    f.write("=================\n\n")

    for i in range(10):
        f.write(f"mode {i+1}: {explained[i]:.5f}\n")

print("Drift removed PCA complete.")
