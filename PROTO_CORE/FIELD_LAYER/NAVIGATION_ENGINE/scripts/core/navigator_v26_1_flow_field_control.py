import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# -----------------------
# Setup
# -----------------------

np.random.seed(42)

cluster_centers = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),  # target
    "C3": np.array([11.0, 28.5]),
}

target = "C2"
target_center = cluster_centers[target]

# -----------------------
# Potential function
# -----------------------

def potential(x):
    # quadratic well around C2
    return np.linalg.norm(x - target_center) ** 2

def grad_potential(x):
    # gradient of quadratic potential
    return 2 * (x - target_center)

# -----------------------
# Dynamics
# -----------------------

def flow_step(x, dt=0.1, noise=0.05):
    grad = grad_potential(x)
    
    # move downhill in potential
    dx = -grad
    
    # add small noise (system dynamics)
    dx += noise * np.random.randn(2)
    
    return x + dt * dx

# -----------------------
# Simulation
# -----------------------

def run_simulation(steps=200):
    x = np.array([9.5, 25.0])  # start near C0
    trajectory = [x.copy()]
    
    clusters = []
    
    for _ in range(steps):
        x = flow_step(x)
        trajectory.append(x.copy())
        
        # assign nearest cluster
        dists = {k: np.linalg.norm(x - v) for k, v in cluster_centers.items()}
        clusters.append(min(dists, key=dists.get))
    
    return np.array(trajectory), clusters

# -----------------------
# Field grid
# -----------------------

def compute_field():
    xs = np.linspace(6, 16, 60)
    ys = np.linspace(21, 31, 60)
    X, Y = np.meshgrid(xs, ys)
    
    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            point = np.array([X[i, j], Y[i, j]])
            grad = grad_potential(point)
            U[i, j] = -grad[0]
            V[i, j] = -grad[1]
    
    return X, Y, U, V

# -----------------------
# Plot
# -----------------------

def plot_results(traj, clusters):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    
    # Q1 — vector field
    X, Y, U, V = compute_field()
    axs[0, 0].quiver(X, Y, U, V, color="white", alpha=0.6)
    
    for k, v in cluster_centers.items():
        axs[0, 0].scatter(v[0], v[1], s=200, label=k)
    
    axs[0, 0].set_title("Q1 — Flow Field (Gradient Control)")
    
    # Q2 — trajectory
    axs[0, 1].plot(traj[:, 0], traj[:, 1], color="orange", label="trajectory")
    axs[0, 1].scatter(traj[0, 0], traj[0, 1], color="green", s=100, label="start")
    axs[0, 1].scatter(traj[-1, 0], traj[-1, 1], color="yellow", s=100, label="end")
    
    axs[0, 1].set_title("Q2 — Continuous Trajectory")
    
    # Q3 — cluster trace
    cluster_ids = list(cluster_centers.keys())
    cluster_map = {c: i for i, c in enumerate(cluster_ids)}
    
    trace = [cluster_map[c] for c in clusters]
    axs[1, 0].plot(trace)
    axs[1, 0].set_title("Q3 — Cluster Trace")
    axs[1, 0].set_yticks(range(len(cluster_ids)))
    axs[1, 0].set_yticklabels(cluster_ids)
    
    # Q4 — visit counts
    counts = Counter(clusters)
    axs[1, 1].bar(counts.keys(), counts.values())
    axs[1, 1].set_title("Q4 — Visit Counts")
    
    plt.tight_layout()
    os.makedirs("FIELD_LAYER/outputs/plots", exist_ok=True)
    plt.savefig("FIELD_LAYER/outputs/plots/v26_1_flow_field_control.png")
    plt.show()

# -----------------------
# Main
# -----------------------

def main():
    print("Running V26.1 Flow Field Control...\n")
    
    traj, clusters = run_simulation()
    
    counts = Counter(clusters)
    print("Visit Counts:")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    
    print(f"\nFinal point: {traj[-1]}")
    
    plot_results(traj, clusters)

if __name__ == "__main__":
    main()
