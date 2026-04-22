import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# --- clusters ---
clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),
    "C3": np.array([11.0, 28.5]),
}

# --- gaussian field ---
def gaussian(x, y, center, depth, sigma=1.2):
    return depth * np.exp(-((x-center[0])**2 + (y-center[1])**2)/(2*sigma**2))

# --- envelope ---
def envelope(t):
    return 1.0 + 0.4 * np.sin(0.03 * t)

# --- dynamic attractor strength ---
def attractor_strengths(t):
    e = envelope(t)

    return {
        "C0": 1.5 * e,
        "C1": 2.0 * (1.0 + 0.4 * np.sin(0.03 * t + np.pi/2)),
        "C2": 3.0 * (1.0 + 0.3 * np.sin(0.03 * t)),
        "C3": -2.0  # repulsive
    }

# --- field ---
def field(x, y, t):
    strengths = attractor_strengths(t)
    val = 0.0
    for c, pos in clusters.items():
        val += gaussian(x, y, pos, strengths[c])
    return val

# --- gradient (finite diff) ---
def grad(x, y, t, eps=1e-3):
    dx = (field(x+eps, y, t) - field(x-eps, y, t)) / (2*eps)
    dy = (field(x, y+eps, t) - field(x, y-eps, t)) / (2*eps)
    return np.array([dx, dy])

# --- simulation ---
def simulate(steps=250):
    x = np.array([9.5, 27.0])  # start near top right
    traj = [x.copy()]
    visited = []

    for t in range(steps):
        g = grad(x[0], x[1], t)
        x = x + 0.15 * g  # step size

        traj.append(x.copy())

        # nearest cluster
        dists = {k: np.linalg.norm(x - v) for k, v in clusters.items()}
        nearest = min(dists, key=dists.get)
        visited.append(nearest)

    return np.array(traj), visited

# --- plot ---
def plot(traj, visited):
    xs = np.linspace(6, 17, 200)
    ys = np.linspace(22, 31, 200)
    X, Y = np.meshgrid(xs, ys)

    Z = field(X, Y, t=200)

    plt.figure(figsize=(10, 8))
    plt.contourf(X, Y, Z, levels=50, cmap="viridis")

    # trajectory
    plt.plot(traj[:,0], traj[:,1], color="white", lw=2)

    # clusters
    for k, v in clusters.items():
        plt.scatter(v[0], v[1], s=150, label=k)

    plt.title("V28 Envelope Field Navigation")
    plt.xlabel("α")
    plt.ylabel("β")
    plt.legend()
    plt.show()

    # counts
    counts = Counter(visited)
    print("\nVisit Counts:")
    for k in clusters.keys():
        print(f"{k}: {counts[k]}")

# --- main ---
def main():
    print("Running V28 Envelope Field...\n")
    traj, visited = simulate()
    plot(traj, visited)

if __name__ == "__main__":
    main()
