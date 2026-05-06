import numpy as np
import matplotlib.pyplot as plt
import os

# 🔧 einfacher Import (gleiches Verzeichnis!)
from field_controller import FieldController


# ----------------------------
# 1. Simulation
# ----------------------------
controller = FieldController()
result = controller.simulate(x0=np.array([-2.0, -1.5]), steps=120)

states = result.states
coherences = result.coherences

# ----------------------------
# 2. Output Folder sicherstellen
# ----------------------------
output_dir = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(output_dir, exist_ok=True)

# ----------------------------
# 3. Trajectory Plot
# ----------------------------
plt.figure()
plt.plot(states[:, 0], states[:, 1], label="trajectory")
plt.scatter(states[0, 0], states[0, 1], label="start")

plt.title("NEXAH Field Controller Demo")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()

trajectory_path = os.path.join(output_dir, "v5_trajectory.png")
plt.savefig(trajectory_path)
print("Saved:", trajectory_path)

plt.close()

# ----------------------------
# 4. Coherence Plot
# ----------------------------
plt.figure()
plt.plot(coherences)

plt.title("Coherence over Time")
plt.xlabel("step")
plt.ylabel("C(x)")

coherence_path = os.path.join(output_dir, "v5_coherence.png")
plt.savefig(coherence_path)
print("Saved:", coherence_path)

plt.close()
