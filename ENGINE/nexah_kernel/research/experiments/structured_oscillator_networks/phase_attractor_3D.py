import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")

phase = np.load(PHASE_FILE)

phase = np.unwrap(phase, axis=0)

# remove drift

global_phase = np.mean(phase, axis=1)

phase -= global_phase[:,None]

phase -= np.mean(phase, axis=0)

# PCA

pca = PCA(n_components=3)

coords = pca.fit_transform(phase)

x = coords[:,0]
y = coords[:,1]
z = coords[:,2]

fig = plt.figure(figsize=(8,6))

ax = fig.add_subplot(111, projection='3d')

ax.plot(x, y, z, linewidth=0.5)

ax.set_xlabel("mode1")
ax.set_ylabel("mode2")
ax.set_zlabel("mode3")

ax.set_title("Phase space attractor")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "phase_attractor_3d.png")

plt.close()

print("3D attractor written.")
