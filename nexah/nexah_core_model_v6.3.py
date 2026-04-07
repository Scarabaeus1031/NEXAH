# ============================================================
# NEXAH v6.3 — Mode Fiber Separation (WORKING VERSION)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Hopf Projection
# ------------------------------------------------------------
def hopf_projection(v, dv, mode, energy):
    
    v_n = (v - 0.7) / 0.4
    dv_n = dv / 0.05
    
    mode_phase = float(mode) * np.pi / 2.0   # <-- wichtig (float!)
    
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
    
    for entry in traj:
        # robust unpack (wichtig!)
        v, dv, mode, energy = entry
        
        mode = int(mode) % 4   # <-- wichtig (safety)
        
        X, Y, Z = hopf_projection(v, dv, mode, energy)
        mode_data[mode].append((X, Y, Z))
    
    colors = ["blue", "red", "green", "orange"]
    
    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111, projection='3d')
    
    for mode in range(4):
        data = mode_data[mode]
        
        if len(data) == 0:
            continue
        
        data = np.array(data)
        
        ax.plot(
            data[:,0],
            data[:,1],
            data[:,2],
            color=colors[mode],
            label=f"mode {mode}",
            linewidth=2
        )
    
    ax.set_title("NEXAH v6.3 — Mode Fibers")
    ax.legend()
    
    plt.show()


# ------------------------------------------------------------
# 🔥 TEST RUN (damit du siehst ob es funktioniert)
# ------------------------------------------------------------
if __name__ == "__main__":
    
    traj = []
    
    for t in np.linspace(0, 20, 500):
        v = 0.7 + 0.2*np.sin(t)
        dv = 0.05*np.cos(t)
        mode = int((t // 3) % 4)
        energy = np.exp(-0.1*t)
        
        traj.append((v, dv, mode, energy))
    
    plot_hopf_modes(traj)
