# ============================================================
# NEXAH v6.3b — Rotation Quantization
# ============================================================

import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Winkel entlang der Trajektorie berechnen
# ------------------------------------------------------------
def compute_angles(X, Y):
    return np.unwrap(np.arctan2(Y, X))


# ------------------------------------------------------------
# Rotation pro Mode messen
# ------------------------------------------------------------
def analyze_mode_rotation(traj, hopf_projection):
    
    mode_data = {0: [], 1: [], 2: [], 3: []}
    
    # --- split trajectory ---
    for v, dv, mode, energy in traj:
        mode = int(mode) % 4
        X, Y, Z = hopf_projection(v, dv, mode, energy)
        mode_data[mode].append((X, Y, Z))
    
    results = {}
    
    for mode in range(4):
        data = mode_data[mode]
        
        if len(data) < 10:
            continue
        
        data = np.array(data)
        
        X = data[:,0]
        Y = data[:,1]
        
        angles = compute_angles(X, Y)
        
        total_rotation = angles[-1] - angles[0]
        rotations = total_rotation / (2*np.pi)
        
        results[mode] = rotations
    
    return results


# ------------------------------------------------------------
# Visualisieren
# ------------------------------------------------------------
def plot_mode_rotations(results):
    
    modes = list(results.keys())
    values = [results[m] for m in modes]
    
    plt.figure(figsize=(6,4))
    plt.bar(modes, values)
    
    plt.xlabel("Mode")
    plt.ylabel("Number of Rotations")
    plt.title("NEXAH v6.3b — Rotation per Mode")
    
    plt.grid(True)
    plt.show()


# ------------------------------------------------------------
# OPTIONAL: Quantization Check
# ------------------------------------------------------------
def check_quantization(results):
    
    print("\n=== Rotation Quantization Check ===")
    
    for mode, rot in results.items():
        
        approx = [
            2, 3, 4, 6, 8, 12, 24, 36, 72
        ]
        
        closest = min(approx, key=lambda x: abs(x - abs(rot)))
        
        print(f"mode {mode}: {rot:.3f} rotations → closest ≈ {closest}")
