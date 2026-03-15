import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from pathlib import Path
import matplotlib.animation as animation

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# -------------------------
# load phase data
# -------------------------

phase = np.load(PHASE_FILE)

phase = np.unwrap(phase, axis=0)

# remove global drift
global_phase = np.mean(phase, axis=1)
phase = phase - global_phase[:, None]

phase -= np.mean(phase, axis=0)

# -------------------------
# PCA
# -------------------------

pca = PCA(n_components=4)

coords = pca.fit_transform(phase)

m1 = coords[:,0]
m2 = coords[:,1]
m3 = coords[:,2]
m4 = coords[:,3]

# -------------------------
# animation setup
# -------------------------

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')

line, = ax.plot([], [], [], lw=1)

ax.set_xlabel("mode1")
ax.set_ylabel("mode2")
ax.set_zlabel("mode3")

ax.set_title("4D attractor rotation")

# axis limits

ax.set_xlim(np.min(m1), np.max(m1))
ax.set_ylim(np.min(m2), np.max(m2))
ax.set_zlim(np.min(m3), np.max(m3))


# -------------------------
# projection function
# -------------------------

def project(theta):

    x = m1*np.cos(theta) - m4*np.sin(theta)
    w = m1*np.sin(theta) + m4*np.cos(theta)

    y = m2*np.cos(theta) - m4*np.sin(theta)
    z = m3*np.cos(theta) - m4*np.sin(theta)

    return x, y, z


# -------------------------
# animation step
# -------------------------

def update(frame):

    theta = frame * 0.05

    x, y, z = project(theta)

    line.set_data(x, y)
    line.set_3d_properties(z)

    return line,


ani = animation.FuncAnimation(
    fig,
    update,
    frames=200,
    interval=50,
)

# save

ani.save(
    OUTPUT_DIR / "attractor_4d_rotation.gif",
    writer="pillow",
    fps=20
)

plt.close()

print("4D attractor animation saved.")
