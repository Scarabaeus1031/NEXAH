import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

# trajectory: (T, 3)
trajectory = np.load("APPLICATIONS/dynamical_systems/halvorsen/data/trajectory.npy")

# cluster assignments: (T,)
clusters = np.load("APPLICATIONS/dynamical_systems/halvorsen/data/clusters.npy")

# transition matrix (policy)
P = np.load("APPLICATIONS/dynamical_systems/halvorsen/outputs/gate_aware_policy_matrix_*.npy")

# residue model (mod 17 empfohlen)
residue_model = np.load("APPLICATIONS/dynamical_systems/halvorsen/outputs/residue_model_mod17.npy")

n_states = P.shape[0]


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def predict_next(cluster):
    r = cluster % residue_model.shape[0]
    probs = residue_model[r]
    return np.argmax(probs)

def true_next(cluster):
    probs = P[cluster]
    return np.argmax(probs)


# ------------------------------------------------------------
# FIGURE SETUP
# ------------------------------------------------------------

fig = plt.figure(figsize=(10, 5))

ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax2 = fig.add_subplot(1, 2, 2)

# Halvorsen plot
ax1.set_title("Halvorsen Flow")
ax1.set_xlim(-20, 20)
ax1.set_ylim(-30, 30)
ax1.set_zlim(0, 50)

line, = ax1.plot([], [], [], lw=1)
point = ax1.scatter([], [], [], s=50)

# NEXAH field (simple grid layout)
coords = np.array([
    [i % 6, i // 6] for i in range(n_states)
])

scat = ax2.scatter(coords[:,0], coords[:,1], s=100, c='gray')

ax2.set_title("NEXAH State Field")
ax2.set_xlim(-1, 6)
ax2.set_ylim(-1, 4)


# ------------------------------------------------------------
# ANIMATION
# ------------------------------------------------------------

history = 50

def update(frame):
    t = frame

    # --- Halvorsen ---
    start = max(0, t - history)
    xs = trajectory[start:t, 0]
    ys = trajectory[start:t, 1]
    zs = trajectory[start:t, 2]

    line.set_data(xs, ys)
    line.set_3d_properties(zs)

    x, y, z = trajectory[t]
    point._offsets3d = ([x], [y], [z])

    # --- States ---
    cluster = clusters[t]
    pred = predict_next(cluster)
    true = true_next(cluster)

    colors = ["gray"] * n_states

    # current
    colors[cluster] = "white"

    # predicted
    colors[pred] = "blue"

    # true next
    colors[true] = "green"

    # overlap (correct prediction)
    if pred == true:
        colors[pred] = "cyan"

    scat.set_color(colors)

    ax2.set_title(f"State: {cluster} | Pred: {pred} | True: {true}")

    return line, point, scat


anim = FuncAnimation(fig, update, frames=len(trajectory), interval=50)

plt.tight_layout()
plt.show()
