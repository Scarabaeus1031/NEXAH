# ============================================================
# NEXAH v6.2 — Hopf Projection Layer
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# ------------------------------------------------------------
# Hopf Projection (S³ → R³)
# ------------------------------------------------------------
def hopf_projection(v, dv, mode, energy):
    """
    Map (v, dv, mode, energy) → 4D → Hopf projection → 3D
    """
    
    # --- normalize physical variables ---
    v_n = (v - 0.7) / 0.4          # center around threshold
    dv_n = dv / 0.05               # scale derivative
    
    # --- encode mode as phase ---
    mode_phase = mode * np.pi / 2.0
    
    x1 = v_n
    x2 = dv_n
    x3 = np.sin(mode_phase)
    x4 = np.cos(mode_phase)
    
    # --- normalize to S³ ---
    norm = np.sqrt(x1**2 + x2**2 + x3**2 + x4**2 + 1e-9)
    
    x1 /= norm
    x2 /= norm
    x3 /= norm
    x4 /= norm
    
    # --- Hopf map ---
    X = 2*(x1*x3 + x2*x4)
    Y = 2*(x2*x3 - x1*x4)
    Z = x1**2 + x2**2 - x3**2 - x4**2
    
    return X, Y, Z


# ------------------------------------------------------------
# Plot trajectory in Hopf space
# ------------------------------------------------------------
def plot_hopf_trajectory(traj, title="NEXAH v6.2 — Hopf Projection"):
    """
    traj = list of (v, dv, mode, energy)
    """
    
    Xs, Ys, Zs = [], [], []
    
    for v, dv, mode, energy in traj:
        X, Y, Z = hopf_projection(v, dv, mode, energy)
        Xs.append(X)
        Ys.append(Y)
        Zs.append(Z)
    
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(Xs, Ys, Zs, linewidth=2)
    
    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# OPTIONAL: Test with dummy trajectory (remove later)
# ------------------------------------------------------------
if __name__ == "__main__":
    
    # Fake trajectory for quick test
    traj = []
    
    for t in np.linspace(0, 10, 300):
        v = 0.7 + 0.2*np.sin(t)
        dv = 0.05*np.cos(t)
        mode = int((t // 2) % 4)   # cycles through 0–3
        energy = np.exp(-0.3*t)
        
        traj.append((v, dv, mode, energy))
    
    plot_hopf_trajectory(traj)
