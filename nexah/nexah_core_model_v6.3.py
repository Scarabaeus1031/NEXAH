# ============================================================
# NEXAH v6.3 — Mode Fiber Separation
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# ------------------------------------------------------------
# Hopf Projection (unchanged)
# ------------------------------------------------------------
def hopf_projection(v, dv, mode, energy):
    
    v_n = (v - 0.7) / 0.4
    dv_n = dv / 0.05
    
    mode_phase = mode * np.pi / 2.0
    
    x1 = v_n
    x2 = dv_n
    x3 = np.sin(mode_phase)
    x4 = np.cos(mode_phase)
    
    norm = np.sqrt(x1**2 + x2**2 + x3**2 + x4**2 + 1e-9)
    
    x1 /= norm
    x2 /= norm
    x3 /= norm
    x4 /= norm
    
    X = 2*(x1*x3 + x2*x4)
    Y = 2*(x2*x3 - x1*x4)
    Z = x1**2 + x2**2 - x3**2 - x4**2
    
    return X, Y, Z


# ------------------------------------------------------------
# Mode-separated plot
# ------------------------------------------------------------
def plot_hopf_modes(traj):
    
    mode_data = {0: [], 1: [], 2: [], 3: []}
    
    # --- split trajectory by mode ---
    for v, dv, mode, energy in traj:
        X, Y, Z = hopf_projection(v, dv, mode, energy)
        mode_data[mode].append((X, Y, Z))
    
    colors = {
        0: "blue",
        1: "red",
        2: "green",
        3: "orange"
    }
    
    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111, projection='3d')
    
    # --- plot each mode separately ---
    for mode in mode_data:
        if len(mode_data[mode]) == 0:
            continue
        
        data = np.array(mode_data[mode])
        
        ax.plot(
            data[:,0],
            data[:,1],
            data[:,2],
            color=colors[mode],
            label=f"mode {mode}",
            linewidth=2
        )
    
    ax.set_title("NEXAH v6.3 — Mode Fibers (Hopf Space)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    ax.legend()
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Optional: highlight transitions (Mode jumps)
# ------------------------------------------------------------
def plot_mode_transitions(traj):
    
    transitions = []
    
    for i in range(1, len(traj)):
        if traj[i][2] != traj[i-1][2]:
            v, dv, mode, energy = traj[i]
            X, Y, Z = hopf_projection(v, dv, mode, energy)
            transitions.append((X, Y, Z))
    
    if len(transitions) == 0:
        return
    
    transitions = np.array(transitions)
    
    fig = plt.figure(figsize=(7,6))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(
        transitions[:,0],
        transitions[:,1],
        transitions[:,2],
        color="black",
        s=40,
        label="mode switches"
    )
    
    ax.set_title("Mode Transition Points (Switch Geometry)")
    ax.legend()
    plt.show()
