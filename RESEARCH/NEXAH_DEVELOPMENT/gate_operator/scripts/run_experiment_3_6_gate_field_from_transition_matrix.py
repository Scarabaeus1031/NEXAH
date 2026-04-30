import numpy as np
import matplotlib.pyplot as plt
import os

print("Running Experiment 3.6 — Gate Field from Transition Matrix")

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

transition_matrix = np.load("../output_results/experiment_3_5_transition_matrix.npy")
sheet_sequence = np.load("../output_results/experiment_3_4_sheet_sequence.npy")

# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------

EPS = 1e-9
GATE_THRESHOLD = 2.5   # adjust if needed

# ------------------------------------------------------------
# COMPUTE GATE STRENGTH MATRIX
# ------------------------------------------------------------

gate_strength = -np.log(transition_matrix + EPS)

# normalize (optional)
gate_strength_norm = gate_strength / np.max(gate_strength)

# ------------------------------------------------------------
# DETECT RARE TRANSITIONS (GATES)
# ------------------------------------------------------------

gate_edges = []

n_states = transition_matrix.shape[0]

for i in range(n_states):
    for j in range(n_states):
        if i != j and transition_matrix[i, j] > 0:
            score = gate_strength[i, j]
            if score > GATE_THRESHOLD:
                gate_edges.append((i, j, score))

print(f"Detected gate edges: {len(gate_edges)}")

# ------------------------------------------------------------
# MAP BACK TO TIME
# ------------------------------------------------------------

gate_times = []

for t in range(len(sheet_sequence) - 1):
    i = int(sheet_sequence[t])
    j = int(sheet_sequence[t + 1])

    if i != j:
        prob = transition_matrix[i, j]
        score = -np.log(prob + EPS)

        if score > GATE_THRESHOLD:
            gate_times.append(t)

print(f"Gate events in time: {len(gate_times)}")

# ------------------------------------------------------------
# PLOT 1 — GATE MATRIX
# ------------------------------------------------------------

plt.figure(figsize=(6, 5))
plt.imshow(gate_strength_norm, cmap="inferno")
plt.colorbar(label="normalized gate strength")
plt.title("Experiment 3.6 — Gate Strength Matrix")
plt.xlabel("to state")
plt.ylabel("from state")
plt.tight_layout()

os.makedirs("../output_results", exist_ok=True)
plt.savefig("../output_results/experiment_3_6_gate_matrix.png", dpi=200)
plt.close()

# ------------------------------------------------------------
# PLOT 2 — GATE EVENTS OVER TIME
# ------------------------------------------------------------

plt.figure(figsize=(16, 4))

plt.plot(sheet_sequence, alpha=0.6, label="sheet")

if len(gate_times) > 0:
    plt.scatter(gate_times,
                sheet_sequence[gate_times],
                color="red",
                label="gates",
                s=10)

plt.title("Experiment 3.6 — Gate Events (Time)")
plt.xlabel("time")
plt.ylabel("sheet")
plt.legend()

plt.tight_layout()
plt.savefig("../output_results/experiment_3_6_gate_events.png", dpi=200)
plt.close()

# ------------------------------------------------------------
# SAVE DATA
# ------------------------------------------------------------

np.save("../output_results/experiment_3_6_gate_strength.npy", gate_strength)
np.save("../output_results/experiment_3_6_gate_times.npy", np.array(gate_times))

print("Saved Experiment 3.6 outputs")
