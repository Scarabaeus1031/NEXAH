import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from pathlib import Path

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")

phase = np.load(PHASE_FILE)

# unwrap
phase = np.unwrap(phase, axis=0)

# remove drift
global_phase = np.mean(phase, axis=1)
phase = phase - global_phase[:,None]

phase -= np.mean(phase, axis=0)

# PCA
pca = PCA(n_components=3)
coords = pca.fit_transform(phase)

x = coords[:,0]
y = coords[:,1]
z = coords[:,2]

# flow (derivative)
dx = np.gradient(x)
dy = np.gradient(y)
dz = np.gradient(z)

# subsample for clarity
step = 40

xq = x[::step]
yq = y[::step]
zq = z[::step]

dxq = dx[::step]
dyq = dy[::step]
dzq = dz[::step]

fig = plt.figure(figsize=(9,7))
ax = fig.add_subplot(111, projection='3d')

# trajectory
ax.plot(x, y, z, alpha=0.4)

# flow arrows
ax.quiver(
    xq, yq, zq,
    dxq, dyq, dzq,
    length=0.5,
    normalize=True
)

ax.set_xlabel("mode1")
ax.set_ylabel("mode2")
ax.set_zlabel("mode3")

ax.set_title("Flow field in PCA phase space")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "pca_flow_field.png")

plt.close()

print("Flow field visualization saved.")
