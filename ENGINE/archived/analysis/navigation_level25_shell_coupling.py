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
CENTER = np.array([SIZE / 2, SIZE / 2], dtype=float)

N_AGENTS = 120
STEPS = 520

STEP_SIZE = 0.18
NOISE = 0.004
DAMPING = 0.945

ALPHA_FLOW = 0.48
BETA_SWIRL = 0.50
GAMMA_MEMORY = 0.20
DELTA_RESONANCE = 0.38

FIELD_DECAY = 0.993
MEMORY_DECAY = 0.997

# --------------------------------------------------
# MULTI-SHELL SYSTEM
# --------------------------------------------------

TARGET_RADII = np.array([10.0, 18.0, 28.0], dtype=float)
SHELL_STRENGTH = 0.40
SHELL_TANGENTIAL_GAIN = 0.34
SHELL_WIDTH = 3.2

# NEW: shell coupling
COUPLING_STRENGTH = 0.22
COUPLING_BAND = 2.6
SHELL_SWITCH_PROB = 0.010

# --------------------------------------------------
# PHASE SYSTEM
# --------------------------------------------------

KAPPA_PHASE = 0.040
PHASE_RADIUS = 8.0

OMEGA_MEAN = 0.05
OMEGA_STD = 0.014
PHASE_BREAK_PROB = 0.007

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

SAVE_DIR = "ENGINE/visuals/navigation_level25"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_stability_landscape(SIZE)
memory = np.zeros((SIZE, SIZE), dtype=float)

agents = np.random.rand(N_AGENTS, 2) * SIZE
vel = np.zeros((N_AGENTS, 2), dtype=float)

theta = np.random.rand(N_AGENTS) * 2 * np.pi
omega = np.random.normal(OMEGA_MEAN, OMEGA_STD, N_AGENTS)

agent_shell_idx = np.random.randint(0, len(TARGET_RADII), size=N_AGENTS)

frames = []

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def sample_scalar(arr, x, y):
    xi = int(np.clip(x, 0, SIZE - 1))
    yi = int(np.clip(y, 0, SIZE - 1))
    return arr[xi, yi]

def gradient(arr, x, y):
    xi = int(x) % SIZE
    yi = int(y) % SIZE
    dx = arr[(xi + 1) % SIZE, yi] - arr[(xi - 1) % SIZE, yi]
    dy = arr[xi, (yi + 1) % SIZE] - arr[xi, (yi - 1) % SIZE]
    return np.array([dx, dy], dtype=float)

def normalize(v):
    n = np.linalg.norm(v)
    if n < 1e-12:
        return np.zeros_like(v)
    return v / n

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

for step in range(STEPS):

    new_positions = []

    for i in range(N_AGENTS):
        x, y = agents[i]

        # ----------------------------
        # BASE FORCES
        # ----------------------------

        grad = gradient(field, x, y)
        flow = normalize(grad)

        swirl = np.array([-flow[1], flow[0]])

        mem_grad = gradient(memory, x, y)

        # ----------------------------
        # SHELL FORCE
        # ----------------------------

        vec_center = agents[i] - CENTER
        r = np.linalg.norm(vec_center) + 1e-8

        target_r = TARGET_RADII[agent_shell_idx[i]]
        radial_error = r - target_r

        radial_force = -normalize(vec_center) * radial_error

        tangent = np.array([-vec_center[1], vec_center[0]])
        tangent = normalize(tangent)

        shell_force = (
            SHELL_STRENGTH * radial_force +
            SHELL_TANGENTIAL_GAIN * tangent
        )

        # ----------------------------
        # SHELL COUPLING (NEW)
        # ----------------------------

        coupling_force = np.zeros(2)

        for j in range(N_AGENTS):
            if i == j:
                continue

            dx = agents[j] - agents[i]
            dist = np.linalg.norm(dx)

            if dist < COUPLING_BAND:
                diff = TARGET_RADII[agent_shell_idx[j]] - TARGET_RADII[agent_shell_idx[i]]
                coupling_force += normalize(dx) * diff

        coupling_force *= COUPLING_STRENGTH

        # random shell switching
        if np.random.rand() < SHELL_SWITCH_PROB:
            agent_shell_idx[i] = np.random.randint(0, len(TARGET_RADII))

        # ----------------------------
        # PHASE COUPLING
        # ----------------------------

        phase_force = 0.0
        neighbors = 0

        for j in range(N_AGENTS):
            if i == j:
                continue

            d = np.linalg.norm(agents[j] - agents[i])
            if d < PHASE_RADIUS:
                phase_force += np.sin(theta[j] - theta[i])
                neighbors += 1

        if neighbors > 0:
            phase_force /= neighbors

        if np.random.rand() < PHASE_BREAK_PROB:
            phase_force *= -1

        theta[i] += omega[i] + KAPPA_PHASE * phase_force

        # ----------------------------
        # TOTAL FORCE
        # ----------------------------

        total_force = (
            ALPHA_FLOW * flow +
            BETA_SWIRL * swirl +
            GAMMA_MEMORY * mem_grad +
            DELTA_RESONANCE * shell_force +
            coupling_force
        )

        # ----------------------------
        # UPDATE
        # ----------------------------

        vel[i] = DAMPING * vel[i] + STEP_SIZE * total_force
        vel[i] += np.random.randn(2) * NOISE

        agents[i] += vel[i]
        agents[i] = np.clip(agents[i], 0, SIZE - 1)

        xi, yi = int(agents[i][0]), int(agents[i][1])
        memory[xi, yi] += 1.0

        new_positions.append(agents[i].copy())

    memory *= MEMORY_DECAY
    field *= FIELD_DECAY

    frames.append(np.array(new_positions))

# --------------------------------------------------
# METRICS
# --------------------------------------------------

entropy = -np.sum((memory / np.sum(memory + 1e-8)) * np.log(memory / np.sum(memory + 1e-8) + 1e-8))
recurrence = np.mean(memory > np.percentile(memory, 95))

# --------------------------------------------------
# SAVE OUTPUT
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

log = {
    "run_id": run_id,
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(recurrence)
    }
}

with open(os.path.join(LOG_DIR, f"{run_id}.json"), "w") as f:
    json.dump(log, f, indent=2)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

plt.figure(figsize=(12, 10))

plt.subplot(2, 2, 1)
plt.title("Field")
plt.imshow(field)

plt.subplot(2, 2, 2)
plt.title("Flow")
gx, gy = np.gradient(field)
plt.quiver(gx, gy)

plt.subplot(2, 2, 3)
plt.title("Shell Coupling Trajectories")
for traj in frames[::10]:
    plt.plot(traj[:, 0], traj[:, 1], alpha=0.3)

plt.subplot(2, 2, 4)
plt.title("Memory / Shell Interaction")
plt.imshow(memory)

plt.tight_layout()
plt.savefig(os.path.join(SAVE_DIR, f"level25_{run_id}.png"), dpi=200)

print(f"Run complete: {run_id}")
print(f"Entropy: {entropy}")
print(f"Recurrence: {recurrence}")
