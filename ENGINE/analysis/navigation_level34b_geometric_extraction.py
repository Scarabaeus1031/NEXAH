import numpy as np
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime
from itertools import combinations
from scipy.ndimage import label, center_of_mass
from scipy.spatial.distance import cdist

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 80
N_AGENTS = 100
STEPS = 600

STEP_SIZE = 0.14
NOISE = 0.0025
DAMPING = 0.955

MEMORY_DECAY = 0.992
SYMBOL_THRESHOLD = 0.12

GROUP_DISTANCE = 6.0
GRAMMAR_DISTANCE = 14.0
MAX_CONNECTIONS = 3

PHI = (1 + np.sqrt(5)) / 2
PHI_TOL = 0.18

# --------------------------------------------------
# SETUP
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

OUTPUT_DIR = "ENGINE/visuals/navigation_level34b"
LOG_DIR = "ENGINE/logs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD
# --------------------------------------------------

field = generate_stability_landscape(size=SIZE)

# --------------------------------------------------
# AGENTS
# --------------------------------------------------

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)
memory = np.zeros((SIZE, SIZE))

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def distance(a, b):
    return float(np.linalg.norm(a - b))

def safe_angle(a, b, c):
    # angle at b for triangle a-b-c
    ba = a - b
    bc = c - b
    nba = np.linalg.norm(ba)
    nbc = np.linalg.norm(bc)
    if nba < 1e-12 or nbc < 1e-12:
        return None
    cosang = np.dot(ba, bc) / (nba * nbc)
    cosang = np.clip(cosang, -1.0, 1.0)
    return float(np.degrees(np.arccos(cosang)))

def classify_triangle(sides):
    s = np.sort(np.array(sides))
    if s[0] < 1e-12:
        return "degenerate"

    tol = 0.08
    eq01 = abs(s[0] - s[1]) / max(s[1], 1e-12) < tol
    eq12 = abs(s[1] - s[2]) / max(s[2], 1e-12) < tol

    if eq01 and eq12:
        return "equilateral"
    if eq01 or eq12:
        return "isosceles"
    return "scalene"

def phi_relations(sides):
    s = np.sort(np.array(sides))
    ratios = []
    for i in range(3):
        for j in range(i + 1, 3):
            if s[i] > 1e-12:
                ratios.append(float(s[j] / s[i]))
    phi_hits = [r for r in ratios if abs(r - PHI) < PHI_TOL]
    return ratios, phi_hits

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):
    grads = np.gradient(field)

    for i in range(N_AGENTS):
        x, y = positions[i]
        xi, yi = int(x), int(y)

        gx = grads[1][yi % SIZE, xi % SIZE]
        gy = grads[0][yi % SIZE, xi % SIZE]

        force = np.array([gx, gy], dtype=float)

        velocities[i] += STEP_SIZE * force
        velocities[i] += NOISE * np.random.randn(2)
        velocities[i] *= DAMPING

        positions[i] += velocities[i]
        positions[i] = np.clip(positions[i], 0, SIZE - 1)

        px, py = int(positions[i][0]), int(positions[i][1])
        memory[py, px] += 1.0

    memory *= MEMORY_DECAY

# --------------------------------------------------
# SYMBOL DETECTION
# --------------------------------------------------

mem_norm = memory / (memory.max() + 1e-8)
symbol_mask = mem_norm > SYMBOL_THRESHOLD

labeled, num_features = label(symbol_mask)
centroids = center_of_mass(symbol_mask, labeled, range(1, num_features + 1))
centroids = np.array(centroids) if len(centroids) > 0 else np.zeros((0, 2))

# --------------------------------------------------
# GRAMMAR GRAPH
# --------------------------------------------------

edges = []

if len(centroids) > 1:
    dist_matrix = cdist(centroids, centroids)

    for i in range(len(centroids)):
        nearest = np.argsort(dist_matrix[i])[1:MAX_CONNECTIONS + 1]
        for j in nearest:
            d = dist_matrix[i][j]
            if d < GRAMMAR_DISTANCE:
                edges.append((i, j))

# make unique undirected edge set for geometry
edge_set = set()
for i,
