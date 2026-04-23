"""
Symmetry Resonance Atlas
========================

Generates a visual atlas of symmetry / drift patterns.

For each (n, drift):
 - render pattern
 - save PNG
 - store metrics

Outputs:

demos/
  visuals/
    symmetry_resonance_atlas/
      sym_n05_drift_2.00.png
      ...

  data/
    symmetry_resonance_atlas/
      resonance_metrics.csv
      top_resonances.json
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
from pathlib import Path

# --------------------------------------------------
# directory setup
# --------------------------------------------------

base_dir = Path(__file__).resolve().parent

visual_dir = base_dir / "visuals" / "symmetry_resonance_atlas"
data_dir = base_dir / "data" / "symmetry_resonance_atlas"

visual_dir.mkdir(parents=True, exist_ok=True)
data_dir.mkdir(parents=True, exist_ok=True)

print("Visual output:", visual_dir)
print("Data output:", data_dir)

# --------------------------------------------------
# parameters
# --------------------------------------------------

radius = 5
iterations = 1800

n_values = range(3, 21)
drift_values = np.linspace(0, 6, 18)

# --------------------------------------------------
# pattern generator
# --------------------------------------------------

def radial_profile(k):
    return radius * (0.7 + 0.3 * np.cos(k * 0.02))


def generate_pattern(n, drift_deg):

    base_angle = 2*np.pi/n
    drift = np.deg2rad(drift_deg)

    k = np.arange(iterations)

    theta = k*(base_angle + drift)
    r = radial_profile(k)

    x = r*np.cos(theta)
    y = r*np.sin(theta)

    return x, y, r, theta


# --------------------------------------------------
# metrics
# --------------------------------------------------

def closure_error(x, y):
    dx = x[-1] - x[0]
    dy = y[-1] - y[0]
    return np.sqrt(dx*dx + dy*dy) / radius


def radial_variance(r):
    return np.std(r) / np.mean(r)


def angular_irregularity(theta):
    d = np.diff(np.unwrap(theta))
    return np.std(d) / np.mean(np.abs(d))


def resonance_score(c, rv, ai):
    return 1.0 / (1.0 + 3*c + 1.5*rv + 2*ai)


# --------------------------------------------------
# atlas generation
# --------------------------------------------------

records = []

for n in n_values:

    for drift in drift_values:

        x, y, r, theta = generate_pattern(n, drift)

        c = closure_error(x, y)
        rv = radial_variance(r)
        ai = angular_irregularity(theta)

        score = resonance_score(c, rv, ai)

        # record metrics
        records.append({
            "n": n,
            "drift": float(drift),
            "score": float(score),
            "closure_error": float(c),
            "radial_variance": float(rv),
            "angular_irregularity": float(ai)
        })

        # --------------------------------------------------
        # render visual
        # --------------------------------------------------

        fig, ax = plt.subplots(figsize=(4,4))

        ax.plot(x, y, lw=0.7)

        ax.set_aspect("equal")
        ax.set_xlim(-6,6)
        ax.set_ylim(-6,6)

        ax.axis("off")

        ax.set_title(f"n={n}  drift={drift:.2f}°")

        file_name = f"sym_n{n:02d}_drift_{drift:.2f}.png"

        plt.savefig(visual_dir / file_name, dpi=180)
        plt.close()

print("Visual atlas generated.")

# --------------------------------------------------
# save metrics
# --------------------------------------------------

df = pd.DataFrame(records)

csv_file = data_dir / "resonance_metrics.csv"
df.to_csv(csv_file, index=False)

print("Metrics saved:", csv_file)

# --------------------------------------------------
# compute top resonances
# --------------------------------------------------

top = df.sort_values("score", ascending=False).head(25)

json_file = data_dir / "top_resonances.json"

with open(json_file, "w") as f:
    json.dump(top.to_dict(orient="records"), f, indent=2)

print("Top resonances saved:", json_file)

print("\nTop resonance candidates:\n")

for _, row in top.head(10).iterrows():

    print(
        f"n={int(row['n'])}  "
        f"drift={row['drift']:.2f}°  "
        f"score={row['score']:.4f}"
    )
