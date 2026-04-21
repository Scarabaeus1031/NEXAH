import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# =========================
# PARAMETERS (CLEAN)
# =========================
NUM_PARTICLES = 35          # weniger = klarer
STEPS = 400
MOD = 7
TRAIL_LENGTH = 35           # längere Trails → Struktur sichtbar
SMOOTHING = 0.2            # langsamer → flüssiger

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
# TRANSITIONS (mod 7)
# =========================
primes = generate_primes(4000)
mod_seq = [p % MOD for p in primes]

transitions = {i: [] for i in range(MOD)}
for i in range(len(mod_seq) - 1):
    transitions[mod_seq[i]].append(mod_seq[i + 1])

# =========================
# EMBEDDING
# =========================
def embed(n):
    angle = 2 * np.pi * n / MOD
    return np.array([np.cos(angle), np.sin(angle)])

# =========================
# INIT PARTICLES
# =========================
states = np.random.randint(0, MOD, size=NUM_PARTICLES)
positions = np.array([embed(s) for s in states])

trails = [[positions[i].copy()] for i in range(NUM_PARTICLES)]

# =========================
# FIGURE
# =========================
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect('equal')
ax.axis('off')

# soft circle
circle = plt.Circle((0,0), 1.0, fill=False, alpha=0.15, lw=1)
ax.add_artist(circle)

# scatter (small + subtle)
scat = ax.scatter(positions[:,0], positions[:,1], s=15, alpha=0.8)

# trails
lines = [ax.plot([], [], lw=1.5, alpha=0.5)[0] for _ in range(NUM_PARTICLES)]

# =========================
# UPDATE
# =========================
def update(frame):
    global states, positions, trails

    for i in range(NUM_PARTICLES):
        current = states[i]

        if transitions[current]:
            next_state = np.random.choice(transitions[current])
        else:
            next_state = np.random.randint(0, MOD)

        states[i] = next_state
        target = embed(next_state)

        # smoother motion (cleaner flow)
        positions[i] = (1 - SMOOTHING) * positions[i] + SMOOTHING * target

        # update trail
        trails[i].append(positions[i].copy())
        if len(trails[i]) > TRAIL_LENGTH:
            trails[i].pop(0)

    scat.set_offsets(positions)

    # update trails with fade
    for i, line in enumerate(lines):
        trail = np.array(trails[i])
        if len(trail) > 1:
            line.set_data(trail[:,0], trail[:,1])

            # stronger fade gradient
            alpha = len(trail) / TRAIL_LENGTH
            line.set_alpha(0.15 + 0.6 * alpha)

    return [scat] + lines

# =========================
# ANIMATION
# =========================
ani = FuncAnimation(fig, update, frames=STEPS, interval=35)

plt.title("mod7 Prime Flow — Clean")

# =========================
# SAVE
# =========================
if os.environ.get("AUTO_SAVE") == "1":
    print("[INFO] Saving CLEAN GIF...")
    os.makedirs("output/plots", exist_ok=True)

    ani.save(
        "output/plots/mod7_particle_flow_clean.gif",
        writer="pillow",
        fps=25
    )

    print("[OK] Saved to output/plots/mod7_particle_flow_clean.gif")
else:
    plt.show()
