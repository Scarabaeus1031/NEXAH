import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# =========================
# LOAD DATA
# =========================

traj = np.load("../data/trajectory.npy")
clusters = np.load("../data/clusters.npy")

N = len(traj)

mod = 17  # change to 7 if you want

# =========================
# SETUP FIGURE
# =========================

fig = plt.figure(figsize=(10, 5))

ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax2 = fig.add_subplot(1, 2, 2)

# Halvorsen trajectory plot
ax1.set_title("Halvorsen Flow")
ax1.set_xlim(traj[:,0].min(), traj[:,0].max())
ax1.set_ylim(traj[:,1].min(), traj[:,1].max())
ax1.set_zlim(traj[:,2].min(), traj[:,2].max())

line, = ax1.plot([], [], [], lw=1)
point, = ax1.plot([], [], [], 'ro')

# Residue / cluster plot
ax2.set_title(f"Cluster + Residue (mod {mod})")
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)

text_cluster = ax2.text(0.1, 0.7, "", fontsize=14)
text_residue = ax2.text(0.1, 0.5, "", fontsize=14)
text_jump = ax2.text(0.1, 0.3, "", fontsize=14)

pulse = ax2.scatter([0.5], [0.1], s=50)

# =========================
# ANIMATION
# =========================

def update(frame):

    i = frame

    # --- trajectory ---
    line.set_data(traj[:i,0], traj[:i,1])
    line.set_3d_properties(traj[:i,2])

    point.set_data(traj[i,0], traj[i,1])
    point.set_3d_properties(traj[i,2])

    # --- cluster / residue ---
    c = int(clusters[i])
    r = c % mod

    text_cluster.set_text(f"cluster: {c}")
    text_residue.set_text(f"residue: {r}")

    # --- jump detection ---
    if i > 0:
        prev = int(clusters[i-1])
        jump = (c - prev)

        text_jump.set_text(f"jump: {jump}")

        # pulse effect
        size = 50 + abs(jump) * 20
        pulse.set_sizes([size])
    else:
        text_jump.set_text("jump: -")

    return line, point, text_cluster, text_residue, text_jump, pulse

# =========================
# RUN
# =========================

ani = FuncAnimation(
    fig,
    update,
    frames=min(N, 2000),
    interval=20,
    blit=False
)

plt.tight_layout()
plt.show()
