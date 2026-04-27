import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# =========================
# LOAD DATA
# =========================

traj_h = np.load("../data/trajectory.npy")
traj_l = np.load("../data/trajectory_lorenz.npy")
clusters = np.load("../data/clusters.npy")

N = min(len(traj_h), len(traj_l))
mod = 17

# =========================
# SETUP FIGURE
# =========================

fig = plt.figure(figsize=(12, 5))

# --- LEFT: Lorenz ---
axL = fig.add_subplot(1, 3, 1, projection='3d')
axL.set_title("Lorenz")

axL.set_xlim(traj_l[:,0].min(), traj_l[:,0].max())
axL.set_ylim(traj_l[:,1].min(), traj_l[:,1].max())
axL.set_zlim(traj_l[:,2].min(), traj_l[:,2].max())

lineL, = axL.plot([], [], [], lw=1)
pointL, = axL.plot([], [], [], 'o')

# --- MIDDLE: Halvorsen ---
axH = fig.add_subplot(1, 3, 2, projection='3d')
axH.set_title("Halvorsen")

axH.set_xlim(traj_h[:,0].min(), traj_h[:,0].max())
axH.set_ylim(traj_h[:,1].min(), traj_h[:,1].max())
axH.set_zlim(traj_h[:,2].min(), traj_h[:,2].max())

lineH, = axH.plot([], [], [], lw=1)
pointH, = axH.plot([], [], [], 'o')

# --- RIGHT: State Panel ---
axS = fig.add_subplot(1, 3, 3)
axS.set_title(f"State / Residue (mod {mod})")
axS.set_xlim(0, 1)
axS.set_ylim(0, 1)
axS.axis("off")

text_cluster = axS.text(0.1, 0.7, "", fontsize=14)
text_residue = axS.text(0.1, 0.5, "", fontsize=14)
text_jump = axS.text(0.1, 0.3, "", fontsize=14)

pulse = axS.scatter([0.5], [0.1], s=50)

# =========================
# ANIMATION
# =========================

def update(frame):
    i = frame

    # --- Lorenz ---
    lineL.set_data(traj_l[:i,0], traj_l[:i,1])
    lineL.set_3d_properties(traj_l[:i,2])

    xL, yL, zL = traj_l[i]
    pointL.set_data([xL], [yL])
    pointL.set_3d_properties([zL])

    # --- Halvorsen ---
    lineH.set_data(traj_h[:i,0], traj_h[:i,1])
    lineH.set_3d_properties(traj_h[:i,2])

    xH, yH, zH = traj_h[i]
    pointH.set_data([xH], [yH])
    pointH.set_3d_properties([zH])

    # --- cluster / residue (Halvorsen only for now) ---
    c = int(clusters[i])
    r = c % mod

    text_cluster.set_text(f"cluster: {c}")
    text_residue.set_text(f"residue: {r}")

    # color both systems with same residue color
    color = plt.cm.hsv(r / mod)
    pointH.set_color(color)
    pointL.set_color(color)

    # --- jump ---
    if i > 0:
        prev = int(clusters[i-1])
        jump = c - prev

        text_jump.set_text(f"jump: {jump}")

        size = 50 + abs(jump) * 25
        pulse.set_sizes([size])
    else:
        text_jump.set_text("jump: -")

    return (
        lineL, pointL,
        lineH, pointH,
        text_cluster, text_residue, text_jump, pulse
    )

# =========================
# RUN + SAVE
# =========================

ani = FuncAnimation(
    fig,
    update,
    frames=min(N, 2000),
    interval=20,
    blit=False
)

print("→ saving dual animation...")

ani.save(
    "../outputs/halvorsen_lorenz_dual.gif",
    writer="pillow",
    fps=25
)

print("✓ saved: ../outputs/halvorsen_lorenz_dual.mp4")
