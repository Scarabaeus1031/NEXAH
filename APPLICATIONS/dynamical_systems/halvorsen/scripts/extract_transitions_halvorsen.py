# ⚡ NEXAH — Transition Extraction (Halvorsen)
# ------------------------------------------------------------
# Extracts transition structure from Halvorsen trajectory
#
# Pipeline:
# trajectory → discretization → transitions → normalization
#
# Output:
# - transition_counts.txt
# - transition_probabilities.txt
# - transition_matrix.png
#
# ------------------------------------------------------------

import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt


# -----------------------------
# Halvorsen system
# -----------------------------

def halvorsen(state, a=1.4):
    x, y, z = state

    dx = -a * x - 4*y - 4*z - y**2
    dy = -a * y - 4*z - 4*x - z**2
    dz = -a * z - 4*x - 4*y - x**2

    return np.array([dx, dy, dz])


# -----------------------------
# RK4 integrator
# -----------------------------

def rk4_step(f, state, dt):
    k1 = f(state)
    k2 = f(state + 0.5 * dt * k1)
    k3 = f(state + 0.5 * dt * k2)
    k4 = f(state + dt * k3)

    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


# -----------------------------
# Simulation
# -----------------------------

def simulate(n_steps=50000, dt=0.01):
    state = np.array([1.0, 0.0, 0.0])
    traj = np.zeros((n_steps, 3))

    for i in range(n_steps):
        state = rk4_step(halvorsen, state, dt)
        traj[i] = state

    return traj


# -----------------------------
# Discretization (VERY IMPORTANT)
# -----------------------------

def discretize(traj, bins=5):
    """
    Simple grid-based discretization
    maps continuous space → discrete regions
    """

    mins = traj.min(axis=0)
    maxs = traj.max(axis=0)

    normalized = (traj - mins) / (maxs - mins + 1e-9)

    indices = (normalized * bins).astype(int)
    indices = np.clip(indices, 0, bins-1)

    # compress 3D index → single state ID
    state_ids = indices[:,0] * bins**2 + indices[:,1] * bins + indices[:,2]

    return state_ids


# -----------------------------
# Transition extraction
# -----------------------------

def extract_transitions(state_ids):
    transitions = {}

    for i in range(len(state_ids)-1):
        a = state_ids[i]
        b = state_ids[i+1]

        if a not in transitions:
            transitions[a] = {}

        if b not in transitions[a]:
            transitions[a][b] = 0

        transitions[a][b] += 1

    return transitions


# -----------------------------
# Normalize transitions
# -----------------------------

def normalize(transitions):
    probs = {}

    for state, edges in transitions.items():
        total = sum(edges.values())

        probs[state] = {
            target: count / total
            for target, count in edges.items()
        }

    return probs


# -----------------------------
# Save outputs
# -----------------------------

def save_outputs(counts, probs, base_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    txt_path = os.path.join(base_dir, f"transitions_{timestamp}.txt")

    with open(txt_path, "w") as f:
        f.write("RAW COUNTS\n")
        f.write("="*40 + "\n")
        for k,v in counts.items():
            f.write(f"{k} -> {v}\n")

        f.write("\nPROBABILITIES\n")
        f.write("="*40 + "\n")
        for k,v in probs.items():
            f.write(f"{k} -> {v}\n")

    print(f"[✓] TXT saved: {txt_path}")


# -----------------------------
# Simple matrix visualization
# -----------------------------

def plot_matrix(probs, base_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    states = list(probs.keys())
    size = len(states)

    matrix = np.zeros((size, size))

    index_map = {s:i for i,s in enumerate(states)}

    for s, edges in probs.items():
        for t, p in edges.items():
            if t in index_map:
                matrix[index_map[s], index_map[t]] = p

    fig, ax = plt.subplots(figsize=(6,6))
    im = ax.imshow(matrix)

    plt.colorbar(im)
    ax.set_title("Transition Probability Matrix")

    plt.tight_layout()

    path = os.path.join(base_dir, f"transition_matrix_{timestamp}.png")
    fig.savefig(path, dpi=300)

    print(f"[✓] PNG saved: {path}")


# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":

    base_dir = os.path.join(
        "APPLICATIONS",
        "dynamical_systems",
        "halvorsen",
        "outputs"
    )
    os.makedirs(base_dir, exist_ok=True)

    print("→ simulate")
    traj = simulate()

    print("→ discretize")
    states = discretize(traj, bins=6)

    print("→ extract transitions")
    counts = extract_transitions(states)

    print("→ normalize")
    probs = normalize(counts)

    print("→ save")
    save_outputs(counts, probs, base_dir)
    plot_matrix(probs, base_dir)

    print("✔ DONE")
