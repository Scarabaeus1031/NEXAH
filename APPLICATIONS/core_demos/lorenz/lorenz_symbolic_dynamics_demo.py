"""
NEXAH — Lorenz Symbolic Dynamics Demo

Goal:
Convert continuous chaotic dynamics into discrete symbolic states.

Pipeline:
- Lorenz system
- risk computation
- quantile phase mapping
- symbolic state extraction
- transition graph construction

This is the first real bridge:
CHAOS → STATES → GRAPH
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

plt.style.use("dark_background")


# ==================================================
# 1. LORENZ SYSTEM
# ==================================================

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

def lorenz(x):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])


# ==================================================
# 2. COHERENCE / RISK
# ==================================================

def compute_coherence(x, dx_obs):
    dx_field = lorenz(x)
    num = np.dot(dx_obs, dx_field)
    denom = np.linalg.norm(dx_obs) * np.linalg.norm(dx_field) + 1e-8
    return num / denom

def compute_risk(x, dx_obs):
    return 1 - compute_coherence(x, dx_obs)

def grad_risk(x, dx_obs, eps=1e-3):
    grad = np.zeros(3)
    for i in range(3):
        dx = np.zeros(3)
        dx[i] = eps
        r1 = compute_risk(x + dx, dx_obs)
        r2 = compute_risk(x - dx, dx_obs)
        grad[i] = (r1 - r2) / (2 * eps)
    return grad


# ==================================================
# 3. SIMULATION
# ==================================================

dt = 0.01
steps = 6000

noise_strength = 1.0
control_strength = 0.3

# 🔥 inside attractor start (wichtig!)
x = np.array([8.0, 8.0, 25.0])

trajectory = []
risk_series = []

for _ in range(steps):
    dx = lorenz(x)
    noise = noise_strength * np.random.randn(3)
    dx_obs = dx + noise

    r = compute_risk(x, dx_obs)
    g = grad_risk(x, dx_obs)

    u = -control_strength * g
    x = x + dt * (dx_obs + u)

    trajectory.append(x.copy())
    risk_series.append(r)

trajectory = np.array(trajectory)
risk_series = np.array(risk_series)


# ==================================================
# 4. PHASE (QUANTILE)
# ==================================================

sorted_idx = np.argsort(risk_series)
rank = np.empty_like(sorted_idx)
rank[sorted_idx] = np.arange(len(risk_series))

phase = rank / (len(risk_series) - 1)

# smoothing
window = 25
phase_smooth = np.convolve(phase, np.ones(window) / window, mode="same")


# ==================================================
# 5. SYMBOLIC STATES
# ==================================================

N_STATES = 6

states = np.floor(phase_smooth * N_STATES).astype(int)
states = np.clip(states, 0, N_STATES - 1)

state_labels = [f"S{i}" for i in range(N_STATES)]


# ==================================================
# 6. TRANSITIONS
# ==================================================

transition_counts = np.zeros((N_STATES, N_STATES), dtype=int)

for i in range(len(states) - 1):
    a = states[i]
    b = states[i + 1]
    transition_counts[a, b] += 1

transition_probs = np.zeros_like(transition_counts, dtype=float)

for i in range(N_STATES):
    s = np.sum(transition_counts[i])
    if s > 0:
        transition_probs[i] = transition_counts[i] / s


# ==================================================
# 7. GRAPH
# ==================================================

G = nx.DiGraph()

for i in range(N_STATES):
    G.add_node(i, label=state_labels[i])

for i in range(N_STATES):
    for j in range(N_STATES):
        if transition_counts[i, j] > 0:
            G.add_edge(i, j, weight=transition_probs[i, j])


# ==================================================
# 8. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(16, 10))


# --- XY symbolic map ---
ax1 = fig.add_subplot(221)

for i in range(len(trajectory) - 1):
    color = plt.cm.plasma(states[i] / (N_STATES - 1))
    ax1.plot(
        trajectory[i:i+2, 0],
        trajectory[i:i+2, 1],
        color=color,
        linewidth=0.6
    )

ax1.set_title("Symbolic State Map (XY)")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")


# --- state sequence ---
ax2 = fig.add_subplot(222)

ax2.plot(states, color="cyan")
ax2.set_title("State Sequence")
ax2.set_xlabel("Step")
ax2.set_ylabel("State")


# --- transition matrix ---
ax3 = fig.add_subplot(223)

im = ax3.imshow(transition_probs, cmap="inferno", origin="lower")
ax3.set_title("Transition Matrix")
ax3.set_xlabel("To")
ax3.set_ylabel("From")

ax3.set_xticks(range(N_STATES))
ax3.set_yticks(range(N_STATES))
ax3.set_xticklabels(state_labels)
ax3.set_yticklabels(state_labels)

plt.colorbar(im, ax=ax3)


# --- graph ---
ax4 = fig.add_subplot(224)

pos = nx.spring_layout(G, seed=42)

weights = [G[u][v]["weight"] for u, v in G.edges()]
widths = [1 + 6*w for w in weights]

nx.draw_networkx_nodes(
    G, pos,
    node_color=np.arange(N_STATES),
    cmap=plt.cm.plasma,
    node_size=900,
    ax=ax4
)

nx.draw_networkx_labels(
    G, pos,
    labels={i: state_labels[i] for i in G.nodes()},
    font_color="white",
    ax=ax4
)

nx.draw_networkx_edges(
    G, pos,
    width=widths,
    edge_color="white",
    arrows=True,
    arrowsize=18,
    ax=ax4
)

ax4.set_title("State Transition Graph")
ax4.axis("off")


plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_symbolic_dynamics.png", dpi=150)
plt.show()


# ==================================================
# 9. OUTPUT
# ==================================================

print("\n--- SYMBOLIC DYNAMICS ---")
print("States:", state_labels)
print("Visited:", sorted(set(states.tolist())))

print("\nTransition Counts:")
print(transition_counts)

print("\nTransition Probabilities:")
print(np.round(transition_probs, 3))

print("\n🧭 Interpretation:\n")
print("""
Chaos → Symbols → Graph

You now see:

• discrete attractor zones
• transition probabilities
• state memory

----------------------------------------

🧠 Key Insight:

The system is no longer continuous.

It is now:
→ a STATE MACHINE

----------------------------------------

🚀 Meaning:

This is EXACTLY your adapter layer.

From here:
→ NEXAH Navigation
→ decision policies
→ real systems
""")
