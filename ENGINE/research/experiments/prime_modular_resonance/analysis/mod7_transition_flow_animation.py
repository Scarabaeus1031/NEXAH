import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import Counter
import os

# =========================
# PARAMETERS
# =========================
MOD = 7
N_PRIMES = 4000
NUM_PARTICLES = 28
FRAMES = 420
INTERVAL = 40
SMOOTHING = 0.22
TRAIL_LENGTH = 20
MIN_EDGE_WEIGHT = 0.08

# =========================
# PRIME GENERATOR
# =========================
def generate_primes(n: int):
    primes = []
    num = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1
    return primes

# =========================
# CIRCLE EMBEDDING
# =========================
def embed_circle(mod: int):
    angles = np.array([2 * np.pi * i / mod for i in range(mod)])
    return np.column_stack((np.cos(angles), np.sin(angles)))

# =========================
# BUILD TRANSITIONS
# =========================
def build_transition_data(mod: int, n_primes: int):
    primes = generate_primes(n_primes)
    residues = [p % mod for p in primes]

    seq_pairs = list(zip(residues[:-1], residues[1:]))
    pair_counts = Counter(seq_pairs)

    max_count = max(pair_counts.values()) if pair_counts else 1
    edge_weights = {k: v / max_count for k, v in pair_counts.items()}

    # build probability map
    transition_probs = {i: [] for i in range(mod)}
    for (a, b), w in edge_weights.items():
        transition_probs[a].append((b, w))

    # normalize per node
    for k in transition_probs:
        total = sum(w for _, w in transition_probs[k])
        if total > 0:
            transition_probs[k] = [(b, w / total) for b, w in transition_probs[k]]

    return edge_weights, transition_probs

# =========================
# PARTICLE SYSTEM
# =========================
class Particle:
    def __init__(self, node, pos):
        self.node = node
        self.pos = pos.copy()
        self.target = pos.copy()
        self.trail = []

    def update(self):
        self.pos += (self.target - self.pos) * SMOOTHING
        self.trail.append(self.pos.copy())
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)

# =========================
# MAIN
# =========================
def main():
    coords = embed_circle(MOD)
    edge_weights, transition_probs = build_transition_data(MOD, N_PRIMES)

    # particles init
    particles = []
    for _ in range(NUM_PARTICLES):
        node = np.random.randint(0, MOD)
        particles.append(Particle(node, coords[node]))

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_aspect("equal")
    ax.axis("off")

    # draw base circle
    theta = np.linspace(0, 2*np.pi, 400)
    ax.plot(np.cos(theta), np.sin(theta), alpha=0.15)

    # draw edges once (static)
    for (a, b), w in edge_weights.items():
        if w < MIN_EDGE_WEIGHT:
            continue
        x1, y1 = coords[a]
        x2, y2 = coords[b]
        ax.plot(
            [x1, x2],
            [y1, y2],
            alpha=0.1 + 0.4 * w,
            linewidth=1 + 2 * w
        )

    # nodes
    node_scatter = ax.scatter(coords[:,0], coords[:,1], s=120, zorder=5)

    trail_lines = [ax.plot([], [], lw=1)[0] for _ in range(NUM_PARTICLES)]
    particle_dots = ax.scatter([], [], s=20, zorder=6)

    # =========================
    # UPDATE LOOP
    # =========================
    def update(frame):
        xs, ys = [], []

        for i, p in enumerate(particles):

            # occasionally jump to new node
            if frame % 12 == 0:
                probs = transition_probs[p.node]
                if probs:
                    nodes, weights = zip(*probs)
                    p.node = np.random.choice(nodes, p=weights)
                    p.target = coords[p.node]

            p.update()

            # trails
            trail = np.array(p.trail)
            if len(trail) > 1:
                trail_lines[i].set_data(trail[:,0], trail[:,1])
                trail_lines[i].set_alpha(0.4)
            else:
                trail_lines[i].set_data([], [])

            xs.append(p.pos[0])
            ys.append(p.pos[1])

        particle_dots.set_offsets(np.column_stack([xs, ys]))

        return trail_lines + [particle_dots]

    ani = FuncAnimation(fig, update, frames=FRAMES, interval=INTERVAL)

    # =========================
    # SAVE
    # =========================
    os.makedirs("output/plots", exist_ok=True)
    path = "output/plots/mod7_transition_flow.gif"

    print("[INFO] Saving GIF...")
    ani.save(path, writer="pillow", fps=25)
    print(f"[OK] Saved to {path}")

    plt.close()

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
