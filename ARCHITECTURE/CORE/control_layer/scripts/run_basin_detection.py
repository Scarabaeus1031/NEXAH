import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# --------------------------------------------------
# ⚙️ FIELD DEFINITION (gleich wie Control Layer)
# --------------------------------------------------

def field(x, y):
    dx = -y - x * (x**2 + y**2 - 1)
    dy = x - y * (x**2 + y**2 - 1)
    return dx, dy


# --------------------------------------------------
# 🚀 TRAJECTORY SIMULATION
# --------------------------------------------------

def simulate_trajectory(x0, y0, steps=200, dt=0.05):
    x, y = x0, y0
    traj = []

    for _ in range(steps):
        dx, dy = field(x, y)
        x += dx * dt
        y += dy * dt
        traj.append([x, y])

    return np.array(traj)


# --------------------------------------------------
# 🌱 SAMPLE START POINTS
# --------------------------------------------------

np.random.seed(42)

n_points = 200
start_points = np.random.uniform(-2, 2, (n_points, 2))

endpoints = []
trajectories = []

for (x0, y0) in start_points:
    traj = simulate_trajectory(x0, y0)
    trajectories.append(traj)
    endpoints.append(traj[-1])

endpoints = np.array(endpoints)


# --------------------------------------------------
# 🧩 BASIN CLUSTERING
# --------------------------------------------------

n_basins = 3  # kannst du variieren
kmeans = KMeans(n_clusters=n_basins, n_init=10)
labels = kmeans.fit_predict(endpoints)
centers = kmeans.cluster_centers_


# --------------------------------------------------
# 🎨 VISUALIZATION
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 8))

# Feld visualisieren
grid_x, grid_y = np.meshgrid(
    np.linspace(-2, 2, 25),
    np.linspace(-2, 2, 25)
)

dx, dy = field(grid_x, grid_y)
ax.streamplot(grid_x, grid_y, dx, dy, color='black', density=1.2)

# Trajektorien einfärben nach Basin
colors = ['blue', 'green', 'red', 'purple', 'orange']

for i, traj in enumerate(trajectories):
    c = colors[labels[i] % len(colors)]
    ax.plot(traj[:, 0], traj[:, 1], color=c, alpha=0.4)

# Startpunkte
ax.scatter(start_points[:, 0], start_points[:, 1],
           color='black', s=10, label='start')

# Endpunkte (Basins)
for i in range(n_basins):
    pts = endpoints[labels == i]
    ax.scatter(pts[:, 0], pts[:, 1],
               color=colors[i], s=30, label=f'basin {i}')

# Zentren (Attractors)
ax.scatter(centers[:, 0], centers[:, 1],
           color='yellow', s=200, edgecolor='black', label='basin centers')

ax.set_title("NEXAH Basin Detection")
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.legend()
ax.grid(True)

# --------------------------------------------------
# 💾 SAVE
# --------------------------------------------------

output_path = "ARCHITECTURE/CORE/control_layer/outputs/demo/nexah_basin_detection.png"
plt.savefig(output_path, dpi=200)
print(f"✔ Saved → {output_path}")

# --------------------------------------------------
# 🧠 INTERPRETATION
# --------------------------------------------------

print("\n🧠 Interpretation:\n")
print("Colored trajectories → basin membership")
print("Clustered endpoints → attractor regions")
print("Yellow points → basin centers (approx attractors)")
print("\n→ system partitions state space into basins")
print("→ each basin defines a stable long-term behavior")
