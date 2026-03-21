import numpy as np
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 80
CENTER = np.array([SIZE//2, SIZE//2])

N_AGENTS = 120
STEPS = 400

STEP_SIZE = 0.22
NOISE = 0.006
DAMPING = 0.93

ALPHA_FLOW = 0.65
BETA_SWIRL = 0.75
GAMMA_MEMORY = 0.35
DELTA_RESONANCE = 0.25

# 🧬 Crown Dynamics
LAMBDA_RADIUS = 0.35     # radial attraction
TARGET_RADIUS = 18.0     # preferred shell radius
RADIUS_WIDTH = 6.0       # shell thickness

# Phase
KAPPA_PHASE = 0.08
PHASE_RADIUS = 10.0

OMEGA_MEAN = 0.05
OMEGA_STD = 0.015

PHASE_BREAK_PROB = 0.005

FIELD_DECAY = 0.992
MEMORY_DECAY = 0.995

SAVE_DIR = "ENGINE/visuals/navigation_level22"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD
# --------------------------------------------------

field = generate_stability_landscape(SIZE)

# --------------------------------------------------
# INIT
# --------------------------------------------------

agents = np.random.rand(N_AGENTS, 2) * SIZE
vel = np.zeros((N_AGENTS, 2))

memory = np.zeros((SIZE, SIZE))

theta = np.random.rand(N_AGENTS) * 2*np.pi
omega = np.random.normal(OMEGA_MEAN, OMEGA_STD, N_AGENTS)

trajectories = []

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def gradient(field, x, y):
    xi = int(x) % SIZE
    yi = int(y) % SIZE

    dx = field[(xi+1)%SIZE, yi] - field[(xi-1)%SIZE, yi]
    dy = field[xi, (yi+1)%SIZE] - field[xi, (yi-1)%SIZE]

    return np.array([dx, dy])

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    frame = []

    for i in range(N_AGENTS):

        x, y = agents[i]

        # --- FIELD FLOW ---
        grad = gradient(field, x, y)
        flow = ALPHA_FLOW * grad

        # --- SWIRL ---
        swirl = BETA_SWIRL * np.array([-grad[1], grad[0]])

        # --- MEMORY ---
        mem_val = memory[int(x)%SIZE, int(y)%SIZE]
        mem_force = GAMMA_MEMORY * mem_val * np.random.randn(2)

        # --- RADIAL FORCE (CROWN) ---
        vec_to_center = CENTER - agents[i]
        dist = np.linalg.norm(vec_to_center) + 1e-6

        radial_dir = vec_to_center / dist

        # shell targeting (Gaussian around target radius)
        radial_strength = np.exp(-((dist - TARGET_RADIUS)**2) / (2 * RADIUS_WIDTH**2))

        radial_force = LAMBDA_RADIUS * radial_strength * radial_dir

        # --- PHASE COUPLING ---
        neighbors = []
        for j in range(N_AGENTS):
            if i != j and np.linalg.norm(agents[j] - agents[i]) < PHASE_RADIUS:
                neighbors.append(j)

        if neighbors:
            coupling = np.mean([
                np.sin(theta[j] - theta[i]) for j in neighbors
            ])
        else:
            coupling = 0

        theta[i] += omega[i] + KAPPA_PHASE * coupling

        # --- PHASE BREAK ---
        if np.random.rand() < PHASE_BREAK_PROB:
            theta[i] += np.random.randn() * 0.3

        # --- TANGENTIAL MOTION (ORBIT) ---
        tangent = np.array([-radial_dir[1], radial_dir[0]])
        orbit_force = DELTA_RESONANCE * tangent * np.cos(theta[i])

        # --- TOTAL FORCE ---
        force = flow + swirl + mem_force + radial_force + orbit_force

        vel[i] = DAMPING * vel[i] + STEP_SIZE * force + NOISE * np.random.randn(2)

        agents[i] += vel[i]
        agents[i] = agents[i] % SIZE

        frame.append(agents[i].copy())

        # --- MEMORY ---
        xi, yi = int(agents[i][0]) % SIZE, int(agents[i][1]) % SIZE
        memory[xi, yi] += 1

    trajectories.append(np.array(frame))

    field *= FIELD_DECAY
    memory *= MEMORY_DECAY

# --------------------------------------------------
# METRICS
# --------------------------------------------------

entropy = -np.sum((memory/np.sum(memory)+1e-9)*np.log(memory/np.sum(memory)+1e-9))
recurrence = np.mean(memory > np.percentile(memory, 99))
phase_coherence = np.abs(np.mean(np.exp(1j * theta)))

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

axs[0,0].imshow(field)
axs[0,0].set_title("Field")

gx, gy = np.gradient(field)
axs[0,1].quiver(gx, gy)
axs[0,1].set_title("Flow")

for i in range(N_AGENTS):
    traj = np.array([t[i] for t in trajectories])
    axs[1,0].plot(traj[:,0], traj[:,1], alpha=0.4)

axs[1,0].scatter(CENTER[0], CENTER[1], c='white', s=50)
axs[1,0].set_title("Crown Trajectories")

axs[1,1].imshow(memory)
axs[1,1].set_title("Memory / Shell Density")

plt.tight_layout()

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

plt.savefig(f"{SAVE_DIR}/level22_{run_id}.png")
plt.close()

# --------------------------------------------------
# LOG
# --------------------------------------------------

log = {
    "run_id": run_id,
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(recurrence),
        "phase_coherence": float(phase_coherence)
    }
}

with open(f"{LOG_DIR}/log_level22_{run_id}.json", "w") as f:
    json.dump(log, f, indent=2)

print("Run complete:", run_id)
