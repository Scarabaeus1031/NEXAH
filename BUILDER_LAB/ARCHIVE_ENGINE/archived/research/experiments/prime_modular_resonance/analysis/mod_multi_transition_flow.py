import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import Counter
import os

# =========================
# PARAMETERS
# =========================
MOD_LIST = [7, 11, 13]
N_PRIMES = 5000
NUM_PARTICLES = 32
FRAMES = 360
INTERVAL = 40
SMOOTHING = 0.22
TRAIL_LENGTH = 18
MIN_EDGE_WEIGHT = 0.06

OUTPUT_DIR = "output/curated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# PRIME GENERATOR
# =========================
def generate_primes(n):
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
# EMBEDDING
# =========================
def embed_circle(mod):
    angles = np.array([2 * np.pi * i / mod for i in range(mod)])
    return np.column_stack((np.cos(angles), np.sin(angles)))

# =========================
# TRANSITION BUILD
# =========================
def build_transition(mod, primes):
    residues = [p % mod for p in primes]
    pairs = list(zip(residues[:-1], residues[1:]))

    counts = Counter(pairs)
    max_count = max(counts.values()) if counts else 1

    transitions = {
        k: v / max_count
        for k, v in counts.items()
    }

    return transitions

# =========================
# PARTICLE INIT
# =========================
def init_particles(mod):
    states = np.random.randint(0, mod, size=NUM_PARTICLES)
    positions = embed_circle(mod)[states]
    trails = [[pos.copy()] for pos in positions]
    return states, positions, trails

# =========================
# STEP
# =========================
def step_particles(states, transitions, mod):
    new_states = []

    for s in states:
        options = [(a, b, w) for (a, b), w in transitions.items() if a == s]

        if not options:
            new_states.append(s)
            continue

        probs = np.array([w for _, _, w in options])
        probs = probs / probs.sum()

        choice = np.random.choice(len(options), p=probs)
        new_states.append(options[choice][1])

    return np.array(new_states)

# =========================
# RUN PER MOD
# =========================
def run_mod(mod, primes):

    print(f"[INFO] Running mod {mod}")

    transitions = build_transition(mod, primes)
    circle = embed_circle(mod)

    states, positions, trails = init_particles(mod)

    fig, ax = plt.subplots(figsize=(7, 7))

    def update(frame):
        nonlocal states, positions, trails

        ax.clear()

        # circle
        theta = np.linspace(0, 2*np.pi, 200)
        ax.plot(np.cos(theta), np.sin(theta), alpha=0.2)

        # nodes
        ax.scatter(circle[:,0], circle[:,1], s=80)

        for i, (x, y) in enumerate(circle):
            ax.text(x*1.08, y*1.08, str(i), ha='center')

        # step
        states = step_particles(states, transitions, mod)
        target_positions = circle[states]

        positions = positions + SMOOTHING * (target_positions - positions)

        # trails
        for i in range(len(positions)):
            trails[i].append(positions[i].copy())
            if len(trails[i]) > TRAIL_LENGTH:
                trails[i].pop(0)

            trail = np.array(trails[i])
            ax.plot(trail[:,0], trail[:,1], alpha=0.4)

        # particles
        ax.scatter(positions[:,0], positions[:,1], s=30)

        ax.set_title(f"mod {mod} Prime Flow")
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')

    anim = FuncAnimation(fig, update, frames=FRAMES, interval=INTERVAL)

    path = os.path.join(OUTPUT_DIR, f"mod{mod}_flow.gif")
    print(f"[INFO] Saving {path}")
    anim.save(path, writer="pillow")
    print(f"[OK] Done mod {mod}")

# =========================
# MAIN
# =========================
if __name__ == "__main__":

    primes = generate_primes(N_PRIMES)

    for mod in MOD_LIST:
        run_mod(mod, primes)

    print("[DONE] All mods processed")
