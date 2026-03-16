"""
NEXAH Mode Evolution Simulator
==============================

Simulates how resonance modes evolve when parameters change.

Outputs:

mode_evolution.gif
mode_evolution.json
"""

from pathlib import Path
import numpy as np
import json
import matplotlib.pyplot as plt
import imageio


OUT_DIR = Path(
    "ENGINE/nexah_kernel/demos/visuals/mode_evolution"
)

OUT_DIR.mkdir(parents=True, exist_ok=True)

GIF_FILE = OUT_DIR / "mode_evolution.gif"
JSON_FILE = OUT_DIR / "mode_evolution.json"


# --------------------------------------------------
# Pattern generator (same logic as kernel demos)
# --------------------------------------------------

def generate_pattern(n, drift, steps=400):

    angle = 0
    points = []

    for i in range(steps):

        angle += (2*np.pi/n) + np.radians(drift)

        r = 1 + 0.3*np.sin(i*0.1)

        x = r*np.cos(angle)
        y = r*np.sin(angle)

        points.append((x,y))

    return np.array(points)


# --------------------------------------------------
# Fourier mode strength
# --------------------------------------------------

def compute_mode_strength(points):

    x = points[:,0]
    y = points[:,1]

    signal = x + 1j*y

    fft = np.fft.fft(signal)

    power = np.abs(fft)

    return power


# --------------------------------------------------
# Evolution sweep
# --------------------------------------------------

def simulate():

    frames = []
    mode_data = []

    drift_values = np.linspace(0,6,60)

    n = 18

    for drift in drift_values:

        pts = generate_pattern(n,drift)

        power = compute_mode_strength(pts)

        dominant = np.argmax(power[1:20]) + 1

        mode_data.append({

            "drift": float(drift),
            "dominant_mode": int(dominant),
            "strength": float(power[dominant])
        })

        fig, ax = plt.subplots(figsize=(4,4))

        ax.plot(pts[:,0], pts[:,1], color="cyan", linewidth=0.5)

        ax.set_title(
            f"n={n} drift={drift:.2f}° mode={dominant}"
        )

        ax.axis("equal")
        ax.axis("off")

        frame_path = OUT_DIR / f"frame_{len(frames):03}.png"

        plt.savefig(frame_path, dpi=120)
        plt.close()

        frames.append(imageio.imread(frame_path))

    imageio.mimsave(GIF_FILE, frames, duration=0.08)

    with open(JSON_FILE,"w") as f:

        json.dump(mode_data,f,indent=2)

    print("\nSaved animation:",GIF_FILE)
    print("Saved mode data:",JSON_FILE)


# --------------------------------------------------

if __name__ == "__main__":

    print("\nSimulating mode evolution...\n")

    simulate()
