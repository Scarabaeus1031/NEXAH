import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# OUTPUT
out_dir = "RESEARCH/VALIDATION/visuals/outputs"
os.makedirs(out_dir, exist_ok=True)

# --- simulate simple system (Kuramoto-like phase)
t = np.linspace(0, 50, 1000)

phi = np.sin(t) + 0.2*np.sin(3*t)
omega = np.gradient(phi)
omega_hat = np.convolve(omega, np.ones(50)/50, mode='same')

M = np.abs(omega - omega_hat)

# threshold for transition
threshold = np.percentile(M, 90)
iota = M > threshold

# --- figure
fig, axs = plt.subplots(3, 1, figsize=(8, 8))

# --- animation update
def update(frame):
    for ax in axs:
        ax.clear()

    # Phase
    axs[0].plot(t[:frame], phi[:frame])
    axs[0].set_title("Phase φ(t)")

    # Omega vs expected
    axs[1].plot(t[:frame], omega[:frame], label="ω")
    axs[1].plot(t[:frame], omega_hat[:frame], label="ω̂")
    axs[1].legend()
    axs[1].set_title("Phase Velocity")

    # Mismatch + events
    axs[2].plot(t[:frame], M[:frame])
    axs[2].scatter(t[:frame][iota[:frame]], M[:frame][iota[:frame]], color="red", s=5)
    axs[2].axhline(threshold, linestyle="--")
    axs[2].set_title("Mismatch + IOTA events")

    plt.tight_layout()

# --- create animation
ani = FuncAnimation(fig, update, frames=len(t), interval=20)

# --- save
gif_path = os.path.join(out_dir, "phase_mismatch.gif")
ani.save(gif_path, writer='pillow')

print(f"Saved to: {gif_path}")
