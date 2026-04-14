import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

# -----------------------------
# LOAD DATA (anpassen falls nötig)
# -----------------------------
# Beispiel: nimm lambda aus einem closed loop run
data_path = "APPLICATIONS/power_systems/nexah_ieee9/results/run_v5_closed_loop_steering_20260413_220034/lambda.npy"

lambdas = np.load(data_path)

# -----------------------------
# SETTINGS
# -----------------------------
gif_path = "APPLICATIONS/power_systems/nexah_ieee9/results/visuals/nexah_navigation_v11.gif"

os.makedirs(os.path.dirname(gif_path), exist_ok=True)

frames = []

# -----------------------------
# CREATE FRAMES
# -----------------------------
for i in range(2, len(lambdas)):

    plt.figure()

    # trajectory so far
    plt.plot(lambdas[:i], label="λ trajectory")

    # current point
    plt.scatter(i-1, lambdas[i-1])

    # critical + target lines (optional)
    plt.axhline(0.793, linestyle="--", label="critical λ")
    plt.axhline(0.773, linestyle="--", label="target λ")

    plt.xlabel("Step")
    plt.ylabel("Lambda (Load)")
    plt.title("NEXAH Navigation Trajectory")

    plt.legend()

    # save temp frame
    fname = f"_frame_{i}.png"
    plt.savefig(fname)
    plt.close()

    frames.append(imageio.imread(fname))
    os.remove(fname)

# -----------------------------
# SAVE GIF
# -----------------------------
imageio.mimsave(gif_path, frames, duration=0.1)

print(f"✅ GIF saved: {gif_path}")
