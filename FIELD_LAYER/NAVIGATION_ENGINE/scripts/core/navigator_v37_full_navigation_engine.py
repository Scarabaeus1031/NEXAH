import os
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)

# ============================================================
# 1. CLUSTERS / NODES
# ============================================================

clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),  # TARGET
    "C3": np.array([11.0, 28.5]),
}

cluster_colors = {
    "C0": "#1f77b4",
    "C1": "#ff7f0e",
    "C2": "#2ca02c",
    "C3": "#d62728",
}

nodes = ["C0", "C1", "C2", "C3"]

# ============================================================
# 2. FIELD
# ============================================================

def gaussian(x, y, center, strength, sigma=1.2):
    return strength * np.exp(-((x-center[0])**2 + (y-center[1])**2)/(2*sigma**2))

def scalar_field(x, y):
    return (
        gaussian(x,y,clusters["C0"], 1.5)
        + gaussian(x,y,clusters["C1"], 2.0)
        + gaussian(x,y,clusters["C2"], 3.0)
        - gaussian(x,y,clusters["C3"], 2.0)
    )

def grad_field(x,y,eps=1e-3):
    dx = (scalar_field(x+eps,y)-scalar_field(x-eps,y))/(2*eps)
    dy = (scalar_field(x,y+eps)-scalar_field(x,y-eps))/(2*eps)
    return np.array([dx,dy])

def rotational_field(x,y):
    p = np.array([x,y])
    v = np.zeros(2)

    for c in ["C2","C3"]:
        r = p - clusters[c]
        d = np.linalg.norm(r)+1e-9
        swirl = np.array([r[1], -r[0]]) * np.exp(-(d**2)/(2*1.5**2))
        v += swirl

    return 0.6*v

def combined_field(x,y):
    return grad_field(x,y) + rotational_field(x,y)

# ============================================================
# 3. GRAPH (weights from V36 approx)
# ============================================================

edges = {
    ("C0","C1"):2.4,
    ("C0","C2"):3.6,
    ("C0","C3"):4.3,
    ("C1","C2"):2.3,
    ("C1","C3"):6.6,
    ("C2","C3"):5.6,
}

# symmetric
for (a,b),w in list(edges.items()):
    edges[(b,a)] = w

# ============================================================
# 4. DIJKSTRA
# ============================================================

def shortest_path(start, goal):
    dist = {n: np.inf for n in nodes}
    prev = {n: None for n in nodes}
    dist[start] = 0

    Q = nodes.copy()

    while Q:
        u = min(Q, key=lambda n: dist[n])
        Q.remove(u)

        if u == goal:
            break

        for v in nodes:
            if (u,v) in edges:
                alt = dist[u] + edges[(u,v)]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

    # reconstruct
    path = []
    u = goal
    while u:
        path.insert(0,u)
        u = prev[u]

    return path

# ============================================================
# 5. FIELD TRAJECTORY
# ============================================================

def follow_field(start, target, steps=200, step_size=0.08):
    traj = [start.copy()]
    x = start.copy()

    for _ in range(steps):
        v = combined_field(x[0],x[1])
        direction = v + 0.3*(target - x)  # bias toward node
        direction = direction/(np.linalg.norm(direction)+1e-9)

        x = x + step_size * direction
        traj.append(x.copy())

        if np.linalg.norm(x-target) < 0.2:
            break

    return np.array(traj)

# ============================================================
# 6. FULL NAVIGATION
# ============================================================

start_point = np.array([8.0, 28.0])  # frei wählbar
target_node = "C2"

# nearest node
def nearest_node(p):
    return min(nodes, key=lambda n: np.linalg.norm(p-clusters[n]))

start_node = nearest_node(start_point)

graph_path = shortest_path(start_node, target_node)

print("Graph path:", graph_path)

# build full trajectory
full_traj = []

current_pos = start_point.copy()

for node in graph_path:
    target = clusters[node]
    segment = follow_field(current_pos, target)
    full_traj.extend(segment)
    current_pos = segment[-1]

full_traj = np.array(full_traj)

# ============================================================
# 7. VISUALIZATION
# ============================================================

xv = np.linspace(6,17,200)
yv = np.linspace(22,31,200)
X,Y = np.meshgrid(xv,yv)
Z = scalar_field(X,Y)

plt.figure(figsize=(10,8))

plt.contourf(X,Y,Z,levels=40)

# clusters
for c,p in clusters.items():
    plt.scatter(p[0],p[1],color=cluster_colors[c],s=120)
    plt.text(p[0]+0.1,p[1]+0.1,c)

# trajectory
plt.plot(full_traj[:,0],full_traj[:,1],color="cyan",lw=3,label="Navigator Path")

# start
plt.scatter(start_point[0],start_point[1],color="white",s=100,label="Start")

plt.title("V37 — Full Field + Graph Navigation")
plt.xlabel("α")
plt.ylabel("β")
plt.legend()

out_path = os.path.join(OUTPUT_DIR, "v37_full_navigation.png")
plt.savefig(out_path, dpi=150)
plt.close()

print("Saved:", out_path)
