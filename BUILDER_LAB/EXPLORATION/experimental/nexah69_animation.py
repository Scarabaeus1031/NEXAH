import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# =========================
# INPUT (anpassen!)
# =========================

# trajectory: shape (T, 2)
# flow field: X, Y grid + U, V over time

# Beispiel-Placeholder (ersetzen!)
T = len(trajectory)

# =========================
# PHASE (zentral!)
# =========================

theta = np.unwrap(np.arctan2(trajectory[:,1], trajectory[:,0]))
phase_norm = (theta - theta.min()) / (theta.max() - theta.min())

# colormap (clean + scientific)
cmap = plt.cm.hsv
colors = cmap(phase_norm)

# =========================
# FIGURE SETUP (clean)
# =========================

fig, ax = plt.subplots(figsize=(6,6))
ax.set_facecolor("white")

# limits
ax.set_xlim(np.min(X), np.max(X))
ax.set_ylim(np.min(Y), np.max(Y))

# remove clutter
ax.set_xticks([])
ax.set_yticks([])

# =========================
# INITIAL ELEMENTS
# =========================

# flow field (light, not dominant)
quiver = ax.quiver(
    X, Y, U[0], V[0],
    color='black',
    alpha=0.15,
    scale=40
)

# trajectory line
line, = ax.plot([], [], lw=2, color='black')

# phase-colored points
scatter = ax.scatter([], [], c=[], s=10)

# =========================
# DRIFT DISPLAY
# =========================

drift_text = ax.text(
    0.02, 0.95,
    "",
    transform=ax.transAxes,
    fontsize=10
)

# =========================
# UPDATE FUNCTION
# =========================

def update(frame):
    
    # update flow
    quiver.set_UVC(U[frame], V[frame])

    # trajectory
    x = trajectory[:frame, 0]
    y = trajectory[:frame, 1]

    line.set_data(x, y)

    # phase coloring
    scatter.set_offsets(np.c_[x, y])
    scatter.set_color(colors[:frame])

    # drift (μ Δθ)
    if frame > 10:
        drift = np.mean(np.diff(theta[:frame]))
        drift_text.set_text(f"drift μΔθ ≈ {drift:.4f}")
    else:
        drift_text.set_text("")

    return line, scatter, quiver, drift_text

# =========================
# ANIMATION
# =========================

anim = FuncAnimation(
    fig,
    update,
    frames=T,
    interval=30,
    blit=False
)

# =========================
# SAVE (clean output)
# =========================

anim.save(
    "nexah_phase_flow_clean.gif",
    writer="pillow",
    fps=30
)

# optional mp4 (besser für papers)
# anim.save("nexah_phase_flow_clean.mp4", fps=30, dpi=200)
