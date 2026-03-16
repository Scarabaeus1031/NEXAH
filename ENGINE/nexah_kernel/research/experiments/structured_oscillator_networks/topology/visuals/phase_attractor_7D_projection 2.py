import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# LOAD
# ---------------------------------------------------------

phase = np.load(PHASE_FILE)

phase = np.unwrap(phase, axis=0)

# remove global drift
global_phase = np.mean(phase, axis=1)
phase = phase - global_phase[:, None]

# center
phase -= np.mean(phase, axis=0)

# ---------------------------------------------------------
# PCA → 7D state
# ---------------------------------------------------------

pca = PCA(n_components=7)

coords = pca.fit_transform(phase)

print("Explained variance first 7 modes:")
print(pca.explained_variance_ratio_)

# ---------------------------------------------------------
# 3D projection (mode1,2,3)
# ---------------------------------------------------------

x = coords[:,0]
y = coords[:,1]
z = coords[:,2]

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')

ax.plot(x, y, z, linewidth=0.6)

ax.set_xlabel("mode1")
ax.set_ylabel("mode2")
ax.set_zlabel("mode3")

ax.set_title("Phase attractor (PCA modes 1–3)")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "attractor_3d_modes123.png")
plt.close()

# ---------------------------------------------------------
# 4D → 3D projection
# (mode1,2,3,4 → rotated projection)
# ---------------------------------------------------------

m1 = coords[:,0]
m2 = coords[:,1]
m3 = coords[:,2]
m4 = coords[:,3]

# rotation projection
x = m1 + 0.5*m4
y = m2 + 0.5*m4
z = m3 + 0.5*m4

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')

ax.plot(x, y, z, linewidth=0.6)

ax.set_xlabel("mode1 + 0.5 mode4")
ax.set_ylabel("mode2 + 0.5 mode4")
ax.set_zlabel("mode3 + 0.5 mode4")

ax.set_title("4D → 3D projection of attractor")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "attractor_4d_projection.png")
plt.close()

# ---------------------------------------------------------
# pair plots of first 6 modes
# ---------------------------------------------------------

fig, axes = plt.subplots(3,2, figsize=(10,10))

pairs = [(0,1),(0,2),(1,2),(2,3),(3,4),(4,5)]

for ax,(i,j) in zip(axes.flat,pairs):

    ax.plot(coords[:,i], coords[:,j], linewidth=0.5)

    ax.set_xlabel(f"mode{i+1}")
    ax.set_ylabel(f"mode{j+1}")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "mode_pair_projections.png")
plt.close()

print("7D attractor analysis complete.")
