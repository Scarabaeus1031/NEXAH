import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# =========================
# PARAMETERS
# =========================
NUM_PARTICLES = 120
STEPS = 400
MOD = 7

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
# BUILD TRANSITIONS (mod 7)
# =========================
primes = generate_primes(2000)
mod_seq = [p % MOD for p in primes]

transitions = {i: [] for i in range(MOD)}

for i in range(len(mod_seq) - 1):
    a = mod_seq[i]
    b = mod_seq[i + 1]
    transitions[a].append(b)

# =========================
# CIRCLE EMBEDDING
# =========================
def embed(n):
    angle = 2 * np.pi * n / MOD
    return np.array([np.cos(angle), np.sin(angle)])

# =========================
# INIT PARTICLES
# =========================
states = np.random.randint(0, MOD, size=NUM_PARTICLES)
positions = np.array([embed(s) for s in states])

# =========================
# FIGURE
# =========================
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.axis('off')

# circle background
circle = plt.Circle((0,0), 1.0, fill=False, alpha=0.3)
ax.add_artist(circle)

# scatter
scat = ax.scatter(positions[:,0], positions[:,1], s=20)

# =========================
# UPDATE FUNCTION
# =========================
def update(frame):
    global states, positions

    new_positions = []

    for i in range(NUM_PARTICLES):
        current = states[i]

        # pick next state from real transitions
        if transitions[current]:
            next_state = np.random.choice(transitions[current])
        else:
            next_state = np.random.randint(0, MOD)

        states[i] = next_state

        target = embed(next_state)

        # smooth movement (interpolation)
        positions[i] = positions[i] * 0.7 + target * 0.3
        new_positions.append(positions[i])

    new_positions = np.array(new_positions)
    scat.set_offsets(new_positions)

    return scat,

# =========================
# ANIMATION
# =========================
ani = FuncAnimation(fig, update, frames=STEPS, interval=30)

plt.title("mod7 Prime Flow Field")

# =========================
# SAVE GIF (optional)
# =========================
if os.environ.get("AUTO_SAVE") == "1":
    print("[INFO] Saving GIF...")
    os.makedirs("output/plots", exist_ok=True)

    ani.save(
        "output/plots/mod7_particle_flow.gif",
        writer="pillow",
        fps=30
    )

    print("[OK] Saved to output/plots/mod7_particle_flow.gif")
else:
    plt.show()
