# ============================================================
# NEXAH v6.9 — Phase Field Reconstruction
# ============================================================

import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Hopf Projection (same as before)
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
# Dummy trajectory (replace later)
# ------------------------------------------------------------
def generate_dummy_traj(n=5000):
    
    traj = []
    
    for t in range(n):
        v = 0.7 + 0.3*np.sin(t * 0.02)
        dv = 0.05*np.cos(t * 0.02)
        mode = (t // 300) % 4
        energy = dv**2
        
        traj.append((v, dv, mode, energy))
    
    return traj


# ------------------------------------------------------------
# Build phase-space trajectory
# ------------------------------------------------------------
def build_phase_trajectory(traj):
    
    points = []
    
    for v, dv, mode, energy in traj:
        X, Y, Z = hopf_projection(v, dv, mode, energy)
        points.append([X, Y])
    
    return np.array(points)


# ------------------------------------------------------------
# Estimate flow field (grid-based)
# ------------------------------------------------------------
def compute_flow_field(points, grid_size=30):
    
    xmin, ymin = points.min(axis=0)
    xmax, ymax = points.max(axis=0)
    
    xs = np.linspace(xmin, xmax, grid_size)
    ys = np.linspace(ymin, ymax, grid_size)
    
    U = np.zeros((grid_size, grid_size))
    V = np.zeros((grid_size, grid_size))
    counts = np.zeros((grid_size, grid_size))
    
    # compute local velocities
    for i in range(len(points) - 1):
        
        x, y = points[i]
        dx, dy = points[i+1] - points[i]
        
        xi = np.searchsorted(xs, x) - 1
        yi = np.searchsorted(ys, y) - 1
        
        if 0 <= xi < grid_size and 0 <= yi < grid_size:
            U[yi, xi] += dx
            V[yi, xi] += dy
            counts[yi, xi] += 1
    
    # normalize
    mask = counts > 0
    U[mask] /= counts[mask]
    V[mask] /= counts[mask]
    
    return xs, ys, U, V


# ------------------------------------------------------------
# Detect fixed points (low velocity regions)
# ------------------------------------------------------------
def detect_fixed_points(U, V, xs, ys, threshold=0.01):
    
    fixed_points = []
    
    for i in range(U.shape[0]):
        for j in range(U.shape[1]):
            
            speed = np.sqrt(U[i,j]**2 + V[i,j]**2)
            
            if speed < threshold:
                fixed_points.append((xs[j], ys[i]))
    
    return fixed_points


# ------------------------------------------------------------
# Plot field + trajectory
# ------------------------------------------------------------
def plot_phase_field(points, xs, ys, U, V, fixed_points):
    
    Xg, Yg = np.meshgrid(xs, ys)
    
    plt.figure(figsize=(8,6))
    
    # flow field
    plt.quiver(Xg, Yg, U, V, alpha=0.6)
    
    # trajectory
    plt.plot(points[:,0], points[:,1], color='black', linewidth=1, label="trajectory")
    
    # fixed points
    if len(fixed_points) > 0:
        fp = np.array(fixed_points)
        plt.scatter(fp[:,0], fp[:,1], color='red', s=40, label="fixed points")
    
    plt.title("NEXAH v6.9 — Phase Field Reconstruction")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.show()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":
    
    # 1. trajectory
    traj = generate_dummy_traj()
    print("Trajectory size:", len(traj))
    
    # 2. phase points
    points = build_phase_trajectory(traj)
    
    # 3. field
    xs, ys, U, V = compute_flow_field(points)
    
    # 4. fixed points
    fixed_points = detect_fixed_points(U, V, xs, ys)
    print("Fixed points detected:", len(fixed_points))
    
    # 5. plot
    plot_phase_field(points, xs, ys, U, V, fixed_points)
