import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from matplotlib.animation import FuncAnimation, PillowWriter

# =========================================================
# PATHS
# =========================================================

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))
sys.path.append(ROOT)

IEEE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(IEEE_DIR)

OUTPUT_DIR = os.path.join(IEEE_DIR, "outputs", "rotation_animation")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# IMPORTS
# =========================================================

from nexah.field_layer import Field

# =========================================================
# DUMMY PIPELINE (replace later)
# =========================================================

def run_powerflow(lam):
    n = 10
    V = 1.0 - 0.3 * lam + 0.01 * np.random.randn(n)
    theta = 0.1 * lam + 0.01 * np.random.randn(n)
    return V, theta

# =========================================================
# DATA
# =========================================================

lambda_values = np.linspace(0.5, 1.5, 120)

states = []
for lam in lambda_values:
    V, theta = run_powerflow(lam)
    states.append(np.concatenate([V, theta]))

states = np.array(states)

# =========================================================
# FIELD
# =========================================================

field = Field(states)
vectors = field.get_vector_field()

# =========================================================
# PCA 3D
# =========================================================

pca3 = PCA(n_components=3)
states_3d = pca3.fit_transform(states)
vectors_3d = pca3.transform(states + vectors) - states_3d

# =========================================================
# FIGURE
# =========================================================

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(projection="3d")

# draw once
ax.plot(
    states_3d[:, 0],
    states_3d[:, 1],
    states_3d[:, 2],
    color="white",
    linewidth=2,
    alpha=0.65,
    label="trajectory"
)

for i in range(0, len(states_3d), 5):
    ax.quiver(
        states_3d[i, 0],
        states_3d[i, 1],
        states_3d[i, 2],
        vectors_3d[i, 0],
        vectors_3d[i, 1],
        vectors_3d[i, 2],
        length=0.045,
        normalize=True,
        alpha=0.75
    )

ax.scatter(
    states_3d[-1, 0],
    states_3d[-1, 1],
    states_3d[-1, 2],
    color="yellow",
    edgecolor="black",
    s=45,
    label="collapse"
)

ax.set_title("NEXAH FIELD — 3D Rotation")
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_zlabel("PC3")
ax.legend()

# fix axis ranges for stable animation
pad = 0.02
ax.set_xlim(states_3d[:, 0].min() - pad, states_3d[:, 0].max() + pad)
ax.set_ylim(states_3d[:, 1].min() - pad, states_3d[:, 1].max() + pad)
ax.set_zlim(states_3d[:, 2].min() - pad, states_3d[:, 2].max() + pad)

def update(angle):
    ax.view_init(elev=28, azim=angle)
    return fig,

anim = FuncAnimation(fig, update, frames=np.arange(0, 360, 4), interval=80, blit=False)

gif_path = os.path.join(OUTPUT_DIR, "field_rotation.gif")
anim.save(gif_path, writer=PillowWriter(fps=12), dpi=160)

plt.show()
print(f"Saved animation to: {gif_path}")
