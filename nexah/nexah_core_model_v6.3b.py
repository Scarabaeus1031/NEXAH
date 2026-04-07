# ============================================================
# NEXAH v6.3b — Rotation Quantization (STABLE)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Winkel entlang der Trajektorie berechnen
# ------------------------------------------------------------
def compute_angles(X, Y):
    return np.unwrap(np.arctan2(Y, X))


# ------------------------------------------------------------
# Rotation pro Mode messen (FIXED)
# ------------------------------------------------------------
def analyze_mode_rotation(traj, hopf_projection):
    
    print("Starting rotation analysis...")
    
    mode_data = {0: [], 1: [], 2: [], 3: []}
    
    # --- split trajectory ---
    for entry in traj:
        try:
            v, dv, mode, energy = entry
        except:
            continue
        
        mode = int(mode) % 4
        
        X, Y, Z = hopf_projection(v, dv, mode, energy)
        mode_data[mode].append((X, Y, Z))
    
    results = {}
    
    for mode in range(4):
        data = mode_data[mode]
        
        if len(data) < 20:
            print(f"Mode {mode}: skipped (too few points)")
            continue
        
        data = np.array(data)
        
        # 🔥 CRITICAL FIX: Downsampling
        step = max(1, len(data) // 500)
        data = data[::step]
        
        print(f"Mode {mode}: processing {len(data)} points")
        
        X = data[:, 0]
        Y = data[:, 1]
        
        # safety (avoid NaN issues)
        if np.any(np.isnan(X)) or np.any(np.isnan(Y)):
            print(f"Mode {mode}: NaN detected → skipped")
            continue
        
        angles = compute_angles(X, Y)
        
        total_rotation = angles[-1] - angles[0]
        rotations = total_rotation / (2*np.pi)
        
        results[mode] = rotations
    
    print("Done.\n")
    
    return results


# ------------------------------------------------------------
# Visualisieren
# ------------------------------------------------------------
def plot_mode_rotations(results):
    
    if len(results) == 0:
        print("No rotation data to plot.")
        return
    
    modes = list(results.keys())
    values = [results[m] for m in modes]
    
    plt.figure(figsize=(6,4))
    plt.bar(modes, values)
    
    plt.xlabel("Mode")
    plt.ylabel("Rotations")
    plt.title("NEXAH v6.3b — Rotation per Mode")
    
    plt.grid(True)
    plt.show()


# ------------------------------------------------------------
# Quantization Check
# ------------------------------------------------------------
def check_quantization(results):
    
    print("=== Rotation Quantization Check ===")
    
    approx = [2, 3, 4, 6, 8, 12, 24, 36, 72]
    
    for mode, rot in results.items():
        closest = min(approx, key=lambda x: abs(x - abs(rot)))
        print(f"mode {mode}: {rot:.3f} → closest ≈ {closest}")


# ------------------------------------------------------------
# TEST / RUN BLOCK (IMPORTANT)
# ------------------------------------------------------------
if __name__ == "__main__":
    
    print("Trajectory size:", len(traj))
    
    results = analyze_mode_rotation(traj, hopf_projection)
    
    print("Results:", results)
    
    plot_mode_rotations(results)
    
    check_quantization(results)
